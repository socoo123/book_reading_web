# DDIA 第二版 · 制作与交接

> 2026-11-07：**第5轮全书整合与guide已完成，待验收并停止。** 主Agent独立完成，无子Agent或后台写作任务。保留14章、250节、64幅章节图及1幅概览图，新增12节[全书导航](guide.html)。前四轮待验收状态保留；[整合／深度复核报告](notes/integration-report.md)记录实际范围与验证。

## 版本与资料

- Martin Kleppmann、Chris Riccomini，*Designing Data-Intensive Applications, Second Edition: The Big Ideas Behind Reliable, Scalable, and Maintainable Systems*。O’Reilly，February 2026，First Release 2026-02-18，版权2026，ISBN 978-1-098-11906-5。中文名称与术语为本站译法。
- 固定PDF：`/Users/zy/ai_learn/ddia_2nd/Designing_Data_Intensive_Applications_2nd_Edition.pdf`。本轮重新打开，673页、未加密、可提取文字；版权见PDF6，前言PDF19—24。
- 正文 **PDF页序＝印刷页＋24**，均从1起算；程序索引另减1。Glossary 为印刷603—608／PDF627—632。
- `originals/ddia2-frontmatter.txt`（PDF1—24）、`ddia2-ch01.txt`—`ddia2-ch14.txt`、`ddia2-glossary.txt`，共16份逐页标记文本。分章文件含章末参考文献；仅本地使用。`originals/manifest.json` 保存范围和粗略词数，`originals/outline.md` 保存书签小节定位；后者不包含所有低层标题，写作前结合全文补齐覆盖表。
- 提取命令：`python3 books/designing-data-intensive-applications-2nd/originals/prepare.py`，需要本地 PyMuPDF。准备轮提取成功不等于逐章通读；第1—14章现已完成逐章写作与主审。图、公式、表格及异常断词必须回看原PDF。
- 旧稿：`/Users/zy/ai_learn/ddia_2nd/chNN-中文章名.md`，确切文件名见根PLAN第4节，目录只读。先读负责章原文，再完整对照旧稿；旧稿不是事实依据，其Obsidian与原地改写约定不带入本站。
- 2026-11-07实际访问 [O’Reilly Confirmed Errata](https://www.oreilly.com/catalog/errata.csp?isbn=9781098119065)，显示 **No confirmed errata were found for this product**。只核对已确认页，未将“无条目”等同无错误。[作者参考文献仓库](https://github.com/ept/ddia2-references)可访问；未声称逐项阅读所列文献。

## 分章体量与投入预估

目标是以原书正文约三分之一的篇幅，充分解释核心机制、论证与案例；不是只覆盖三分之一知识点。下表先去掉章末参考文献，保留Summary；同页开始References时，正文范围与参考文献页会重叠。自动词数保留图注、脚注、代码及部分页脚，只用于估计各章相对体量；本轮没有把词数当作通读证据。

“中文投入”是初稿规划区间，以中文正文约千字为单位，不含来源清单、导航与大段代码。它综合原文体量和机制展开需要，**不是英文字数除三，也不是验收字数配额**。中英文排版与信息密度不同，约三分之一最终由主审对照原书核心小节、推理链、算例和失败路径判断；首轮完成后可根据实际展开校准。长章可超出区间，不为达数扩写无关材料。

| 章 | 正文印刷页（含Summary） | 参考文献起页 | 英文词数粗估 | 中文投入（千字） | 重点投入与审稿焦点 | 轮／角色 |
| --- | --- | --- | ---: | --- | --- | --- |
| 01 | 1—26 | 26 | 10,614 | 7—9 | OLTP／OLAP与数据责任；云存算分离、单机与分布式的取舍 | 1／A |
| 02 | 33—56 | 57 | 9,461 | 7—9 | 时间线读写扇出、负载参数、尾延迟与排队；分位数口径 | 1／B |
| 03 | 65—108 | 108 | 15,697 | 11—14 | 同一数据的模型与查询；关系与图遍历例子；CQRS、GraphQL、DataFrames | 1／C |
| 04 | 115—151 | 151 | 14,132 | 10—13 | LSM／B-tree读写和恢复；列式执行；倒排与向量检索 | 1／D |
| 05 | 161—192 | 193 | 11,606 | 8—11 | 新旧读写者兼容方向；格式算例；RPC、持久化执行的副作用边界 | 2／A |
| 06 | 197—244 | 244 | 18,480 | 13—17 | 三类复制正常／故障路径；quorum、因果和并发；本地优先 | 2／B |
| 07 | 251—272 | 273 | 8,204 | 6—8 | 少量键演示分片、热键与迁移；本地／全局索引查询 | 2／C |
| 08 | 277—337 | 337 | 23,107 | 17—22 | 逐一演示隔离异常；2PL／SSI、2PC及恢复；端到端消息处理 | 2／D |
| 09 | 345—389 | 389 | 19,017 | 13—17 | 部分失败、时钟、租约与fencing；安全性／活性与测试证据 | 3／A |
| 10 | 401—443 | 443 | 17,102 | 13—17 | 调用区间、ID排序、共识和协调；模型假设与可用性边界 | 3／B |
| 11 | 451—482 | 482 | 12,545 | 9—12 | 可运行的小管道；shuffle／join；现代引擎、发布与重跑 | 3／C |
| 12 | 487—531 | 531 | 18,609 | 13—17 | CDC衔接、时间窗口、三类连接；状态／位点／输出恢复 | 3／D |
| 13 | 539—580 | 580 | 17,500 | 12—16 | 数据系统组合、读写路径、请求ID、约束、及时性与完整性 | 4／A |
| 14 | 585—598 | 598 | 6,183 | 4—6 | 预测反馈循环、隐私与权力；区分作者判断、史实和法规 | 4／B |

14章正文英文词数粗估合计 **202,257**。正文页界通过逐章定位References确定，完整章节PDF范围仍以根PLAN为准。内容覆盖以根PLAN第4、5节＋原文为准，表中短语仅是投入提示。

## 统一术语

起点来自根PLAN；准备轮完整读取原书Glossary（印刷603—608），补充下列区分。Glossary自身说明定义只是简写，具体保证回到对应正文；不要把术语表的简化句扩大成协议定义。

| 英文 | 本站译法／边界 |
| --- | --- |
| operational / analytical systems | 运营型／分析型系统；前者支持日常业务，不是运维监控 |
| OLTP / OLAP | 在线事务处理／在线分析处理；以访问模式区分，不凭产品名判定 |
| system of record / derived data | 权威记录系统／派生数据；由使用角色决定，不由存储产品决定 |
| data warehouse / data lake / ETL | 数据仓库／数据湖／提取—转换—加载 |
| latency / response time / throughput | 延迟／响应时间／吞吐量；说明测量起止点与单位 |
| percentile / tail latency | 分位数／尾延迟；样本、窗口和聚合口径明确 |
| fault / failure / fault tolerance | 故障／失效／容错；区分组件问题与系统服务失败 |
| scalability / elasticity | 可扩展性／弹性；负载增长与动态调整资源分别讨论 |
| operability / simplicity / evolvability | 可运维性／简单性／可演化性 |
| backpressure / flow control | 背压／流量控制；接收方跟不上时减慢发送，而非增加处理容量 |
| normalized / denormalized | 规范化／反规范化；后者有意保留冗余，需解释更新代价 |
| declarative query / join | 声明式查询／连接；join不是网络连接 |
| schema | 模式（schema）；按语境区分数据结构描述与数据库命名空间 |
| materialize / materialized view | 物化／物化视图；提前计算并保存结果，与按需计算相对 |
| locality | 局部性；把经常一起访问的数据放在一起 |
| log / WAL | 日志／预写日志；存储日志、复制日志和事件日志各有职责 |
| compaction / compression | 压缩合并／压缩；LSM合并文件与数据编码压缩分开 |
| replication / sharding / network partition | 复制／分片／网络分区；partitioning数据划分按语境译分片 |
| leader / follower / replica | 主节点／从节点／副本；单主、多主、无主复制 |
| failover / split brain | 故障切换／脑裂；多个节点自认主节点不等于合法多主协议 |
| rebalance / skew / hot spot | 再平衡／倾斜／热点；负载倾斜与时钟偏差分开 |
| quorum / majority | 法定人数／多数派；不是所有协议中都同义 |
| happens-before / causality / concurrency | 先发生关系／因果关系／并发；并发指无因果先后，不要求墙钟相同 |
| atomicity / isolation / durability | 原子性／隔离性／持久性；整体提交、并发干扰、确认后保存分别解释 |
| atomic operation | 原子操作；并发语境的不可分割效果，与事务全有或全无按语境区分 |
| serializability / serialization | 可串行化（隔离保证）／序列化或编码（数据表示） |
| snapshot isolation / MVCC / write skew | 快照隔离／多版本并发控制／写偏斜 |
| two-phase locking / two-phase commit | 两阶段锁（2PL）／两阶段提交（2PC）；隔离与提交是不同问题 |
| linearizability / consensus | 线性一致性／共识；线性一致性须保留实时先后约束，不能仅写成单副本 |
| safety / liveness | 安全性／活性；此处安全性不是信息安全 |
| timeout / failure detection | 超时／故障检测；未及时收到响应不证明远端未执行 |
| lease / fencing token | 租约／隔离令牌（fencing token）；资源端验证陈旧操作的责任不能省略 |
| monotonic clock / time-of-day clock | 单调时钟／墙上时钟；用途与误差来源不同 |
| Byzantine fault / partial failure | 拜占庭故障／部分失败 |
| synchronous / asynchronous | 同步／异步；说明是在等待响应、复制确认还是网络时间模型语境 |
| total order / partial order | 全序／偏序；是否任意两项都可比较，与墙钟排序不同 |
| deterministic | 确定性的；相同输入产生相同输出，时间、随机值等需纳入输入或控制 |
| event sourcing / CDC / CQRS | 事件溯源／变更数据捕获／命令查询职责分离 |
| local-first / durable execution | 本地优先／持久化执行；重放不自动使外部副作用恰好一次 |
| event time / processing time / watermark | 事件时间／处理时间／水位线；水位线须交代迟到假设 |
| bounded / unbounded | 有界／无界；输入是否有可到达的终点，不要求预知精确大小；无界不必然指现实中真的无限 |
| exactly-once / idempotence | 恰好一次语义／幂等性；明确输入、内部状态、输出和外部效果的保证范围 |
| timeliness / integrity | 及时性／完整性；此处完整性含业务不变量与数据正确性，不只是字段齐全 |
| unbundling databases / federated databases | 拆分数据库／联邦数据库；前者把内部派生职责组合为跨系统数据流，不是分片；后者在读取侧统一查询 |

译法冲突由负责人报告、主Agent集中更新。首次出现术语在正文解释，不要求读者先背本表。第5轮面向读者的[43组术语对照](guide.html#terms)与[保证范围](guide.html#guarantees)已连接具体小节。

## 页面与写作约定

- 本书[概览](index.html)已开放全部14章，含版本／读者／第二版说明和代表图；[概览内容源](notes/overview.md)保存文字依据。书架已接入第四本，采用共享样式 `.cover-ddia2`。
- 写作负责人只改 `notes/chNN.md`、`chapters/chNN.html`、`diagrams/sources/chNN-*`、`diagrams/exports/chNN-*`。根PLAN／CONTINUE／README／index、assets、本书README／index／guide均由主Agent维护；不改其他章和旧稿。
- 静态阅读页外壳参照 `books/just-enough-software-architecture/chapters/ch02.html`，只复用结构与样式，完整替换旧书名、目录、锚点、来源和翻页。中文标题“第 N 章｜章名”，英文书名可在页眉缩写为“DDIA · Second Edition”。
- 章节页引用 `../../../assets/styles.css`、`theme.js`、`reader.js`；主题脚本在head，reader脚本defer。正文 `.article` 为16px、行高1.95、最大720px；包含桌面`.toc`和`.mobile-toc`、语义化section、来源`<details id="sources" class="source-note">`、面包屑及`.chapter-pagination`。
- 第1章上一页是`../index.html`；第1—14章顺序互链，第14章下一页返回概览。全部章节面包屑和页尾均有`../guide.html`，书架与概览也已接入专题导航。
- Markdown与HTML正文、示例、图注、来源同步；Markdown章间可用`chNN.md#anchor`，HTML改为`chNN.html#anchor`。网页不链接PDF、originals、notes、sources。表格用`.table-scroll`局部滚动；代码用`pre > code`。
- 写作参照Google第2章的连贯文章、JESA第3章的问题—机制—证据—取舍、Hard Parts第9章的具体操作顺序与纠错。参照文件见根PLAN §2.3；以DDIA原文决定结构，不套相同节数与固定问答模板。
- 写前根据原文建立核心小节覆盖表，交付列明对应笔记锚点、保留的原书案例、必要取舍、旧稿修正与补充出处。正常机制和代表性异常都要讲清操作顺序，不以名词清单替代解释。
- 来源区标明实际阅读的原书小节、印刷页／PDF页序、回看的原图与必要外部链接及日期。原书观点、笔记假设、书外补充分清；纠错按“原表述 → 问题及依据 → 修正解释”就地说明。

## Excalidraw制作与导出

代表图：`diagrams/sources/overview-dataflow.excalidraw` → `diagrams/exports/overview-dataflow.svg`。16个原生元素，文本、矩形和绑定箭头可编辑；根据第1章印刷10—11页原创组织，展示数据流角色，不声称共同事务或指定投递语义。可在Excalidraw菜单打开本地场景继续编辑。

本轮采用 **@excalidraw/excalidraw 0.18.0** 的 `convertToExcalidrawElements`、`exportToSvg`、`restoreElements` 与实际编辑器API，不是手写SVG冒充导出。生产网页仅使用静态SVG，没有React／Excalidraw运行依赖。

可复用本地制作工具保留在 `diagrams/sources/`（发布排除）：

- `overview-dataflow.skeleton.json`：本图的简写元素定义；`.excalidraw`是主要可编辑交付。
- `excalidraw-browser.js`：官方API桥接。
- `export-excalidraw.mjs`：以浏览器字体度量导出，附加主题与无障碍信息；导出后重新载入保存的场景，通过编辑器修改并恢复一段文字验证可编辑性。

工具依赖放在本机临时目录，默认 `.../T/opencode/ddia2-tools/`，也可通过`DDIA_TOOLS`指定；该目录须有package.json和node_modules。安装／重建命令：

```sh
npm install --prefix "$DDIA_TOOLS" @excalidraw/excalidraw@0.18.0 react@19 react-dom@19 esbuild playwright
node books/designing-data-intensive-applications-2nd/diagrams/sources/export-excalidraw.mjs
```

第一次安装前将`DDIA_TOOLS`设为自己的临时工具目录；若保持脚本默认，本机已准备好，直接运行第二行。脚本使用本机Google Chrome，不额外安装浏览器。npm曾提示部分传递依赖的peer版本冲突，官方导出与编辑器往返实际通过；无需将该工具链变成网站依赖。

后续可传入本章 `.skeleton.json` 或 `.excalidraw` 路径及本章标题／描述（见脚本参数），导出到同书exports；输入场景置于sources。配色沿用已约定的五种颜色，确保主题替换生效。修改场景后从`.excalidraw`重新导出，避免再用旧skeleton覆盖编辑结果。

```sh
node books/designing-data-intensive-applications-2nd/diagrams/sources/export-excalidraw.mjs books/designing-data-intensive-applications-2nd/diagrams/sources/chNN-example.excalidraw "本图标题" "节点与箭头的替代描述"
```

文字用fontFamily=2（Helvetica），SVG添加Arial、PingFang SC、Microsoft YaHei回退；中文使用系统字体，不加载远程字体。图中正文建议至少17px，框内主标签21px左右，手绘roughness保持克制。每图只回答一个问题，复杂关系拆“总览＋细节”，复杂布局先沟通。

导出保留官方生成的几何，仅把浅色五种色值替换成主题CSS变量。深色配色与本站surface一致；img继承宿主color-scheme，独立打开的SVG读取同站`reading-notes-theme`。图内文字、线型与标签共同区分含义。页面用`.concept-figure`包裹大图链接与img，提供alt、读图说明和figcaption，手机最小560px局部滚动。

## 第0轮执行与验证

- 主Agent：GPT-6 Astra（`openai/gpt-6-astra`）；本会话推理档位未由工具暴露，不声称为xhigh。模型目录实际确认active且包含xhigh；后续所有内容调用显式使用`openai/gpt-6-astra#xhigh`。
- 本轮未启动正文子Agent，无子会话或后台写作任务；第1轮A／B／C／D分别负责1／2／3／4章。每轮交付后全部返回、停止编辑，再由主Agent统审并交接。
- 实际准备阅读：三本书约定参考稿与页面外壳，DDIA版权、前言相关段落、Glossary全部六页、第1章权威／派生原文两页；全部章节范围与References分界已定位。其余章正文留待写作轮完整阅读，旧稿尚未逐章全文复核。
- 原文16份提取、14章页界、模型、概览与可编辑代表图已经准备。14章逐页标记连续覆盖PDF25—626共602页（含参考文献）；概览本地链接／锚点、无重复ID、SVG XML与全部场景文字对应检查通过。按现有Pages规则本书发布文件仅概览HTML和代表图SVG，原文与制作脚本均排除。
- Chrome实际检查：桌面1440／手机375 × 浅／深色4组，以及独立SVG两主题2组通过。系统跟随、手动覆盖与刷新保存、16px正文／31.2px行高、来源折叠、手机图示局部滚动均正常，无页面横向溢出或捕获的JS／HTTP错误；SVG文字无裁切。实际查看浅色独立图、深色嵌入图及手机概览截图。
- 首次手机检查发现概览目录grid的自动最小宽度将整页撑开，增加`min-width:0`后复验通过；长书名封面字号与概览解释正文限宽调整后复验通过，四组封面文字均未溢出，既有JESA概览375px定点回归通过。保存的.excalidraw重新导出与编辑器往返也通过。验证脚本、JSON结果和截图位于`.../T/opencode/ddia2-tools/`。站点没有编译步骤。
- 待后续轮完成：14章写作、各章事实核查、具体原图／公式回看、书架接入、guide及跨章整合。无原书或模型阻塞。当前未部署。

## 第1轮完成与主审（2026-11-07）

四名全新负责人显式使用`openai/gpt-6-astra#xhigh`，无递归委派；主Agent确认四人全部返回、停止编辑后才接管章节文件。主Agent为GPT-6 Astra，本会话推理档位未暴露。

| 负责人／章 | 会话ID | 正文节数 | 汉字粗计 | 章节图 | 状态／覆盖核查报告 |
| --- | --- | ---: | ---: | ---: | --- |
| A／01 | `ses_e4bba7d92ffeJ6EXd1Vy5ptqFz` | 13 | 9,957 | 2 | 已返回、停止编辑；[报告](notes/ch01-report.md) |
| B／02 | `ses_e4bba7d8fffeZbs0yL1CnXiPJg` | 12 | 9,391 | 3 | 已返回、停止编辑；[报告](notes/ch02-report.md) |
| C／03 | `ses_e4bba7d8dffe7zSZtKIjDAdjb4` | 16 | 12,589 | 3 | 已返回、停止编辑；[报告](notes/ch03-report.md) |
| D／04 | `ses_e4bba7d8cffeT1HsSYDG4uDJfR` | 14 | 12,926 | 5 | 已返回、停止编辑；[报告](notes/ch04-report.md) |

汉字统一按来源区前、去围栏代码、保留标题／表格／图注／替代文本统计，共44,863；不是纯叙述段落字数，也不是英文字数除三。第1、2章略超初始投入区间，原因是保留计算前提、失败路径和就地纠错；第3、4章处于预估区间。主审已按原书小节覆盖、推理链和案例判断展开程度，没有用字数替代内容检查。

### 交付与接入

- `notes/ch01.md`—`ch04.md`、`chapters/ch01.html`—`ch04.html`：55节、10张正文表、1张来源对应表、18代码块（含说明性文本，非18个产品集成测试）。
- 13组`diagrams/sources/chNN-*.excalidraw`与`diagrams/exports/chNN-*.svg`，共319个原生元素；每组均由官方API导出并经负责人实际编辑器重载／改字验证。加准备轮概览图，目前全书14图。
- 概览及其Markdown同步为4／14章，书架新增第四本。翻页链：概览→1→2→3→4→概览；第5—14章仅待制作文字，下一轮接通4→5。
- 逐章渲染与核对脚本位于各章`diagrams/sources/chNN-*`，依赖只用于本地制作。修改笔记后使用对应render／build脚本同步HTML；网页仍无运行依赖与构建步骤。

### 主Agent实际审稿与纠错

主Agent通读四份正文、来源区及四份交付报告，核对覆盖和统一术语；重看固定PDF版权及印刷25、35、36、39、42、99、106、127、129、131、140等关键页文字，并查看原图2-1—2-3与4-6。13份图源的文字、箭头绑定与导出均检查，实际查看四章图示拼图和代表性浅深色阅读截图。

- 第1章：核对权威／派生角色、存算分离及重建边界；对照EUR-Lex第5、6(4)、17、44—45条复核“其他用途一律禁止”“无条件删除”“欧洲数据一律不得出境”的修正。
- 第2章：核对关注方向、按帖子加权的扇出、排队／新鲜度区别、统一最近秩、独立调用尾延迟及两种错误预算口径；保留历史研究按原书转述的标识。
- 第3章：核对图查询两条件绑定同一人、零跳／环、事件重放与副作用、缺失评分语义；查GraphQL官方Demand control，确认接口表达受限不等于无昂贵查询。主审发现正文把homogeneous data写成“同构”会与图同构混淆，依据原书印刷84—85改为同质数据并同步HTML；不是原书错误。
- 第4章：独立复算四层／五层B-tree叶页容量；对照RocksDB Write Stalls、PostgreSQL17 Routine Vacuuming、Roaring官方说明，保留写背压、普通VACUUM／FULL及三类容器的校正。确认墓碑、WAL先行与发布、列位置、IVF遗漏和近似召回边界。
- 原书层面的纠错是有依据的笔记修正，均列原句／问题／修正，不冒称出版社已确认勘误；旧稿保持只读。

### 实际验证与范围

- 6页（书架、概览、4章）271项href/src引用、全部本地目标／锚点、无重复ID、图像alt通过。四章全部段落、代码、表格、图注与来源可在HTML逐项匹配；Markdown尾部文字翻页与HTML导航卡片结构不同，已人工核对目标。
- 13组场景JSON／SVG XML、全部场景文字与导出一致，319个原生元素；现有Pages白名单包含本书19文件＝5 HTML＋14 SVG，排除notes／sources／originals及PDF。
- 主Agent执行Chrome：书架2组、概览2组、每章桌面浅色／手机深色8组、第4章额外桌面深色／手机浅色2组，共14组；13个独立SVG各浅／深色共26组。40项通过，正文16px、行高31.2px，主题保存、双端目录和来源交互正常，页面无横向溢出，图中文字无裁切，捕获JS／HTTP错误为0。各负责人另已完成本章四种端／主题组合，详见各报告。
- 独立执行第1章销售SQL、第2章关注查询、分位数／尾延迟／积压算例、B-tree容量、墓碑反例、位图筛选、嵌入距离及IVF遗漏；复跑第3章SQL、递归零跳／环、集合闭包、事件重放及Pandas 2.3.3透视／重复坐标检查，均通过。
- 主Agent验证工具和结果位于`.../T/opencode/ddia2-tools/verify-round1.py`、`verify-round1.mjs`、`round1-static-results.json`、`round1-browser-results.json`、`round1-numeric-results.json`及截图。首遍独立SVG的fullPage截图超时，改固定视口后通过；静态检查先因未单独渲染details中的Markdown漏计来源表，修正检查器后通过。两者均为验证工具问题。
- 接入定点验证已实际点击书架第四本→概览→第1—4章→概览，并反向逐章返回；目录4个有效章节链接、10个待制作项正确。桌面／手机新卡片截图已查看；`round1-navigation-results.json`保存结果。55节完整正文及4份来源区另外以规范化全文逐章匹配通过。

### 遗留与下一轮

本轮无已知内容／资料／绘图阻塞。Cypher、SPARQL、GraphQL、MongoDB及PostgreSQL专有日期查询未连接对应服务运行；Datalog以Python集合核对规则，未运行产品引擎。未做真实存储崩溃注入、数据库性能或ANN基准，未通读所有外部参考论文；这些范围已与实际小数据验证区分。

第1轮交接时第5—14章、全书guide与跨轮整合留待后续，未部署；当时下一轮为第2轮。四个首轮会话已返回且停止编辑。本轮最新状态如下。

## 第2轮完成与主审（2026-11-07）

模型目录再次确认`openai/gpt-6-astra` active且支持xhigh；四名全新负责人显式使用`openai/gpt-6-astra#xhigh`，没有续用第1轮会话或递归委派。四人全部返回、停止编辑后，主Agent才接管章节主审。主Agent为GPT-6 Astra，推理档位未由工具暴露。

| 负责人／章 | 全新会话ID | 正文节数 | 汉字粗计 | 章节图 | 状态／覆盖核查报告 |
| --- | --- | ---: | ---: | ---: | --- |
| A／05 | `ses_e4b56c731ffe6x5WcalQmBymmn` | 15 | 11,861 | 3 | 已返回、停止编辑；[报告](notes/ch05-report.md) |
| B／06 | `ses_e4b5676daffeicEKjTSOctg6V3` | 21 | 17,334 | 5 | 已返回、停止编辑；[报告](notes/ch06-report.md) |
| C／07 | `ses_e4b56295bffeTP8iNpKV23ECtq` | 13 | 8,080 | 4 | 已返回、停止编辑；[报告](notes/ch07-report.md) |
| D／08 | `ses_e4b55e004ffe3WjUAHwTVkP87V` | 24 | 21,789 | 7 | 已返回、停止编辑；[报告](notes/ch08-report.md) |

合计73节、59,064汉字，统计口径同首轮。第5—7章略超原投入区间，第8章为长章；主审已根据核心覆盖、机制步骤、推理、算例与失败路径确认充分展开，没有以字数机械换算原书三分之一。第5章作者初报11,863，统一检查得到11,861，已只修正报告统计。

### 交付与接入

- `notes/ch05.md`—`ch08.md`与`chapters/ch05.html`—`ch08.html`同步，9张正文表＋1张来源表、14个代码／说明块；各章覆盖／核查报告保留实际来源与验证边界。
- 19组原生`.excalidraw`及官方SVG，共422个原生元素；累计32幅章节图与1幅概览图。图源、生成器、渲染及检查工具仍在`diagrams/sources/`，网页只用导出。
- 书架、概览、`notes/overview.md`同步为8／14；累计正文128节、103,927汉字。翻页链为概览→1→2→3→4→5→6→7→8→概览；第9—14章显示待制作。
- 第4章尾部、翻页及`ch04-render.py`同步接到第5章并重新生成HTML。同轮第5／6／7章报告中的待落盘链接已通过整合检查关闭，第8章暂回概览。

### 主Agent实际审稿与纠错复核

主Agent通读四章全部正文、来源区及覆盖报告，核对关键机制、反例与边界。回看固定PDF印刷168、170、175、188、189、207、233、234、258、271、294、320、322、326、332、333、334页文字，并查看印刷174、294页图像。全部19幅图的源元素／箭头与SVG已检查，四张全图联系表已目检。

- **第5章编码与演化：** 以MessagePack、Protobuf及Avro1.12官方资料复核fixstr低5位、int64与ZigZag、writer／reader兼容方向、long→int拒绝与union默认值。对照Temporal官方资料确认“副作用成功但完成未记录”可能重试，重放不保证外部效果恰好一次。
- **第6章复制：** 以PostgreSQL17同步提交与MySQL8.4官方文档复核确认语义、默认ROW而非MIXED等纠错。检查quorum交集的固定成员／成功读写前提、读不等待修复反例、先发生关系、版本号与向量的边界。MySQL直接请求曾403，后用webfetch取得官方正文，未留下资料缺口。
- **第7章分片：** 对照HBase官方分裂实现确认先引用父文件、后续压缩合并的实现反例；检查哈希变化、固定分片、热键、迁移屏障／新代次、本地／全局索引回表，避免把均匀键空间等同均匀负载。
- **第8章事务：** 回看隔离、SSI、2PC及幂等原文；以Ports／Grittner SSI论文§7.1确认SSI与本地2PC可组合，PostgreSQL17官方文档核对产品行为，SQS官方资料核对重复投递与ack后删除去重记录的条件。区分读写依赖、可串行化、原子提交与端到端副作用。
- 原书、旧稿及笔记解释的纠错对象已区分；上述原书修正不冒称出版社已确认勘误。正文无需主审重写，统一统计和共享接入已完成，原书与旧稿保持只读。

### 实际验证与证据

- **静态整合：** 接入后重新运行`verify-round2.py`，10页688项href/src引用、本地链接／锚点、无重复ID、图像alt通过。73节及4份来源区MD／HTML规范化全文匹配；9张正文表＋1张来源表、14代码块与19图对应。`parity_exceptions`仅四章尾部文字翻页与HTML卡片结构差异，导航目标已实测。
- **图源与发布：** 19组场景JSON／SVG XML与全部文字对应通过，422原生元素；各作者已实际用官方编辑器重载、改字并恢复。现有Pages白名单包含本书42文件＝9 HTML＋33 SVG，排除原文、notes、图源和制作工具。
- **浏览器：** 本机Chrome14组页面（书架2、概览2、四章各桌面浅色／手机深色8、第8章额外桌面深色／手机浅色2）＋19图各浅深色38组，共52组通过。正文16px／31.2px，主题保存、双端目录、来源折叠、图示局部滚动正常，整页无横向溢出，SVG文字无裁切，捕获JS／HTTP错误为0。
- **实际导航：** 点击书架→概览→4→5→6→7→8→概览，反向8→7→6→5→4；概览8个有效入口、6个待制作项正确。主审已查看第8章桌面浅色、手机深色正文、手机深色图示及手机概览截图。
- **关键例子：** 主Agent复跑`ch05-check.py`、`ch06-check.py`、`ch07-verify.py`、`ch08-check.py`通过。覆盖81／66／33／32字节编码与库级兼容，quorum反例／因果闭包／版本向量，分片移动／索引／迁移假设模型，隔离异常／SSI依赖／2PC持久决定恢复／幂等原子提交模型。
- 机器记录、截图与整合脚本位于`/private/var/folders/5k/y6qh6sfd2g30js0v0qrv4mfr0000gn/T/opencode/ddia2-tools/`：`verify-round2.py`、`verify-round2.mjs`、`round2-static-results.json`、`round2-browser-results.json`及`ch05-`—`ch08-`检查结果；浏览器服务器已关闭。网站没有编译步骤，未初始化Git、推送或部署。

### 遗留与停止

本轮无已知资料、模型、内容或绘图阻塞。未启动真实数据库、Temporal、支付网关或消息代理做集成验证，未做实际集群迁移、网络／崩溃故障注入或性能测试；教学模型不等于完整分布式协议证明，外部参考文献未逐篇全部通读。作者报告保留各自验证时点，末尾补记主审已完成接入，不将后来验证归为作者当时执行。

第2轮交接时第9—14章、全书guide与跨轮整合待后续轮次；当时下一轮为第3轮。四个第2轮会话均已返回、停止编辑，原待验收状态保留。最新完成记录如下。

## 第3轮完成与主审（2026-11-07）

模型目录重新确认`openai/gpt-6-astra` active且支持xhigh；四次写作调用均显式指定`openai/gpt-6-astra#xhigh`，使用全新会话，每人一章，无递归委派。四人全部返回、停止编辑后，主Agent逐章通读正文、来源区和覆盖报告，再接管整合。主Agent为GPT-6 Astra，推理档位未由工具暴露。

| 负责人／章 | 全新会话ID | 正文节数 | 统一汉字粗计 | 章节图 | 状态／覆盖核查报告 |
| --- | --- | ---: | ---: | ---: | --- |
| A／09 | `ses_e4a5dcd4cffeyyZRklnE98Ajjd` | 21 | 15,876 | 6 | 已返回、停止编辑；[报告](notes/ch09-report.md) |
| B／10 | `ses_e4a5dcce2ffdVxD8vzbf3frlMd` | 22 | 17,328 | 6 | 已返回、停止编辑；[报告](notes/ch10-report.md) |
| C／11 | `ses_e4a5dcce1ffeb6F5A3dw9nJzds` | 18 | 12,352 | 4 | 已返回、停止编辑；[报告](notes/ch11-report.md) |
| D／12 | `ses_e4a5dcce0ffepcfrFvxQ8TI2lk` | 23 | 16,450 | 7 | 已返回、停止编辑；[报告](notes/ch12-report.md) |

合计84节、62,006汉字、6张正文表＋2张来源表、12个代码／说明块。汉字按来源区前去围栏代码、保留标题／表格／图注／替代文本统计；第10章作者的17,349含21个代码注释汉字，统一口径为17,328。第12章主审修正有界输入后由16,429增为16,450。主审根据原书小节覆盖、推理、案例与失败路径确认充分展开，不以字数机械换算中英文三分之一；第10／11章略超初始投入区间。

### 交付与接入

- `notes/ch09.md`—`ch12.md`及`chapters/ch09.html`—`ch12.html`同步；逐章报告保留作者当时阅读／验证事实，追加主审结果。
- 23组原生Excalidraw／官方导出SVG，共535个原生元素；每组经负责人实际编辑器重载、改字／恢复。主审检查全部源文字、绑定及SVG并目检全部23图。累计55幅章节图，另有1幅概览图。
- 书架、概览、`notes/overview.md`同步为12／14；累计212节。按当前文件重算共165,920汉字；与历史各轮数直接相加的13字差额，来自第2轮第4章衔接删7字及本轮第8章衔接删6字，历史统计保留当时口径。
- 第8章尾段与翻页、`ch08-render.py`同步更新并重新生成HTML；接通8→9→10→11→12→概览。第13／14章仅待制作文字。第9／11章报告中的同轮待落盘链接现已关闭。

### 主Agent实际审稿与纠错复核

已通读四章全文及报告；回看固定PDF印刷375、376、382、426、431、432、433、436、461、466、471、479、499、504、505、506、522、525、527、528页文字，并查看375页隔离图、470页shuffle图、522页窗口原页及432／435／436／442原页联系表。查看四章全部23幅图的联系表、第10章深色联系表及第12章代表桌面浅色／手机深色正文、手机深色图示。

- **第9章：** 核对网络超时与执行结果、时钟误差界、提交等待条件、租约与进程暂停、原子持久隔离，以及先推进资源代次再读取状态的顺序。区分多数交集与协议投票规则、单副本陈旧读与多副本版本选择；DST是确定性模拟测试而非夏令时的上下文已清楚。
- **第10章：** 对照Herlihy论文定理3／4核对FAA的共识数2指共享内存等待自由模型的参与进程数；回看Raft扩展论文§5.4.2／§8，复核旧任期多数不足直接提交、当前任期提交依据、与本次读取匹配的多数确认及应用进度。etcd3.6 API保证用于核对线性一致读与serializable读取选项；共识多数和原子提交全员准备分别讲解。
- **第11章：** 对照Flink2.1执行模式／容错文档，核对批模式不使用流式检查点；对照S3目录桶RenameObject官方文档，保留对象存储重命名的产品边界。核对shuffle、连接键／排序键、倾斜处理、版本发布屏障与外部副作用。
- **第12章：** 核对CDC快照切点、三时刻校正、半开窗口、迟到更新、三类连接、一致检查点和外部效果保证边界。主审将开篇“文件大小已知”修正为“存在可到达的输入终点，不要求预知精确大小”，与第11章一致；同步HTML和统一术语。此项是笔记表述修正，不是原书勘误。
- 原书／旧稿／笔记解释的纠错对象均保留；有依据的原书修正不冒称出版社已确认勘误，原书与外部旧稿保持只读。

### 实际验证与证据

- **静态整合：** `verify-round3.py`通过14页960项href/src引用、本地链接／锚点、无重复ID和图像alt检查；84节及4份来源区MD／HTML规范化全文一致，8表／12代码块／23图对应，`parity_exceptions`为空。章节检查另覆盖引言。
- **图源与发布：** 23组场景JSON／SVG XML、全部源文字与箭头绑定通过，535原生元素；现有Pages白名单筛出本书69文件＝13 HTML＋56 SVG，不包含PDF、原文、Markdown、图源及制作工具。
- **浏览器：** 本机Chrome14组页面＋23图各浅深色46组，共60组通过。页面含书架2、概览2、四章各桌面浅色／375px手机深色8、第12章额外桌面深色／手机浅色2。正文16px／31.2px，主题保存、双端目录、来源折叠正常，图示加载成功、整页无横向溢出，SVG文字无裁切，捕获JS／HTTP错误为0。作者另各有本章四组合及局部滚动交互检查。
- **实际导航：** 点击书架→概览→8→9→10→11→12→概览，反向12→11→10→9→8；12个有效章节入口、2个待制作项正确。
- **关键例子：** 主Agent复跑`ch09-check.py`—`ch12-check.py`通过：漂移／排队／隔离交错与多副本版本；线性化历史、quorum写回、Lamport／HLC、两进程FAA、共识提交与读屏障；Unix管道／Python／SQLite、shuffle与连接、发布模型；CDC衔接、窗口／迟到、连接SQL、检查点错配及余额／位点原子事务。
- **保留范围：** 比较第3轮开始保存的161份SHA256基线，158份完全相同，仅第8章Markdown、HTML、渲染脚本发生预期衔接变更；第1—7章及旧稿未变。结果为`round3-final-summary.json`。
- 工具与机器证据位于`/private/var/folders/5k/y6qh6sfd2g30js0v0qrv4mfr0000gn/T/opencode/ddia2-tools/`：`verify-round3.py`／`.mjs`、`round3-static-results.json`、`round3-browser-results.json`、`round3-final-summary.json`及截图；章节生成／核查脚本在本书`diagrams/sources/`。临时浏览器及服务器已关闭。网站没有编译步骤，未初始化Git、提交、推送或部署。

### 遗留与停止

无已知资料、模型、内容或绘图阻塞。教学模型与Unix／SQLite执行不等于真实etcd、ZooKeeper、Spark、Flink、Kafka、Debezium、对象存储或邮件／支付服务集成；未做分布式集群故障注入、性能测试或完整协议证明，外部文献未逐篇全部通读。

第3轮交接时第13—14章留第4轮，全书guide及跨轮整合留第5轮。四个第3轮会话均已返回、停止编辑，原待验收状态保留。最新完成记录如下。

## 第4轮完成与主审（2026-11-07）

模型目录重新确认`openai/gpt-6-astra` active且支持xhigh，两次调用显式指定`openai/gpt-6-astra#xhigh`。两个全新会话每人一章，未递归委派或续用前三轮会话；两人全部返回、停止编辑后主Agent才接管章节。主Agent为GPT-6 Astra，推理档位未由工具暴露。

| 负责人／章 | 全新会话ID | 正文节数 | 最终汉字粗计 | 章节图 | 状态／覆盖核查报告 |
| --- | --- | ---: | ---: | ---: | --- |
| A／13 | `ses_e49dd25c8ffeCyR6o5pKhaJXtP` | 26 | 17,008 | 6 | 已返回、停止编辑；[报告](notes/ch13-report.md) |
| B／14 | `ses_e49dd25c3ffezEZYGD23P5plhe` | 12 | 6,210 | 3 | 已返回、停止编辑；[报告](notes/ch14-report.md) |

合计38节、23,218汉字、3张正文表、1个SQL代码块、9组原生Excalidraw／官方SVG，共193元素。统计仍按来源区前去围栏代码、保留标题／表格／图注／替代文本。第14章作者交付6,135字，主审补FTC2026后续状态增75字。第13章稍长用于展开支付前提、两种恢复路径和读隔离边界；第14章自然收束，均已对照核心小节、推理、案例与失败路径审查，没有用字数机械换算三分之一。

### 交付与接入

- `notes/ch13.md`／`ch14.md`、对应`chapters/ch13.html`／`ch14.html`及两份覆盖报告齐备；9组`.excalidraw`／`.svg`保留，生成器、渲染与检查器位于`diagrams/sources/ch13-*`／`ch14-*`。
- 书架、概览及`notes/overview.md`更新为14／14；累计250节、189,123汉字、64幅章节图＋1幅概览图。第12章衔接删15字，由16,450变为16,435；历史统计保留原时点，当前总数以文件重算。
- 第12章尾段、翻页和`ch12-render.py`同步并重新生成HTML；接通12→13→14→概览。第14章报告中作者当时等待第13章落盘的事项已关闭；没有提前创建guide。

### 主Agent实际审稿与核查

主Agent完整通读两章新正文、来源区、覆盖报告、分章原文及只读旧稿。重新打开固定673页PDF，实际查看印刷556、564、569、596原页图像；563、570、571、592仅渲染备用，不算实际图像回看。查看两章全部9幅图联系表、第13章桌面浅色、第14章手机深色正文和手机深色图示，以及第13章最终支付深色图；文字、箭头、边界与正文相符。

- **第13章：** 复核派生顺序、回填／追赶、读写边界、稳定请求ID、唯一约束及端到端责任。阅读OLEP论文相关机制与Disadvantages：目的账户允许入账是前提；预留转正式出账不重复扣款；同请求的不同分录角色分别去重；输出尚未完成时保留可恢复责任；最终完整性不保证跨账户即时原子可见。以Spanner官方说明复核跨地域外部一致事务，以CT官方说明复核日志收录／追加证明不等于证书可信或业务事实正确。
- **第14章：** 复核概率组与个人、代理变量、反馈循环、隐私自主权和数据最小化。以EUR-Lex第5—7条核对用途与同意边界；读取德国定价论文作者摘要，保留非垄断／双寡头双方采用的条件，不据摘要声称观测到自主学习合谋。补读FTC于2026-01-14公布的最终和解命令公告，将2025拟议和解与后续状态分别写明，保留和解不等于法院事实判决的限定；已同步Markdown、HTML及来源链接。
- 原书修正、旧稿收紧、笔记假设及工程补充分开记录；不冒称出版社确认勘误，旧稿只读。

### 实际验证与证据

- **静态整合：** `verify-round4.py`通过16页1,137项href/src引用、本地链接／锚点、无重复ID及图像alt检查。38节、两份来源区规范化全文一致；章节专属`ch13-verify.py`、`ch14-verify.py`另覆盖引言。两个`parity_exceptions`仅章尾文字翻页与HTML卡片结构差异，目标已实际点击。
- **图源与发布：** 9组JSON／SVG XML、全部源文字与绑定对应通过，共193原生元素；作者已分别实际编辑器重载／改字／恢复。Pages白名单筛出本书80文件＝15 HTML＋65 SVG，排除原文、Markdown、图源和制作工具。
- **浏览器：** `verify-round4.mjs`运行Chrome10组页面＋18组独立SVG，共28组通过。页面覆盖书架2、概览2、两章桌面浅色／375px手机深色4、第14章桌面深色／手机浅色2。正文16px／31.2px、主题保存、双端目录、来源折叠正常，无整页溢出或SVG文字裁切，捕获JS／HTTP错误为0。作者另各有本章四组合及局部滚动检查。
- **实际导航：** 点击书架→概览→12→13→14→概览，反向14→13→12；14个有效章节入口、0个待制作项正确。
- **关键例子：** 主Agent复跑`ch13-check.py`通过SQLite请求唯一性／回滚、支付预留与分录去重、部分发布恢复、汇率和集合并集；部分读取总额130与最终69＋30＋1＝100区分清楚。`ch14-verify.py`复算100×20%＝20、余80。
- **保留范围：** 263份SHA256基线中260份完全相同，仅第12章Markdown、HTML、渲染器发生预期衔接变化；第1—11章、其余既有材料、共享assets及外部旧稿未改。结果见`round4-final-summary.json`。
- 工具、JSON及截图在`/private/var/folders/5k/y6qh6sfd2g30js0v0qrv4mfr0000gn/T/opencode/ddia2-tools/`，主要证据为`round4-static-results.json`、`round4-browser-results.json`、`round4-final-summary.json`和两章联系表。临时浏览器与服务器已关闭；网站没有编译步骤，未初始化Git、提交、推送或部署。

### 遗留与停止

本轮无实现阻塞。德国定价论文全文下载受限，只依据原书及已取得作者／UCL摘要限定结论；ACM官网403，仅按原书转述职业准则。外部参考文献未逐篇通读。SQLite与内存教学模型不等于真实Kafka／Flink／支付集成，未做集群故障注入、性能测试、完整协议证明或社会因果识别。

第4轮交接时四份文档同步，两名负责人均已返回、停止编辑。第4轮待验收状态保留；随后第5轮完成记录如下。

## 第5轮全书整合（2026-11-07，完成待验收）

- **模型与职责：**主Agent GPT-6 Astra（`openai/gpt-6-astra`）独立完成，档位未由环境暴露。未调用子Agent、未续用前四轮会话，无后台写作任务。
- **产出：**`notes/guide.md`／`guide.html`含12节、五条路线、43组术语、11行保证范围、15项案例、14章来源、16组纠错与三书补充；书架／概览／14章接通guide。新增或细化40个跨章小节入口。14个页面生成器及`guide-render.py`可持续保留导航。
- **内容保留与深度：**14章250节、64幅章节图保持；正文及来源共32张表、45个代码块，另有1幅概览图。当前正文189,130汉字，仅第1章CDC提示增加7字，第8章“本轮→本章”；guide的8,348汉字不计入章节深度。逐章报告、代表段落、原文回看与整合前后全文比对共同支持保留结论，不按中英字数机械换算约三分之一。
- **实际审阅：**完整读取14份覆盖报告、Glossary及全部标题／锚点，逐章抽读机制、案例和失败路径；针对跨章结论回看原文，实际查看印刷413、569图像。没有本轮重新通读14章全部正文或全部外部参考的声明。具体页码、14章深度矩阵与案例口径见[整合报告](notes/integration-report.md)。
- **统一边界：**接收／持久化／可读、可重放／幂等／恰好一次、2PC全员准备／共识副本法定人数分开；第6与10章quorum阈值、第13章11元与三分片支付保持不同模型；删除后重建限制进入责任路线。原书、旧稿、笔记纠错与时效补充保留对象及证据限制，未新增出版社确认勘误声明。
- **静态检查：**17页1,504项引用／本地链接／锚点，250＋12节及15份来源／引言MD—HTML全文、表格／代码数量通过。对比整合前14章，250节及历史来源保留，仅放行两项明确文字变化。65组图源／SVG、1,485原生元素及全部源文字／箭头绑定通过，SHA256均不变。发布白名单81文件＝16 HTML＋65 SVG。
- **浏览器：**Chrome12组页面＋4组代表SVG，共16组通过；guide四组合、书架／概览／第6／13章代表页、浅深色／375px手机／1440px桌面、16px／31.2px、主题保存、双端目录、来源和局部滚动正常。JS／HTTP错误0；五路线、跨书及来源跳转、14章完整正反导航、无JS手机guide及表格键盘聚焦均实测。代表截图已目检。
- **基线：**332份既有文件290份不变、42份预期变更；共享assets、全部原文、外部旧稿、图源／SVG和历史报告保持。根书架与根交接文档不在该基线内，另为本轮预期编辑。
- **证据与重跑：**制作目录保留`guide-render.py`与`book-check.py`。运行`python3 books/designing-data-intensive-applications-2nd/diagrams/sources/book-check.py OUTPUT_DIR`可检查全书；本轮OUTPUT_DIR为既有`/private/var/folders/5k/y6qh6sfd2g30js0v0qrv4mfr0000gn/T/opencode/ddia2-tools/`，内有`round5-static-results.json`、`round5-browser-results.json`、基线、旧章节快照与截图。网站本身无编译步骤。
- **遗留与停止：**无实现阻塞；德国定价全文／ACM官网等缺口、各轮产品集成与验证边界保留。浏览器和临时服务已关闭，未初始化Git、提交、推送或部署。四份交接文档同步，前四轮待验收状态保留，**第5轮停止待验收**。

最终阅读：[书架](../../index.html) → [概览](index.html) → [全书导航](guide.html) → 14章详解。
