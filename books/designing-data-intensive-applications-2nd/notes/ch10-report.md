# 第10章制作报告（第3轮 Agent B）

状态：**已完成并通过本章最小验收，可交主Agent整合。** 2026-11-07。负责人B只写本章独占文件，未递归委派；交付后停止编辑。

## 写前覆盖表 · 2026-11-07

已先读根AGENTS／PLAN／CONTINUE、本书README及参考文章／ch08页面；完整通读 `originals/ddia2-ch10.txt` 1—2020行（含参考文献），再完整对照只读旧稿2384行。固定版本：Martin Kleppmann／Chris Riccomini，O’Reilly 2026英文第二版。正文印刷401—443／PDF425—467；章含文献至PDF474。本书目录没有独立CONTINUE，采用根CONTINUE。

| 原书小节／印刷页 | 预定笔记覆盖 | 机制与案例／边界 |
| --- | --- | --- |
| 引言401—402；Linearizability 402—407 | 契约；调用区间与线性化点 | 体育比分；新值已被读到而写尚未返回；CAS与失败读 |
| Linearizability Versus Serializability 407—408 | 线性一致／可串行化／因果 | 单对象与事务；严格可串行化；不把单机等同强隔离 |
| Relying on Linearizability 408—411 | 唯一约束；锁；跨通道 | 用户名竞争；视频存储与消息队列；fencing责任 |
| Implementing Linearizable Systems 411—413 | 复制保证；quorum反例 | n=3,w=3,r=2；同步写回与版本规则；普通寄存器不等于CAS |
| The Cost of Linearizability 413—417 | CAP与延迟 | 双地域分区；CAP的形式可用性；不作产品二分和绝对性能断言 |
| ID Generators 417—420 | 唯一／局部递增／因果／实时排序 | 分片、号段、随机UUID、墙钟ID；发号顺序不同于事务提交顺序 |
| Logical Clocks 420—422 | Lamport／HLC／向量 | 聊天回复；因果单向蕴含；HLC回拨与并发唯一化 |
| Linearizable ID Generators 423—425 | 隐私案例；TSO／TrueTime；排序与决策 | 跨设备权限与照片；持久预留号段；最小号未必已知 |
| Consensus／FLP 425—426；Single-value 427—428 | 模型／四属性／活性 | 非拜占庭、持久状态；FLP不因任意timeout消失 |
| CAS／shared log 429—431 | CAS归约；共享日志与状态机复制 | 决定值可恢复；槽位／缺口；确定性与重试去重 |
| Fetch-and-add 431—432 | 共识数2的准确模型 | 先发布提议再抢号；赢家崩溃；CAS循环不是等待自由证明 |
| Atomic commitment 432—433 | 全员prepare与副本多数派不同 | commit须全体赞成；普通2PC阻塞；共识稳定提交决定 |
| Consensus in Practice 433—437 | 选主／日志／提交／读路径 | epoch、quorum交集和继承规则；Raft/Paxos必要补充；读屏障 |
| Coordination Services 437—440 | 小型控制面；租约／通知／发现 | 三或五投票节点；资源端隔离令牌；缓存与observer边界 |
| Summary 440—443 | 收束与章节衔接 | 从实际不变量选择保证；前09后11 |

## 已落实的取舍

保留旧稿有依据的操作顺序、quorum反例、权限时间戳算例；重写为连贯文章。旧稿Raft／etcd源码、PBFT／HotStuff、库与产品列表、面试题不进入正文；仅取Raft日志新旧比较、当前任期提交规则、ReadIndex与Paxos继承规则作为明确标识的必要书外补充并查原始资料。图示拆分线性化区间、跨通道、因果与实时、日志接管、读屏障等小图，复用已验证官方导出工具。

## 产出与统计

以下路径相对于 `books/designing-data-intensive-applications-2nd/`：

