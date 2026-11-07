# 第 2 章交付报告

## 写前原书小节覆盖表

版本：Martin Kleppmann、Chris Riccomini，O’Reilly 英文第二版 February 2026，ISBN 9781098119065。已完整读取 `originals/ddia2-ch02.txt`（含参考文献，印刷33—64／PDF57—88）后，完整读取只读旧稿 `ch02-定义非功能性需求.md` 1—1172行。正文印刷33—56。

| 原书小节 | 印刷页 | 成品正文锚点与覆盖（写前规划，交付已逐项确认） |
| --- | --- | --- |
| 章首 Defining Nonfunctional Requirements | 33 | 导读：四项质量要求与明确口径 |
| Case Study: Social Network Home Timelines | 34—36 | timeline-read、timeline-write：教学假设、读写取舍 |
| Representing Users, Posts, and Follows | 34—35 | timeline-read：三表、关注方向、SQL、轮询计算 |
| Materializing and Updating Timelines | 35—36 | timeline-write：物化、扇出、队列、新鲜度、高关注与高粉丝的区别、混合 |
| Describing Performance | 37—38 | response-time：吞吐量与响应时间、容量与排队 |
| When an Overloaded System Won’t Recover（框） | 38 | overload：重试反馈、亚稳态失效与缓解 |
| Latency and Response Time | 38—39 | response-time：服务时间、网络延迟、排队、队头阻塞 |
| Average, Median, and Percentiles | 40—41 | percentiles：分布、排序、尾部、Amazon语境与收益递减 |
| The User Impact of Response Times（框） | 41 | tail-slo：内容混杂因素、实验结果不能直接迁移 |
| Use of Response Time Metrics | 41—42 | tail-slo：并行最慢分支、独立性假设、SLO与SLA |
| Computing Percentiles（框） | 42 | percentiles：窗口、直方图／近似算法、不可平均或简单相加 |
| Reliability and Fault Tolerance | 43—44 | faults：故障与失效、层级、单点与容错范围 |
| Fault Tolerance | 43—44 | faults：投递中断、漏投与重复、故障注入、不可撤销后果 |
| Hardware and Software Faults | 44—47 | correlated-faults：规模下日常硬件故障、相关失效 |
| Tolerating hardware faults through redundancy | 45—46 | correlated-faults：冗余、故障域、跨区与滚动维护 |
| Software faults | 46—47 | correlated-faults：同版本共同缺陷、资源耗尽、级联、隐含假设 |
| Humans and Reliability | 47—48 | human-reliability：社会技术系统、回滚与渐进发布、无责复盘 |
| How Important Is Reliability? | 48—49 | human-reliability：暂时不可用与永久损坏、相册与Horizon（按书转述） |
| Scalability | 49—52 | load、scaling：增长维度、简单灵活优先 |
| Understanding Load | 50—51 | load：负载参数、固定资源／固定性能、线性与成本 |
| Shared-Memory, Shared-Disk, and Shared-Nothing Architectures | 51 | scaling：资源共享边界、瓶颈、云原生专用存储API |
| Principles for Scalability | 52 | scaling：相同字节吞吐不同请求、独立组件与务实混合 |
| Maintainability | 52—53 | maintainability：长期成本与组织知识 |
| Operability: Making Life Easy for Operations | 53—54 | maintainability：运行模型、观测、自愈与人工控制、自动化悖论 |
| Simplicity: Managing Complexity | 54—55 | maintainability：理解成本、抽象、本质／偶然复杂性边界 |
| Evolvability: Making Change Easy | 55—56 | maintainability：多服务演化、松耦合、不可逆性 |
| Summary | 56 | closing：把形容词变成可检查的约定 |

## 交付状态与文件

2026-11-07，第1轮 Agent B 完成，仅负责第2章，未递归委派。正文、静态页面、图示及本报告均已落盘。**本次交付后停止编辑，交由主Agent接管审稿。**

