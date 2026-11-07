"""Render chapter 13 content into the shared static reading-page structure."""
from pathlib import Path
import html
import re
import xml.etree.ElementTree as ET
import markdown

BOOK = Path(__file__).resolve().parents[2]
source = (BOOK / 'notes/ch13.md').read_text()
reference = (BOOK / 'chapters/ch12.html').read_text()


def render(text):
    output = markdown.markdown(text, extensions=['tables', 'fenced_code'])
    output = re.sub(r'href="ch(\d{2})\.md', r'href="ch\1.html', output)
    output = output.replace('<table>', '<div class="table-scroll"><table>').replace('</table>', '</table></div>')

    def figure(match):
        image, caption = match.group(1), match.group(2)
        src = re.search(r'src="([^"]+)"', image).group(1)
        svg = ET.parse(BOOK / 'chapters' / src).getroot()
        image = image.replace(' />', f' width="{svg.get("width")}" height="{svg.get("height")}" loading="lazy">')
        return f'<figure class="concept-figure"><a href="{src}" target="_blank" rel="noopener">{image}</a><figcaption>{caption}</figcaption></figure>'

    output = re.sub(r'<p>(<img [^>]+>)</p>\s*<p>(图 13-\d+：.*?)</p>', figure, output, flags=re.S)
    output = re.sub(r'<a href="([^"]+\.svg)"(?! target)', r'<a href="\1" target="_blank" rel="noopener"', output)
    return output


body, sources = source.split('<details id="sources">', 1)
sources = sources.split('</details>', 1)[0]
summary = re.search(r'<summary>(.*?)</summary>', sources).group(1)
sources = re.sub(r'^\s*<summary>.*?</summary>\s*', '', sources, flags=re.S)
body = re.sub(r'^# .*?\n\n\*\*.*?\*\*\n\n', '', body, count=1, flags=re.S)
parts = re.split(r'<a id="([^"]+)"></a>\s*\n\n## (\d+)　([^\n]+)\n\n', body)
intro = render(parts[0])
sections, toc = [], []
for i in range(1, len(parts), 4):
    anchor, number, title, content = parts[i:i+4]
    toc.append(f'<li><a href="#{anchor}">{number}　{html.escape(title)}</a></li>')
    sections.append(f'<section id="{anchor}">\n<h2><span class="section-number">{number}</span>{html.escape(title)}</h2>\n{render(content)}\n</section>')
toc_html = '\n'.join(toc)
head = reference.split('  <main id="main"', 1)[0]
head = re.sub(r'<title>.*?</title>', '<title>第 13 章｜流系统的哲学 · DDIA 第二版 · 架构提升读书笔记</title>', head)
head = re.sub(r'<meta name="description" content="[^"]*">', '<meta name="description" content="DDIA第二版第13章中文读书笔记：数据集成、拆分数据库、读写路径与订阅、稳定请求ID、多分片支付、及时性和完整性，以及端到端审计。">', head)
page = head + f'''  <main id="main" class="container reader-container">
    <nav class="breadcrumb" aria-label="当前位置"><ol><li><a href="../../../index.html">书架</a></li><li><a href="../index.html">书籍概览</a></li><li aria-current="page">第 13 章</li></ol></nav>
    <div class="reading-layout">
      <aside class="toc"><nav aria-label="本页目录"><h2>本页目录</h2><ul>{toc_html}</ul><p class="toc-note"><a href="#sources">来源与核查</a> · <a href="../index.html">书籍概览</a></p></nav></aside>
      <article class="article">
        <header class="article-header"><p class="eyebrow">READING NOTES / CHAPTER 13</p><h1>第 13 章｜流系统的哲学</h1><p class="article-deck"><span lang="en">A Philosophy of Streaming Systems</span> · 组合数据系统，也组合正确性责任</p></header>
        {intro}
        <details class="mobile-toc"><summary>本页目录 · {len(sections)} 个小节</summary><nav aria-label="移动端本页目录"><ul>{toc_html}</ul><p><a href="#sources">来源、原书对应与核查</a></p></nav></details>
        {''.join(sections)}
        <details id="sources" class="source-note"><summary>{summary}</summary>{render(sources)}</details>
        <nav class="chapter-pagination" aria-label="章节翻页"><a class="page-link prev" href="ch12.html" rel="prev"><span class="page-label">← 上一章 · 第 12 章</span><span class="page-title">流处理</span></a><a class="page-link next" href="ch14.html" rel="next"><span class="page-label">下一章 · 第 14 章 →</span><span class="page-title">做正确的事</span></a><a class="pagination-home" href="../index.html">书籍概览与目录</a></nav>
      </article>
    </div>
  </main>
  <footer class="site-footer"><div class="container footer-inner"><span>个人书架 / 中文读书笔记</span><a href="#main">回到顶部 ↑</a></div></footer>
</body>
</html>
'''
page = page.replace('<li aria-current="page">', '<li><a href="../guide.html">全书导航</a></li><li aria-current="page">')
page = page.replace('书籍概览与目录</a></nav>', '书籍概览与目录</a><a class="pagination-home" href="../guide.html">全书专题导航</a></nav>')
(BOOK / 'chapters/ch13.html').write_text(page)
print(f'ch13.html: {len(sections)} sections, {len(re.findall("<figure", page))} figures')
