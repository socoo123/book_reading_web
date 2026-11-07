# 图示资源

第二章的 `ch02-feedback-timing.svg`（反馈时机与返工）、`ch02-shared-knowledge.svg`（知识单点与共享维护）作为图文风格参考。后续已制作章节沿用 `chNN-<主题>.svg` 命名，具体图示随对应章节维护。

- `sources/`：保存可编辑图源，如 `.d2`、`.excalidraw`、Mermaid 或原生 SVG 源文件。目前各章采用原创手写 SVG。
- `exports/`：保存网页引用的导出资源，优先 SVG。

后续图源与导出文件使用同一基础名称，按已确认的章节和图示主题命名。图示聚焦一个问题，正文附阅读说明与图注；适配浅深色及移动端，不仅依赖颜色表达含义。复杂图先沟通再制作。

本次源文件与导出文件内容一致，修改时同步两个目录；SVG 内含浅深色规则，嵌入页面时跟随页面主题。新图以 `exports/ch25-replaceable-work.svg` 为模板：保留其颜色变量、`prefers-color-scheme` 与 `data-theme` 深色规则，以及读取 `reading-notes-theme` 的小脚本，单独打开大图时也跟随已保存的主题；全部图示已统一为这一写法。网页只引用 `exports/`，发布工作流排除 `sources/`。手机局部横向滚动，点击可打开大图。