- `notes/ch02.md`：12个主体小节，3个维护性三级标题，1张比较表，1段SQL，3幅原创图；来源区以`details`折叠。正文区含标题、图注约9,391个汉字，不含来源区；稍高于7—9千投入预估，用于保留必要算例、故障过程和就地纠错。
- `chapters/ch02.html`：与Markdown的12节正文和来源文本逐项比对一致，桌面／手机目录、面包屑、来源折叠、共享主题及阅读脚本、上一章`ch01.html`／下一章`ch03.html`齐全。
- `diagrams/sources/ch02-build.py`：章节专用页面生成器，使用本机已有Python Markdown，基于JESA第2章外壳生成；不属于网站运行依赖。修改本章Markdown后可运行此脚本同步HTML。
- 本报告：`notes/ch02-report.md`。

| 图 | 可编辑场景／简写源 | 网页SVG | 原生元素数 | 作用 |
| --- | --- | --- | ---: | --- |
| 图2-1 | `diagrams/sources/ch02-timeline-paths.excalidraw`、同stem `.skeleton.json` | `diagrams/exports/ch02-timeline-paths.svg` | 22 | 读时聚合与写时物化，两行比较工作转移 |
| 图2-2 | `diagrams/sources/ch02-hybrid-timeline.excalidraw`、同stem `.skeleton.json` | `diagrams/exports/ch02-hybrid-timeline.svg` | 18 | 普通账号预投递、高粉丝账号读时拉取与合并 |
| 图2-3 | `diagrams/sources/ch02-response-budget.excalidraw`、同stem `.skeleton.json` | `diagrams/exports/ch02-response-budget.svg` | 20 | 单次请求的网络／排队／服务时间与端到端80 ms |

三图复用README中的Excalidraw 0.18.0官方导出工具及默认`DDIA_TOOLS`。官方API生成60个原生元素，导出SVG后重载编辑器、修改并恢复文字，三图全部返回`editable:true`。SVG保留官方几何，沿用既有五色主题替换与独立打开主题支持；未手写SVG冒充官方导出。场景文字与SVG文本已比对。

## 覆盖与取舍

上方覆盖表包含章首、所有正文标题、三个框文、硬件冗余／软件故障低层小节及Summary。全章原书核心内容均已进入正文，重点投入如下：

1. 以有方向的关注边解释三表查询，区分“关注很多人”和“被很多人关注”；从读时重复收集过渡到写时扇出，再解释混合方案与新鲜度。
2. 响应时间、服务时间、网络及排队延迟按起止范围解释；一次80 ms请求、单线程队头阻塞、重试风暴与恢复条件都给出过程。
3. 平均数与分位数各有用途；明确最近秩约定，以可排序样本说明不可平均，以六次独立调用说明尾延迟放大；串行阶段分位数不能简单相加。
4. 以投递一半崩溃说明fault/failure层级、不漏与不重复的责任；硬件冗余、共同故障域、软件同源缺陷与组织条件均覆盖。
5. 负载参数、固定资源／固定性能两类问题、三种共享架构与数据库专用存储服务逐项解释；维护三维使用时间线运行与迁移情境展开。

压缩内容：未逐项复制硬件研究中的所有故障率、未逐字转述每项商业转化研究数字、未复刻所有参考文献、黑洞幽默及产品清单。保留这些段落承担的论证（规模下故障常态化、指标因果口径、容错范围），以免统计或产品名称淹没主线。旧稿面试题、长篇产品推荐、未经本章需要验证的Python库代码未移植。

## 旧稿修正与依据

本次未认定新的原书事实错误；以下主要是旧稿的算术、表述或适用条件问题，未归咎于原书。外部依据实际读取日期均为2026-11-07。

