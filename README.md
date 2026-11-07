# 架构提升读书笔记

当前接入 **4 本书**，正文沿用 16px。在线阅读：<https://socoo123.github.io/book_reading_web/>。

**当前任务：第四本《Designing Data-Intensive Applications》英文第二版（2026），第5轮全书整合已完成、待验收。** [概览与目录](books/designing-data-intensive-applications-2nd/index.html)开放全部14章；[全书导航](books/designing-data-intensive-applications-2nd/guide.html)提供五条路线、术语、保证范围、案例、来源及纠错。正文保留250节、64幅章节图及原有深度，另有1幅概览图；前四轮待验收状态保留。完整安排见 [`PLAN.md`](PLAN.md)，最终交接见 [`CONTINUE.md`](CONTINUE.md)。

**第5轮已停止，无后台写作任务。** 主Agent GPT-6 Astra（`openai/gpt-6-astra`）独立完成，档位未由环境暴露；未调用子Agent、未续用前四轮会话。当前等待用户验收。原书固定路径：`/Users/zy/ai_learn/ddia_2nd/Designing_Data_Intensive_Applications_2nd_Edition.pdf`（673页，正文PDF页序＝印刷页码＋24）。

- **Just Enough Software Architecture**：第 1—5 步已验收；**第 6 步全书整合已完成，待验收**。当前收录 16／16 章，附术语、案例、来源及纠错导航；全书 PDF 固定路径见下。
- **Software Engineering at Google**：第二章至第二十五章及后记已验收；第一章补写已完成审稿验证、待验收。依据 Abseil 官方公开英文 HTML 版，已读取第 1—25 章及后记正文与脚注；与用户 PDF 的一致性尚待核对。

本站持续收录多本书，以内容充分、连贯的文章讲清核心观点、推理和案例，篇幅服从理解需要。优先自然叙述，减少反问、反驳及反复限定；用少量色块突出重点、小图解释观点或流程，来源收在文末。写作标准见 [`PLAN.md`](PLAN.md)。

第三本 **Software Architecture: The Hard Parts** 已接入书架与[概览](books/software-architecture-the-hard-parts/index.html)，**第5轮全书整合已完成，待验收**。全书15章、188节、46幅原创图、29张表、13个代码块（含说明性片段）；[全书导航](books/software-architecture-the-hard-parts/guide.html)含五条专题路径、34组术语、13项案例ADR、15章来源和12组纠错入口。正文按第 **1—4、5—8、9—12、13—15 章**分四轮制作，每名全新 **GPT-6 Astra · high**（`openai/gpt-6-astra#high`）子 Agent只负责一章，交付后均已返回、停止编辑；第5轮由主Agent独立接管整合。该书计划见[历史计划](books/software-architecture-the-hard-parts/PLAN-history.md)，轮次交接见[历史交接](books/software-architecture-the-hard-parts/CONTINUE-history.md)，前两本书的历史交接见 [`CONTINUE-history.md`](CONTINUE-history.md)。

**Hard Parts第5轮已结束。** 主Agent完成术语、案例与来源整合、最小验证及交接；该轮未调用子Agent，未续用旧内容会话。各轮待验收状态保留；当前制作计划已切换至DDIA第二版。

新书原文：`/Users/zy/Downloads/Software.Architecture.The.Hard.Parts.pdf`（462 页，已确认可读）；全文、15 章分章及前言／附录文本已提取至本书 `originals/`。版本、术语及页面约定见[本书说明](books/software-architecture-the-hard-parts/README.md)。

JESA 原文固定路径：`~/Downloads/Just Enough Software Architecture A Risk-Driven Approach.pdf`（378 页，已确认可读）。后续直接读取，无须重复上传；解析文本保存在该书 `originals/`，不进入部署产物。

## 本地预览

在本项目目录运行：

```sh
python3 -m http.server 8000
```

浏览器打开 <http://localhost:8000>。按 `Ctrl+C` 停止服务。

