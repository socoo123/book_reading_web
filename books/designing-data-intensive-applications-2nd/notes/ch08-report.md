# 第8章交付报告

状态：**已完成并通过本章最小验收，可交主Agent整合。** 负责人D仅写第8章；未递归委派或启动其他Agent。2026-11-07已完整读取原章提取文本2823行（印刷277—344／PDF301—368，正文至337）和只读旧稿1852行；固定版本为Martin Kleppmann、Chris Riccomini，O’Reilly February 2026英文第二版。

## 写前原书小节覆盖表（现已逐项落实）

| 原书小节（印刷页） | 拟定笔记节／锚点 | 必须保留的机制、案例与边界 |
| --- | --- | --- |
| 开篇；What Exactly Is a Transaction?（277—279） | 01 transaction-contract | 故障／并发；事务的编程模型；System R、NoSQL与可扩展事务的历史语境 |
| The Meaning of ACID；Atomicity；Consistency；Isolation（279—282） | 02 acid | 可中止性；不变量；声明约束／应用责任；可串行化与实时顺序分开 |
| Durability；Replication and Durability（282—284） | 03 durability | WAL／同步／复制／备份职责与相关故障 |
| Single-Object and Multi-Object Operations；Single-object writes；The need for multi-object transactions（284—287） | 04 transaction-boundary | 邮件与未读数、文档、引用、索引；批API不等于事务 |
| Handling errors and aborts（287—288） | 05 abort-retry | 全事务重试、未知提交、过载、永久错误、外部副作用、持久输入 |
| Weak Isolation Levels；Read Committed；No dirty reads；No dirty writes；Implementing read-committed（288—293） | 06 read-committed | 脏读／脏写明确时序、行锁与旧版本、无脏写不防丢失更新 |
| Snapshot Isolation and Repeatable Read（293—295） | 07 read-skew | 一次原子转账、两次读取夹在提交前后；备份与长读 |
| Multiversion concurrency control；Visibility rules（295—297） | 08 mvcc | 版本、活跃事务集、插删可见性、自身写、快照取点 |
| Indexes and snapshot isolation；Snapshot isolation, repeatable read, and naming confusion（298—299） | 09 isolation-names | 索引版本可见性、写时复制、GC；PG17／MySQL8.4限定版本比较 |
| Preventing Lost Updates；Atomic write operations；Explicit locking（299—301） | 10 lost-update | 42→43反例、表达式更新、锁后读取、死锁、转账检查 |
| Automatically detecting lost updates；Conditional writes；Conflict resolution and replication（301—303） | 11 conditional-write | SI同记录冲突、版本CAS、影响行数、跨请求、多主合并边界 |
| Write Skew and Phantoms；Characterizing write skew；More examples（303—306） | 12 write-skew | 医生两人同时离岗；锁住全部依赖且重检；棋子／用户名／流水余额 |
| Phantoms causing write skew；Materializing conflicts（307—308） | 13 phantoms | 空集检查、重叠区间、插入时序、范围锁与物化冲突 |
| Serializability；Actual Serial Execution；Stored procedures；Pros and cons；Sharding；Summary（308—313） | 14 serial-execution | 串行等价、短事务、交互往返、确定性、跨分片协调 |
| Two-Phase Locking；Implementation；Performance（313—315） | 15 two-phase-locking | S／X、增长／收缩、强严格变体、等待环和尾延迟；2PL≠2PC |
| Predicate locks；Index-range locks（316—317） | 16 predicate-locks | 未来行、扩大锁集合的安全近似、索引／表粒度 |
| Serializable Snapshot Isolation；Pessimistic versus optimistic；Outdated premise；Stale MVCC reads；Writes affecting prior reads；Performance（317—322） | 17 ssi | 两类读写依赖、医生依赖环、中止／重跑；SSI非无锁／只读可能失败 |
| Distributed Transactions（323—324） | 18 atomic-commit | 单机提交日志与跨节点部分提交、原子性／隔离分工 |
| Two-Phase Commit；A system of promises（324—327） | 19 two-phase-commit | 全局ID、prepare持久承诺、协调者持久决定、重复消息 |
| Coordinator failure；Three-phase commit（327—328） | 20 in-doubt | 决定丢失与未知、两种历史、故障后恢复、3PC前提 |
| Distributed Transactions Across Different Systems；Exactly-once message processing；XA transactions；Holding locks；Recovering；Problems with XA（328—333） | 21 xa | 异构资源、XA接口、日志与恢复所有权、锁保留、启发式决定、全局隔离缺口 |
| Database-Internal Distributed Transactions（333） | 22 internal-transactions | 同构协议、复制协调者／分片、共识与提交分工 |
| Exactly-Once Message Processing Revisited（334—335） | 23 idempotent-consumer | 同事务消息ID＋结果，唯一约束，commit后ack，去重保留和外部副作用 |
| Summary；Table8-1（335—337） | 24 conclusion | 异常矩阵、三类可串行化、两类分布式事务与第9章衔接 |

