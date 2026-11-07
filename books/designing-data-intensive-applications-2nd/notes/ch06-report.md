# 第6章交付报告：复制

状态：**第2轮第6章已完成，交付主Agent审稿；负责人B返回后停止编辑。** 日期2026-11-07。只处理ch06，未递归委派或启动其他Agent。

## 固定资料与实际阅读

- Martin Kleppmann、Chris Riccomini，O’Reilly，February 2026，第二版；正文印刷197—244／PDF221—268，含参考文献完整章至印刷250／PDF274。
- 已完整读取`originals/ddia2-ch06.txt`（2118行，含参考文献）及只读旧稿`/Users/zy/ai_learn/ddia_2nd/ch06-复制.md`（1354行）。
- 已读根AGENTS、PLAN、CONTINUE、本书README；本书没有独立CONTINUE，交接以根文件为准。写作结构参考PLAN §2.3三个指定稿及本书ch04页面。

## 写前原书小节覆盖表（已按表落实）

| 原书小节／印刷页 | 已完成笔记锚点 | 核心覆盖与取舍 |
| --- | --- | --- |
| Introduction；Backups and Replication／197—198 | replication-purpose | 复制动机、变化、备份区别；复制与分片分别讨论 |
| Single-Leader Replication／198—200 | single-leader | 单主写顺序、从节点读、分片内单主 |
| Synchronous Versus Asynchronous Replication／200—201 | sync-ack | 确认边界、异步丢写、半同步／多数派；补核实际确认语义 |
| Setting Up New Followers／201—202 | bootstrap-storage | 一致快照＋精确日志位点、追赶与保留 |
| Databases Backed by Object Storage／202—203 | bootstrap-storage | 分层、独立WAL、零盘，条件写原语和实现责任 |
| Handling Node Outages；Follower failure／204 | failover | 从节点重放、日志缺口与恢复负载 |
| Leader failure: Failover／204—206 | failover | 超时、选主、切流与隔离旧主；GitHub事故按原书转述 |
| Implementation of Replication Logs；Statement-based／206—207 | replication-logs | 非确定性、执行顺序、副作用；MySQL默认值需核官方文档 |
| Write-ahead log shipping／207—208 | replication-logs | 存储耦合及跨版本边界 |
| Logical (row-based) log replication／208 | replication-logs | 行增删改、事务提交与CDC |
| Problems with Replication Lag／209 | read-your-writes | 最终一致性不保证时限 |
| Reading your own writes／210—211 | read-your-writes | 路由、会话位点、时间窗、跨设备 |
| Regions and Availability Zones／212 | multi-region | 地域／可用区故障域 |
| Monotonic reads／212—213 | session-order | 不倒退、切换副本前提 |
| Consistent prefix reads／213—214 | session-order | 问答因果、分片快慢不同 |
| Solutions for Replication Lag／214—215 | session-order | 应用补偿复杂性，强保证与其代价 |
| Multi-Leader Replication／215—216 | multi-region | 多写入口、同步多主为何未继续展开 |
| Geographically Distributed Operation／216—218 | multi-region | 本地写、断网与恢复、全局约束 |
| Multi-leader replication topologies；Problems／218—220 | multi-region | 环／星／全互联、防环、insert-update超车 |
| Sync Engines and Local-First Software／220 | local-first | 离线日历及设备副本 |
| Real-time collaboration, offline-first, local-first／220—221 | local-first | 三个概念及服务退出后的数据可用性 |
| Pros and cons of sync engines／221—222 | local-first | 本地持久状态、后台交接、响应式更新、预取规模；游戏仅一句范围说明 |
| Dealing with Conflicting Writes／222—223 | conflicts-lww | wiki标题并发，单主与业务丢失更新区别 |
| Conflict avoidance／223—224 | conflicts-lww | 归属路由、迁移窗口、奇偶ID |
| Last write wins／224—225 | conflicts-lww | 确定性选赢家、时钟反例、逻辑时钟边界 |
| Manual conflict resolution／225—226 | merge-crdt | siblings、购物车删除复活、合并自身并发 |
| Automatic conflict resolution／226—227 | merge-crdt | 强最终一致、集合／文本／计数器／映射 |
| CRDT and OT／227—228 | merge-crdt | ice→nice!，索引转换与稳定ID；补充小计数器算例 |
| Types of conflict／228—229 | business-constraints | 同字段冲突与跨记录预订冲突、合并不能自动保约束 |
| Leaderless Replication／229 | leaderless-repair | 协调者不是主节点，Dynamo与DynamoDB区分 |
| Writing When a Node Is Down／229—230 | leaderless-repair | 3副本2确认，恢复后读旧及版本选择 |
| Catching up on missed writes／231 | leaderless-repair | 读修复、提示移交、反熵各自触发及缺口 |
| Using quorums／231—233 | quorum | 集合交集推导、法定人数不等于多数派、容错算例 |
| Limitations of quorum consistency／233—234 | quorum-limits | 部分写、读倒退、恢复数据回退、成员变化、并发与时钟 |
| Monitoring staleness／234—235 | performance-regions | 日志距离／时间区分、无主无单一进度 |
| Single-Leader Versus Leaderless Performance／235—236 | performance-regions | 最快r个、灰故障、修复负载、sloppy quorum反例 |
| Multi-Region Operation／236—237 | performance-regions | 本地／全局quorum范围，转发优化按原书说明 |
| Detecting Concurrent Writes／237—238 | causality | 到达顺序不能当统一版本顺序 |
| Happens-before；Concurrency, Time, Relativity／238—239 | causality | 先发生、传递性、并发不靠墙钟；相对论仅保留信息传播直觉 |
| Capturing happens-before／239—241 | version-number | 五次购物车写，传入上下文与新分配版本分开 |
| Version vectors；Version vectors and vector clocks／242 | version-vectors | 分量偏序、合并上下文、跨副本写；dotted变体只说明职责 |
| Summary／243—244 | conclusion | 三种模型的排序／等待／冲突责任和跨章衔接 |