- `notes/ch10.md`：22节长篇笔记。来源折叠前汉字 **17,349**，全文件汉字18,042；计数含标题、表格、图注、替代文本与伪代码注释，不把英文字符计入汉字数。
- `chapters/ch10.html`：与Markdown同步的静态阅读页，沿用ch08页面外壳及共享阅读样式；正文16px／1.95、双端目录、来源折叠、6图；前页 `ch09.html`，后页 `ch11.html`。
- `notes/ch10-report.md`：保留写前覆盖表，并记录实际纠错、证据与验收。
- `diagrams/sources/ch10-diagrams.mjs`：本章原生图形生成入口，复用共享 `export-excalidraw.mjs` 与 `excalidraw-browser.js`。
- `diagrams/sources/ch10-render.py`：Markdown→HTML生成器，只读取ch08外壳。
- `diagrams/sources/ch10-check.py`：有限教学模型、全文同步、链接与图源文字检查。
- `diagrams/sources/ch10-browser.mjs`：本机Chrome／Playwright阅读与图形验收。

每个stem保留 `.skeleton.json`、`.excalidraw` 和导出的 `.svg`，其中前两份在sources、后一份在exports，共18份图形文件：

| 本站图号 | stem | 聚焦问题 | 原生元素数 |
| --- | --- | --- | --- |
| 10-1 | ch10-linearization | 两次读虽都与写并发，仍不能先新后旧 | 37 |
| 10-2 | ch10-cross-channel | 队列通知快于文件复制 | 27 |
| 10-3 | ch10-clock-orders | 已传播因果与未传播的现实先后 | 22 |
| 10-4 | ch10-log-handoff | 多数派交接与已提交历史继承 | 22 |
| 10-5 | ch10-read-barrier | 当前任期依据、读确认、应用进度 | 18 |
| 10-6 | ch10-coordination | 小型控制面与资源端隔离责任 | 30 |

合计 **25份本章交付文件**。6个场景含156个原生元素，未把SVG或位图作为整张场景嵌入。6图均通过官方API导出及编辑器重载、改字读回、恢复验证，返回 `editable:true`。共享工具与既有依赖只读复用，没有安装新依赖。

## 重点核查与就地修正

| 原表述／问题 | 依据与修正 | 正文位置 |
| --- | --- | --- |
| 原书427页先将fetch-and-add与其他原语概括为等价 | 按原书431—432、442页及Herlihy限定：读写寄存器＋FAA的等待自由共识数为2；2指参与进程，不是服务副本或客户端容量 | §15 |
| “先互相发提议”可能被实现成等待对方消息；赢家崩溃后无法宣布 | 先向可访问的共享寄存器发布，再FAA；返回1者可读唯一对方，即使赢家已停止。三人不可能性归于定理，不以一个失败例子代替证明 | §15 |
| CAS递增循环被当作等待自由实现 | 功能正确不保证每个线程有限自身步数内成功；竞争下可反复失败 | §15 |
| 原书433页原子提交与共识的“等价”缺少模型／进度条件 | 事务全员赞成与复制多数派分开；普通2PC可阻塞；原书超时构造允许全yes但延迟时中止；反向归约还需隔离及终止条件 | §17 |
| 原书426页“有timeout就能解共识” | FLP与部分同步原论文：任意timeout不排除无界错误怀疑；活性需部分同步、合适故障检测或随机化等条件 | §14 |
| 原书436、442页“每次线性一致读都经quorum” | 限定为所讲无租约路径；Raft§8和官方库允许租约优化，但须额外时间假设 | §20 |
| 旧稿ReadIndex发出心跳即返回，或只检查日志进度 | 先当前任期提交依据，再记录位置并等待匹配确认，最后等应用位置追上；从节点也可取得安全位置后服务读 | §20、图10-5 |
| 旧稿“日志提交当且仅当复制到多数派” | Raft§5.4／图8：直接数副本提交需当前任期条目；旧任期条目通过提交当前任期前缀继承 | §18—19 |
| 旧稿Paxos“看见任意旧值就继承” | Paxos Made Simple§2.2：从当前prepare法定人数响应中选择最高已接受ballot的值 | §19 |
| 旧稿“单机天然严格可串行化” | 单副本不消除并发事务及弱隔离；完整事务需串行解释和实时先后 | §03 |
| 旧稿“绝不允许两节点同时认为自己抢到租约” | 旧进程可保留过期认识；约束服务端有效授予及资源端接受效果，需fencing | §04、§21 |
| 旧稿同步读修复写成“全部确认” | 原子寄存器构造等待所需quorum，未必全体；版本分配、写回和恢复规则不可省略 | §07 |
| 旧稿16／17奇偶颠倒；把发号顺序等同提交顺序 | 修正为16偶／17奇；ID10先分配但ID11事务先提交仍可能发生 | §09 |
| 旧稿HLC可精确日期查询、二元组自动唯一 | HLC原论文图5：回拨时保逻辑单调，日期精度仍依赖物理钟；跨节点唯一需平局处理，补接收四分支 | §11 |
| 隐私示例数值与原图混用 | 实际回看原图10-10：私密15、照片12、快照13；旧稿100／98／99属于另编算例，不称原图数值 | §12、图10-3 |
| 旧稿把ZK Watch都说成一次性、混淆cversion与zxid | ZK3.9.4官方文档：3.6起有持久／递归Watch；cversion是节点子项计数，zxid是事务顺序 | §21 |