## 已落实的纠错与限定

- 第7节：旧稿将图8-6误读为扣款、入账分开提交 → 已回看固定PDF印刷294页，只有一个Commit → 恢复同事务转账、两次读取跨提交点得到900的反例。
- 第10节：旧稿“Flexcoin式”算例A=50、B=50总额仍100 → 不能推出凭空多50 → 只保留丢失更新机制，不沿用真实代码归属及错误算术结论。
- 第9节：旧稿PG的RU可脏读、MySQL8.0+默认RC → PG17和MySQL8.4官方文档相反 → 分别修正为PG RU映射RC、InnoDB默认RR，保留配置可改的前提。
- 第8节：快照取点一概等于BEGIN、只按ID大小判断可见性 → PG17与原书活跃事务规则更细 → 补自身写、活跃事务集、首次非事务控制语句取点，说明插删标记为教学模型。
- 第12—13节：旧稿锁住医生后直接更新、空集FOR UPDATE一概无效 → 锁不替代人数规则，InnoDB范围锁与PG元组锁不同 → 补锁后重检与版本／语句／索引前提。
- 第17节：原书320页的“旧写已提交就中止”教学简化；旧稿“只读永不中止”“全程无锁” → 原书322页、PG17和SSI论文的依赖与锁规则 → 改为危险依赖结构、只读可参与异常、原有写锁仍存在。
- 第21节：原书XA“does not work with SSI” → Ports／Grittner §7.1明确实现本地SSI与2PC组合 → 限定为XA接口本身不提供跨异构资源全局SSI；准备前检查、准备后不可任意中止。
- 第5、10—11节：只重发旧值、未检查更新行数的扣款／库存／版本操作 → 旧业务决定可能失效 → 补全事务重读重算、零行结果处理、多对象同事务。
- 第19—20节：旧稿“投YES后持久化”、协调者异常即rollback → 原书承诺体系要求相反顺序 → prepare持久化先于YES，持久决定不能因客户端异常改写；日志损坏不等于没有COMMIT。
- 第4节：原书把断开连接概括为中止 → 与提交响应丢失及准备事务情形不符 → 限定为仍未提交的普通会话事务。
- 第23节：旧稿重复分支直接return跳过ack → 业务幂等但可能不断重投 → 两分支均在提交成功后确认；ID、业务写与结果同事务。
- 第23节：原书334页“确认后可删ID” → RabbitMQ确认异步、SQS删除后仍可能重投，另有生产者重复和手动重放 → 清理以不再遇到同ID的明确契约为前提，不以ack调用返回为充分条件。
- 未沿用无版本产品大全、固定运维阈值、Redlock通用解法、大片Saga扩展、未核实VoltDB API；保留原书机制，Outbox只作有AWS官方出处的短补充。

## 产出与统计

以下路径均相对于`books/designing-data-intensive-applications-2nd/`：

- `notes/ch08.md`：24节正文，来源前去代码汉字数**21,789**（含标题、表格、图注及替代文本），约2.18万；末尾来源折叠、原书对应表与上一章／概览导航。
- `chapters/ch08.html`：由Markdown生成的静态阅读页；24节正文与双端目录、7幅图、来源折叠。上一章为`ch07.html`，下一入口为`../index.html`，明确第9章待后续轮制作。
- `notes/ch08-report.md`：本报告，保留写前覆盖表、依据、纠错与验收记录。
- `diagrams/sources/ch08-diagrams.mjs`：本章图形生成入口，调用共享官方Excalidraw导出器。
- `diagrams/sources/ch08-render.py`：本章Markdown→HTML生成器，只读取第4章页面外壳，不修改共享页面或资产。
- `diagrams/sources/ch08-check.py`：确定性教学模型与静态同步检查。
- `diagrams/sources/ch08-verify.mjs`：本章浏览器／资源验收。
- 下列每个stem均含`diagrams/sources/<stem>.skeleton.json`、`diagrams/sources/<stem>.excalidraw`、`diagrams/exports/<stem>.svg`三份，合计21份图形文件：

| 图 | stem | 聚焦问题 | 原生元素数 |
| --- | --- | --- | --- |
| 8-1 | ch08-read-skew | 一次提交、跨时点读取 | 25 |
| 8-2 | ch08-mvcc | 快照筛选旧／新版本 | 18 |
| 8-3 | ch08-write-skew | 写不同的行破坏共同不变量 | 19 |
| 8-4 | ch08-ssi-cycle | rw反依赖环不可能排序 | 13 |
| 8-5 | ch08-2pc-normal | 持久准备与持久决定顺序 | 35 |
| 8-6 | ch08-2pc-recovery | 协调者恢复、原决定重发 | 29 |
| 8-7 | ch08-idempotent | 同事务去重，提交后确认 | 22 |

合计28份本章交付文件。7份Excalidraw场景含161个原生元素，没有内嵌图片或以SVG作为整张场景；均经共享官方API导出，并在官方编辑器API重载后完成改字、读回、恢复验证（`editable:true`）。共享导出器与桥接脚本只读。

