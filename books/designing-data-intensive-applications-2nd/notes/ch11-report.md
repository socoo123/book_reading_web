# 第11章《批处理》覆盖与核查报告

> 第3轮 Agent C；2026-11-07。第11章制作与验证完成，交付后停止编辑，等待主 Agent 主审接入。仅写本章授权文件，未递归委派。

## 资料与阅读

- 固定原书：Martin Kleppmann／Chris Riccomini，O’Reilly 2026英文第二版，ISBN978-1-098-11906-5。PDF475—510／印刷451—486；正文至印刷482页，之后为参考文献。PDF页序＝印刷页＋24。
- 已完整阅读 `originals/ddia2-ch11.txt` 1—1482行（含References），然后完整对照只读旧稿 `/Users/zy/ai_learn/ddia_2nd/ch11-批处理.md` 1—1238行。
- 已读根AGENTS／PLAN／CONTINUE、本书README、ch08页面与渲染工具、PLAN指定Google ch02与JESA ch03的文章风格参考。

## 原书覆盖结果

下表沿用写前已经落盘的覆盖表，所有锚点现已落实到 Markdown 与 HTML。参考文献清单完整读过，不表示逐篇通读全部引用论文。

| 原书小节／印刷页 | 实际笔记锚点 | 已保留机制、案例与边界 |
| --- | --- | --- |
| Introduction 451—453 | bounded-reruns | 不可变有界输入、派生输出、人为错误恢复、吞吐／新鲜度；第二版现代框架主线 |
| Unix Tools／Simple Log Analysis 454—455 | unix-pipeline | NGINX热门URL；自拟可运行8行日志、逐阶段结果 |
| Chain of Commands／Sorting Versus In-Memory Aggregation 456—457 | working-set | distinct key工作集、哈希聚合与外部归并、磁盘与内存代价 |
| Distributed Systems／Distributed Filesystems 457—460 | storage-compute | 三种职责、块／缓存／元数据／接口、复制与纠删码、局部性 |
| Object Stores 460—461 | object-storage | 对象键／前缀、存算分离、接口兼容不等于语义相同、原子发布前提 |
| Distributed Job Orchestration／Resource allocation 461—464 | scheduling | 执行器／资源视图／调度器，160核与两份100核工作、群组调度／抢占／饥饿 |
| Scheduling workflows 464—465 | workflows | DAG、多团队消费、跨工具、中间物化／流水线／背压、两级调度职责 |
| Handling faults 465—466 | fault-recovery | 任务级重试、抢占、部分输出、血缘重算、Flink批流恢复区别 |
| MapReduce 466—468 | mapreduce | 输入记录、map、同键分组reduce、第二次排序、确定性与纯函数边界 |
| Dataflow Engines 468—469 | dataflow | 算子融合、按需排序、局部性、进程复用、物化与恢复取舍 |
| Shuffling Data 469—471／图11-1 | shuffle | m_i,r_j逻辑分区、拉取／归并、同键归属；分片内有序不等于全局有序 |
| Joins and Grouping 471—473／图11-2、11-3 | joins | 活动事件与出生日期、二级排序、一对多、按URL再次分组 |
| join策略补充（非原章逐项展开） | join-costs | 广播／共分片／哈希连接、倾斜／内存／网络、清楚标记笔记补充 |
| Query Languages／Convergence／DataFrames 473—475 | sql-dataframes | SQL与DF统一计划、惰性／立即执行、无隐含顺序、数仓融合与成本前提 |
| ETL／Analytics 476—478 | etl-analytics | 缺字段排查、数据契约、湖仓表元数据、预聚合／即席查询 |
| Machine Learning 478—479 | machine-learning | 特征／训练／推理、BSP图迭代、网页预处理与token纠错 |
| Serving Derived Data 479—481 | publish | 外部写重复／半成品、流缓冲、版本暂存＋完整性屏障＋切换、bulk load |
| Summary 481—482 | conclusion | 机制判断与第12章有界到无界衔接 |

## 交付文件与统计

