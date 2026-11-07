"""Chapter-local Markdown to static HTML renderer; no website runtime dependency."""
from pathlib import Path
import html
import re
import xml.etree.ElementTree as ET
import markdown

BOOK = Path(__file__).resolve().parents[2]


def render(text):
    output = markdown.markdown(text, extensions=['tables', 'fenced_code'])
    output = re.sub(r'href="ch(\d{2})\.md', r'href="ch\1.html', output)
    output = output.replace('<table>', '<div class="table-scroll"><table>').replace('</table>', '</table></div>')

    def figure(match):
        image, caption = match.group(1), match.group(2)
        src = re.search(r'src="([^"]+)"', image).group(1)
        tree = ET.parse(BOOK / 'chapters' / src).getroot()
        width, height = (tree.get(k) for k in ('width', 'height'))
        image = image.replace(' />', f' width="{width}" height="{height}" loading="lazy">')
        return f'<figure class="concept-figure"><a href="{src}" target="_blank" rel="noopener">{image}</a><figcaption>{caption}</figcaption></figure>'

    output = re.sub(r'<p>(<img [^>]+>)</p>\s*<p>(图 9-\d+：.*?)</p>', figure, output, flags=re.S)
    return re.sub(r'<a href="([^"]+\.svg)"(?! target)', r'<a href="\1" target="_blank" rel="noopener"', output)


def build():
    source = (BOOK / 'notes/ch09.md').read_text()
    reference = (BOOK / 'chapters/ch08.html').read_text()
    title = source.splitlines()[0][2:]
    deck = source.splitlines()[2][2:-2]
    body, sources = source.split('<details id="sources">', 1)
    sources = sources.split('</details>', 1)[0]
    summary = re.search(r'<summary>(.*?)</summary>', sources).group(1)
    sources = re.sub(r'^\s*<summary>.*?</summary>\s*', '', sources, flags=re.S)
    body = re.sub(r'^# .*?\n\n\*\*.*?\*\*\n\n', '', body, count=1, flags=re.S)
    parts = re.split(r'<a id="([^"]+)"></a>\s*\n\n## (\d+)　([^\n]+)\n\n', body)
    intro = render(parts[0])
    sections, toc = [], []
    for i in range(1, len(parts), 4):
        anchor, number, heading, content = parts[i:i+4]
        toc.append(f'<li><a href="#{anchor}">{number}　{html.escape(heading)}</a></li>')
        sections.append(f'<section id="{anchor}">\n<h2><span class="section-number">{number}</span>{html.escape(heading)}</h2>\n{render(content)}\n</section>')
    toc_html = '\n'.join(toc)
    head = reference.split('  <main id="main"', 1)[0]
    head = re.sub(r'<title>.*?</title>', f'<title>{title} · DDIA 第二版 · 架构提升读书笔记</title>', head)
    head = re.sub(r'<meta name="description" content="[^"]*">', '<meta name="description" content="DDIA第二版第9章中文读书笔记：部分失败、TCP与超时、时钟误差、进程暂停、租约和资源端隔离令牌、安全性与活性、形式化方法和确定性模拟测试。">', head)
    page = head + f'''  <main id="main" class="container reader-container">
    <nav class="breadcrumb" aria-label="当前位置"><ol><li><a href="../../../index.html">书架</a></li><li><a href="../index.html">书籍概览</a></li><li aria-current="page">第 9 章</li></ol></nav>
    <div class="reading-layout">
      <aside class="toc"><nav aria-label="本页目录"><h2>本页目录</h2><ul>{toc_html}</ul><p class="toc-note"><a href="#sources">来源与核查</a> · <a href="../index.html">书籍概览</a></p></nav></aside>
      <article class="article">
        <header class="article-header"><p class="eyebrow">READING NOTES / CHAPTER 09</p><h1>{title}</h1><p class="article-deck">{html.escape(deck)}</p></header>
        {intro}
        <details class="mobile-toc"><summary>本页目录 · {len(sections)} 个小节</summary><nav aria-label="移动端本页目录"><ul>{toc_html}</ul><p><a href="#sources">来源、原书对应与核查</a></p></nav></details>
        {''.join(sections)}
        <details id="sources" class="source-note"><summary>{summary}</summary>{render(sources)}</details>
        <nav class="chapter-pagination" aria-label="章节翻页"><a class="page-link prev" href="ch08.html" rel="prev"><span class="page-label">← 上一章 · 第 8 章</span><span class="page-title">事务</span></a><a class="page-link next" href="ch10.html" rel="next"><span class="page-label">下一章 · 第 10 章 →</span><span class="page-title">一致性与共识</span></a><a class="pagination-home" href="../index.html">书籍概览与目录</a></nav>
      </article>
    </div>
  </main>
  <footer class="site-footer"><div class="container footer-inner"><span>个人书架 / 中文读书笔记</span><a href="#main">回到顶部 ↑</a></div></footer>
</body>
</html>
'''
    page = page.replace('<li aria-current="page">', '<li><a href="../guide.html">全书导航</a></li><li aria-current="page">')
    page = page.replace('书籍概览与目录</a></nav>', '书籍概览与目录</a><a class="pagination-home" href="../guide.html">全书专题导航</a></nav>')
    (BOOK / 'chapters/ch09.html').write_text(page)
    print(f'ch09.html: {len(sections)} sections, {len(re.findall("<figure", page))} figures')


if __name__ == '__main__':
    build()