纯 HTML、CSS、JavaScript，无第三方依赖、安装步骤或构建步骤。静态托管时保留相对路径与目录结构即可；核心页面和导航无需 JavaScript。

## 文件结构

```text
index.html                                  # 书架首页
CONTINUE.md                                 # 当前进度与新会话提示词
.github/workflows/pages.yml                  # GitHub Pages 静态文件部署
assets/
  styles.css                                # 共享排版、组件及浅深色样式
  theme.js                                  # 主题切换按钮（跟随系统／浅色／深色）与本地保存
  reader.js                                 # 阅读页顶部进度条与侧栏目录高亮当前小节
  favicon.svg                               # 站点图标
books/just-enough-software-architecture/
  README.md                                 # 版本、原文位置、页序与核查记录
  index.html                                # 书籍概览与16章目录
  guide.html                                # 术语、跨章案例、来源与纠错导航
  notes/guide.md                            # 导航的 Markdown 内容源
  notes/ch01.md … ch16.md                    # 已收录十六章 Markdown 内容源
  chapters/ch01.html … ch16.html             # 对应静态阅读页
  diagrams/sources/                         # 可编辑图源
  diagrams/exports/                         # 网页SVG副本
  originals/                               # 官方试读PDF、全书及分章解析文本，仅本地留存
books/software-engineering-at-google/
  index.html                                # 书籍概览与已核对目录
  notes/ch01.md                             # 第一章 Markdown 内容源
  chapters/ch01.html                        # 第一章补写阅读页
  notes/ch02.md                             # 第二章图文样稿内容源
  chapters/ch02.html                        # 第二章图文样稿阅读页
  notes/ch03.md … ch06.md                    # 已验收四章 Markdown 内容源
  chapters/ch03.html … ch06.html             # 已验收四章阅读页
  notes/ch07.md … ch10.md                    # 已验收四章 Markdown 内容源
  chapters/ch07.html … ch10.html             # 已验收四章阅读页
  notes/ch11.md … ch14.md                    # 已验收四章 Markdown 内容源
  chapters/ch11.html … ch14.html             # 已验收四章阅读页
  notes/ch15.md … ch18.md                    # 已验收四章 Markdown 内容源
  chapters/ch15.html … ch18.html             # 已验收四章阅读页
  notes/ch19.md … ch22.md                    # 已验收四章 Markdown 内容源
  chapters/ch19.html … ch22.html             # 已验收四章阅读页
  notes/ch23.md … ch25.md                    # 已验收三个主体章节内容源
  chapters/ch23.html … ch25.html             # 已验收三个主体章节阅读页
  notes/afterword.md                         # 后记内容源
  chapters/afterword.html                    # 后记阅读页，不计为第26章
  chapters/reading-template.html            # 阅读布局示例，不是正式章节
  diagrams/
    README.md                               # 图源与导出约定
    sources/README.md                        # 可编辑图源目录说明
    exports/README.md                        # 网页导出资源目录说明
```

第三本书文件组织：

```text
books/software-architecture-the-hard-parts/
  README.md                  # 版本、术语、案例状态与核查交接
  index.html                 # 概览与15章完整目录
  guide.html                 # 全书路线、术语、ADR、来源、纠错与附录导航
  notes/guide.md             # 导航内容源
  notes/ch01.md … ch15.md    # 已收录十五章内容源
  chapters/ch01.html … ch15.html
  diagrams/sources/          # 可编辑解释图
  diagrams/exports/          # 网页使用的SVG副本
  originals/                 # 全文、前言、15章与附录提取文本，仅本地
```

## 阅读与验收

第四本书沿用同一目录组织：`books/designing-data-intensive-applications-2nd/`下的`notes/ch01.md`—`ch14.md`为内容源，`chapters/ch01.html`—`ch14.html`为阅读页，`notes/guide.md`／`guide.html`为全书导航；`notes/chNN-report.md`与`notes/integration-report.md`为逐章及整合核查记录。`diagrams/sources/`与`diagrams/exports/`保留图源和网页SVG；`originals/`仅本地。

