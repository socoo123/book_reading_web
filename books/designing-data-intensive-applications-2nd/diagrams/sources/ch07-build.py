"""Authoring-only: render chapter 7 Markdown into the existing static reader shell."""
from pathlib import Path
import html
import re
import xml.etree.ElementTree as ET
import markdown

BOOK = Path(__file__).resolve().parents[2]
source = (BOOK / 'notes/ch07.md').read_text()
source = re.sub(r'\]\(ch(\d+)\.md', r'](ch\1.html', source)
intro, rest = source.split('<a id="shards-and-replicas"></a>', 1)
intro = '\n'.join(intro.splitlines()[4:])
body, sources = ('<a id="shards-and-replicas"></a>' + rest).split('<details id="sources" class="source-note">', 1)
sections = re.findall(r'<a id="([^"]+)"></a>\s*## (\d+)　([^\n]+)\n(.*?)(?=<a id="|\Z)', body, re.S)

def render(text):
    value = markdown.markdown(text, extensions=['fenced_code', 'tables'])
    value = re.sub(r'<table>(.*?)</table>', r'<div class="table-scroll" tabindex="0" role="region" aria-label="可横向滚动的数据表格"><table>\1</table></div>', value, flags=re.S)
    def figure(match):
        image, caption = match.groups()
        path = re.search(r'src="([^"]+)"', image).group(1)
        width, height = ET.parse(BOOK / 'chapters' / path).getroot().attrib['viewBox'].split()[2:]
        image = image.replace('<img ', f'<img width="{width}" height="{height}" loading="lazy" ')
        return f'<figure class="concept-figure" tabindex="0" aria-label="可横向滚动的图示"><a href="{path}" target="_blank" rel="noopener">{image}</a><figcaption>{caption}</figcaption></figure>'
    return re.sub(r'<p>(<img [^>]+/?>)</p>\s*<p>(图 7-[1-4]：.*?)</p>', figure, value, flags=re.S)

toc = '\n'.join(f'<li><a href="#{anchor}">{number}　{html.escape(title)}</a></li>' for anchor, number, title, _ in sections)
toc += '<li><a href="#sources">来源与核查说明</a></li>'
article = '\n'.join(f'<section id="{anchor}"><h2><span class="section-number">{number}</span>{html.escape(title)}</h2>\n{render(text)}</section>' for anchor, number, title, text in sections)
sources = re.sub(r'^\s*<summary>.*?</summary>', '', sources, flags=re.S).split('</details>', 1)[0]
sources_html = '<details id="sources" class="source-note"><summary>来源、原书对应与核查说明</summary>' + render(sources) + '</details>'
reference = (BOOK / 'chapters/ch01.html').read_text()
header = re.search(r'<header class="site-header reader-header">.*?</header>', reference, re.S).group()
page = f'''<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>第 7 章｜分片 · DDIA 第二版 · 中文读书笔记</title>
  <meta name="description" content="DDIA第二版第7章：范围、哈希与复合键，分片和节点的区别，热点与再平衡，协调迁移，请求路由，以及本地和全局二级索引的读写代价。">
  <link rel="icon" href="../../../assets/favicon.svg" type="image/svg+xml">
  <script src="../../../assets/theme.js"></script>
  <script src="../../../assets/reader.js" defer></script>
  <link rel="stylesheet" href="../../../assets/styles.css">
</head>
<body>
  <a class="skip-link" href="#main">跳到主要内容</a>
  {header}
  <main id="main" class="container reader-container">
    <nav class="breadcrumb" aria-label="当前位置"><ol><li><a href="../../../index.html">书架</a></li><li><a href="../index.html">书籍概览</a></li><li aria-current="page">第 7 章</li></ol></nav>
    <div class="reading-layout">
      <aside class="toc"><nav aria-label="本页目录"><h2>本页目录</h2><ul>{toc}</ul><p class="toc-note"><a href="../index.html">← 书籍概览</a></p></nav></aside>
      <article class="article">
        <header class="article-header">
          <p class="eyebrow">READING NOTES / CHAPTER 07</p>
          <h1>第 7 章｜分片</h1>
          <p class="article-deck"><span lang="en">Sharding</span> · 拆开数据以后，怎样分担工作、找到记录并完成交接</p>
        </header>
        {render(intro)}
        <details class="mobile-toc"><summary>本页目录 · {len(sections)} 个小节</summary><nav aria-label="移动端本页目录"><ul>{toc}</ul></nav></details>
        {article}
        {sources_html}
        <nav class="chapter-pagination" aria-label="章节翻页"><a class="page-link prev" href="ch06.html" rel="prev"><span class="page-label">← 上一章 · 第 6 章</span><span class="page-title">复制</span></a><a class="page-link next" href="ch08.html" rel="next"><span class="page-label">下一章 · 第 8 章 →</span><span class="page-title">事务</span></a><a class="pagination-home" href="../index.html">书籍概览与目录</a></nav>
      </article>
    </div>
  </main>
  <footer class="site-footer"><div class="container footer-inner"><span>个人书架 / 中文读书笔记</span><a href="#main">回到顶部 ↑</a></div></footer>
</body>
</html>
'''
page = page.replace('<li aria-current="page">', '<li><a href="../guide.html">全书导航</a></li><li aria-current="page">')
page = page.replace('书籍概览与目录</a></nav>', '书籍概览与目录</a><a class="pagination-home" href="../guide.html">全书专题导航</a></nav>')
(BOOK / 'chapters/ch07.html').write_text(page)
print(f'Rendered {len(sections)} sections, {len(page)} HTML characters')
