# 全书导航｜术语、案例与来源

本页是第 1—16 章笔记的阅读索引。按问题寻找术语、沿案例连接章节，或回到具体来源与纠错说明；完整推理仍在各章正文中。中文术语为本站笔记译法。

## 01　两条阅读主线

- **决定投入多少**：[架构与质量属性](../chapters/ch02.html#function-and-quality) → [风险—技术—证据闭环](../chapters/ch03.html#risk-loop) → [播放器的实际取舍](../chapters/ch04.html#evidence-and-stopping) → [建模建议](../chapters/ch05.html#focus-on-risks) → [结论中的停止点](../chapters/ch16.html#stop-modeling-functionality)。
- **用模型形成可检查的认识**：[模型往返](../chapters/ch06.html#model-roundtrip) → [领域／设计／代码模型](../chapters/ch07.html#three-primary-models) → [元素](../chapters/ch12.html#component-types-instances)与[关系](../chapters/ch13.html#using-the-relationships) → [风格约束](../chapters/ch14.html#styles-as-constraints) → [模型分析](../chapters/ch15.html#analysis-roundtrip) → [运行验证](../chapters/ch16.html#validate-in-running-system)。

初读可从[第 1 章](../chapters/ch01.html)顺序阅读；复习时，先明确自己在问投入、结构、行为还是证据，再选择下面的入口。

## 02　风险、质量与设计工作

| 统一术语／英文 | 含义与阅读位置 |
| --- | --- |
| 架构设计活动 / architecting | 与架构师角色、架构产物分开理解：[第 1 章](../chapters/ch01.html#role-activity-artifact)。 |
| 风险驱动模型 / risk-driven model | 识别并排序风险，选择并应用技术，评估风险降低；新证据也可能揭露新风险：[第 3 章](../chapters/ch03.html#risk-loop)。 |
| 质量属性 / quality attributes | 系统以何种性质完成功能；可修改性、可扩展性等须放在具体情境中：[第 2 章](../chapters/ch02.html#function-and-quality)。 |
| 延迟 / latency；吞吐量 / throughput | 前者是一次操作所需时间，后者是单位时间完成量；不能直接互换：[第 6 章](../chapters/ch06.html#website-performance)。 |
| 质量属性场景 / quality attribute scenario | 用刺激源、刺激、环境、对象、响应、响应度量明确要求：[第 9 章](../chapters/ch09.html#quality-scenarios-drivers)。 |
| 架构驱动因素 / architecture driver | 对架构选择影响显著的要求；如何分配职责见[第 12 章](../chapters/ch12.html#drivers-and-responsibilities)。 |
| 预设架构 / presumptive architecture | 一个领域中通常默认采用的架构；与供设计参照的参考架构区分：[第 2 章](../chapters/ch02.html#presumptive-architecture)。 |
| 架构提升 / architecture hoisting | 由共同架构机制承担某项目标或性质的实现责任：[第 2 章](../chapters/ch02.html#hoisting-mechanism)。 |
| 架构失配 / architectural mismatch | 组件对环境、控制或交互的假设不兼容：[播放器案例](../chapters/ch04.html#cots-boundary)、[第 15 章](../chapters/ch15.html#architectural-mismatch)。 |
| 关注架构的设计 / architecture-focused design | 有意识地选择结构与约束以支持目标：[第 2 章](../chapters/ch02.html#indifferent-and-focused)。 |
| 横切关注点 / crosscutting concern | 跨越既定边界的责任或性质，不能仅靠一种划分全部封装：[第 16 章](../chapters/ch16.html#dynamic-and-crosscutting)。 |

## 03　模型、元素与关系

| 统一术语／英文 | 区别与阅读位置 |
| --- | --- |
| 领域／设计／代码模型 / domain / design / code model | 分别组织问题领域事实、设计承诺与实现细节，不是必须单向完成的三个阶段：[第 7 章](../chapters/ch07.html#three-primary-models)。 |
| 边界模型／内部模型 / boundary / internals model | 从使用者所需承诺与内部实现两个尺度说明同一实体：[第 9 章](../chapters/ch09.html#boundary-and-refinement)。 |
| 主模型／视图／视图类型 / master model / view / viewtype | 视图是选择性表达；视图类型按元素与关系组织表达：[第 7 章](../chapters/ch07.html#master-model-and-views)、[第 9 章](../chapters/ch09.html#viewtypes-and-instances)。 |
| 模块／运行时／分配视图类型 | 分别看实现组织、运行协作及软件与环境的对应；运行时也称组件与连接器（C&C）视图类型：[第 9 章](../chapters/ch09.html#viewtypes-and-instances)。 |
| 模块／组件／连接器／节点 / module / component / connector / node | 代码组织、运行实体、交互机制与分配环境中的计算资源不能只凭名称等同：[第 12 章](../chapters/ch12.html#modules-and-components)、[分配元素](../chapters/ch12.html#allocation-elements)。 |
| 提供端口／所需端口 / provided / required port | 边界提供的能力与所依赖的能力；端口还可包含协议：[第 12 章](../chapters/ch12.html#ports-types-interfaces)。 |
| 角色／附接 / role / attachment | 角色是连接器端点；附接把组件端口与连接器角色连接起来：[第 12 章](../chapters/ch12.html#bindings-and-attachment)。 |
| 绑定 / binding | 内外端口对应见[第 12 章](../chapters/ch12.html#bindings-and-attachment)；把模式占位符及约束应用到模型的另一语境见[第 13 章](../chapters/ch13.html#binding-and-dependency)。 |
| 信息模型／快照／不变量 / information model / snapshot / invariant | 概念与关系、某一具体状态、所有合法状态应满足的规则：[第 8 章](../chapters/ch08.html#navigation-and-invariants)。 |
| 功能场景／脑内演练 / functionality scenario / mental animation | 场景给出具体轨迹，脑内演练沿轨迹检查状态、责任与规则：[第 12 章](../chapters/ch12.html#functionality-scenarios)、[第 15 章](../chapters/ch15.html#mental-animation)。 |
| 指称关系 / designation | 说明模型中的概念代表什么，不要求复制被指称对象的全部结构：[第 7 章](../chapters/ch07.html#designation)、[第 13 章](../chapters/ch13.html#designation)。 |
| 精化关系 / refinement | 增加细节并承接抽象层已有承诺：[第 7 章](../chapters/ch07.html#refinement)、[第 13 章](../chapters/ch13.html#refinement)。 |
| 开放／闭合精化语义 / open / closed refinement semantics | 决定能否增加指定类别的内容，闭合不等于所有细节都已列尽：[第 13 章](../chapters/ch13.html#open-and-closed)。 |
| 分类／泛化 / classification / generalization | 类型—实例与一般—特殊类型是两种关系：[第 13 章](../chapters/ch13.html#classification-and-generalization)。 |
| 投影／划分／组合 / projection / partition / composition | 选择性表达、把整体拆开、把部分合成整体：[第 13 章](../chapters/ch13.html#projection)及[划分与组合](../chapters/ch13.html#partition-and-composition)。 |
| 封装／设计秘密／抽象数据类型 / encapsulation / design secret / ADT | 缩小使用者必须理解的范围，隐藏可变决定，以契约描述操作：[第 11 章](../chapters/ch11.html#effective-encapsulation)。 |
| 架构显式编码风格／模型入码原则 | 让架构抽象及设计意图能在代码中被识别：[第 10 章](../chapters/ch10.html#intent-and-model-in-code)。 |
| 理想风格／具身风格 / Platonic / embodied style | 严格的理想形式与真实系统中体现的形式；后者可能偏离理想约束：[第 14 章](../chapters/ch14.html#ideal-and-embodied)。 |
| 分层 / layered；运行服务层级 / tier | layer 讨论模块依赖，tier 讨论运行服务链，都不能直接按机器数计算：[第 14 章](../chapters/ch14.html#layers-vs-tiers)。 |

## 04　沿着案例跨章阅读

- **Rackspace 日志查询**：[第 1 章三代系统](../chapters/ch01.html#rackspace-generations) → [第 14 章 MapReduce 风格](../chapters/ch14.html#map-reduce) → [第 16 章约束取舍](../chapters/ch16.html#constraints-as-guide-rails)。保持查询响应、索引新鲜度、新种类分析等待三个口径；第 14 章是一般机制解释，不是为 Rackspace 补写实施细节。
- **家庭媒体播放器**：[第 4 章背景与风险](../chapters/ch04.html#prototype-and-risks) → [暂停场景](../chapters/ch04.html#pause-and-connectors)、[适配与故障隔离](../chapters/ch04.html#adapters-and-failure)、[延迟测量](../chapters/ch04.html#overlay-and-latency) → [第 16 章运行验证](../chapters/ch16.html#validate-in-running-system)。50ms 响应目标与约一秒恢复是不同指标；内部适配器不各自等于一个顶层进程。
- **Yinzer 社交网络**：[第 7 章三类模型](../chapters/ch07.html#three-primary-models) → [第 8 章领域词汇](../chapters/ch08.html#yinzer-vocabulary) → [第 9 章边界与内部](../chapters/ch09.html#yinzer-internals) → [第 11 章邀请快照](../chapters/ch11.html#invitation-snapshots) → [第 16 章异步邮件取舍](../chapters/ch16.html#constraints-as-guide-rails)。领域场景、系统场景和接口快照说明不同层次，不拼成同一次操作；一秒目标指系统发出网页。
- **邮件处理流水线**：[第 10 章结构与实现](../chapters/ch10.html#email-pipeline) → [Pipe 读取／关闭问题](../chapters/ch10.html#pipe-code-check)与[线程启动问题](../chapters/ch10.html#run-versus-start) → [第 14 章管道风格](../chapters/ch14.html#pipe-and-filter)。这是独立的邮件过滤示例，不把它等同于 Yinzer 的异步发信实现。
- **图书馆**：[第 12 章组件及实例](../chapters/ch12.html#component-types-instances) → [装配](../chapters/ch12.html#assemblies-and-refinement)与[两层场景](../chapters/ch12.html#two-level-general-behavior) → [第 15 章归还](../chapters/ch15.html#return-scenario)、[借出契约](../chapters/ch15.html#action-specifications)。六端口完整边界与四业务端口局部图各有范围；模型逐步暴露缺口，不把后续补全反写成最初就已具备。

## 05　来源定位与核查范围

依据 George Fairbanks，*Just Enough Software Architecture: A Risk-Driven Approach*，Marshall & Brainerd，2010 年 8 月首次印刷，ISBN `978-0-9846181-0-1`。[作者官网](https://www.georgefairbanks.com/book/)提供书目信息；第 1 章笔记实际依据[官方 99 页试读](https://www.georgefairbanks.com/assets/jesa/Just_Enough_Software_Architecture__Fairbanks_2010-demo.pdf)，第 2—16 章依据用户提供的 378 页全书。两文件未逐页比对，保留各自来源记录。

每章文末折叠区保留原书小节对应、页序、补充链接和核查范围：

- 导论：[01 来源](../chapters/ch01.html#sources)。
- 风险驱动：[02](../chapters/ch02.html#sources) · [03](../chapters/ch03.html#sources) · [04](../chapters/ch04.html#sources) · [05](../chapters/ch05.html#sources)。
- 模型基础：[06](../chapters/ch06.html#sources) · [07](../chapters/ch07.html#sources) · [08](../chapters/ch08.html#sources) · [09](../chapters/ch09.html#sources)。
- 实现、元素与关系：[10](../chapters/ch10.html#sources) · [11](../chapters/ch11.html#sources) · [12](../chapters/ch12.html#sources) · [13](../chapters/ch13.html#sources)。
- 风格、使用与结论：[14](../chapters/ch14.html#sources) · [15](../chapters/ch15.html#sources) · [16](../chapters/ch16.html#sources)。

原书中的历史案例按原书归属；未独立通读的引用资料在各章说明。Java、OMG UML／OCL、Fielding、Bloch、NIST、MapReduce 原始论文及 SEI 等补充依据用于核查具体问题，不追认为 2010 年原书新增内容。既有外部核查日期为 2026-11-06；本索引汇总已有记录，不表示重新验证了所有外部链接或重跑了所有示例。

## 06　纠错与适用边界索引

以下按阅读位置区分原文错误、术语澄清、模型前提与时代背景。链接处保留完整的“原表述 → 问题及依据 → 修正解释”。

### 原文错误与内部不一致

- **§2.1 JavaBeans 大小写**：`getTargetVelocity()` 对应 `TargetVelocity` → 默认内省首字母规则不符 → 应为 `targetVelocity`；[原文位置与 Oracle 依据](../chapters/ch02.html#sources)。
- **§3.7 指标名称**：“90% 消息在 25ms 内交付”称吞吐量预算 → 实为延迟分布 → 按延迟目标解释；[核查说明](../chapters/ch03.html#sources)。第 6 章同样区分[单请求延迟与吞吐量](../chapters/ch06.html#website-performance)。
- **图 7.3 图注**：精化图却写领域类型与设计类型对应 → 与图及正文冲突 → 按代码对设计的精化解释；[详细说明](../chapters/ch07.html#refinement)。
- **§8.3 OCL 不变量**：空联系网络代入原式得 `0 = 1` → 排除模型本来允许的零联系状态 → 应容纳空网络并明确关系规则；[反例与修正思路](../chapters/ch08.html#navigation-and-invariants)。未提供已执行的修正版 OCL。
- **§9.5.8 六要素漏项**：文字称六项却列五项 → 图 9.7 明列 Artifact → 补齐“对象”；[六要素说明](../chapters/ch09.html#quality-scenarios-drivers)。同章 `Own`／Owen、Web 入口计数及邮件动作未展开见[来源记录](../chapters/ch09.html#sources)。
- **§10.8 Pipe**：注释承诺等待，代码空队列却返回 `null`；正文关闭语义也未由读取实现 → 队列线程安全不等于关闭协议正确 → 分别说明等待、结束、可见性、原子性与唤醒；[代码核查](../chapters/ch10.html#pipe-code-check)。
- **图 10.11 线程**：直接调用 `run()` → 不启动独立线程 → 用 `Thread.start()` 等启动机制区分结构装配与执行；[代码与官方依据](../chapters/ch10.html#run-versus-start)。
- **§12.2 分类／泛化**：类型—实例误称 generalization → 与第 13 章及 UML 区分冲突 → 统一为 classification；[纠错](../chapters/ch12.html#component-types-instances)。同章绑定段的 B.P1／B.P2 笔误按图 12.22 解释为外部 P1—内部 P2，见[绑定](../chapters/ch12.html#bindings-and-attachment)。
- **§13.7.4 算法归属**：将 Bloch 中点溢出案例写作 Quicksort → 原文章具体展示二分搜索并扩展到归并排序 → 更正归属，保留非负有序 Java `int` 索引前提；[案例与安全式](../chapters/ch13.html#overflow-and-model-risk)。
- **§14.10 模型居中依赖**：称视图与控制器独立于中央模型 → 同页正文与图明确依赖模型 → 解释为外围彼此独立、共同依赖模型；[说明](../chapters/ch14.html#model-centered)。
- **§14.15 镜像可靠性**：由两机更可能有一台坏掉推断服务可靠性下降 → 部件故障不等于服务失效 → 区分冗余前提、接管与共同原因故障；[NIST 依据与解释](../chapters/ch14.html#allocation-styles)。
- **§15.3.1／§15.13 缺失引用**：`(?, )` → 引用未排出 → 补 Kruchten 1995 年“4+1”论文；[书目与核查范围](../chapters/ch15.html#sources)。
- **§16.4 措辞**：将 risk 与应被促进或保证的目标并列 → 字面含义与降低失败风险矛盾 → 解释为促进功能、支持质量属性或降低风险；[原表述与位置](../chapters/ch16.html#sources)。

### 概念澄清、简化前提与时代背景

- **本站术语表修正**：先前将具身风格概括为“由框架等具体技术承载”，范围偏窄；§14.2 指真实系统中体现的风格。英文统一为 Platonic／embodied，与[第 14 章](../chapters/ch14.html#ideal-and-embodied)正文一致。
- **跨章属性命名**：§12.9 的 `is_removed` 与 §15.3.3 的 `isRemoved` 都用于说明 Copy 是否移出馆藏。保留原书两种拼写并说明对应，不推定为两个独立属性；见[第 15 章](../chapters/ch15.html#action-specifications)。
- **术语范围**：原书广义“架构重构”与严格保持可观察行为的重构定义有别，见[第 3 章](../chapters/ch03.html#architecture-refactoring)；REST 不能仅由消息格式说明，见[第 14 章 Fielding 依据](../chapters/ch14.html#sources)。
- **模型范围**：[第 4 章音乐元数据基数](../chapters/ch04.html#bounded-domain-model)、[第 8 章 Employment 简化](../chapters/ch08.html#relationships-and-multiplicity)、[第 11 章 Person／Member 命名差异](../chapters/ch11.html#sources)均保留说明；不将局部示例扩大为通用领域规范。
- **实现前提**：[第 12 章 UI 验证量词例](../chapters/ch12.html#drivers-and-responsibilities)不等于安全建议；[MapReduce](../chapters/ch14.html#map-reduce)顺序等价涉及确定函数与提交语义，不自动覆盖外部副作用；[Alloy 有限范围分析](../chapters/ch15.html#analysis-scope)无反例不等于证明实际系统。
- **时代背景**：[Java 模块系统](../chapters/ch10.html#patterns-module-boundaries)区分原书 Java 7 预期与 Java 9 实际交付；[动态架构与工具](../chapters/ch16.html#dynamic-and-crosscutting)保留 2010 年语境，不写成当前工具能力结论。

[返回书籍概览](../index.html) · [重读结论](../chapters/ch16.html)