- **DDIA第二版第5轮入口：[全书导航](books/designing-data-intensive-applications-2nd/guide.html)。** 12节guide含五条路线、43组术语、11行保证范围、15项案例、14章来源及16组纠错；40个跨章小节入口新增或细化。17页1,504项引用、262节与15份来源／引言MD—HTML全文、65组图源及81文件发布筛选通过；Chrome16组和14章正反导航通过，正文16px。整合前250节及历史来源保留，当前正文189,130汉字；332份基线290份不变，42份预期编辑。模型、深度复核、证据和遗留见[整合报告](books/designing-data-intensive-applications-2nd/notes/integration-report.md)。已停止待验收，未部署。

- DDIA第二版第4轮入口：[概览](books/designing-data-intensive-applications-2nd/index.html) → [第13章：流系统的哲学](books/designing-data-intensive-applications-2nd/chapters/ch13.html) → [第14章：做正确的事](books/designing-data-intensive-applications-2nd/chapters/ch14.html)。两章38节、23,218汉字、9图；主审复核端到端去重／支付恢复／读隔离，以及预测反馈、隐私与用途限制，补上FTC2026最终和解状态。16页1,137项引用、MD／HTML全文、9组图源及80文件发布筛选通过；Chrome28组与正反翻页通过。SQL／支付教学模型及概率算例通过；263份基线仅第12章三份衔接文件变更，旧稿未动。累计正文189,123汉字；第4轮完成待验收并停止，guide留第5轮。德国定价论文仅取得摘要、ACM准则按原书转述；未做真实产品集成、集群故障注入、性能测试或社会因果识别。详情见[本书说明](books/designing-data-intensive-applications-2nd/README.md)。
- DDIA第3轮历史：[第9章：分布式系统的困难](books/designing-data-intensive-applications-2nd/chapters/ch09.html) → 一致性与共识 → 批处理 → 流处理。四章84节、62,006汉字、23图；主审、14页960项引用、Chrome60组、关键教学模型及Unix／SQLite验证完成，原待验收状态保留。
- DDIA第2轮历史：[第5章：编码与演化](books/designing-data-intensive-applications-2nd/chapters/ch05.html) → 复制 → 分片 → 事务，73节、59,064汉字、19图。主审、静态／浏览器验证与关键教学例子检查已完成，原待验收状态保留。
- DDIA第1轮历史：第1—4章55节、44,863汉字、13图；主审、静态／浏览器检查与关键示例验证已完成，原待验收状态保留，详细记录见本书说明。

