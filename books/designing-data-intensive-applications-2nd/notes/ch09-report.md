# 第9章覆盖、核查与验证报告

## 写作前覆盖表（2026-11-07）

本轮Agent A独占第9章；不递归委派。已通读`originals/ddia2-ch09.txt`全部2324行（含参考文献），再完整对照只读旧稿全部937行。固定版本为Kleppmann／Riccomini，2026英文第二版；正文印刷345—389，PDF369—413；章含参考文献至PDF424。已读项目AGENTS、PLAN、本书README、根CONTINUE（本书目录无CONTINUE），并参考第8章文章／页面及PLAN指定的三本参考稿。

| 原书小节 | 印刷页 | 计划笔记覆盖／关键推理 |
| --- | --- | --- |
| Faults and Partial Failures | 346—347 | 部分失败、观察歧义、滚动升级收益；不把单机绝对化 |
| Unreliable Networks；The Limitations of TCP | 347—349 | 六种无响应路径；OS ACK、应用确认、重连重复；图9-1 |
| Network Faults in Practice；Fault Detection | 350—352 | 非对称／部分网络分区、反馈局限、怀疑与判定 |
| Timeouts and Unbounded Delays；queueing；TCP/UDP | 352—355 | 2d+r前提、排队四处、误判级联、自适应；图9-2 |
| Synchronous Versus Asynchronous Networks | 355—358 | 电路预留、突发流量、资源利用率取舍、QoS边界 |
| Monotonic Versus Time-of-Day Clocks | 358—360 | 时间点／间隔、不可跨机比单调钟、Linux休眠差别 |
| Clock Synchronization and Accuracy | 360—362 | 200ppm复算、NTP误差、闰秒、监控；限定历史数据 |
| Relying on Synchronized Clocks | 362—366 | LWW因果反例42.004/42.003、误差区间、TrueTime提交等待；图9-3 |
| Process Pauses；real-time；GC | 366—371 | 校验与操作间暂停、延迟写、全栈实时成本、现代GC边界 |
| The Majority Rules | 372—373 | 自认存活与协议权力、多数交集还需投票约束 |
| Distributed Locks and Leases；fencing | 373—376 | 原HBase案例、暂停／在途请求、33/34隔离令牌、原子资源检查、交接屏障；图9-4—9-6 |
| Fencing with multiple replicas | 376—377 | 代次优先排序、quorum读取、少数旧写不等于全局胜出；图9-7 |
| Byzantine Faults；weak forms of lying | 377—380 | 非恶意任意错误、BFT成本与相关故障、实用校验 |
| System Model and Reality | 380—384 | 三类时序、崩溃恢复／灰色故障、安全性／活性、稳定存储假设 |
| Formal Methods and Randomized Testing | 384—388 | 证明／有限模型／故障注入／DST三层、可重放非穷尽、确定性复用 |
| Summary | 388—389 | 假设—性质—证据闭环，衔接第10章 |

计划保留原书网络案例、LWW数字、HBase锁失效、33/34令牌、复制隔离和FoundationDB／TigerBeetle测试案例。笔记算例单独标注；不带入旧稿产品速查与面试问答。重点修正旧稿`<=`拒绝同租约后续写且检查／写非原子的伪代码、缺少新持有者首次资源写屏障、令牌单调条件误写成完成先后、多数交集自动安全、Redlock论战过度归纳、BFT排除软件bug等。

## 完成记录

**已完成，交付日期：2026-11-07。** 第9章正文、同步静态页、六幅原生图示与本报告均已落盘。以下路径除特别说明外，相对于本书目录 `books/designing-data-intensive-applications-2nd/`。

### 1. 交付文件与统计

| 产出 | 文件／数量 | 说明 |
| --- | --- | --- |
| 中文笔记 | [notes/ch09.md](ch09.md) | 21节；正文区15,876个汉字，来源折叠区和围栏代码不计，标题、图注及替代文字计入 |
| 静态阅读页 | [chapters/ch09.html](../chapters/ch09.html) | 导言、21节与来源区全文同步；桌面／手机目录、来源折叠、上一章／下一章导航 |
| 可编辑图示 | `diagrams/sources/ch09-*.excalidraw`，6份 | 原生文本、矩形、箭头／线元素，共106个元素 |
| 图示生成输入 | 同名 `.skeleton.json`，6份 | 保留初始场景输入；后续编辑以原生 `.excalidraw` 为准 |
| 网页图示 | `diagrams/exports/ch09-*.svg`，6份 | 官方导出；浅深色适配、替代文本、图注及独立大图入口 |
| 章节工具 | `diagrams/sources/ch09-render.py`、`ch09-diagrams.mjs`、`ch09-check.py`、`ch09-verify.mjs` | 分别用于静态页生成、初始图示生成、机制／同步／资源检查、浏览器检查 |

