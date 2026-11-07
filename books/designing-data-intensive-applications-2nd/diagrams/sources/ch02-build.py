"""Chapter-local authoring utility; generate ch02.html from the synchronized Markdown."""
from pathlib import Path
import html
import re
import xml.etree.ElementTree as ET

import markdown


book = Path(__file__).resolve().parents[2]
root = book.parents[1]
source = (book / "notes/ch02.md").read_text()
main, sources = source.split('<details id="sources">', 1)
sources = sources.split('</details>', 1)[0]
sources = re.sub(r'^\s*<summary>.*?</summary>\s*', '', sources, flags=re.S)
parts = re.split(r'<a id="([^"]+)"></a>\n\n## (\d+)　([^\n]+)\n', main)
intro = parts[0]
intro = re.sub(r'^# [^\n]+\n\n\*\*[^\n]+\*\*\n\n', '', intro)
sections = [parts[i:i + 4] for i in range(1, len(parts), 4)]


def render(text):
    result = markdown.markdown(text.strip(), extensions=['tables', 'fenced_code'])
    result = re.sub(r'href="ch(\d{2})\.md(?=["#])', r'href="ch\1.html', result)
    result = result.replace('<table>', '<div class="table-scroll" tabindex="0" role="region" aria-label="资源共享方式比较表"><table>')
    result = result.replace('</table>', '</table></div>')

    def figure(match):
        image, caption = match.groups()
        image_path = re.search(r'src="([^"]+)"', image).group(1)
        svg = ET.parse((book / 'chapters' / image_path).resolve()).getroot()
        width = round(float(svg.attrib['width']))
        height = round(float(svg.attrib['height']))
        image = image.replace(' />', f' width="{width}" height="{height}" loading="lazy">')
        caption = caption.replace('<a ', '<a target="_blank" rel="noopener" ')
        return (f'<figure class="concept-figure"><a href="{image_path}" target="_blank" rel="noopener">'
                f'{image}</a><figcaption>{caption}</figcaption></figure>')

    return re.sub(r'<p>(<img [^>]+>)</p>\s*<p>(图 .*?)</p>', figure, result, flags=re.S)


toc = '\n'.join(f'<li><a href="#{anchor}">{number}　{html.escape(title)}</a></li>'
                for anchor, number, title, _ in sections)
reference = (root / 'books/just-enough-software-architecture/chapters/ch02.html').read_text()
prefix = reference.split('      <aside class="toc">', 1)[0]
prefix = re.sub(r'<title>.*?</title>', '<title>第 2 章｜定义非功能性需求 · DDIA 第二版 · 中文读书笔记</title>', prefix)
prefix = re.sub(r'<meta name="description" content="[^"]*">', '<meta name="description" content="DDIA 英文第二版第2章：时间线读写物化、响应时间与分位数、尾延迟与排队、容错、可扩展性和可维护性的中文详解。">', prefix)
prefix = prefix.replace('Just Enough Software Architecture</a>', 'DDIA · Second Edition</a>')
article_sections = '\n\n'.join(
    f'<section id="{anchor}">\n<h2><span class="section-number">{number}</span>{html.escape(title)}</h2>\n{render(content)}\n</section>'
    for anchor, number, title, content in sections)
page = prefix + f'''      <aside class="toc"><nav aria-label="本页目录"><h2>本页目录</h2><ul>
{toc}
      </ul><p class="toc-note"><a href="#sources">来源与核查</a><br><a href="../index.html">← 书籍概览</a></p></nav></aside>
      <article class="article">
        <header class="article-header">
          <p class="eyebrow">READING NOTES / CHAPTER 02</p>
          <h1>第 2 章｜定义非功能性需求</h1>
          <p class="article-deck"><span lang="en">Defining Nonfunctional Requirements</span> · 把“快、可靠、能增长”写成可以检验的约定</p>
        </header>
{render(intro)}
        <details class="mobile-toc"><summary>本页目录 · 12 个小节</summary><nav aria-label="移动端本页目录"><ul>
{toc}
        <li><a href="#sources">来源与核查</a></li></ul></nav></details>

{article_sections}

        <details id="sources" class="source-note">
          <summary>来源、原书对应与核查说明</summary>
{render(sources)}
        </details>
        <nav class="chapter-pagination" aria-label="章节翻页"><a class="page-link prev" href="ch01.html" rel="prev"><span class="page-label">← 上一章 · 第 1 章</span><span class="page-title">数据系统架构的权衡取舍</span></a><a class="page-link next" href="ch03.html" rel="next"><span class="page-label">下一章 · 第 3 章 →</span><span class="page-title">数据模型与查询语言</span></a><a class="pagination-home" href="../index.html">书籍概览与目录</a></nav>
      </article>
    </div>
  </main>
  <footer class="site-footer"><div class="container footer-inner"><span>个人书架 / 中文读书笔记</span><a href="#main">回到顶部 ↑</a></div></footer>
</body>
</html>
'''
page = page.replace('<li aria-current="page">', '<li><a href="../guide.html">全书导航</a></li><li aria-current="page">')
page = page.replace('书籍概览与目录</a></nav>', '书籍概览与目录</a><a class="pagination-home" href="../guide.html">全书专题导航</a></nav>')
(book / 'chapters').mkdir(exist_ok=True)
(book / 'chapters/ch02.html').write_text(page)
print(f'Generated {book / "chapters/ch02.html"}: {len(sections)} sections, {page.count("<figure ")} figures')