## 产出与统计

- 阅读页：`chapters/ch06.html`；同步内容源：`notes/ch06.md`；本报告：`notes/ch06-report.md`。
- 正文 **21节、3张表、2个说明性代码块、5幅图**。来源区前去围栏代码、保留标题／表格／图注／替代文本，汉字粗计 **17,334**；略超初估13—17千，增加的是确认层次、quorum假设与反例、五写购物车过程，不以产品清单扩长。
- 五组`diagrams/sources/ch06-{sync-ack,local-first,quorum-intersection,quorum-inflight,causal-versions}.excalidraw`及同stem官方SVG，合计 **110个原生元素**；对应元素数18、25、17、30、20。
- 同stem `.skeleton.json` 保留初始简写。制作／同步／验证脚本：`ch06-diagrams.py`、`ch06-render.py`、`ch06-check.py`、`ch06-verify.mjs`，均位于本章图源目录。复用共享`export-excalidraw.mjs`和`excalidraw-browser.js`，未改共享工具。
- 修改正文后运行 `python3 books/designing-data-intensive-applications-2nd/diagrams/sources/ch06-render.py`；改图后从现有`.excalidraw`调用共享导出器。HTML使用现有静态阅读组件，无新增网页运行依赖、无站点编译步骤。

## 原书覆盖与展开程度

表中正文小节全部覆盖，包括第二版的对象存储／零盘架构、同步引擎／本地优先、无主与单主性能比较、多地域quorum。主线正常与故障路径均有明确操作顺序：

1. 单主：按序传播→同步／异步确认→快照100与日志101—160接续→从节点追赶／日志缺口→旧主105、候选104／98→选主与旧主隔离。
2. 复制延迟：头像A→B、位点41／42、跨设备上下文；固定副本失效后的单调读；问题Q与回答R跨分片的因果前缀。
3. 多主：地域内确认→断网独立写→恢复合并；拓扑转发与insert/update超车；设备本地保存→后台同步→合并刷新。
4. 冲突：wiki A→B／C；LWW时钟110／105；购物车删Book／DVD后并集复活；ice插n／!的OT索引转换与稳定字符ID；会议室跨记录业务冲突。
5. 无主：三副本写二→旧副本恢复→读修复、提示移交、反熵；quorum交集推导→写尚未完成时AB读1、BC读0；成员变化／宽松quorum／异地本地quorum反例。
6. 因果：五次购物车写完整区分传入上下文与新分配版本；因果DAG保留跨客户端依赖；两副本向量偏序、合并与后续并发分支，明确不是生产版本向量实现。