正文还区分了：单键CAS与先查后写、严格可串行化与API的serializable旧读选项、CAP形式可用性与运维可用率、共享日志与外部恰好一次效果、领导权证据与迟到确认、协调服务通知与缓存权限。Raft／Paxos、HLC接收分支及产品细节均标明书外补充或版本边界，没有冒称出版社已确认勘误。

## 实际阅读及外部依据

- 原章提取文本2020行（含文献）、旧稿2384行均已完整读取；旧稿只作对照与查漏，原书与旧稿保持只读。
- 实际回看固定PDF图10-1—10-10全部：印刷403、404、405、406、410、413、414、418、421、423页；另外回看426、431、432、435、436、442页的FLP、FAA、原子提交、选主与读取条件。原图10-10的数值已依图更正。
- 外部论文核读：Herlihy *Wait-Free Synchronization*（定义与共识数）；Raft扩展论文§5.4／图8／§8；*Paxos Made Simple* §2.2；FLP的模型与不终止结论；Dwork等部分同步定义；HLC技术报告§3／图5；Gray／Lamport *Consensus on Transaction Commit* 的提交模型、2PC与Paxos Commit概要。
- 产品文档核查日期2026-11-07：etcd v3.6 API guarantees、etcd-io/raft README、ZooKeeper 3.9.4 Programmer’s Guide。完整URL和各自核查范围在笔记末尾来源折叠内。
- 提交论文下载先遇到Lamport网站旧路径404，后通过Microsoft官方作者页面取得正确PDF；没有资料阻塞。Attiya—Welch延迟下界按原书转述并保留模型限定，没有声称重新验证完整证明。

## 实际验收

执行入口：

```sh
node books/designing-data-intensive-applications-2nd/diagrams/sources/ch10-diagrams.mjs
python3 books/designing-data-intensive-applications-2nd/diagrams/sources/ch10-render.py
python3 books/designing-data-intensive-applications-2nd/diagrams/sources/ch10-check.py
node books/designing-data-intensive-applications-2nd/diagrams/sources/ch10-browser.mjs
```

### 构建、内容与教学模型：通过

