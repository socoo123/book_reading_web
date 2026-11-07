# 全书导航｜机制、保证与数据责任

本页连接《Designing Data-Intensive Applications》英文第二版的14章详解、250个正文小节与64幅章节图。五条路线是本站的专题组织，保留原书章序与各章完整论证；初读可从[第1章](ch01.md)顺读，复习可从下面的问题进入。术语采用本站译法，原书、笔记假设、工程补充及跨书观点分别注明。

<a id="reading"></a>

## 01　先找问题，再沿失败路径回读

全书有一条连续的主线：先决定系统为谁处理什么数据，再选择表示与存储；数据跨版本、机器和服务传播以后，明确并发与故障下还承诺什么；最后把这些局部机制组成端到端流程，并判断它对人的影响。读完某种技术，最好能回答三个问题：它减少了哪一种困难，把哪一种责任交给了别人，发生失败时依据什么恢复。

例如，“订单已经成功”可能指请求已被接收、数据库已提交、派生视图已追上，或现实支付已经完成。这些状态不是一回事。沿[保证范围](#guarantees)辨认成功的含义，再回到各章的操作顺序，才能判断一个承诺是否足够。只读术语和结论表，会跳过使结论成立的条件。

| 当前问题 | 建议路线 | 读完后应能留下的具体判断 |
| --- | --- | --- |
| 数据库、模型和处理引擎怎样选 | [选型与性能：1→2→3→4→7→11](#selection-performance) | 写清查询、负载、数据移动与恢复成本 |
| 副本、事务和共识分别保证什么 | [一致性与故障：6→8→9→10](#consistency-failure) | 写清顺序域、原子范围、故障假设和等待条件 |
| 旧数据怎样进入新应用 | [演化与数据流：5→11→12→13](#evolution-dataflow) | 指明格式版本、快照切点、追赶与发布边界 |
| 重试、故障接管后会不会漏做或多做 | [端到端正确性：8→9→10→12→13](#end-to-end) | 找到稳定身份、持久责任和每个效果的提交点 |
| 保留和重放怎样兼顾人的权益 | [数据责任：1→14，并回看12—13](#data-responsibility) | 说明用途、保留范围、删除传播和重建限制 |

<a id="selection-performance"></a>

## 02　选型与性能：1→2→3→4→7→11

[第1章](ch01.md#oltp-olap) → [第2章](ch02.md#load) → [第3章](ch03.md#model-layers) → [第4章](ch04.md#amplification) → [第7章](ch07.md#design-check) → [第11章](ch11.md#conclusion)。

**先定义工作，而不是先挑产品。** 第1章把运营型点查与分析型聚合区分开，再分辨权威记录和派生数据。同一种数据库可以承担不同角色；读副本、搜索索引和数据仓库也不会因为保存同一事实就拥有同样的更新权。第2章接着把“快”变成可测量的要求：记录请求起止点、有效请求、负载分布和统计窗口，区分响应时间与数据新鲜度。异步投递可以让页面快速返回，却留下较旧的时间线。

**模型决定要表达什么，布局决定付出什么。** 第3章的关系、文档与图模型不直接规定磁盘布局；GraphQL属于接口层，也不会自动选择图数据库。第4章把一次查询还原为日志、页、索引与合并工作。LSM与B-tree不能只按“写快／读快”排胜负，必须固定键值大小、缓存、范围查询、持久化条件和稳态合并负担。向量近邻提供候选，召回率也不能替代事实正确性。

**扩展以后，把数据移动计入查询。** 第7章的全局索引可能只把“找ID”局部化，取原记录仍跨片；哈希均匀也不能拆散一个热键。第11章把同一问题推进到批量连接：shuffle让相同键相遇，广播减少大表搬运，却要求小表能在每个执行位置容纳；共分片还需布局兼容。现代dataflow引擎的价值在于按整个计算图安排这些工作，而不是只把MapReduce换一个名字。

可沿[首页时间线](ch02.md#timeline-write) → [只物化帖子与作者ID](ch03.md#normalization) → [索引与预计算](ch04.md#execution-cubes)回读计算怎样从读路径移到写路径。然后用[尾延迟](ch02.md#tail-slo)、[全局索引回表](ch07.md#global-index)和[批结果发布](ch11.md#publish)反查代价：投递积压、慢分片和半成品输出都可能使“局部更快”失去用户意义。这里没有全书统一的性能倍数，也没有据教学算例得出的产品基准排名。

<a id="consistency-failure"></a>

## 03　一致性与故障：6→8→9→10

[第6章](ch06.md#sync-ack) → [第8章](ch08.md#acid) → [第9章](ch09.md#partial-failure) → [第10章](ch10.md#isolation-and-causality)。

**第6章先问副本知道什么。** 收到日志、可靠保存、应用后可查是不同进度。读己之写、单调读和一致前缀读各自排除一类观察异常；它们不是所有副本瞬间相同的同义词。多主合并与CRDT收敛可以保存并发修改，但两地独立批准同一时段的会议室预订，仍可能一致地保留两个互相冲突的承诺。

**第8章再问并发决定能否共同成立。** 医生分别修改不同的行，仍可能因写偏斜破坏“至少一人值班”。快照隔离提供稳定读取，却不自动排除这类循环依赖；可串行化要求完整事务能解释为某个串行顺序。两阶段锁负责隔离，两阶段提交负责多参与者共同提交或中止。参与者已准备、最终决定未知时，不能靠本地超时擅自回滚。

**第9章解释为什么不能猜测远端。** 超时既可能对应请求未到，也可能对应效果已发生但响应丢失；旧进程暂停后还会恢复，租约服务撤销资格不会让它自动停止。隔离令牌要在资源端原子检查并持久保存，且新持有者应先推进资源代次，再读状态继续工作。安全性与活性分开后，网络异常可以使请求等待，但不应在协议声明的故障模型内允许错误提交。

**第10章把承诺落实到操作历史。** 线性一致性保留非重叠操作的实时先后，可串行化保留事务串行解释，严格可串行化把两者结合到完整事务。共识还需要跨任期继承、持久投票与提交规则；交集本身不够。线性一致读既要取得适当的领导权证据，也要等待状态机应用到安全读取位置。

两处对照尤其值得一起读：[第6章的2写／2读反例](ch06.md#quorum-limits)与[第10章的3写／2读反例](ch10.md#quorum-counterexample)阈值不同，但都让尚未完成的新写先被一次读取暴露，随后另一读返回旧值；不能把两例的w混写。再对照[2PC存疑状态](ch08.md#in-doubt)与[原子提交和共识](ch10.md#atomic-commit)：事务参与者全员准备与保存决定的副本法定人数是两种集合，“多数派”不能替代某个业务参与者的准备承诺。

<a id="evolution-dataflow"></a>

## 04　演化与数据流：5→11→12→13

[第5章](ch05.md#compatibility) → [第11章](ch11.md#publish) → [第12章](ch12.md#snapshot-handoff) → [第13章](ch13.md#reprocessing)。

演化首先是**新旧解释共存**。第5章按写者和读者版本确定兼容方向：新读旧是向后兼容，旧读新是向前兼容；API请求和响应分别判断。能解码不代表能无损写回，旧转换器可能丢掉新字段；金额从分改成元，也不会因字节仍可读而保持语义兼容。历史schema、工作流历史与仍运行的旧代码，都是迁移的一部分。

接着是**产生新结果而不破坏旧读取**。第11章用有界输入组织可重跑计算，把任务尝试与正式产物分开。V18构建完成之前继续读V17；发布要求完整分片集合及消费结束边界，不能把一条“作业完成”消息等同于所有下游已应用数据。每个下游原子切换，也不等于全系统共同切换。

第12章把这个问题延伸到持续写入：初始快照对应明确日志切点，后续变化从正确位置接上，才能避免遗漏和旧快照覆盖新值。CDC观察数据库变化，事件溯源以业务事件作为权威记录，CQRS分离读写模型，三者有关联而不等同。历史税率、汇率等维度必须选择版本或时间语义；恰好一次处理不会替你选择正确税率。

第13章最后把演化组织成**回填→追赶→切换**。旧视图持续维护，新视图在独立空间验证，切换后保留实际可用的退路。若旧格式已无法解释新数据、历史被清理或错误输出已触发现实动作，改回路由就不能完成回退。可重放依赖输入、顺序、代码及外部依赖仍可恢复；选择延长保留期时，还应沿[数据责任路线](#data-responsibility)检查用途与删除要求。

这条路线中的失败检查很具体：在[旧版读改写](ch05.md#compatibility)、[发布通知先到](ch11.md#publish)、[快照和日志错位](ch12.md#snapshot-handoff)、[旧视图停止维护](ch13.md#reprocessing)四个位置各放一次中断，观察究竟丢了字段、记录、可见性还是回退能力。它们分别需要相应契约，不能靠一个“零停机迁移”标签解决。

<a id="end-to-end"></a>

## 05　端到端正确性：8→9→10→12→13

[第8章](ch08.md#idempotent-consumer) → [第9章](ch09.md#fencing) → [第10章](ch10.md#shared-log) → [第12章](ch12.md#exactly-once-boundary) → [第13章](ch13.md#request-id)。

从一次“提交成功，但回复丢失”开始。第8章把消息ID、业务修改与结果纳入同一本地事务，允许重投而不重复数据库效果。第9章提醒我们，重复消息和旧持有者是两种威胁：稳定ID识别同一操作，隔离令牌拒绝陈旧授权，两者互不替代。第10章的共识日志可以可靠决定顺序，但若同一次意图重试时换了ID，日志仍可能正确地记录两次扣款。

第12章要求沿四层检查恰好一次：输入位点、内部状态、输出记录、外部副作用。检查点若恢复到不匹配的状态和位点，会漏算或重复计算；Kafka事务输出也不自动包含应用自行修改的外部数据库。邮件、支付等效果必须由接收方承担相应去重或提交责任。准确说法是“在这些输入与恢复条件下，这个范围内的效果等价于一次成功处理”，不是代码只运行了一次。

第13章将请求身份从意图产生端传到最终效果。相同参数可能是两次合法支付，不能无条件以表单内容哈希代替请求ID。多分片支付进一步说明：记得见过请求还不够，还要记得未完成的输出。批准、预留、待发责任和分录身份必须可以恢复；重启时仅跳过已见ID可能永久漏掉手续费或出账分录。

请把[局部事务去重](ch13.md#request-id)和[三分片支付](ch13.md#payment-flow)当作不同模型。前者的11元教学事务共同更新两个账户；后者的100元初始余额、30元收款与1元手续费是另一组假设，先预留31，再形成69＋30＋1的最终结果。三分片模型要求目的账户可接受入账；中途任意跨账户读取不保证总和为100。这里的最终完整性既不承诺即时原子可见，也不包含所有银行拒付与补偿规则。

最后读[审计](ch13.md#audit-provenance)：比较应有与已应用分录时，要固定共同事件边界或显式计入在途状态。同一错误代码重算两次得到相同结果，仍可能一直算错；独立不变量与来源检查提供的是另一种证据。

<a id="data-responsibility"></a>

## 06　数据责任：1→14，并回看12—13

[第1章](ch01.md#data-responsibility) → [第14章](ch14.md#purpose-and-impact)，再回看[第12章保留与重放](ch12.md#retention-replay)、[历史与删除](ch12.md#state-history)、[第13章重处理](ch13.md#reprocessing)和[审计来源](ch13.md#audit-provenance)。

第1章把保存数据的成本从存储账单扩展到泄露、追踪、纠正与删除责任。第14章进一步追问用途及后果：预测会改变机会分配，决策又会影响后续训练数据；删除敏感字段不能保证消除代理变量，群体概率也不能直接判定某个人。作者的价值判断、历史案例与已取得的实证材料，需要分别阅读。

这与前面强调“保留输入，便于重算”存在真实取舍。第12章说明保留期限制恢复期限，日志压缩合并可能只保留当前状态，墓碑过早清理会使离线消费者错过删除。第13章要求重建具有来源与版本，却没有要求所有个人历史永久保留。确定可重算范围以后，应相应限定未来可恢复的内容；不能一边删除必要输入，一边继续承诺恢复任意历史输出。

**笔记整合的假设场景：**搜索改进只需要短期点击统计。先限定字段、用途和保留期限；需要执行删除时，沿权威库→日志／快照→分析表→客户端副本查找已有表示，再检查旧快照恢复和新版视图回填会不会把它重新带回。删除标记必须传播到应处理它的消费者，已越过保留边界的离线设备可能需要重新初始化，而非盲目从旧位点续读。具体实现随系统而异，这里给出的是应核对的数据路径。

同一场景还说明为什么“追加删除事件”和“销毁密钥”不自动等于完成所有删除义务：旧明文、派生文件、备份和密钥副本仍可能存在，训练样本移除也不自动证明既有模型影响被消除。原书提出了这些工程张力；本笔记没有给出通用机器遗忘算法或完整法律合规方案。

法律口径统一参见[第1章的用途／删除／跨境限定](ch01.md#data-responsibility)与[第14章的同意](ch14.md#consent-and-choice)、[用途与最小化](ch14.md#law-and-minimization)：GDPR约束不相容的进一步处理，并非一律禁止新用途；同意不是唯一处理依据，删除权也有条件与例外。第14章德国定价案例仅取得作者摘要，不把市场利润率变化扩大成算法内部学习过程的已证实机制。

<a id="terms"></a>

## 07　关键术语：按作用域理解同一个词

术语以原书Glossary（印刷603—608）及对应正文校对。Glossary本身说明定义是简写；下列边界按章节展开，不把一个短定义当作完整协议。

| 英文／本站译法 | 统一含义与入口 |
| --- | --- |
| operational / analytical，运营型／分析型 | 前者支持日常业务，不指运维监控；OLTP／OLAP按访问模式区分。[1章](ch01.md#oltp-olap) |
| system of record / derived data，权威记录系统／派生数据 | 权威是事实接受与纠正的角色；派生可重建依赖输入与转换条件。[1章](ch01.md#authority-derived) |
| latency / response time / throughput，延迟／响应时间／吞吐量 | 说明计时边界和单位；本书的latency与业界宽泛用法有差别。[2章](ch02.md#response-time) |
| percentile / tail latency，分位数／尾延迟 | 说明样本、窗口和取秩约定，不能平均机器p99得到整体p99。[2章](ch02.md#percentiles) |
| fault / failure，故障／失效 | 部件问题与服务未兑现承诺分开；容错有明确故障范围。[2章](ch02.md#faults) |
| scalability / elasticity，可扩展性／弹性 | 承载增长与动态调整资源分别讨论；增加机器不自动拆散热点。[2章](ch02.md#load) |
| backpressure，背压 | 接收方跟不上时减慢发送；缓冲和背压都不创造处理容量。[2章](ch02.md#overload)、[12章](ch12.md#delivery-contract) |
| normalization / denormalization，规范化／反规范化 | 减少事实冗余与有意预存冗余；后者增加维护责任。[3章](ch03.md#normalization) |
| materialized view，物化视图 | 提前计算并保存读取结果；新鲜度取决于更新路径。[4章](ch04.md#execution-cubes)、[13章](ch13.md#read-write-boundary) |
| model / query API / storage，模型／查询接口／存储 | 数据关系、请求表达与物理布局三个层次；GraphQL不等于图数据库。[3章](ch03.md#model-layers) |
| log / WAL，日志／预写日志 | 存储、复制、事件日志职责不同；WAL保存恢复依据，不记录全部业务意图。[4章](ch04.md#wal-recovery)、[6章](ch06.md#replication-logs) |
| compaction / compression，压缩合并／压缩 | 前者清理覆盖版本并组织文件，后者减少编码字节；压缩合并不保留所有历史。[4章](ch04.md#bloom-compaction)、[12章](ch12.md#compaction) |
| serialization / serializability，序列化或编码／可串行化 | 数据表示与事务隔离两个问题。[5章](ch05.md#representations)、[8章](ch08.md#acid) |
| backward / forward compatibility，向后／向前兼容 | 新读旧／旧读新；读改写无损及语义兼容另行判断。[5章](ch05.md#compatibility) |
| schema，模式 | 这里主要指字段与类型约定；writer／reader schema及历史版本需可定位。[5章](ch05.md#avro-resolution) |
| durable execution，持久化执行 | 已记录完成的活动可复用结果；未确认完成的活动及外部效果可能重试。[5章](ch05.md#durable-boundary) |
| replication / sharding / network partition，复制／分片／网络分区 | 同数据多份／逻辑数据拆分／网络通信故障。[7章](ch07.md#shards-and-replicas)、[9章](ch09.md#failure-detection) |
| leader / follower / replica，主节点／从节点／副本 | 属于指定复制范围；单主不消除读改写丢失更新。[6章](ch06.md#single-leader) |
| failover / fencing，故障切换／隔离陈旧授权 | 选出接管者和资源拒绝旧操作是不同职责。[6章](ch06.md#failover)、[9章](ch09.md#fencing) |
| quorum / majority，法定人数／多数派 | 法定人数不总等于多数派；交集不是完整一致性协议。[6章](ch06.md#quorum) |
| happens-before / concurrency，先发生关系／并发 | 无因果先后即并发，不要求墙钟同时；向量保留已知来源进度。[6章](ch06.md#causality) |
| local-first / CRDT，本地优先／无冲突复制数据类型 | 设备参与持久状态与同步；收敛不自动满足所有业务不变量。[6章](ch06.md#local-first)、[业务约束](ch06.md#business-constraints) |
| rebalance / skew / hot key，再平衡／倾斜／热键 | 数据移动、负载不均、单键热点；与clock skew的时钟偏差分开。[7章](ch07.md#migration) |
| atomicity / isolation / durability，原子性／隔离性／持久性 | 整体提交、并发干扰、确认后保存分别解释；原子操作另有不可分割效果语境。[8章](ch08.md#acid) |
| snapshot isolation / MVCC，快照隔离／多版本并发控制 | 隔离保证与实现机制有别；MVCC并非只能实现一种隔离级别。[8章](ch08.md#mvcc) |
| read skew / lost update / write skew，读偏斜／丢失更新／写偏斜 | 跨时点拼读／覆盖他人修改／不同记录共同破坏规则。[8章](ch08.md#read-skew)、[更新](ch08.md#lost-update)、[偏斜](ch08.md#write-skew) |
| 2PL / 2PC，两阶段锁／两阶段提交 | 隔离算法与原子提交协议，不以“两个阶段”互换。[8章](ch08.md#two-phase-locking)、[提交](ch08.md#two-phase-commit) |
| timeout / lease / fencing token，超时／租约／隔离令牌 | 怀疑故障、限时授权与资源端拒绝旧代次分别处理。[9章](ch09.md#failure-detection)、[令牌](ch09.md#fencing) |
| monotonic / time-of-day clock，单调／墙上时钟 | 间隔与时间点用途不同；单调钟不可直接跨机器比较。[9章](ch09.md#two-clocks) |
| safety / liveness，安全性／活性 | 不发生坏事／最终取得进展；此处安全性不是信息安全。[9章](ch09.md#safety-liveness) |
| linearizability / strict serializability，线性一致性／严格可串行化 | 操作实时顺序／完整事务串行解释加实时顺序。[10章](ch10.md#isolation-and-causality) |
| consensus / atomic commitment，共识／原子提交 | 共同决定与事务全员准备条件分别解释。[10章](ch10.md#atomic-commit) |
| total / partial order，全序／偏序 | 任意两项能否比较；排序不等于已经知道所有竞争请求。[10章](ch10.md#ordering-not-decision) |
| deterministic，确定性的 | 相同输入和状态产生相同结果，外部时间、随机值与维度须纳入恢复条件。[9章](ch09.md#deterministic-simulation) |
| bounded / unbounded，有界／无界 | 数据流是否有可到达的终点，不要求预知精确大小；网络模型中的有界另指延迟等上限。[11章](ch11.md#bounded-reruns)、[9章](ch09.md#system-models) |
| shuffle / join，重分布／连接 | 让相关记录相遇／组合记录；连接不是网络连接，shuffle不一律意味着排序。[11章](ch11.md#shuffle) |
| CDC / event sourcing / CQRS，变更数据捕获／事件溯源／命令查询职责分离 | 行变化、权威事件和读写模型划分，三者不互为必要条件。[12章](ch12.md#events-outbox) |
| offset / checkpoint，消费位点／检查点 | 本书消费例子以“下一条位置”为约定；恢复切面还须包含对应状态与所需输出责任。[12章](ch12.md#offsets)、[检查点](ch12.md#checkpoints) |
| event time / processing time / watermark，事件时间／处理时间／水位线 | 事件发生、系统处理与进度假设；水位线不证明所有旧事件绝不会再来。[12章](ch12.md#watermarks) |
| exactly-once / idempotence，恰好一次语义／幂等性 | 效果等价于一次／重复操作效果不增；都须说明保护范围和恢复条件。[12章](ch12.md#exactly-once-boundary) |
| timeliness / integrity，及时性／完整性 | 状态足够新／无丢失重复损坏且派生与不变量正确；完整性不只是字段齐全。[13章](ch13.md#timeliness-integrity) |
| unbundling / federation，拆分数据库／联邦数据库 | 写传播职责组合／读取侧统一查询；前者不是分片，后者不是微服务的同义词。[13章](ch13.md#unified-reads-writes) |
| purpose limitation / data minimization，用途限制／数据最小化 | 为何处理与需要哪些数据；保留期限另行决定。[14章](ch14.md#law-and-minimization) |

<a id="guarantees"></a>

## 08　保证范围：把“成功”落到具体边界

以下是本站跨章对照，不是原书一张总表。每行都要保留它自己的输入、存储与故障假设。

| 机制与入口 | 在哪些条件下承担什么责任 | 不能据此推出什么 |
| --- | --- | --- |
| [WAL与持久确认](ch04.md#wal-recovery) | 必要恢复信息可靠保存，存储栈兑现承诺，恢复已提交修改 | 客户端一定知道结果；所有副本及视图已可读 |
| [同步复制](ch06.md#sync-ack) | 等到配置要求的接收、持久化或应用阶段 | 所有“同步”都等到查询可见；不经安全选主也不丢写 |
| [事务与隔离](ch08.md#acid) | 在事务覆盖的对象上，按所选隔离与提交保证处理并发／失败 | ACID自动懂业务，或自动覆盖现实支付／邮件 |
| [共识及读屏障](ch10.md#linearizable-reads) | 在声明模型内继承提交历史，取得有效读证据并应用到安全位置 | 任一自认主节点都能直接读；所有业务请求天然去重 |
| [隔离令牌](ch09.md#fencing) | 资源原子持久推进代次后拒绝旧授权；同代次按资源规则处理 | 同一请求不重复；同代次写自动有序；身份认证已完成 |
| [幂等消费](ch08.md#idempotent-consumer) | 稳定身份、唯一约束，ID／效果／结果共同提交，去重仍保留 | ack后必可删除ID；输入永久丢失也能最终完成 |
| [持久化执行](ch05.md#durable-boundary) | 历史可恢复，重放控制流相容，复用已记录结果 | 未记录完成的外部活动绝不重试 |
| [批结果发布](ch11.md#publish) | 隔离版本、完整性证据、受协调切换，读者固定版本 | 任务代码执行次数等于一；多个下游有共同提交点 |
| [流式恢复](ch12.md#exactly-once-boundary) | 可重放源、一致状态／位点、输出提交或幂等接收协作 | 任意外部动作随检查点回滚；用户意图自动识别 |
| [日志驱动支付](ch13.md#payment-recovery) | 批准决定可恢复、未发完责任不丢、各分录去重且最终推进 | 任意跨账户即时读取原子可见；收款拒绝已被解决 |
| [可重建与审计](ch13.md#audit-provenance) | 所需输入、版本、顺序及依赖可得，按相同边界检查 | 相同代码重算即证明业务正确；可无限期重建已删除输入 |

“最多一次效果”是安全性质，“最终一次效果”还要输入不丢、持续恢复与有效处理等活性条件。这里也不以“最终”回避永久错误、无人处理的死信或已经过期的日志。需要额外讨论时，应回到对应章的反例，而不是把保证表当作配置指南。

<a id="cases"></a>

## 09　案例导航：相同主题，不混成一个真实项目

原书案例保留其归属；以下数字与小数据若来自笔记，会明确说明。全书没有虚构一家公司依次采用所有架构。

| 案例与入口 | 归属／贯穿的推理 | 失败路径与口径 |
| --- | --- | --- |
| [商品权威价格](ch01.md#authority-derived) → [双写](ch12.md#cdc) → [视图演化](ch13.md#reprocessing) | 权威／派生主线来自原书；100→90、catalog-v1／v2为笔记假设 | 双写部分成功或反序；回填成功不等于追赶完成 |
| [社交时间线](ch02.md#timeline-read) → [规范化](ch03.md#normalization) → [表—表连接](ch12.md#table-table) → [读写边界](ch13.md#read-write-boundary) | 原书简化社交案例及历史实现；并非对X当前架构的调查 | 按帖子加权扇出；新增／取消关注与删帖都影响视图 |
| [简历与地点查询](ch03.md#relational-document) → [图路径](ch03.md#cypher-sql) | 简历／Lucy原书主线；Lin／Mei数据及部分地点路径为教学重组 | 同一人同时满足两条件；零跳、环与重复结果分别检查 |
| [会议座位](ch03.md#events-cqrs) → [视图恢复](ch03.md#replay-boundaries) | 原书事件模型；500→497→492→495为笔记数据 | 重复取消变498；末席并发成功需写侧裁决，重放邮件有外部效果 |
| [会议室／值班医生](ch06.md#business-constraints) → [写偏斜](ch08.md#write-skew) → [严格约束](ch13.md#uniqueness) | 原书用于解释跨记录业务冲突的不同例子 | CRDT收敛、单主、快照读取均不能单独代替正确约束检查 |
| [字节与模式](ch05.md#bytes) → [Avro演化](ch05.md#avro-evolution) | 原书Martin／1337样例；81／66／33／32字节按所列编码复核 | 数字不是一般压缩比；long→int与未知字段读改写有边界 |
| [工作流付款](ch05.md#durable-boundary) | 原书风控／扣款／入账；payment-742键为笔记假设 | 外部成功但历史未记录仍可重试；未提供完整拒付补偿实现 |
| [购物车与版本](ch06.md#version-number) → [版本向量](ch06.md#version-vectors) | 原书五写过程与笔记向量展开 | 新分配序号不等于客户端知识；集合并集会使删除复活 |
| [quorum先新后旧](ch06.md#quorum-limits) → [线性化反例](ch10.md#quorum-counterexample) | 6章笔记n=3,w=2,r=2；10章原图改写w=3,r=2 | 两者均无返回前阻塞写回；未完成写不能套用已完成写交集前提 |
| [分片迁移](ch07.md#migration) → [CDC快照](ch12.md#snapshot-handoff) | 位点40—48与S100／101—103是不同笔记模型 | 一致基线、增量与交接屏障，避免漏写、旧值覆盖或旧主继续写 |
| [33／34租约](ch09.md#fencing) → [协调服务](ch10.md#coordination) | 令牌数字来自原书；advance伪代码为笔记展开 | 资源先建立新代次屏障；锁服务正确仍可能发生陈旧写 |
| [Unix热门URL](ch11.md#unix-pipeline) → [连接](ch11.md#joins) → [版本发布](ch11.md#publish) | 原书问题，8行日志与V17／V18为笔记样本 | 真实运行Unix／SQLite只验证小数据；未实测分布式引擎 |
| [迟到窗口](ch12.md#watermarks) → [历史税率](ch12.md#temporal-joins) → [汇率](ch13.md#exchange-rate) | 原书时间语义；计数2→3、100美元换算为笔记假设 | 更新同一结果不能累计成5；维度版本不同会改变重算结果 |
| [11元请求去重](ch13.md#request-id) → [三分片支付](ch13.md#payment-flow) → [恢复](ch13.md#payment-recovery) | 前者改写原书SQL；后者100／31／30／1元为独立教学模型 | r7只是各例局部请求名，不能合成同一笔业务；预留不重复扣款，按分录角色去重 |
| [信用—就业反馈](ch14.md#feedback-loops) → [用途选择](ch14.md#privacy-as-agency) | 原书风险机制与罕见病分享案例 | 预测改变未来数据；风险机制不是所有群体的统一因果效果 |

<a id="chapter-sources"></a>

## 10　十四章来源与原文定位

固定版本为Martin Kleppmann、Chris Riccomini，O’Reilly英文第二版，February 2026，First Release 2026-02-18，ISBN 978-1-098-11906-5。依据673页用户PDF；正文PDF页序＝印刷页＋24。下表为**正文含Summary**的范围，References可能从末页中段开始；完整章及外部资料的实际读取范围见各章折叠来源。网页不分发原书或本地提取文本。

| 章／原章名 | 正文印刷页／PDF页序 | 来源与核查入口 |
| --- | --- | --- |
| 1 · Trade-Offs in Data Systems Architecture | 1—26／25—50 | [来源](ch01.md#sources) · [权威与派生](ch01.md#authority-derived) |
| 2 · Defining Nonfunctional Requirements | 33—56／57—80 | [来源](ch02.md#sources) · [指标口径](ch02.md#percentiles) |
| 3 · Data Models and Query Languages | 65—108／89—132 | [来源](ch03.md#sources) · [模型与接口](ch03.md#model-layers) |
| 4 · Storage and Retrieval | 115—151／139—175 | [来源](ch04.md#sources) · [恢复与放大](ch04.md#wal-recovery) |
| 5 · Encoding and Evolution | 161—192／185—216 | [来源](ch05.md#sources) · [兼容方向](ch05.md#compatibility) |
| 6 · Replication | 197—244／221—268 | [来源](ch06.md#sources) · [quorum边界](ch06.md#quorum-limits) |
| 7 · Sharding | 251—272／275—296 | [来源](ch07.md#sources) · [迁移](ch07.md#migration) |
| 8 · Transactions | 277—337／301—361 | [来源](ch08.md#sources) · [事务范围](ch08.md#transaction-boundary) |
| 9 · The Trouble with Distributed Systems | 345—389／369—413 | [来源](ch09.md#sources) · [系统模型](ch09.md#system-models) |
| 10 · Consistency and Consensus | 401—443／425—467 | [来源](ch10.md#sources) · [保证区别](ch10.md#isolation-and-causality) |
| 11 · Batch Processing | 451—482／475—506 | [来源](ch11.md#sources) · [恢复与发布](ch11.md#fault-recovery) |
| 12 · Stream Processing | 487—531／511—555 | [来源](ch12.md#sources) · [处理边界](ch12.md#exactly-once-boundary) |
| 13 · A Philosophy of Streaming Systems | 539—580／563—604 | [来源](ch13.md#sources) · [支付恢复](ch13.md#payment-recovery) |
| 14 · Doing the Right Thing | 585—598／609—622 | [来源](ch14.md#sources) · [用途与最小化](ch14.md#law-and-minimization) |

本页不重新宣称每条外部参考都已通读。各章记录了2026-11-07核查的文档版本，例如PostgreSQL17／18、MySQL8.4、Avro1.12、etcd3.6、Flink2.1、Kafka4.1；这些是具体核查版本，不等同所有产品的最新或历史行为。德国定价全文及ACM官网取得受限等缺口，仍保留在[第14章来源](ch14.md#sources)。

<a id="corrections"></a>

## 11　纠错导航：先看对象，再看证据

“原书修正”指笔记依据原页、规范或算例提出的限定，不冒称出版社确认勘误；“旧稿修正”针对只读参考稿；“笔记修正”针对本站写作时的表述。下表是查找入口，原句、完整依据及适用条件仍留在对应正文与来源区。

| 对象／入口 | 原表述 → 问题依据 → 修正解释 |
| --- | --- |
| 原书及旧稿 · [1章](ch01.md#data-responsibility)、[14章](ch14.md#law-and-minimization) | 任何其他用途都禁止 → GDPR第5、6(4)等条款针对相容性与处理条件 → 保留用途限制及研究保障，删除／跨境另有条件 |
| 旧稿 · [2章扇出](ch02.md#timeline-write)、[分位数](ch02.md#percentiles)、[预算](ch02.md#tail-slo) | 400倍性能、平均p99、成功率直接换停机分钟 → 操作成本、分布与分母不同 → 统一假设与统计口径 |
| 原书／旧稿及本站 · [3章图查询](ch03.md#cypher-sql)、[GraphQL](ch03.md#graphql-api)、[DataFrame](ch03.md#dataframes)、[同质数据](ch03.md#property-graph) | 标签大小写混写、GraphQL无昂贵查询、NumPy稀疏数组、homogeneous译“同构” → 原页／官方资料与概念区分 → 分别修正代码条件、成本控制、表示及译法；最后一项为本站笔记修正 |
| 原书 · [4章容量](ch04.md#btree)、[合并背压](ch04.md#bloom-compaction)、[VACUUM](ch04.md#amplification)、[Roaring](ch04.md#column-layout) | 四层树约250TB、暂停所有读写、普通vacuum重排、Roaring仅两种表示 → 明确叶层复算及官方实现 → 依层数、写背压、VACUUM变体和三类容器限定 |
| 原书及旧稿 · [5章字节](ch05.md#bytes)、[Avro解析](ch05.md#avro-resolution)、[演化](ch05.md#avro-evolution) | fixstr低4位、int64对称一字节范围、long缩int、null默认值固定首支 → 规范与编码验证不支持泛化 → 低5位、区分sint、合法提升及Avro版本规则 |
| 原书及旧稿 · [5章工作流](ch05.md#durable-boundary) | 成功RPC不会再扣一次 → 完成报告可能未持久化，原书及Temporal要求幂等 → 已记录结果与未确认外部效果分开 |
| 原书／旧稿 · [6章日志](ch06.md#replication-logs)、[确认](ch06.md#sync-ack)、[quorum](ch06.md#quorum-limits) | MySQL默认混合、同步即能读、交集即最新 → MySQL8.4／PostgreSQL17及并发反例 → ROW、确认阶段与完整协议各自说明 |
| 原书／旧稿 · [7章分裂](ch07.md#range-splitting)、[哈希](ch07.md#hash-range-and-consistent)、[全局索引](ch07.md#global-index) | 分裂必立即全量重写、jump恒O(1)、全局索引只有一跳 → HBase实现、原论文和原书回表路径 → 保留实现、复杂度与端到端查询边界 |
| 旧稿及原书概括 · [8章读偏斜](ch08.md#read-skew)、[隔离名](ch08.md#isolation-names)、[SSI](ch08.md#ssi)、[XA](ch08.md#xa) | 转账分开提交、按产品隔离名称泛化、SSI不与2PC工作 → 原图、固定版本官方文档、SSI论文§7.1 → 一次提交的跨时点读，本地SSI可结合2PC，XA不自动提供全局SSI |
| 原书／旧稿 · [8章去重](ch08.md#idempotent-consumer) | ack后可删ID、重复分支直接return → 重投、生产者重复与人工重放仍可能存在 → 两分支提交后确认，清理依明确重复窗口 |
| 原书／旧稿 · [9章时钟](ch09.md#two-clocks)、[GC](ch09.md#real-time)、[多数派](ch09.md#quorum-authority)、[隔离](ch09.md#fencing) | DST等于Unix时间跳变、过半天然安全、取得锁即保护资源 → API／JDK版本、协议规则与原页首次写要求 → 分清显示／时钟、持久投票、资源端原子屏障 |
| 原书／旧稿 · [10章共识](ch10.md#consensus-model)、[FAA](ch10.md#cas-and-fetch-add)、[提交](ch10.md#atomic-commit)、[读屏障](ch10.md#linearizable-reads) | timeout解决FLP、FAA无限参与者、2PC等同共识、心跳发出即可读 → 原论文模型与Raft条件 → 限定活性、FAA共识数2、全员准备和匹配确认／应用进度 |
| 原书／旧稿 · [11章对象存储](ch11.md#object-storage)、[恢复](ch11.md#fault-recovery)、[shuffle](ch11.md#shuffle)、[ML](ch11.md#machine-learning) | rename一概非原子、Flink批模式用检查点、M×R物理文件、token等于词 → 固定官方资料 → 按桶类型、执行模式、逻辑分区及tokenization／embedding区分 |
| 原书／旧稿及本站 · [12章有界](ch12.md#unbounded)、[保留](ch12.md#retention-replay)、[压缩](ch12.md#compaction)、[水位线](ch12.md#watermarks)、[恢复](ch12.md#checkpoints) | 已知文件大小才有界、至少22小时、对象日志自动Iceberg、多数才可见、屏障即完成 → 输入终点、容量前提、产品文档及恢复协议 → 逐项限定；有界输入措辞为本站第3轮修正 |
| 原书／旧稿 · [13章正确性](ch13.md#correctness)、[请求身份](ch13.md#request-id)、[支付恢复](ch13.md#payment-recovery)、[审计](ch13.md#cryptographic-audit) | 跨地域事务被排除、内容哈希即可去重、重放自动补齐、CT证明证书可信 → Spanner、意图反例、OLEP与RFC9162 → 分别限定事务能力、稳定ID、恢复责任及证明对象 |
| 原书／旧稿及时效补充 · [14章反馈](ch14.md#feedback-loops)、[跟踪](ch14.md#tracking-and-surveillance) | 定价摘要被扩成学习合谋机制、2025拟议和解当终局 → 摘要证据有限，FTC2026另有最终和解公告 → 保留证据缺口与后续状态，和解不等于法院事实判决 |

第5轮新增的整合澄清，是把支付模型、quorum阈值、保证作用域及删除后的重建限制并列说明；不将这些导航解释记成新发现的出版社勘误。来源折叠内仍保留历史核查日期和实际执行边界。

<a id="cross-book"></a>

## 12　跨书补充与阅读后的应用

以下是**跨书阅读补充**，不归为DDIA两位作者的章节内容，也不把其他书的术语强行换成本书定义。

- **George Fairbanks《Just Enough Software Architecture》**：[第3章风险驱动方法](../../just-enough-software-architecture/notes/ch03.md)。可与DDIA的[负载与测量](ch02.md#load)配合：先说明当前最重要的技术不确定性，再决定需要多深的模型或验证。风险驱动方法不是数据库一致性协议。
- **Neal Ford、Mark Richards、Pramod Sadalage、Zhamak Dehghani《Software Architecture: The Hard Parts》**：[数据所有权与事务](../../software-architecture-the-hard-parts/notes/ch09.md)、[八种Saga与补偿](../../software-architecture-the-hard-parts/notes/ch12.md)、[契约兼容](../../software-architecture-the-hard-parts/notes/ch13.md#compatibility)。它们补充服务和团队边界的权衡；Saga补偿是新的业务动作，不等于DDIA第8章数据库回滚，也不把第13章日志支付自动归为一个完整Saga实现。
- **Titus Winters、Tom Manshreck、Hyrum Wright编《Software Engineering at Google》**：[第2章团队协作](../../software-engineering-at-google/notes/ch02.md)。可与DDIA的[人的因素与可靠性](ch02.md#human-reliability)相互参照，理解为什么系统运行依赖团队沟通与可学习的事故处理；它不替代数据系统的故障模型。

实际应用时，可留下一个小而完整的判断：在明确负载和不变量下，谁接受事实，数据怎样传播，读者什么时候能看到，失败后由谁继续，哪些输入保留到何时。再从本页跳回一个正常过程和一个失败过程，检查所选机制是否覆盖这份判断。章节中的代码与算例以教学核对为限，不能替代真实产品的集成、性能、故障或社会效果验证。

<details id="sources">
<summary>本页来源、整合范围与验证边界</summary>

本页依据上述固定英文第二版、本站14章笔记及逐章覆盖核查报告整理，专题路线、术语对照、保证表与案例导航为本站整合。版本、原书正文页界及14章来源见[原文定位](#chapter-sources)；原书Glossary为印刷603—608／PDF627—632，其简写定义须与正文合读。

2026-11-07整合时重读Glossary六页，并针对跨章结论回看原文：权威／派生与数据责任（10—11、25），兼容和持久化执行（162、188—189），quorum限制（233—234），同事务去重（334—335），隔离令牌（375—376），线性一致与可串行化（407—408）、原子提交（432），批结果发布（480），快照／压缩与删除（505、512）、幂等（528），重处理（545）、请求身份（564）、多分片支付及及时性／完整性（569—572），用途限制（596）。图10-6、13-2另回看PDF印刷413、569原页；本页没有新增图示或改动章节图源。

各章外部来源与纠错对象保留原有归属和核查日期；本页不将历史核查记成本轮重新访问。跨书补充依据本站对应读书笔记，不是DDIA引用链。[作者参考文献仓库](https://github.com/ept/ddia2-references)用于定位原始材料；[出版社已确认勘误页](https://www.oreilly.com/catalog/errata.csp?isbn=9781098119065)在准备轮访问时显示无确认条目，不代表本书无错误。

本站14章保留机制推理、案例、失败路径和原有深度；“约原书正文三分之一”按这些内容的展开程度复核，不以中英文字符数相除判定。本页是索引，不能计入章节详解来补足篇幅。已有代码／数值验证的执行范围见章节来源；没有因本页整合而新增真实产品集成、分布式故障注入、协议证明或部署声明。

</details>