取舍：原书产品枚举与研究历史仅保留帮助机制判断的例子；游戏netcode一段范围说明；未展开dotted version vector内部协议、CRDT完整实现及第10章共识证明。章末参考文献完整读取其列表，但没有声称65篇论文均已通读。

## 旧稿保留、修正与未沿用内容

保留并按原文重构：同步／异步正常过程、快照与日志衔接、GitHub事故机制（明确按原书转述）、三种读取保证、三种拓扑、设备副本、LWW时钟反例、购物车删除复活、ice→nice!、五步购物车版本号、quorum容错数。

| 对象／原表述 | 问题与依据 | 本次处理 |
| --- | --- | --- |
| 原书印刷207及旧稿：MySQL默认遇非确定性才转行模式 | 原PDF确有此句；MySQL8.4官方文档默认ROW，自动切换属于MIXED | §06就地记录原句→依据→修正，标记为笔记核查而非出版社勘误 |
| 旧稿：同步确认收到→从库立即可读、故障不丢 | PostgreSQL17区分remote_write、on、remote_apply | §03分开收到、可靠保存、查询可见，§07检查应用进度 |
| 旧稿：GTID保证failover不丢已提交事务 | GTID是事务身份／去重信息，不重建未复制数据 | §05明确身份、传播及安全选主的不同职责 |
| 旧稿：r+w>n保证每次最新；QUORUM等于强一致 | 集合交集成立但不足以定义读写协议；原文233—234列出边界 | §15给有前提推导，§16给未完成写与部分失败的逐步反例 |
| 旧稿：读写永远发给全部n副本 | 原书用normally说明常见发送方式 | §15改为本文常见模型，r/w是响应阈值，具体实现可不同 |
| 旧稿：同步多主不存在／实践都指异步 | 原文是出于断连可写目标不再展开同步多主 | §09改成章节范围说明 |
| 旧稿：WAL一概不能跨版本，逻辑复制自动零停机 | 兼容取决于版本与协议；逻辑解耦提供条件，不自动完成切流 | §06限定物理格式与具体兼容范围，保留模式／切流责任 |
| 旧稿：LWW随机选；CRDT相同ID集合必然收敛 | LWW实现必须确定性；唯一ID不能替代完整合并协议 | §11说明语义上任意而非实现随机，§12补足排序／删除／重复等规则 |
| 旧稿：无主灰故障天然不存在，sloppy保证分区时写不失败 | 仍有足够副本、共享资源和临时保存条件 | §17说明最快r响应的前提、修复负载及临时副本集合反例 |
| 旧稿：日志位点差就是可精确测量的时间延迟 | 位点可能按字节／记录计量，不等于秒；接收、刷盘、应用不同 | §17明确口径 |
| 旧稿简化购物车图漏跨客户端因果边 | 原图6-15／6-16明确v1→v4、v2→v5 | 图6-5补全直接依赖，脚本检查传递闭包与并发关系 |
| 旧稿事件溯源指向ch05、fencing指向第10章 | 第二版原文分别定位第3章、第9章 | 正文改为实际章序；未来章节只写文字 |

未沿用：大段生产产品速查、Kafka／ES／Redis配置扩展、所谓生产铁律、面试题，以及零盘“秒级伸缩到0”“延迟必高一个数量级”等无本次核查依据的判断。它们不作为本章写作依据，外部旧稿保持只读。

## 实际资料核查

- 固定PDF实际用PyMuPDF回看印刷200、207、227、232、240、242，对应PDF224、231、251、256、264、266；实际查看六张页面图。核对图6-2、6-11、6-13、6-15、6-16及MySQL原句。
- 2026-11-07访问PostgreSQL17 `runtime-config-wal.html#GUC-SYNCHRONOUS-COMMIT`，核对确认语义；访问MySQL8.4 `replication-formats.html`与`replication-gtids-concepts.html`，核对ROW／MIXED及GTID身份／去重。正文来源区均有链接。
- 最初尝试MySQL的`binary-logging-formats.html`返回404，改用实际存在的`replication-formats.html`取得官方正文；没有把失败请求算成核查来源。
- 其他具体系统架构与历史案例按原书转述；补充的两节点只增计数器、版本向量数值例子和quorum交错显式标为笔记推演。

## 实际验证结果

### 内容、资源与场景