| 旧稿原表述／问题 | 核对结果与修正 | 成品位置 |
| --- | --- | --- |
| 5,800×200约一百万，与四亿相比“少400倍”；缓存读取为O(1) | 精确更新量为1,160,000次/秒，数量比约344.83；读查找与写更新单位成本不同，不能推响应性能倍数；返回N条结果仍有读取与传输成本 | timeline-write就地说明 |
| “普通用户那样丢”，名人不能丢 | 原书允许采样的是“某个收件人关注极多且看不完”的特定情境，不是普通作者的帖子天然可丢 | timeline-write |
| 用用户平均粉丝数直接推每条帖平均扇出 | 必须使用按发帖活动加权的接收者数；原书在写量估算处另明确假设平均每帖到达200人 | timeline-write |
| “服务端测会漏掉排队延迟” | 仅服务时间不含排队；服务端入口到出口测量可以包含内部排队，仍不等于完整客户端时间 | response-time |
| Full Jitter优于Equal Jitter由“AWS Brooker用数学证明”，并称峰值最低 | AWS原文是特定OCC竞争模拟，比较工作量和完成时间；不能升级为一般性最优定理 | overload；已读[AWS原文](https://aws.amazon.com/blogs/architecture/exponential-backoff-and-jitter/) |
| B为99次10 ms＋1次1,000 ms，却写p99=1,000 ms；总体却用第198个取秩 | 同一最近秩法下B的p99应为10 ms；改成98＋2并明确方法，得到单机100／1,000、整体100，平均550仍错误 | percentiles；数值独立复算；[Prometheus官方](https://prometheus.io/docs/practices/histograms/)核对聚合原则 |
| “百分位才是对的度量”“p9999一般不值得优化” | 平均数仍可用于适当容量估算；Amazon万分位优化的成本结论属于历史业务处境 | percentiles、tail-slo |
| 并行总响应=max（各下游）且直接套概率 | max只是在同时开始、等全体返回时的下游等待段；端到端还包含额外阶段；1−0.99⁶明确要求独立、相同超阈概率 | tail-slo |
| 请求成功率99.9%直接换算三十天43分钟停机 | 请求数口径与时间口径分开：三千万请求预算三万次；三十天按时间计才对应43.2分钟 | tail-slo |
| 硬件故障按独立理解，多机就可无感升级 | 硬件亦有共同故障域；多机滚动维护还需剩余容量、复制与兼容条件 | correlated-faults |
| 将S3等通用对象存储直接作为“为数据库定制API”例子 | 原书此处讨论专用数据库存储接口与NAS／SAN的差别；不能把所有存算分离形态混为一种 | scaling |
| 自动化越多／无共享越可扩展等绝对化倾向 | 保留自动化排障代价、热点与协调成本，回到具体工作负载和组织条件 | scaling、maintainability |

旧稿代码区另有明确问题，因不属本章必要展开而未移植：错误预算示例注释把三千万请求、99.9%目标写成约43,000次，正确为30,000次；`actual_failures / budget`表示预算消耗比例，并非具有时间口径的消耗速率。这些在阅读时已识别，旧稿保持只读。本章新SQL只验证查询方向和排序，没有复制旧Python库与熔断器实现。

## 原图、代码与数值回看

已实际渲染并查看9张原书页面：

- 印刷34／PDF58：图2-1，关注边方向与三张表的连接键。
- 印刷35／PDF59：SQL、每五秒轮询、两百万查询／四亿作者查找数量级。
- 印刷36／PDF60：图2-2，按关注者扇出与派生时间线读取。
- 印刷37／PDF61：图2-3，响应时间随容量逼近而上升的定性曲线。
- 印刷39／PDF63：图2-4，两个方向网络、两段排队、服务时间与整体计时范围。
- 印刷40／PDF64：图2-5，100次样本柱、均值／中位／高分位横线。
- 印刷42／PDF66：图2-6，原图7个下游分支及最慢487 ms；正文另外使用明确自拟的3分支与6次概率例，不冒称原图数字。
- 印刷51／PDF75：shared-memory／disk／nothing和数据库专用API原表述。
- 印刷52／PDF76：100,000×1 kB/s与3×2 GB/min的100 MB/s比较。

数值验证用本地Python独立计算，结果保存于临时目录`numeric-check.json`：

| 核查项 | 结果 |
| --- | --- |
| 轮询与作者查找 | 2,000,000查询/秒；400,000,000查找/秒 |
| 写时物化 | 1,160,000次更新/秒；操作数量比344.827586…，非性能倍数 |
| 十秒假设尖峰 | 每秒30,000,000更新；积压280,000,000；恢复后净消化840,000/秒，约333.33秒清空 |
| 单请求分段／队头阻塞 | 80 ms总响应；后到请求等待99 ms＋处理2 ms＝101 ms |
| 均值／分位反例 | 199 ms；两机p99=100／1,000 ms；合并p99=100 ms而非550 ms |
| 六次独立调用 | 1−0.99⁶＝5.851985…% |
| 两种预算口径 | 30,000次失败／43.2分钟，各自口径独立 |
| 磁盘数量级 | 每天期望0.5479—1.3699次，非每天固定一块 |
| 数据吞吐单位 | 两种负载均为100,000,000 B/s，采用十进制kB／GB |
| SQL | SQLite内存库3位用户、3条帖子、两条方向不同的关注边，当前用户10仅返回被关注作者20的帖子，顺序[2,1]；未关注作者30的帖子不出现 |

SQL验证不冒称生产数据库执行计划测试；新增数字都是说明机制的假设，不是平台实测。

## 页面与资源验证

- 静态核对：15个ID无重复，12节Markdown／HTML及来源正文逐项一致；图片3张均有alt、图注和大图入口；源场景31个文本元素与SVG文字一致。
- 所有本地链接／资源与锚点通过。第一次核对时第3章仍由并行负责人制作，最终核对时第1、3、4章页面均已存在，无缺失目标。未来章节只作文字提示。
- 网页没有指向PDF、`notes/`、`originals/`或`diagrams/sources/`的发布无效链接。现有Pages白名单会收录本章HTML＋3个SVG，共4个发布文件；笔记、报告、场景与制作脚本被现有目录规则排除。
- 本站无静态编译步骤；执行的是本章页面生成、资源及浏览器验证，不报告虚构的全站构建。
- Chrome／Playwright实际运行1440px桌面、375px手机 × 系统浅色／深色，共4组。正文计算样式16px、31.2px行高；整页无横向溢出；图与表仅局部滚动；全部图片加载成功，无捕获的页面JS或HTTP错误。
- 各组实际操作手动切换到相反主题并刷新，偏好保存成功；手机目录展开并跳至分位数节成功；来源折叠展开成功。
- 3张独立SVG分别在浅／深色共6组加载，文本边界均未裁切；实际查看混合图浅色、请求计时图浅色、读写路径图深色、手机深色页面与局部滚动图、桌面浅色页面截图，文字与箭头无重叠。
- 页面尾部最后几处纯文本修正后，重新生成HTML并再次核对12节／来源一致性及全部链接；未改布局或图形，无新增浏览器疑点，不重复整套浏览器检查。

验证与截图位于：`/private/var/folders/5k/y6qh6sfd2g30js0v0qrv4mfr0000gn/T/opencode/ddia2-ch02/`。包含`numeric-check.json`、`static-check.json`、`browser-check.json`、原书页面拼图和阅读／SVG截图。所有浏览器进程已在验证结束时关闭，无后台写作或预览服务。

## 跨章衔接与遗留

- 向前连接第1章的权威记录／派生数据及架构选择，向后连接第3章的数据模型、第4章的索引与存储成本；后续复制、分片、事务、故障、流处理只作文字预告。
- 没有资料、公式、图示或页面阻塞。原书全部100条参考文献未逐篇另行通读，硬件统计、Horizon与历史商业实践按原书转述并标明范围；没有补写当前产品实现或法律结论。
- 主Agent后续负责全文主审、共享概览／导航状态与本轮交接文件。本Agent未修改任何共享文件、其他章节或只读旧稿。
- **已完成本章任务并停止编辑；主Agent可接管上述文件。**