正文包含6幅图、1张模型对比表；来源区另有1张对应表，页面合计2张表；3个代码／时序说明块。统一使用“隔离令牌”，首次出现保留 fencing token。原书观点、笔记假设和书外核查在相关段落中分别标明。

### 2. 完成覆盖与定位

以下21节均已完成；链接可直接进入静态阅读页。

| 节 | 页面锚点／内容 | 原书印刷页 | 已展开的关键内容 |
| --- | --- | --- | --- |
| 01 | [partial-failure](../chapters/ch09.html#partial-failure) | 346—348 | 部分失败、六种无响应路径、业务结果不确定与重试副作用 |
| 02 | [tcp-boundary](../chapters/ch09.html#tcp-boundary) | 348—349 | TCP确认与应用提交的边界、连接失效及重连重复 |
| 03 | [failure-detection](../chapters/ch09.html#failure-detection) | 350—352 | 实际网络故障、非对称分区、反馈局限与怀疑 |
| 04 | [timeouts-queues](../chapters/ch09.html#timeouts-queues) | 352—355 | `2d+r`的条件、排队来源、误判级联和自适应超时 |
| 05 | [network-model](../chapters/ch09.html#network-model) | 355—358 | 电路预留与分组网络、突发流量、利用率与延迟保证 |
| 06 | [two-clocks](../chapters/ch09.html#two-clocks) | 358—360 | 墙上时钟／单调时钟、跨机不可比、Linux挂起计时区别 |
| 07 | [clock-accuracy](../chapters/ch09.html#clock-accuracy) | 360—362 | 漂移复算、NTP误差、闰秒及钟差监测 |
| 08 | [clock-causality](../chapters/ch09.html#clock-causality) | 362—364 | 原书42.004／42.003因果反例、LWW收敛与正确性区别 |
| 09 | [time-intervals](../chapters/ch09.html#time-intervals) | 364—366 | 区间顺序、TrueTime误差界、时间戳选择与提交等待、全局快照边界 |
| 10 | [process-pauses](../chapters/ch09.html#process-pauses) | 366—369 | 租约检查后暂停、恢复执行位置、网络中迟到的请求 |
| 11 | [real-time](../chapters/ch09.html#real-time) | 369—371 | 全栈硬实时条件、GC缓解及现代JDK版本纠正 |
| 12 | [quorum-authority](../chapters/ch09.html#quorum-authority) | 372—373 | 存活与权力、多数交集、投票／持久承诺规则 |
| 13 | [lease-failures](../chapters/ch09.html#lease-failures) | 373—375 | HBase案例、正常读改写路径、恢复进程及在途旧写两条失败路径 |
| 14 | [fencing](../chapters/ch09.html#fencing) | 375—376 | 33／34令牌、资源端原子持久检查、交接屏障、同代次写与重试边界 |
| 15 | [replicated-fencing](../chapters/ch09.html#replicated-fencing) | 376—377 | 代次优先元组、三个两副本读集合、局部旧写和全局胜出版本；Redlock书外讨论 |
| 16 | [byzantine](../chapters/ch09.html#byzantine) | 377—380 | 任意故障含非恶意错误、共同软件缺陷、BFT条件及实用校验 |
| 17 | [system-models](../chapters/ch09.html#system-models) | 380—382 | 三类时序模型、崩溃恢复／灰色故障、故障与存储假设 |
| 18 | [safety-liveness](../chapters/ch09.html#safety-liveness) | 382—384 | 安全性／活性、令牌单调性真实时间条件、模型外行为 |
| 19 | [formal-testing](../chapters/ch09.html#formal-testing) | 384—386 | 证明、有限模型检查、实现故障注入各自的证据边界 |
| 20 | [deterministic-simulation](../chapters/ch09.html#deterministic-simulation) | 386—388 | FoundationDB／TigerBeetle等原书案例、调度复用、不变量、种子重放与非穷尽性 |
| 21 | [conclusion](../chapters/ch09.html#conclusion) | 388—389 | 假设—性质—证据闭环，衔接第10章一致性与共识 |

保留了网络案例、HBase锁问题、原书LWW数字和33／34令牌等关键线索。计数器重试、排队净增、文件10／11／12、TrueTime区间、元组版本及教学模拟明确作为笔记假设。旧稿产品速查、面试题、通用监控阈值和强制工具清单未带入。

### 3. 原书图表与公式回看

固定PDF：`/Users/zy/ai_learn/ddia_2nd/Designing_Data_Intensive_Applications_2nd_Edition.pdf`。正文印刷345—389页对应PDF369—413页，PDF页序＝印刷页＋24。以下均实际回看了PDF渲染图像，不仅依赖抽取文本。

| 印刷页 | PDF页序 | 回看对象 |
| --- | --- | --- |
| 348 | 372 | 图9-1：请求／响应丢失与客户端观察 |
| 354 | 378 | 图9-2：排队导致的网络延迟 |
| 359 | 383 | 墙上时钟、Unix时间与时钟调整表述 |
| 361 | 385 | 同步误差、闰秒和2035相关表述 |
| 363 | 387 | 图9-3：42.004／42.003的LWW因果反例 |
| 366 | 390 | 时间区间不等式、快照与提交等待上下文 |
| 367 | 391 | 租约检查伪代码和15秒暂停反例 |
| 370 | 394 | GC名单、降低暂停影响的办法 |
| 374 | 398 | 图9-4与9-5：暂停恢复及在途延迟两种旧写 |
| 375 | 399 | 图9-6：33／34隔离令牌 |
| 376 | 400 | 新持有者首次资源写与隔离建立条件 |
| 377 | 401 | 图9-7：多副本隔离、版本排序与读取 |
| 382 | 406 | 令牌生成正确性及单调性真实时间条件 |

因此原书图9-1—9-7全部覆盖。另回看Spanner原论文第7页的事务提交规则，结合§3与§4.1.2核查。上述原书页图保存在证据目录的 `ch09-original-p{印刷页}.png`，论文和页图为 `ch09-spanner.pdf`、`ch09-spanner-p7.png`。

### 4. 六幅解释图

| stem（源文件及SVG同名） | 元素数 | 聚焦问题／正文位置 |
| --- | --- | --- |
| `ch09-timeout` | 14 | 同一个超时观察为何对应多种远端事实；01节 |
| `ch09-clock-order` | 15 | 墙上时钟排序如何违背明确因果；08节 |
| `ch09-lease-gap` | 21 | 租约服务正确时仍会发生的两条旧写路径；13节 |
| `ch09-fencing` | 18 | 新代次在资源落盘后，隔离才建立；14节 |
| `ch09-replica-fencing` | 19 | 少数副本接受旧写为何不等于法定人数读选择旧值；15节 |
| `ch09-dst` | 19 | 确定性模拟中的调度、故障、不变量与重放；20节 |

六幅均为重新组织的解释图，合计106个原生元素。复用现有共享工具完成原生场景转换和官方SVG导出，未重新安装或修改共享依赖。六份场景均经官方编辑器重载、改字、恢复验证；SVG与原生场景文字一致，非把整张图片嵌入场景。正文提供箭头／虚线含义、阅读顺序和结论；手机使用局部滚动并可打开大图。

### 5. 外部核查依据

核查日期均为2026-11-07，链接同步收入正文来源折叠区。

- [Linux man-pages：clock_gettime](https://man7.org/linux/man-pages/man2/clock_gettime.2.html)：单调非递减与频率调整、`CLOCK_MONOTONIC`／`CLOCK_BOOTTIME`挂起区别、Unix时间与本地日历显示。
- [Google Spanner官方说明](https://cloud.google.com/spanner/docs/true-time-external-consistency)与[Spanner原论文](https://research.google.com/archive/spanner-osdi2012.pdf)§3、§4.1.2：可信误差界、提交时间戳选择和提交等待条件；历史误差数值不作为当前SLA。
- [BIPM第27届CGPM第4号决议](https://www.bipm.org/en/cgpm-2022/resolution-4)：准确记录“2035年或之前提高UT1−UTC上限”的决定，区分决定与全球实施完成。
- [OpenJDK JEP 363](https://openjdk.org/jeps/363)、[JEP 318](https://openjdk.org/jeps/318)：CMS从JDK14移除；Epsilon不回收内存。
- [Kleppmann的锁文章](https://martin.kleppmann.com/2016/02/08/how-to-do-distributed-locking.html)与[Sanfilippo的回应](https://antirez.com/news/101)：对照双方原文，限定2016年争论的时序模型、正确性主张及资源条件。
- [FoundationDB Simulation and Testing](https://apple.github.io/foundationdb/testing.html)：Flow共享执行、确定性模拟、故障恢复顺序、环状不变量及真实性能测试的职责。

其他历史事故与DST产品案例按原书标明出处转述，未声称逐一复现或通读所有被引文献。

### 6. 纠错与限定记录

原书层面的修正是本笔记依据原页及外部来源给出的解释，不冒称出版社已确认勘误。

| 原表述／来源 | 问题及依据 | 修正与正文位置 |
| --- | --- | --- |
| 旧稿：单机全好或全坏；超时是“唯一可靠”检测 | 单机也可能部分失效；超时只能反映等待未完成 | 区分正常抽象、现实故障和观察歧义；01—03节 |
| 原书359页及旧稿：墙上时钟受DST变化影响的笼统说法 | 本地日历显示切换不意味着Unix时间戳随之跳变 | 分清日历显示、Unix时间与系统校时；06节，Linux文档 |
| 旧稿：把单调时钟等同于绝对均匀或所有平台都计入休眠 | 单调非递减不等于固定速率；Linux两种时钟对挂起的处理不同 | 按具体时钟API说明语义，不跨机比较；06节 |
| 原书2035闰秒概括及旧稿的确定化转述 | 决议不等于迁移已完成，也不是所有时间问题消失 | 按BIPM决定措辞限定；07节 |
| 旧稿：TrueTime固定等待、原子钟主要只为性能 | 统计置信区间不能直接作为安全保证；固定睡眠遗漏协议条件 | 选择 `s >= TT.now().latest`，等待 `TT.now().earliest > s`；可靠误差界与精度分别解释；09节 |
| 原书370页及旧稿：CMS、Epsilon等并列为现行Java回收器名单 | JEP363说明CMS在JDK14移除；JEP318说明Epsilon不回收 | 标出版本限制，不将名单当2026年任意JDK配置建议；11节 |
| 原书373页“只有一个多数”的直觉及旧稿“过半自然避免脑裂” | 多个多数集合可以同时存在；交点若冲突投票，仍不能保安全 | 多数集合必相交，还需投票、持久承诺和跨轮规则；12节 |
| 旧稿：获得新锁即可保护资源 | 原书376页要求新持有者先完成资源写；资源未必已知道新代次 | 先成功推进资源代次，再读取最新状态；隔离屏障前后的性质分开；14节 |
| 旧稿伪代码：`token <= last_token` | 每租约一个令牌时，相同令牌的第二次正常写也会失败 | 拒绝严格较小令牌，允许同代次后续写；幂等和代内排序另行处理；14节 |
| 旧稿：分别调用检查、写值、保存令牌 | 33检查后暂停、34写入、33恢复可覆盖新值 | 三者置于同一原子持久边界，说明崩溃后不得忘记代次；14节 |
| 旧稿：按生成调用完成先后要求令牌递增 | 重叠调用可按相反次序完成；原书382页条件是X完成早于Y开始 | 按非重叠调用的真实时间先后定义单调性；18节 |
| 旧稿：小数拼接版本；多数交集自然保证所有读 | 拼接掩盖代次优先及低位范围；单副本读取仍可陈旧 | 用字典序元组，并列明固定成员、持久版本、成功写与法定人数读条件；15节 |
| 旧稿：Redlock“只依赖时钟同步”，其作者承认只为性能 | 回应讨论相对走时误差，并继续主张互斥安全 | 对照双方原文陈述模型争议，避免产品口号；15节 |
| 旧稿：“软件bug≠拜占庭” | 拜占庭按任意错误行为分类，不以恶意为必要条件 | 软件bug可以表现为拜占庭故障；共同缺陷可能超出容错数量假设；16节 |

### 7. 实际验证与证据

证据目录：`/private/var/folders/5k/y6qh6sfd2g30js0v0qrv4mfr0000gn/T/opencode/ddia2-tools/`。这里保留的是本地验证产物，不作为网页运行依赖。

**静态生成与教学机制检查：通过。** 运行 `ch09-render.py` 生成页面，再运行 `ch09-check.py`；结果为 `ch09-check-results.json`。

- 复算 `2d+r`、200ppm漂移、ISDN时隙、排队净增、LWW反例和TrueTime提交等待条件。
- 实际重现非原子检查导致旧值覆盖新值的交错；枚举旧写、推进屏障、新写三种代表性交错，屏障后拒绝旧代次，最终状态均为34／12；同代次后续操作可接受。
- 三副本中全部三组两副本读均选择 `(34,1)`，单独读取落后R3不能保证这一结果；检查多数交集及重叠令牌调用逆序完成的反例。
- 导言、21节标题与正文、来源区的Markdown／HTML文本一致；锚点无重复；6图原生文字与SVG一致，图片具有替代文本。
- 85项有效本地引用检查通过；唯一待整合目标是验证时尚未落盘的 `ch10.html`，单独记入 `pending`。页面未增加第13／14章链接，未将原稿、笔记或图源目录链接到阅读页。
- 初次检查遇到缺少 `bs4`，已改用标准库 `HTMLParser` 后通过，未为此安装依赖。

**Chrome页面与图示检查：通过。** 运行 `ch09-verify.mjs`；结果为 `ch09-browser-results.json`。

- 1440px、375px两种宽度分别检查系统浅色／深色，共4组页面。正文16px、行高31.2px；桌面文章宽720px，手机335px；页面滚动宽度始终等于视口宽度。
- 桌面与手机目录实际点击可到达隔离令牌节，手机目录和来源区可展开／折叠。首次跟随系统；手动切换后刷新，主题与本地存储一致。
- 表格、代码和图示使用局部滚动；手机图示容器333px、内容宽560px，不造成整页横向溢出。图片加载完成，无捕获的页面错误或HTTP错误。
- 六幅独立SVG分别检查浅色／深色，共12组；文字边界无裁切，独立大图读取保存的深色偏好。
- 页面截图：`ch09-reader-{1440|375}-{light|dark}.png`；隔离图上下文截图：`ch09-fencing-reader-{1440|375}-{light|dark}.png`；图示截图：`ch09-diagram-{stem去掉ch09前缀}-{light|dark}.png`。
- 已实际目检六幅图截图，以及桌面浅色、手机深色正文和手机深色隔离图截图，文字与箭头清楚，未发现需修复问题。

复跑命令（项目根目录执行，沿用现有环境与共享工具）：

```sh
python3 books/designing-data-intensive-applications-2nd/diagrams/sources/ch09-render.py
python3 books/designing-data-intensive-applications-2nd/diagrams/sources/ch09-check.py
node books/designing-data-intensive-applications-2nd/diagrams/sources/ch09-verify.mjs
```

`ch09-diagrams.mjs`用于初始创作，不是常规验证步骤；人工编辑原生场景后应导出该场景，避免用初始输入覆盖后续编辑。浏览器验证使用的独立服务器与Chrome已由脚本关闭，本章没有后台写作任务。

**验证范围：**机制脚本是有限教学模型，不是完整锁服务、复制协议或形式化证明；没有运行真实集群／数据库／网络故障注入，没有运行FoundationDB或TigerBeetle的产品DST。Java计时示例未单独编译。外部文档核查不构成当前产品版本实测。本次完成本章静态生成及本地浏览器检查，未部署。

### 8. 跨章衔接与主Agent整合事项

- 本章上一页为 `ch08.html`，下一页为 `ch10.html`。正文通过第8章MVCC、第6章复制与法定人数关联背景，并把共识的投票、代次和日志规则留给第10章展开。
- 验证时 `ch10.html` 尚不存在，按本轮并行交付约定保留该目标；请主Agent在第10章落盘后完成整合链接检查。
- 第8章“下一章”接入第9章，以及书籍概览／共享导航的汇总接入由主Agent处理。
- 无尚未解决的本章内容或图示问题。修改范围限于本章笔记、报告、页面及 `ch09-*` 图源／导出文件；原稿、旧稿、其他章节和共享工具保持只读。

**交付状态：第9章已完成；提交主Agent整合，停止编辑。**

### 9. 主Agent主审与接入完成（2026-11-07）

四位负责人全部返回、停止编辑后，主Agent通读本章正文、来源及报告，复核超时／时钟／租约、原子持久隔离、资源先推进代次再读状态、版本选择与系统模型。回看印刷375／376／382页及375页隔离原图，查看六幅新图联系表。未发现需重写的核心缺口。

第8章已接到第9章，第10章已落盘，作者交付时的待整合链接全部关闭。主Agent复跑`ch09-check.py`通过，21节／引言／来源同步、6组图源／SVG及教学算例正常；统一统计15,876汉字。全轮14页960项引用、Chrome60组页面／图示及正反翻页通过，结果见本书README和`round3-*.json`。主审未扩大作者所列产品验证边界；本章完成待用户验收。
