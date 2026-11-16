"""Build index.html từ các phần trong src/.

Cách dùng:
    python3 build.py                 # tạo index.html (trang độc lập cho GitHub Pages)
    python3 build.py --fragment out  # tạo bản không có <html>/<head> (dùng cho Claude Artifact)

Quy ước khi viết nội dung trong src/:
    <pre data-lang="ts" data-file="tên file">...</pre>   khối code, viết code thô (không cần escape < >)
    <c>...</c>                                            code inline, viết thô
    <section class="doc" id="..." data-group="Nhóm">     mỗi chủ đề; mục lục sinh tự động từ <h2>
    <div class="panel" data-panel="tab">                  mỗi tab (nest, java, rabbit, kafka, redis)
"""
import html
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent
TABS = ['nest', 'java', 'rabbit', 'kafka', 'redis']


def render() -> str:
    parts = sorted((ROOT / 'src').glob('*.html'))
    src = ''.join(p.read_text(encoding='utf-8') for p in parts)
    src = src.replace("{'{'}", '{').replace("{'}'}", '}')

    def pre(m):
        lang, fname, body = m.group(1), m.group(2), m.group(3).strip('\n')
        lang = {'text': 'plaintext'}.get(lang, lang)
        tag = f'<span class="file">{html.escape(fname)}</span>' if fname else ''
        cls = 'code has-file' if fname else 'code'
        return (f'<div class="{cls}">{tag}<button class="copy" type="button">Sao chép</button>'
                f'<pre><code class="language-{lang}">{html.escape(body, quote=False)}</code></pre></div>')

    src = re.sub(r'<pre data-lang="(\w+)"(?: data-file="([^"]*)")?>(.*?)</pre>', pre, src, flags=re.S)
    src = re.sub(r'<c>(.*?)</c>',
                 lambda m: '<code>' + html.escape(html.unescape(m.group(1)), quote=False) + '</code>',
                 src, flags=re.S)

    starts = sorted((m.start(), m.group(1)) for m in re.finditer(r'data-panel="(\w+)"', src))

    def tab_at(pos):
        cur = 'nest'
        for s, name in starts:
            if s < pos:
                cur = name
        return cur

    groups = {t: [] for t in TABS}
    for m in re.finditer(r'<section class="doc" id="([^"]+)" data-group="([^"]+)">\s*<h2>(.*?)</h2>', src, flags=re.S):
        sid, grp, title = m.groups()
        title = re.sub(r'<span class="badge.*?</span>', '', title)
        title = re.sub(r'<[^>]+>', '', title).strip()
        g = groups[tab_at(m.start())]
        if not g or g[-1][0] != grp:
            g.append((grp, []))
        g[-1][1].append((sid, title))

    bounds = [s for s, _ in starts] + [len(src)]
    for tab in TABS:
        nav = ''.join(
            '<div class="toc-group"><h4>%s</h4><ul>%s</ul></div>' % (
                g, ''.join(f'<li data-target="{i}"><a href="#{i}">{t}</a></li>' for i, t in items))
            for g, items in groups[tab])
        src = src.replace(f'<!--NAV:{tab}-->', nav)
        idx = [n for _, n in starts].index(tab)
        seg = src[bounds[idx]:bounds[idx + 1]] if idx + 1 < len(bounds) else src[bounds[idx]:]
        nsec = sum(len(i) for _, i in groups[tab])
        src = src.replace(f'__SECTIONS_{tab}__', str(nsec)).replace(f'__CODES_{tab}__', str(seg.count('<div class="code')))
        print(f'{tab:7} {nsec:3} chủ đề')

    src = re.sub(r'(<section class="doc" id="[^"]+" data-group="([^"]+)">)',
                 lambda m: m.group(1) + f'<p class="group-label">{m.group(2)}</p>', src)

    ids = set(re.findall(r'id="([^"]+)"', src))
    broken = sorted({h for h in re.findall(r'href="#([^"]+)"', src) if h not in ids})
    leftover = [x for x in ("{'", '<c>', 'data-lang=', '__SECTIONS', '__CODES', '<!--NAV') if x in src]
    if broken or leftover:
        sys.exit(f'Lỗi build: link hỏng {broken}, còn sót {leftover}')
    return src


def standalone(fragment: str) -> str:
    cut = fragment.index('</style>') + len('</style>')
    head = fragment[:cut].replace('<meta name="claude:viewport-fit-sides" content="cover">\n', '')
    reset = ('<style>:root{color-scheme:light;padding-top:env(safe-area-inset-top,0px);'
             'padding-bottom:env(safe-area-inset-bottom,0px)}body{margin:0}img{max-width:100%}'
             '[hidden]{display:none!important}</style>\n')
    return ('<!doctype html>\n<html lang="vi">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
            '<meta name="description" content="Sổ tay tiếng Việt: NestJS, Java, RabbitMQ, Kafka, Redis — '
            'khái niệm, ví dụ code và pattern.">\n'
            f'{reset}{head}\n</head>\n<body>\n{fragment[cut:]}\n</body>\n</html>\n')


if __name__ == '__main__':
    out = render()
    if len(sys.argv) == 3 and sys.argv[1] == '--fragment':
        Path(sys.argv[2]).write_text(out, encoding='utf-8')
        print('→', sys.argv[2])
    else:
        (ROOT / 'index.html').write_text(standalone(out), encoding='utf-8')
        print('→ index.html')