- 正文：[ch11.md](ch11.md)；静态阅读页：[ch11.html](../chapters/ch11.html)。18节、**12,352汉字**、1张正文表、4个代码块、4幅图。统计口径为来源区之前，去围栏代码，保留标题、表格、图注和替代文本；不是纯叙述段落字数。
- 比9—12千字规划略高，主要用于连接策略成本、恢复／发布失败路径及就地纠错；没有按字数加入产品目录或无关知识。初次验证为12,347，最终发布图图注澄清“导入或读取”后为12,352。
- `diagrams/sources/ch11-{layers,shuffle,join,publish}.excalidraw`：四份主要可编辑场景；各有同名 `.skeleton.json` 骨架及 `diagrams/exports/` 下的 `.svg`。
- 本章制作与检查脚本：`diagrams/sources/ch11-diagrams.py`、`ch11-render.py`、`ch11-check.py`、`ch11-browser.mjs`。生成器保留四图布局；修改现有场景后应从 `.excalidraw` 导出，避免骨架覆盖编辑结果。
- 本章共19份文件：2份笔记／报告、1份HTML、4份SVG、8份图源／骨架、4份脚本。共享官方导出器 `export-excalidraw.mjs` 与 API 桥接只读复用。
- 页面复用既有第8章阅读外壳：16px／1.95、桌面及手机目录、来源折叠、面包屑、表格／代码／图示局部滚动、图像alt与点击放大；翻页目标为前ch10、后ch12。

## 原书图表回看与本章图示

实际回看固定PDF中的原图11-1（印刷470／PDF494）、图11-2（472／496）、图11-3（473／497）。核对了mapper至reducer的数据去向、活动表与用户档案的关系，以及按用户连接后再按URL分组的顺序。本章没有独立编号数学公式；块大小、纠删码、广播量与年龄算例已另外复算。

另回看印刷461、462、466、479、480页，分别核对对象重命名、cgroups、Flink恢复、tokenization与embedding、输出全有或全无的上下文，确认问题不只是文本提取误差。图11-1附近的逻辑分区／物理文件解释也与Hadoop文档交叉核对。

以下编号属于**笔记自制图**，不冒称与原书图号逐一相同：

| 笔记图／文件干名 | 解释的问题与取舍 | 原生元素数 |
| --- | --- | ---: |
| 图11-1／`ch11-layers` | 存储、计算、工作流与资源调度的职责；实线读写、虚线控制，按原书457—465页重构 | 22 |
| 图11-2／`ch11-shuffle` | 仅展开r2接收三份有序区段并归并，省略其余去向，避免全连接图拥挤；不是全局排序或物理文件数承诺 | 29 |
| 图11-3／`ch11-join` | 单用户档案先到、两条事件顺序连接；明确一用户一档案的前提和后续改按URL分组 | 15 |
| 图11-4／`ch11-publish` | 笔记教学协议：隔离V18、验证完整性、原子切换引用，失败仍读V17；不宣称多个下游共同事务 | 22 |

共88个原生文本、矩形和箭头元素。四图均经 `@excalidraw/excalidraw 0.18.0` 官方API导出SVG，实际编辑器重载、修改文字、恢复均返回 `editable:true`；不是将SVG封装进场景冒充可编辑图。

最终把发布图图例精确为“实线为数据访问”，图注对应“数据访问（导入或读取）”，同步了场景的 `text`／`originalText`、骨架和生成器；从保存的原生场景重新官方导出，22元素、编辑器往返再次通过。浅深主题使用既有五色变量，独立打开与页面嵌入均已检查。

## 事实核查与纠错

