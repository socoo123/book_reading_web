"""Render the whole-book guide; authoring dependency: Python-Markdown."""
from pathlib import Path
import html
import re
import markdown

BOOK = Path(__file__).resolve().parents[2]
source = (BOOK / 'notes/guide.md').read_text()


def render(text):
    output = markdown.markdown(text, extensions=['tables', 'fenced_code'])
    output = re.sub(r'href="ch(\d{2})\.md', r'href="chapters/ch\1.html', output)
    output = re.sub(r'href="../../([^/]+)/notes/(ch\d{2})\.md',
                    r'href="../\1/chapters/\2.html', output)
    output = output.replace('<table>', '<div class="table-scroll" tabindex="0" role="region" aria-label="可横向滚动的专题对照表"><table>')
    return output.replace('</table>', '</table></div>')


body, sources = source.split('<details id="sources">', 1)
sources = sources.split('</details>', 1)[0]
summary = re.search(r'<summary>(.*?)</summary>', sources).group(1)
sources = sources.split('</summary>', 1)[1]
body = re.sub(r'^# [^\n]+\n\n', '', body)
parts = re.split(r'<a id="([^"]+)"></a>\s*\n\n## (\d+)　([^\n]+)\n\n', body)
sections, toc = [], []
for i in range(1, len(parts), 4):
    anchor, number, title, content = parts[i:i+4]
    toc.append(f'<li><a href="#{anchor}">{number}　{html.escape(title)}</a></li>')
    sections.append(f'<section id="{anchor}"><h2><span class="section-number">{number}</span>{html.escape(title)}</h2>\n{render(content)}\n</section>')
toc_html = '\n'.join(toc)
head = (BOOK / 'chapters/ch14.html').read_text().split('  <main id="main"', 1)[0]
head = head.replace('../../../', '../../').replace('href="../index.html"', 'href="index.html"')
head = re.sub(r'<title>.*?</title>', '<title>全书导航｜机制、保证与数据责任 · DDIA 第二版</title>', head)
head = re.sub(r'<meta name="description" content="[^"]*">', '<meta name="description" content="DDIA第二版全书导航：五条专题路线，关键术语、保证边界、案例、十四章来源与纠错入口。">', head)
page = head + f'''  <main id="main" class="container reader-container">
    <nav class="breadcrumb" aria-label="当前位置"><ol><li><a href="../../index.html">书架</a></li><li><a href="index.html">书籍概览</a></li><li aria-current="page">全书导航</li></ol></nav>
    <div class="reading-layout">
      <aside class="toc"><nav aria-label="本页目录"><h2>本页目录</h2><ul>{toc_html}</ul><p class="toc-note"><a href="#sources">来源与整合范围</a> · <a href="index.html">书籍概览</a></p></nav></aside>
      <article class="article">
        <header class="article-header"><p class="eyebrow">READING NOTES / WHOLE-BOOK GUIDE</p><h1>全书导航｜机制、保证与数据责任</h1><p class="article-deck">五条专题路线 · 从问题和失败路径回到十四章详解</p></header>
        {render(parts[0])}
        <details class="mobile-toc"><summary>本页目录 · {len(sections)} 个小节</summary><nav aria-label="移动端本页目录"><ul>{toc_html}</ul><p><a href="#sources">来源与整合范围</a></p></nav></details>
        {''.join(sections)}
        <details id="sources" class="source-note"><summary>{summary}</summary>{render(sources)}</details>
        <nav class="chapter-pagination" aria-label="阅读导航"><a class="page-link prev" href="index.html"><span class="page-label">← 书籍概览</span><span class="page-title">十四章完整目录</span></a><a class="page-link next" href="chapters/ch01.html"><span class="page-label">按原章序阅读 →</span><span class="page-title">第1章 · 数据系统架构的权衡取舍</span></a></nav>
      </article>
    </div>
  </main>
  <footer class="site-footer"><div class="container footer-inner"><span>个人书架 / 中文读书笔记</span><a href="#main">回到顶部 ↑</a></div></footer>
</body>
</html>
'''
(BOOK / 'guide.html').write_text(page)
print(f'guide.html: {len(sections)} sections')