## 原书与外部依据

- 原章已完整读取，固定PDF实际回看印刷282、285、290、292、294、296、300、304、311、320、321、323、325、326、327、328、332、334、335页，包括关键原图、表8-1与容易误读的连接／提交／恢复段落。
- 外部核查日期为2026-11-07：PostgreSQL 17隔离、串行化失败处理、PREPARE TRANSACTION；MySQL 8.4隔离；Ports／Grittner 2012 SSI论文§3、§4、§7.1；RabbitMQ 4.1确认；SQS标准队列至少一次投递；AWS Transactional Outbox。完整URL与对应段落已放入正文来源区。
- 旧稿只作对照与查漏；笔记构造的数据、假设、产品特定解释和Outbox均与原书观点区分。没有新增未经读取的引文、页码或产品性能数字。

## 实际验证

### 已通过：构建、模型、静态同步、图源可编辑

执行入口：

```sh
node books/designing-data-intensive-applications-2nd/diagrams/sources/ch08-diagrams.mjs
python3 books/designing-data-intensive-applications-2nd/diagrams/sources/ch08-render.py
python3 books/designing-data-intensive-applications-2nd/diagrams/sources/ch08-check.py
node books/designing-data-intensive-applications-2nd/diagrams/sources/ch08-verify.mjs
```

- 官方导出7图；保存的`.excalidraw`逐一通过官方恢复与编辑器改字验证。
- 静态生成24节、7幅图；逐节比较Markdown与HTML的标题及正文文本，双端目录一致；来源文本、图注、页尾导航、7图引用同步；不存在指向未制作第9—13章的链接。
- 核对全部原生文字都出现在对应SVG文本中，场景不含image元素。
- 确定性模型通过：读偏斜900／稳定快照1000；快照排除较早开始但仍活跃事务；丢失更新43／原子自增44；单库存条件更新唯一获胜者；版本CAS；已知中止后重读0而拒绝；医生写偏斜与两个合法串行顺序；区间重叠与相邻不重叠；单依赖可排序、两节点与只读三节点环不可排序；2PC持久决定恢复、重复决定、NO及YES丢失；幂等提交前后崩溃、未知提交重试、重复分支确认，以及拆开ID／业务写的反例。
- **没有启动真实数据库或消息代理。** 以上是教学模型、静态一致性和官方语义核查，不称数据库／XA／消息系统集成验证。

### 浏览器与截图

- 本机Chrome／Playwright已通过1440×960、375×960两尺寸各浅／深色，共4组。正文16px，行高31.2px；页面总滚动宽度分别为1440、375，无整页横向溢出。
- 检查50个去重后的资源／链接引用：本地文件及锚点存在，没有让公开阅读依赖notes、originals或sources目录；没有重复ID、页面脚本错误或失败资源响应，7图均加载成功。
- 首次跟随系统外观、手动切换后刷新保留、手机目录展开收起、来源折叠均通过。表格、代码和宽图沿用局部滚动；手机可横向查看大图，另有独立SVG打开入口。
- 7张独立SVG均无越出画布的文字，并验证浅系统偏好下能读取手动保存的深色选择。已逐张目检7张浅色图，并目检深色2PC图及桌面浅深色、手机浅色正文／深色图文截图，未发现文字遮挡或箭头与说明冲突。
- 初次浏览器脚本把`data-theme="system"`误判为未跟随系统，已仅修正本章校验为同时检查`system`偏好与实际CSS `color-scheme`，随后完整通过；共享主题代码没有改动。
- 截图与机器记录位于临时工具目录`/private/var/folders/5k/y6qh6sfd2g30js0v0qrv4mfr0000gn/T/opencode/ddia2-tools/`，文件前缀`ch08-reader-*`、`ch08-2pc-reader-*`、`ch08-diagram-*`及`ch08-browser-results.json`，不作为网站运行依赖。

## 交接边界

本章以外的正文、共享样式／脚本、共享导出工具、原书及旧稿均未改动。第9章待后续轮，不添加不存在的章节链接。本章交付后由主Agent处理站点共享目录与跨章节整合；负责人D停止编辑。

本章无未解决阻塞；SQL与消息例子未做真实系统集成运行，这一验证边界已在正文与本报告明确说明。未提交、推送或部署。

## 主Agent整合完成（2026-11-07）

四位负责人全部返回并停止编辑后，主Agent已通读本章及来源，回看隔离、SSI、2PC与幂等原页，以SSI论文§7.1、PostgreSQL17及SQS官方资料复核关键边界，并复跑`ch08-check.py`通过。第7→8章已接通，第8章暂回概览；概览、书架为8／14。接入后10页链接／锚点、本轮73节及来源双端全文匹配、19组图源／导出检查通过；Chrome52组及正反翻页通过，本章7图与代表性桌面／手机截图已目检。共享接入已完成，作者原始验证范围保留；全轮证据见本书README和根CONTINUE，无新增阻塞或后台写作任务。