- Hard Parts整合入口：[Hard Parts 全书导航](books/software-architecture-the-hard-parts/guide.html) → [案例ADR](books/software-architecture-the-hard-parts/guide.html#decisions)／[纠错入口](books/software-architecture-the-hard-parts/guide.html#corrections)。第5轮仅做全书整合，保留15章188节46图；补齐第2、4、10、14章前后文链接，统一书架与概览入口。18页链接／锚点、15章正文／来源／图表／代码双端同步、目录翻页、46组SVG与63个本书发布文件筛选通过；Chrome代表页面、主题与交互、独立SVG共14项通过，正文16px。附录A跨书引用、附录B漏列第14章ADR已对照原页说明；最终Saga ADR、生产契约、完整日实现及实测结果等原书缺口保留。详细结果见[本书说明](books/software-architecture-the-hard-parts/README.md)，交接见[历史交接](books/software-architecture-the-hard-parts/CONTINUE-history.md)。
- 前一本书整合入口：[书籍概览](books/just-enough-software-architecture/index.html) → [全书导航](books/just-enough-software-architecture/guide.html)，包含 30 组术语、5 条跨章案例路径、16 章来源及纠错索引。版本、原文路径与核查记录在[本书说明](books/just-enough-software-architecture/README.md)。第 6 步已完成、待验收。
- 全书保留 16 章、178 节、36 图及既有深度，统一术语与案例口径，补齐前后章引用与导航入口。19 页静态链接、正文双端同步、目录翻页及全部图源／导出检查通过；Chrome 导航／概览 8 项、代表章节及独立 SVG 10 项通过，桌面／手机及浅深色阅读正常。具身风格释义与图书馆属性命名已按原文补核。未初始化 Git、推送或部署。
- 上一本书：[第一章补写](books/software-engineering-at-google/chapters/ch01.html)，保留原验收状态。
- 第 3—25 章及后记已验收。上批入口：[第 23 章：持续集成](books/software-engineering-at-google/chapters/ch23.html)、[第 24 章：持续交付](books/software-engineering-at-google/chapters/ch24.html)、[第 25 章：计算即服务](books/software-engineering-at-google/chapters/ch25.html)、[后记](books/software-engineering-at-google/chapters/afterword.html)。
- 上一本书的[第二章](books/software-engineering-at-google/chapters/ch02.html)继续作为深度、案例和图文风格参考；各书后续批次、全书整合及部署按计划另行授权。
- 页面视觉（2026-11-06 改版）：沿用暖色纸张底与宋体标题；书架为带作者、简介和进度的书籍卡片，每本书使用独立配色的笔记封面；导航栏吸顶，阅读页底边显示阅读进度；概览页封面随目录吸附，并提供“开始阅读”入口；翻页为上一章／下一章卡片；重点框、旁注、表格、代码、图示与文末来源区统一圆角与层次。图示 SVG 内置的底色与 `--surface` 一致，调整配色时两者需同步。
- 外观首次跟随系统；可通过页眉的三个图标按钮选择跟随系统、浅色或深色。选择保存于浏览器 `localStorage`，跨页面及刷新保留；存储不可用时仅当前页生效。JavaScript 不可用时仍由 CSS 跟随系统主题。
- 桌面专注阅读与侧目录、手机响应式与顶部目录，以及长文、补充说明、纠错、引用、代码、表格和图示占位样式。
- 键盘 Tab 焦点、“跳到主要内容”、表格和代码区域的局部滚动。
- 已制作的相邻章节互相连接；尚未制作的章节显示文字状态。

书架使用设计封面，不作为原书版本核对依据。`reading-template.html` 保留为排版示例，不计入实际章节。来源与版本缺口见 [本书说明](books/software-engineering-at-google/README.md)。

## 部署到 GitHub Pages

仓库：<https://github.com/socoo123/book_reading_web>。

站点：<https://socoo123.github.io/book_reading_web/>。

仓库 Pages 使用 **GitHub Actions**，推送 `main` 会自动运行 `.github/workflows/pages.yml` 中的 `Deploy GitHub Pages`。可在 [Actions](https://github.com/socoo123/book_reading_web/actions) 查看部署结果或手动触发。

后续更新：

```sh
git add .
git commit -m "Update reading notes"
git push
```

`.gitignore` 排除原书 `originals/`、PDF、本地编辑器配置及生成目录。笔记与可编辑图源纳入 Git 版本管理，网站仅发布下述静态资源。上文各轮验收记录中的“未部署”描述为当轮历史状态。

默认地址规则：

- 普通项目仓库：`https://<用户名>.github.io/<仓库名>/`。
- 名为 `<用户名>.github.io` 的用户站点仓库：`https://<用户名>.github.io/`。
- 组织仓库对应使用组织名；自定义域名以 Pages 设置为准。

页面及资源使用相对路径，部署时保留原有目录结构，因此支持项目子路径，无需设置域名或修改链接前缀。

工作流无需 npm 或构建工具：将根 `index.html` 与 `assets/`、`books/` 下的 HTML、CSS、JavaScript、图片及网页字体复制到临时 `_site/`，仅上传该目录。采用文件类型白名单，并跳过 `notes/`、`sources/`、`originals/` 目录；Markdown 说明、内容源、可编辑图源及 PDF 原书均不进入部署产物。后续内容源与原书资料沿用这些目录，网页使用的图示放在 `diagrams/exports/`；新增网页资源类型时再更新工作流白名单。
