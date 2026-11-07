"""Authoring-only: render this chapter's Markdown into the shared reading shell.

Run from any directory with Python-Markdown installed. No website runtime dependency.
"""
from pathlib import Path
import html
import re
import xml.etree.ElementTree as ET

import markdown

BOOK = Path(__file__).resolve().parents[2]
ROOT = BOOK.parents[1]
source = (BOOK / "notes/ch01.md").read_text()
template = (ROOT / "books/just-enough-software-architecture/chapters/ch02.html").read_text()
title = source.splitlines()[0].removeprefix("# ")
deck = source.splitlines()[2].strip("*")
english, subtitle = deck.split(" · ", 1)
main, references = source.split('<details id="sources">', 1)
references = references.split("</details>", 1)[0]
summary = re.search(r"<summary>(.*?)</summary>", references).group(1)
references = references.split("</summary>", 1)[1].strip()
parts = re.split(r'<a id="([^"]+)"></a>\s*\n## (\d+)　([^\n]+)\n', main)
intro = "\n".join(parts[0].splitlines()[4:]).strip()
sections = [parts[i:i + 4] for i in range(1, len(parts), 4)]


def render(text):
    result = markdown.markdown(text, extensions=["tables", "fenced_code"])
    result = re.sub(r'href="ch(\d+)\.md', r'href="ch\1.html', result)
    result = result.replace("<table>", '<div class="table-scroll" tabindex="0" role="region" aria-label="可横向滚动的数据表格"><table>')
    result = result.replace("</table>", "</table></div>")

    def figure(match):
        image, caption = match.groups()
        path = re.search(r'src="([^"]+)"', image).group(1)
        svg = ET.parse((BOOK / "chapters" / path).resolve()).getroot()
        image = image.replace(" />", f' width="{svg.attrib["width"]}" height="{svg.attrib["height"]}" loading="lazy" />')
        return (f'<figure class="concept-figure"><a href="{path}" target="_blank" rel="noopener">'
                f'{image}</a><figcaption>{caption}</figcaption></figure>')

    return re.sub(r"<p>(<img [^>]+>)</p>\s*<p>(图 .*?)</p>", figure, result, flags=re.S)


toc = "\n".join(f'<li><a href="#{anchor}">{number}　{html.escape(heading)}</a></li>'
                for anchor, number, heading, _ in sections)
toc += '\n<li><a href="#sources">来源与核查说明</a></li>'
header = re.search(r'  <header class="site-header.*?</header>', template, re.S).group()
header = header.replace("Just Enough Software Architecture", "DDIA · Second Edition")
body = "\n\n".join(
    f'<section id="{anchor}">\n<h2><span class="section-number">{number}</span>{html.escape(heading)}</h2>\n'
    f'{render(content)}\n</section>'
    for anchor, number, heading, content in sections)

output = f'''<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)} · DDIA 第二版 · 架构提升读书笔记</title>
  <meta name="description" content="DDIA 英文第二版第1章中文精读：OLTP与OLAP、数据仓库与湖、权威与派生数据、云与自建、存算分离、单机与分布式、微服务、Serverless及数据责任。">
  <link rel="icon" href="../../../assets/favicon.svg" type="image/svg+xml">
  <script src="../../../assets/theme.js"></script>
  <script src="../../../assets/reader.js" defer></script>
  <link rel="stylesheet" href="../../../assets/styles.css">
</head>
<body>
  <a class="skip-link" href="#main">跳到主要内容</a>
{header}
  <main id="main" class="container reader-container">
    <nav class="breadcrumb" aria-label="当前位置"><ol><li><a href="../../../index.html">书架</a></li><li><a href="../index.html">书籍概览</a></li><li aria-current="page">第 1 章</li></ol></nav>
    <div class="reading-layout">
      <aside class="toc"><nav aria-label="本页目录"><h2>本页目录</h2><ul>{toc}</ul><p class="toc-note"><a href="../index.html">← 书籍概览</a></p></nav></aside>
      <article class="article">
        <header class="article-header"><p class="eyebrow">READING NOTES / CHAPTER 01</p><h1>{html.escape(title)}</h1><p class="article-deck"><span lang="en">{html.escape(english)}</span> · {html.escape(subtitle)}</p></header>
        {render(intro)}
        <details class="mobile-toc"><summary>本页目录 · {len(sections)} 个小节</summary><nav aria-label="移动端本页目录"><ul>{toc}</ul></nav></details>
        {body}
        <details id="sources" class="source-note"><summary>{summary}</summary>{render(references)}</details>
        <nav class="chapter-pagination" aria-label="章节翻页"><a class="page-link prev" href="../index.html" rel="prev"><span class="page-label">← 上一页 · 书籍概览</span><span class="page-title">DDIA · Second Edition</span></a><a class="page-link next" href="ch02.html" rel="next"><span class="page-label">下一章 · 第 2 章 →</span><span class="page-title">定义非功能性需求</span></a><a class="pagination-home" href="../index.html">书籍概览与目录</a></nav>
      </article>
    </div>
  </main>
  <footer class="site-footer"><div class="container footer-inner"><span>个人书架 / 中文读书笔记</span><a href="#main">回到顶部 ↑</a></div></footer>
</body>
</html>
'''
output = output.replace('<li aria-current="page">', '<li><a href="../guide.html">全书导航</a></li><li aria-current="page">')
output = output.replace('书籍概览与目录</a></nav>', '书籍概览与目录</a><a class="pagination-home" href="../guide.html">全书专题导航</a></nav>')
destination = BOOK / "chapters/ch01.html"
destination.parent.mkdir(exist_ok=True)
destination.write_text(output)
print(f"Rendered {destination}: {len(sections)} sections, 2 figures")
