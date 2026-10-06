"""Render a game's privacy policy from its Markdown source into this site.

    python tools/render_policy.py <source.md> <out/index.html>

The source lives in the game's own repository (Sudoku: docs/PRIVACY_POLICY.md), next to the
guard tests that check its sentences against the code. This page is a rendering of it and is
never edited by hand, so the two cannot drift: change the source, rerun this, commit both.

Handles exactly the Markdown the policies use: `#`/`##` headings, paragraphs, `-` and `1.`
lists with indented continuation lines, **bold**, `code`, bare https links and HTML comments
(dropped). Anything else fails loudly rather than rendering wrong.
"""
import html
import re
import sys

src, out = sys.argv[1], sys.argv[2]
text = open(src, encoding='utf-8').read()
text = re.sub(r'<!--.*?-->', '', text, flags=re.S)  # notes for maintainers, not readers

ANCHORS = {'Deleting your data': 'deleting'}  # declared in Play Console; must survive


def inline(s):
    s = html.escape(s, quote=False)
    s = re.sub(r'`([^`]+)`', r'<code>\1</code>', s)
    s = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', s)
    s = re.sub(r'(https://[^\s<),]+)', r'<a href="\1">\1</a>', s)
    s = re.sub(r'(?<![\w.@/])([\w.+-]+@[\w-]+\.[\w.]+\w)', r'<a href="mailto:\1">\1</a>', s)
    assert '*' not in re.sub(r'<[^>]+>', '', s) or '→' in s, 'unhandled emphasis: ' + s
    return s


blocks = [b for b in re.split(r'\n\s*\n', text.strip()) if b.strip()]
title, body, meta = None, [], []
for b in blocks:
    lines = b.split('\n')
    first = lines[0]
    if first.startswith('# '):
        title = first[2:].strip()
        continue
    if first.startswith('**Effective date:**'):
        for line in lines:
            meta.append(re.sub(r'\*\*([^*]+):\*\*\s*', r'\1: ', line.strip()))
        continue
    if first.startswith('## '):
        h = first[3:].strip()
        anchor = ANCHORS.get(h)
        body.append(f'<h2 id="{anchor}">{inline(h)}</h2>' if anchor else f'<h2>{inline(h)}</h2>')
        assert len(lines) == 1, 'heading followed directly by text: ' + first
        continue
    if re.match(r'(- |\d+\. )', first):
        tag = 'ol' if first[0].isdigit() else 'ul'
        items = []
        for line in lines:
            if re.match(r'(- |\d+\. )', line):
                items.append(re.sub(r'^(- |\d+\. )', '', line).strip())
            else:
                assert line.startswith('  '), 'list line not indented: ' + line
                items[-1] += ' ' + line.strip()
        body.append(f'<{tag}>\n' + '\n'.join(f'  <li>{inline(i)}</li>' for i in items) + f'\n</{tag}>')
        continue
    assert not first.startswith('#'), 'unhandled heading level: ' + first
    body.append('<p>' + inline(' '.join(line.strip() for line in lines)) + '</p>')

assert title and meta, 'missing title or effective date'
for anchor in ANCHORS.values():
    assert f'id="{anchor}"' in '\n'.join(body), 'anchor lost: ' + anchor

page = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<link rel="stylesheet" href="../../style.css">
</head>
<body>

<h1>{html.escape(title)}</h1>
<p class="sub">{' · '.join(inline(m) for m in meta)}</p>

{chr(10).join(body)}

<footer>
<p>Whizkid World LLP &middot; <a href="/">games.whizkidworld.in</a></p>
</footer>

</body>
</html>
'''
open(out, 'w', encoding='utf-8', newline='\n').write(page)
print('wrote', out, len(body), 'blocks')