核查日期为2026-11-07；完整链接、原书对应和修正解释已同步进入[正文来源区](ch11.md#sources)。这是有依据的笔记纠错与范围限定，不冒称出版社已经确认的勘误。

| 原表述／问题 | 依据及本章处理 |
| --- | --- |
| 原书461页将对象存储rename一概写为非原子 | AWS官方 `Renaming objects in directory buckets`：保留通用桶复制删除局限，补充Express One Zone同目录桶单对象原子RenameObject；不扩大为目录或多对象事务 |
| 原书462页及旧稿把cgroups与防止越权读数据连写 | Linux内核 `Control Group v2`：资源控制与身份、权限及其他隔离机制分工，不能让cgroups独自承担访问授权 |
| 原书466页及旧稿概括Flink周期检查点恢复 | Flink2.1 `DataStream Execution Mode`：BATCH不用检查点，回溯可用中间结果；与STREAMING区分 |
| 原书471页及旧稿将M×R区段写成物理文件数 | Hadoop3.4.2 `MapReduce Tutorial`：map溢写段会归并；区段表示逻辑数据归属，不直接决定文件数量 |
| 旧稿把shuffle必然排序推广到全部引擎，并混同局部与全局有序 | 区分排序型shuffle、其他重分布、分片内输入顺序与全局输出顺序；解释map-only可绕开reduce路径 |
| 原书479页把tokenization简写为拆词并与embedding连写 | Hugging Face `Tokenization algorithms`：token可能为子词、字节或字符片段；token ID与嵌入向量分属不同步骤 |
| 原书480页全有或全无／旧稿任务各执行一次 | Hadoop3.4.2 OutputCommitter与原书上下文：一次逻辑结果不等于一次执行，明确提交器、存储及读者遵循发布协议的前提 |
| 旧稿“排序O(1)内存”“RS(10,4)等同4副本” | 说明排序缓冲、归并缓冲及临时盘；1.4倍编码冗余和丢4片，与4副本丢3份并非同一故障模型 |
| 旧稿广播只传一次且最快、共分片无内存限制、排序合并是唯一大表方案 | Spark4.0.1 SQL调优文档；给出P×B传输量、解码／哈希内存、布局兼容和shuffle hash路径。共分片省Exchange不必省Sort |
| 旧稿固定性能倍数、必然全量重算、固定一天延迟、Kafka唯一正确路径 | 改为按工作负载、增量依赖、调度等待和外部提交范围分析，删除无依据的普遍性能承诺 |

另核查 Iceberg1.10.0 `Reliability` 的不可变快照、元数据引用原子替换、并发冲突与重试；其页面关于旧S3最终一致性的历史文字没有作为现行S3一致性的依据。上述共七个实际访问的官方资料链接保存在正文来源区。

## 旧稿取舍与补充边界

- 保留旧稿中有助理解的Unix投影—排序—计数、分布式数据移动、连接前提、失败重跑与派生结果供给；按第二版重新组织，不延续旧稿偏MapReduce／产品速查的主线。
- 以第二版顺序展开存储／对象存储、资源调度／工作流、现代dataflow、云数仓趋同、DataFrame、ETL／ML；没有把这些内容压成术语清单。
- 广播、共分片、哈希连接和倾斜作为独立的**笔记补充**，不伪装为原章逐项展开。排序合并连接保留原书活动事件／出生日期案例，说明一对多内存前提、重复档案、内连接缺档案和年龄基准。
- NGINX热门URL问题、160核资源安排、活动与档案连接、ETL缺字段、Kafka缓冲与批量导入来自原书；8行日志、用户小数据、V17／V18发布协议及失败时序明确为笔记假设或解释。
- 未迁移旧稿固定倍数表、面试题、宽泛“铁律”及缺少前提的选型结论。Pandas“优化：无”、SQL表达能力、Spark成本等过强断言已在正文相应位置纠正。
- 保留第3／4／5／7／8章相关内部链接，并以有界输入终点自然过渡到第12章。没有引入尚未存在的其他章内部锚点。

## 实际验证与证据

本机证据目录：

`/private/var/folders/5k/y6qh6sfd2g30js0v0qrv4mfr0000gn/T/opencode/ddia2-tools/`

### 渲染、小数据与静态一致性

在项目根目录实际执行：

```sh
python3 books/designing-data-intensive-applications-2nd/diagrams/sources/ch11-render.py
python3 books/designing-data-intensive-applications-2nd/diagrams/sources/ch11-check.py
node books/designing-data-intensive-applications-2nd/diagrams/sources/ch11-browser.mjs
```

- 渲染输出18节、4图。最终措辞修正后重新渲染并运行检查脚本通过；站点没有编译步骤，本项是静态页面生成与核对，不记作框架“构建通过”。
- 检查脚本直接提取正文代码运行：真实8行Unix管道与Python结果均为 `3 /`、`3 /book`、`1 /about`、`1 /css/site.css`；CSS过滤后移除最后一项。SQLite执行正文SQL得到同样排序与计数。
- 三个shuffle有序区段归并为AABBCC，各计数2；排序合并、广播、共分片小模型与独立SQLite内连接结果一致；缺失档案的999事件被内连接排除。2025-06-27年龄为104→36、103→77，URL年龄组计数一致；热用户拆成4个带盐子任务后连接结果保持一致。
- 复算900／128分块、RS(10,4)冗余／丢片、20 MB×50与2 GB×50广播量；恢复／发布教学模型验证失败尝试排除、完成通知提前到达时禁止发布、读者固定旧版本、增加10重试成20与确定性覆盖仍为10。
- 77项href/src引用已扫描；本页及已有目标锚点、资源、图像alt、无重复ID通过。除同轮尚未落盘的ch10／ch12页面外，其余本地目标存在；两个待整合目标单独报告，未伪报全站链接全部正常。
- Markdown与HTML的18节及来源全文对应通过；四图场景文本与SVG对应通过，原生元素合计88。最终统计与待整合目标保存于 `ch11-check-results.json`。
- 首次静态脚本因本机缺少 `bs4` 未执行；已改用标准库 `HTMLParser`，未为此安装依赖，随后及最终复跑均通过。

### Chrome与目检

- `ch11-browser.mjs` 使用本机Google Chrome：1440桌面／375手机×浅深4组，加4幅独立SVG×浅深8组，共12组通过，结果在 `ch11-browser-results.json`。
- 系统主题跟随、手动覆盖／刷新保存、双端目录、来源折叠均通过；正文16px、行高31.2px。代码／表格／手机560px宽图示局部滚动，页面没有横向溢出；图片加载及alt正常，捕获的JS／HTTP错误为0。
- 独立SVG两主题文本均无越界。已实际查看全部四图及桌面浅色、手机深色正文和手机深色嵌图截图，没有发现图内文字裁切或遮挡；手机图示超出视窗的部分可横向滚动或点击大图查看。
- 最终发布图图例修正后，只补做定点验证：独立SVG浅深2组、阅读页桌面浅色／手机深色2组；图例／图注、图像加载、无整页溢出和无JS错误通过。结果在 `ch11-final-touchup-results.json`；实际查看了最终浅色大图与手机深色发布图截图。
- 常规截图：`ch11-reader-{1440,375}-{light,dark}.png`、`ch11-reader-mobile-figure-dark.png`、`ch11-{layers,shuffle,join,publish}-{light,dark}.png`。最终措辞版本见 `ch11-publish-final-{light,dark}.png` 和 `ch11-publish-final-reader-{light,dark}.png`。
- 原PDF回看图像以 `ch11-original-印刷页码.png` 保存于同一临时证据目录。制作产物在项目内，截图／结果JSON是本机核查证据，不是网页运行依赖。浏览器检查临时服务已自动关闭。

### 验证边界与发布白名单

Unix、Python和SQLite为真实执行；shuffle、三种连接、恢复与发布为确定性教学模型。PySpark段落展示API对应，未启动Spark、Flink、Hadoop、Kafka或云服务，没有把本地模型当成真实分布式故障注入、吞吐测试或协议证明。

只读核对现有 `.github/workflows/pages.yml` 并按其目录排除／扩展名规则枚举：本章发布目标恰为 **1 HTML＋4 SVG**；其余14份笔记、图源、骨架与制作脚本均排除。没有修改共享工作流；未执行提交、推送或部署。

## 交接与遗留

1. 本章文件已就绪。最终检查时 `chapters/ch10.html`、`chapters/ch12.html` 尚不存在，这是同轮章节制作的整合项；主 Agent 在相邻负责人返回后接通并复核翻页。
2. 书籍概览、书架、共享导航及轮次状态由主 Agent 在统一审稿后维护，本章未提前改写。正文没有未解决的资料阻塞或待补占位。
3. 主 Agent 可按上面的原书覆盖表、纠错记录及脚本审稿；最后需要统一确认连接策略与第12章发布／恢复术语。

**Agent C 已完成交付，停止编辑第11章；等待主 Agent 审稿。**

## 主Agent主审与接入完成（2026-11-07）

四位负责人全部返回、停止编辑后，主Agent通读本章正文、来源及报告，核对有界输入、shuffle、连接、重跑与版本发布。回看印刷461／466／471／479页文字及470页shuffle原图；以Flink2.1执行模式／容错和S3目录桶RenameObject官方资料复核产品边界，查看四图最终联系表。未发现需重写的核心缺口。

第10／12章已落盘，作者交付时两项待整合链接全部关闭，书架和概览已接入。主Agent复跑`ch11-check.py`通过，Unix／Python／SQLite、连接与发布教学例子、18节／来源同步、4组图源／SVG正常；统一统计12,352汉字。全轮14页960项引用及Chrome60组验证通过，详见本书README与`round3-*.json`。本章产品验证边界保留，完成待用户验收。