- `ch06-check.py`通过：四种n/w/r配置的有限集合交集、n=3/w=1/r=1不相交例、成员切换、宽松quorum及两地本地quorum反例；无阻塞读修复时AB读1→BC读0；五次购物车候选集依次`[1]、[1,2]、[2,3]、[3,4]、[4,5]`；因果DAG传递性／并发；版本向量偏序与合并；计数器重复合并不重复加；集合删除复活；OT错误索引3与正确索引4。
- 标题、导读、21节完整正文、表格、代码、图注、来源与HTML规范化全文匹配；39个去重本地引用检查，除同轮尚未生成的`ch08.html`之外均存在且锚点有效；无重复ID，图像有alt，网页不引用notes／originals／sources或本地PDF。
- 5组场景JSON／SVG XML、110个原生元素与全部文字对应；每幅图通过共享工具的官方restore＋真实编辑器API重载、修改文字及恢复验证，`editable:true`。不是手写SVG冒充Excalidraw。
- 首次静态检查器依赖未安装的bs4而未运行成功；随后改用标准库HTMLParser，无需额外安装，完整检查通过。此为验证工具问题，不算正文失败。

### 浏览器与视觉

- 本机Google Chrome实际执行1440／375px × 浅／深色，共4组页面；首次跟随系统、手动选择及刷新保存通过；正文16px、行高31.2px（1.95），21节、5图加载，无整页横向溢出。
- 手机目录展开／锚点跳转、来源折叠、手机图示局部滚动通过；图像可打开独立大图。捕获JS／HTTP错误为0。
- 5幅独立SVG各浅／深色，共10组检查，文字在图界内、主题变量正确；其中同步图另检验独立SVG读取手动主题保存。
- 实际查看五幅代表导出、桌面浅色开头、手机深色开头及手机深色quorum图。因果图初版“交叉线没有连接点”压在线上，已把文字移到图下方；从保存的`.excalidraw`重新官方导出并再次验证编辑器重载。只对该图补做浅／深两组检查并查看修正截图，没有重跑无关页面。
- 结果与截图在`/private/var/folders/5k/y6qh6sfd2g30js0v0qrv4mfr0000gn/T/opencode/ddia2-tools/`：`ch06-static-results.json`、`ch06-browser-results.json`、`ch06-browser-results-causal-versions.json`、`ch06-reader-*`、`ch06-quorum-*`、`ch06-diagram-*`及原页截图。

范围：上述是静态页面、原生图源和教学小数据验证；没有启动数据库，没有测试产品读写级别、真实故障切换、崩溃持久性、网络分区或吞吐延迟；网站无编译命令，不报告虚构构建通过，未部署。

## 遗留与跨章衔接

- **同轮依赖：** 上页`ch05.html`、下页`ch07.html`已生成且检查通过。正文引用`ch08.html`是用户允许的同轮互链，在本负责人最后静态检查时尚未生成，请主Agent待第8章返回后复核；不因此删除已规划的事务衔接。
- 前章链接：第3章事件溯源、第4章`wal-recovery`、第5章编码与演化；后续第9章网络／时钟／fencing，第10章线性一致性／共识，第12章CDC，第13章业务修复，只作文字提示，不创建未来章失效链接。
- 主Agent可重点复审：同步确认与可读的区别、异步切换105／104／98例、原书MySQL默认模式纠错、quorum反例的“读不等待写回修复”前提、版本向量只作简化分支演示的边界。
- 无其他已知内容／绘图阻塞；共享导航、概览、进度与发布整合由主Agent负责。**本负责人本章完成，返回后停止编辑，等待四位负责人全部返回后主Agent接管。**

## 主Agent整合完成（2026-11-07）

四位负责人全部返回并停止编辑后，主Agent已通读本章及来源，回看复制／quorum原文，以PostgreSQL17和MySQL8.4官方文档复核确认语义及默认ROW纠错，并复跑`ch06-check.py`通过。第8章引用与5→6→7已接通；概览、书架为8／14。接入后10页链接／锚点、本轮73节及来源双端全文匹配、19组图源／导出检查通过；Chrome52组及正反翻页通过，本章5图已目检。上文作者时点的接入待办已关闭，其原始验证范围保留。全轮证据见本书README和根CONTINUE；无新增阻塞或后台写作任务。
