# 第13章交付报告（已完成）

完成日期：2026-11-07。第4轮Agent A的第13章已完成，交回主Agent；完成后停止编辑，不进入第5轮。

## 交付入口与统计

- 正文：[ch13.md](ch13.md)；阅读页：[ch13.html](../chapters/ch13.html)。共26节、2张正文表、1个SQL代码块、6幅图。
- 正文统计为 **17,008个汉字**：取Markdown开头至 `<details id="sources">` 之前，剔除围栏代码块，按Unicode `U+4E00—U+9FFF` 计数；包含章标题、引言、节标题、图注和图片替代文本，不计来源区、章尾翻页、代码、数字及拉丁字母，不把SVG内文字再次计入。
- 相比初始12—16千字规划略长，保留的增加量主要用于支付的前提、预留转换、两条恢复路径、读隔离边界，以及审计能证明什么；未为凑字数添加重复总结。
- 网页具备桌面／移动端26项目录、来源折叠区、浅深色主题、可放大图示、上一章 `ch12.html`／下一章 `ch14.html` 和书籍概览导航。
- 六组原生Excalidraw和官方SVG共138个场景元素。按网站发布规则，本章新增发布资源为1个HTML＋6个SVG；Markdown、图源及制作脚本属于非发布资料。

## 范围与读取

- 第4轮Agent A，仅负责第13章；任务指定 `openai/gpt-6-astra#xhigh`，未递归委派。
- 已读根AGENTS、PLAN、本书README及指定Google ch02、JESA ch03／ch02阅读壳、Hard Parts ch09。
- 已完整通读 `originals/ddia2-ch13.txt` 全1931行：印刷539—584／PDF563—608，含正文539—580、参考文献580—584；随后完整通读只读旧稿 `/Users/zy/ai_learn/ddia_2nd/ch13-流系统的哲学.md` 全842行。
- 固定只读PDF为 `/Users/zy/ai_learn/ddia_2nd/Designing_Data_Intensive_Applications_2nd_Edition.pdf`，英文第二版，February 2026，First Release 2026-02-18，ISBN 978-1-098-11906-5；作者Martin Kleppmann、Chris Riccomini。PDF页序比印刷页大24。
- 已实际图像回看印刷556（原图13-1）、562—564（例13-1／13-2及跨地域事务表述）、569—572（原图13-2、恢复及及时性／完整性）、578（审计工具），对应PDF580、586—588、593—596、602，共9页。印刷567／568只渲染过，未实际查看图像，不列入回看范围；其文字已随本章完整通读。
- 只写本章Markdown、HTML、报告和ch13-*图源／导出；旧稿、原书及共享文件只读。

### 实际补充读取