- 静态生成22节／6图；比较引言、逐节标题与全文、来源说明的Markdown／HTML文本一致。末次补清ReadIndex取点顺序及图注方位后，已重新生成并通过同步检查。
- 43个去重本地链接／资源引用及其锚点存在；无重复HTML ID；页面没有依赖notes、originals或sources目录。当前ch09、ch11都已存在，前后章链接可解析。
- 所有原生图源文本与SVG逐行文字多重集相同，6场景没有image元素。初次检查因官方导出将绑定文字排到容器旁、与scene数组顺序不同而失败，已将检查修正为不依赖绘制排序的逐行多重集比较，未放宽文字完整性要求。
- 小型历史检查：拒绝并发写期间的先新后旧，接受先旧后新／先新后新；拒绝两个对同一初值的CAS同时成功。
- Quorum算例：`n=3,w=3,r=2`仍得到1后0；最大版本同步写回多数派后，第二次读得到1。
- Lamport回信时间戳2；HLC本地前进、回拨及接收四分支；隐私15／照片12／快照13可见性均复算通过。
- 两进程发布／取号的6种合法交错均共同决定同一已发布提议；赢家在取号后停止，幸存者仍可读到该提议。
- 原子提交：全yes才提议commit，见abort提议abort；缺票先等待，超时可提议abort；延迟的全yes情形可出现两种提议，但须服从同一共识结果。
- Raft教学比较验证最后term优先于index、旧任期条目多数派不足以直接提交；Paxos按最高已接受ballot选X。读取模型中日志到50、应用到48仍读0，应用49—50后才读1。
- 上述是有限教学算例及原始资料核查，不是协议完整实现／形式证明，也未启动真实etcd、ZooKeeper或分布式集群。

### 浏览器与目检：通过

- 本机Google Chrome／已有Playwright，1440×960、375×960各浅／深色，共4组；正文16px、行高31.2px；整页滚动宽度分别1440与375，无整页横向溢出。
- 六图均成功加载；无页面脚本异常或失败资源响应。表格、代码、宽图均使用局部滚动，手机图示横向滚动实测有效。
- 首次跟随系统浅深色、手动选择后刷新保存、手机目录展开／锚点跳转／收起、来源折叠、图示点击独立打开均通过。
- 六份独立SVG无画布外文字；在系统浅色下也能读取保存的深色选择。已目检六图的浅深色联系表、桌面浅色正文／深色读屏障、手机深色正文／浅色读屏障，没有发现文字重叠或箭头遮挡。
- 临时证据目录：`/private/var/folders/5k/y6qh6sfd2g30js0v0qrv4mfr0000gn/T/opencode/ddia2-tools/`。机器结果为 `ch10-check-results.json`、`ch10-browser-results.json`；截图前缀为 `ch10-reader-*`、`ch10-barrier-reader-*`、`ch10-diagram-*`、`ch10-contact-*`。论文与原书回看资料在该目录下的 `ch10-review/`。它们不属于网站运行依赖。

## 交接

本章已完成，无未解决资料缺口或验收阻塞。主Agent可接入书架／书籍概览、更新共享进度并统一跨章导航。本负责人已停止编辑；共享文件、其他章节、旧稿及原书未由本负责人改动，未提交、推送或部署。

## 主Agent主审与接入完成（2026-11-07）

四位负责人全部返回、停止编辑后，主Agent通读本章正文、来源及报告，复核线性化区间、quorum反例、时钟顺序、共识与原子提交、任期继承及读取屏障。对照Herlihy定理3／4、Raft§5.4.2／§8及etcd3.6 API保证，回看原书426／431／432／433／436页文字及432／435／436／442页联系表；查看六图浅深色联系表。未发现需重写的核心缺口。

前后章与概览已接入，主Agent复跑`ch10-check.py`通过；22节／引言／来源同步、6组图源／SVG与有限教学算例通过。作者脚本17,349汉字包含21个代码注释汉字，按全书来源区前去围栏代码的统一口径为17,328；原作者执行结果保留。全轮14页960项引用及Chrome60组验证通过，详见本书README与`round3-*.json`；未运行产品集群或完整协议证明。本章完成待用户验收。