1. 原参考[47]：[Online Event Processing](https://martin.kleppmann.com/papers/olep-cacm.pdf)，CACM 62(5)，43—49，2019。下载作者PDF，完整读7页提取正文；重点核对46—48页的日志／消费者假设、第47页目的账户允许入账、第48页Disadvantages的读取隔离限制。本地阅读副本在临时工具目录 `ch13-pdf/olep.pdf`／`.txt`。
2. [End-to-End Arguments in System Design](https://web.mit.edu/Saltzer/www/publications/endtoend/endtoend.pdf)：完整读MIT所存10页版本；重点核对careful file transfer、Duplicate message suppression和Identifying the ends。本地副本在 `ch13-pdf/endtoend.pdf`／`.txt`。
3. [Spanner：TrueTime and external consistency](https://cloud.google.com/spanner/docs/true-time-external-consistency)：读取官方说明，核对跨服务器／多数据中心事务与外部一致性。
4. [AWS：Transactional outbox pattern](https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/transactional-outbox.html)：读取官方模式说明，核对本地事务共同保存状态和待发消息、重复发布与消费侧幂等。
5. [RFC9162](https://www.rfc-editor.org/rfc/rfc9162.html)：读取Introduction、§2.1及§4相关描述；核对Merkle收录／追加证明、发现可疑签发和分叉视图的边界。标明其Experimental状态，不据此判断当前浏览器部署。

以上资料核查日期均为2026-11-07。初次尝试的OLEP地址404、ACM HTML访问403，随后成功读取作者公开PDF，最终没有因此留下资料缺口。原章参考文献已完整读到，但未逐篇访问全部引用；铁路历史和数据库历史bug保留为按原书转述，不作为独立考证或当前产品缺陷判断。

## 原书完整小节覆盖（已落实）

下表包括章首、层级标题、所有子节、铁路说明框及章末总结；原书参考文献的处理范围见上文。锚点均对应交付正文与HTML。

| 原书小节／印刷页 | 笔记对应锚点 | 覆盖重点 |
| --- | --- | --- |
| 章首／539；Data Integration／539 | integration | 本章为作者偏重数据流的一种哲学，非万能架构 |
| Combining Specialized Tools by Deriving Data／540 | integration | OLTP、搜索、缓存和分析的多种表示 |
| Reasoning about dataflows／541 | integration | 写入口、派生方向、并发双写和顺序 |
| Derived data versus distributed transactions／541—542 | transactions-and-logs | 原子提交与确定性重试；读新鲜度及XA边界 |
| The limits of total ordering／542—543 | order-and-causality | 单主吞吐、分片、跨地域、微服务和离线客户端 |
| Ordering events to capture causality／543—544 | order-and-causality | 删除好友后发消息；逻辑时钟不等于有序交付 |
| Batch and Stream Processing／544 | batch-and-stream | 输入有界性、增量和历史计算 |
| Maintaining derived state／544—545 | batch-and-stream | 确定性、托管状态、跨分片索引、异步隔离 |
| Reprocessing data for application evolution／545—546 | reprocessing | 新旧视图、回填与追赶、灰度和回退 |
| Schema Migrations on Railways（框）／545 | reprocessing | 双轨距类比；按原书转述历史 |
| Unifying batch and stream processing／546 | batch-and-stream | 重放、恰好一次和事件时间；Lambda／Kappa限定 |
| Unbundling Databases／546—547 | unbundling | Unix低层组合与关系高层抽象 |
| Composing Data Storage Technologies／547 | unbundling | 内部索引、物化视图与外部派生的对应 |
| Creating an index／548 | unbundling | 快照、回填、增量衔接与持续维护 |
| The meta-database of everything／548—549 | unified-reads-writes | 组织级数据流类比，不宣称全局事务 |
| Federated databases (unifying reads)／548—549 | unified-reads-writes | 联邦查询及模型映射 |
| Unbundled databases (unifying writes)／549 | unified-reads-writes | CDC、日志、可靠写传播 |
| Making unbundling work／549—550 | composition-cost | 系统／团队松耦合及可靠交接 |
| Unbundled versus integrated systems／550—551 | composition-cost | 单库够用时的停止条件与运维成本 |
| Designing Applications Around Dataflow／551 | derivation-code | 电子表格依赖更新 |
| Application code as a derivation function／551—552 | derivation-code | 索引、搜索、模型、UI缓存的转换 |
| Separation of application code and state／552—553 | derivation-code | 部署代码与持久状态；Church笑话缩写 |
| Dataflow: Interplay between state changes and application code／553—554 | derivation-code | 顺序、可靠交付和可靠状态更新 |
| Stream processors and services／554—555 | exchange-rate | 汇率本地副本、流—表连接与历史语义 |
| Observing Derived State／555—556 | read-write-boundary | 写时预计算、读时求值及原图13-1 |
| Materialized views and caching／556—557 | read-write-boundary | 扫描／索引／热点缓存的边界移动 |
| Stateful, offline-capable clients／557—558 | client-dataflow | 本地优先、设备副本、像素视图 |
| Pushing state changes to clients／558—559 | client-dataflow | 快照、订阅、游标、重连与保留边界 |
| End-to-end event streams／559 | client-dataflow | 设备到设备、低延迟不等于硬实时 |
| Reads are events too／559—560 | reads-as-events | 一次性读／持久订阅连接；记录所见状态 |
| Multishard data processing／560—561 | multishard-queries | URL受众集合并集、反欺诈多键连接 |
| Aiming for Correctness／561—562 | correctness | 有状态损坏、强组件不等于正确应用 |
| The End-to-End Argument for Databases／562 | end-to-end | 端点业务语义与底层保证范围 |
| Exactly-once execution of an operation／562—563 | request-id | 最终效果、不确定响应、幂等元数据 |
| Duplicate suppression／563—564 | request-id | TCP／数据库／HTTP三层；原例13-1 |
| Uniquely identifying requests／564—565 | request-id | 稳定请求ID、唯一约束、本地原子性、例13-2 |
| The end-to-end argument／565—566 | end-to-end | 校验、认证与底层机制仍有价值 |
| Applying end-to-end thinking in data systems／566 | end-to-end | 可组合容错抽象及应用责任 |
| Enforcing Constraints／566—567 | uniqueness | 约束域、唯一性与余额规则 |
| Uniqueness constraints require consensus／567 | uniqueness | 冲突值同分片、裁决和安全换主 |
| Uniqueness in log-based messaging／567—568 | uniqueness | 用户名请求、决定输出和客户端等待 |
| Multishard request processing／568—570 | payment-flow / payment-recovery | 原图13-2预留、三条分录、重试与完整交接 |
| Timeliness and Integrity／571—572 | timeliness-integrity | 定义、信用卡账单、暂态和损坏 |
| Correctness of dataflow systems／572—573 | timeliness-integrity | 单输入、确定性、请求ID和不可变历史 |
| Loosely interpreted constraints／573—574 | coordination-boundary | 库存／超售／透支、补偿成本及适用边界 |
| Coordination-avoiding data systems／574—575 | coordination-boundary | 避免跨分片等待，必要处保留协调 |
| Trust, but Verify／575 | auditing | 系统模型与现实硬软件错误 |
| Maintaining integrity in the face of software bugs／576 | auditing | 合法事务也可写错；历史bug按原书转述 |
| Don’t just blindly trust what they promise／576—577 | auditing | 回读、备份恢复、审计 |
| Designing for auditability／577 | audit-provenance | 意图、代码版本、输入依赖、重算 |
| The end-to-end argument again／577—578 | audit-provenance | 覆盖整条派生链、共同错误与检查边界 |
| Tools for auditable data systems／578 | cryptographic-audit | Merkle／签名／区块链／CT的证明范围 |
| Summary／579—580 | synthesis | 技术正确性到第14章影响责任 |

## 已落实的纠错、限定与补充

正文在相应位置区分原书观点、旧稿问题和笔记解释。下列修正不冒称为出版社已确认的勘误。

| 原表述／来源 | 问题及依据 | 本次解释与位置 |
| --- | --- | --- |
| 旧稿把unfriend写成“A取消关注B” | 单向取消关注通常不会阻止B看A的内容，改变原书权限案例的方向 | §03按解除好友／撤销可见关系解释，并区分最终收敛与不可撤回通知 |
| 旧稿“大规模下全局全序不可得” | 原书542—544讨论的是成本、瓶颈和架构中未定义的顺序，不是普遍不可能性 | §03保留协调建立顺序域与跨分片因果依赖两条路径；逻辑时间戳不保证有序交付 |
| 异步消费者“互不受影响”、事务参与者失败就中止 | 前者仍受保留期、积压和背压约束；后者忽略2PC准备后阻塞与既有提交决定 | §02说明等待边界与故障恢复，不把日志隔离说成无条件隔离 |
| 旧稿Lambda“已弃用” | 原书546是流行程度及演进判断，不是统一废弃公告 | §04改为不再流行的作者判断，并保留批流语义与物理策略的区别 |
| 原书／旧稿迁移“每步容易回滚” | 需旧视图仍受维护、输入可用及外部效果可恢复 | §05说明回填、追赶、切换与条件化回退 |
| 旧稿把微服务概括为“统一读” | 职责／部署组织方式不等于联邦查询 | §07区分联邦读取、写传播与微服务；§10说明微服务同样能维护本地订阅副本 |
| 原书562把事务能力通常限定单数据中心并排除地理分布 | Spanner官方说明提供跨服务器及多数据中心的外部一致事务 | §15改为广域协调代价的讨论，不将其解释成技术不可能 |
| 原书／旧稿以表单字段哈希标识请求 | 同内容可能是两次合法意图；稳定身份不能只由内容决定 | §16新意图新ID、重试复用ID、同ID异参数识别误用；去重与业务效果共同提交 |
| 原书图13-2被泛化为任意跨账户支付流程 | OLEP第47页要求批准只依赖付款账户，目的账户允许入账 | §19先声明该前提；目的账户可能拒绝时需额外协议 |
| “重处理就会重新发出所有消息”，或见过ID便跳过 | 若预留已持久而输出尚未发完，跳过会永久漏发；任意当前状态重试也可能改变决定 | §20分别展开一致恢复状态／位点后重放，以及本地事务持久待发清单；未确认输出责任必须保留 |
| 把支付完成效果理解为跨账户即时原子可见 | OLEP第48页明确跨存储读取隔离限制 | §19—20区分预留与正式扣款、请求与分录角色、批准与全部入账；跨账户任意时点求和不保证为100 |
| 旧稿“ACID同时提供线性一致性”及原书572的宽泛对照 | ACID不指定实时顺序，可串行化也不自动等于严格可串行化 | §21按实际隔离、复制与读取路径讨论及时性；进度等待不自动提供跨分片快照 |
| 补偿容易、避免协调便能维护任意约束 | 补偿是新的现实效果，无法撤回泄露；严格冲突约束仍需裁决 | §18／22保留局部顺序域、共识和业务承诺前提 |
| 重算相同就证明数据正确 | 相同错误代码可能重复同一错误 | §24说明来源、版本、共同输入边界及独立不变量检查 |
| 原书578／旧稿“CT检查证书有效性” | RFC9162的收录和日志审计不证明域名授权或证书可信，也不阻止错误签发 | §25限定为帮助发现可疑签发、检查历史；说明分叉视图与可信根边界 |

保留并展开的原书主线包括：日志派生、批流重算、数据库拆分、读写路径、客户端订阅、读作为事件、端到端保证、严格约束、及时性／完整性及审计。商品双写、视图v1／v2、汇率数值、游标40—43、集合并集、100／31／30／1元和SQL整数分均明确标作笔记假设或教学改写。持久待发清单及分录对账是工程补充，不归为原图已经实现的机制。

## 图示与制作文件

| 文件前缀（均为ch13-*） | 聚焦问题 | 原生元素数 |
| --- | --- | --- |
| integration | 权威输入与各视图独立推进 | 23 |
| read-boundary | 三种读写计算边界 | 30 |
| client-subscribe | 快照、增量、游标与断线补读 | 20 |
| request-id | 成功响应丢失后的稳定ID重试 | 22 |
| payment | 付款方批准、预留及三条分录传播 | 21 |
| recovery | 只发布一部分后如何继续履行输出责任 | 22 |

- 可编辑场景：`diagrams/sources/ch13-*.excalidraw`；网页资源：`diagrams/exports/ch13-*.svg`；保留对应 `.skeleton.json` 和 `ch13-make-diagrams.py`。
- 通过只读共享工具 `export-excalidraw.mjs` 调用官方 `convertToExcalidrawElements`／`restoreElements`、`exportToSvg`；六图均实际挂载编辑器、重载保存的原生场景、改字并恢复，结果 `editable:true`。原生对象不是嵌入截图。
- SVG沿用站点浅深色调色、替代标题／描述与独立查看主题支持；正文均有读图说明、图注、替代文本和放大入口。
- 最终目检把支付图回流落点从x120移至x180，使其与客户端提交线分开。直接修订已有原生场景并官方重导出，同时同步skeleton及生成器；保留对象ID和绑定。单独复验其双主题与编辑器恢复。
- `ch13-render.py`从Markdown生成本章HTML，沿用ch12阅读外壳；`ch13-check.py`、`ch13-verify.py`、`ch13-browser.mjs`分别保存教学模型、静态同步和浏览器检查。

## 实际验证与结果

| 验证 | 实际结果 |
| --- | --- |
| 静态生成 | `python3 …/ch13-render.py`成功，26节、6幅图；页面由静态HTML／CSS／JS／SVG组成 |
| MD／HTML全文同步 | `ch13-verify.py`检查引言、全部26节及来源区的规范化全文一致；26个章节锚点、图像替代文字及尺寸有效 |
| 本地引用与发布边界 | 98项本地href／src引用通过，目标文件及锚点存在；页面不链接notes／sources／originals；ch14已存在，无待落盘链接 |
| 图源／SVG | 六份原生JSON、全部文字对应SVG、箭头绑定目标存在；共138元素；最终支付图重新导出及编辑器校验通过 |
| SQL请求去重 | SQLite执行正文SQL；相同r7重试触发唯一约束并回滚，余额仍为8900／1100分，请求记录1条；提交前回滚不留请求或余额效果 |
| 支付恢复教学模型 | A预留31后可用69，后续80请求不满足余额；只送达B时跨存储读总额130；保留待发记录后重送全部，重复B不再次生效，最终A=69、B=30、F=1，预留归零 |
| 小算例 | Decimal验证100×7.20=720、100×7.25=725；集合并集大小4而非相加5 |
| 浏览器阅读 | Chrome／Playwright桌面1440及手机375×浅深色，共4组；无页面横向溢出，正文16px／行高31.2px／行宽≤720px；六图均正常加载 |
| 交互与导航 | 首次跟随系统、手动主题重载保持；双端目录可跳至恢复段落，来源可展开，手机图示可局部横向滚动；实际翻页到ch12和ch14 |
| 独立SVG | 六图×双主题12组，主题调色正确、文字未裁切；支付排版修订后另做2组定向复验 |
| 运行错误与清理 | 主浏览器16组及支付最终2组均无JS／HTTP错误；本人启动的浏览器和临时端口服务器均已关闭 |
| 实际目检 | 六图浅色联系表、桌面浅色／手机深色恢复段落、支付深色图；修订后再次查看支付深色成图，两条入线已分开 |

制作期间的检查器问题已修复：最初缺少 `bs4`，改用标准库 `HTMLParser`；浏览器检查曾错误要求article直接声明 `max-width:720px`，现按实际网格限制后的行宽检查；局部滚动应作用于 `.concept-figure > a`，而非外层figure。上述是检查器适配问题，修正后通过。最后只对支付图排版变更做定向复验，并重跑章内静态同步检查。

结果与截图存放于：`/private/var/folders/5k/y6qh6sfd2g30js0v0qrv4mfr0000gn/T/opencode/ddia2-tools/`。

- `ch13-export-results.json`：六图初次导出及编辑器校验；`ch13-payment-export-results.json`：最终支付图原生重导出。
- `ch13-static-results.json`、`ch13-check-results.json`、`ch13-browser-results.json`：静态、模型、16组浏览器结果。
- `ch13-payment-final-results.json`、`ch13-payment-final-{light,dark}.png`：最终支付图定向结果和截图；旧联系表保留修订前快照，以这两张支付图截图为准。
- `ch13-pdf/`：实际读取的补充论文及PDF回看图像。临时结果可能被环境清理，关键结论已写入本报告。

### 验证边界

- SQLite及内存教学模型只核对文中局部事务、重复效果、未发完输出和数值推理；没有运行真实Kafka／Flink／支付服务集成，没有做分布式故障注入、性能基准或完整协议证明。
- 支付模型用一个原子步骤表示接收方的去重与余额提交，不能据此声称已验证真实接收方存储实现；状态／位点重放路径主要按原书与论文解释，执行检查使用持久待发清单路径。
- 浏览器实际覆盖Chrome下上述尺寸、主题和操作，不宣称覆盖全部浏览器或设备；站点为静态交付，本次验证了本章生成与本地服务，没有执行GitHub Actions部署或全站发布构建。
- 未初始化Git、提交、推送或部署。原书全部参考文献并未逐篇独立核查，补充来源的实际读取范围以上文为准。

## 待办与交接

- 第13章范围内无未解决阻塞或待补资料；本章到ch12／ch14／书籍概览的链接已通过。
- 主Agent负责第4轮统一术语／导航整合、书籍概览和ch12到ch13入口，以及全站发布检查；本章已提供完成文件，不自行改写这些共享入口。
- **第4轮Agent A已完成；完成后停止编辑，不进入第5轮，等待主Agent接管。**

## 主Agent接入完成补记（2026-11-07）

- 两名负责人均返回、停止编辑后，主Agent已通读本章正文／来源／报告、原文及只读旧稿；复核OLEP支付前提与读隔离限制、Spanner跨地域事务和CT证明边界，保留正文深度与全部6图。
- 全部6图已在最终联系表目检，另查看支付深色图及桌面浅色正文；图源文字、箭头绑定与SVG对应通过。
- 接通12→13→14→概览并实际点击正反导航；概览与书架现为14／14。原交付中的共享接入待办已关闭。
- 主Agent复跑`ch13-check.py`、`ch13-verify.py`通过；SQL去重与回滚、预留／分录去重、部分发布恢复及数值例子符合正文。统一整合检查通过16页1,137项引用、两章38节／来源同步、9组图与80个发布文件筛选；Chrome28组通过，捕获错误0。
- 最终本章仍为26节、17,008汉字、2表、1代码块、6图。完整本轮验证、统计及边界见本书README第4轮记录；证据`ddia2-tools/round4-*.json`。以上为主Agent后续执行，不改写作者当时的验证记录。guide留第5轮，本轮已停止。
