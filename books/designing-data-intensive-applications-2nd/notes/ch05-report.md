# 第5章交付报告（已完成，返回后停止编辑）

负责人：第2轮A，仅第5章；不递归委派。日期2026-11-07。

已先读根AGENTS、PLAN、CONTINUE及本书README；本书没有独立CONTINUE，交接以根文件为准。已完整通读原文 `originals/ddia2-ch05.txt` 1431行（含参考文献），再完整对照只读旧稿818行。依据固定PDF：Martin Kleppmann、Chris Riccomini，O’Reilly February 2026，正文印刷161—192／PDF185—216，含参考文献至196／220。

## 写前原书小节覆盖表与最终对应

以下表在正文前落盘，正文完成后保持15节对应；最终各行均已覆盖。

| 原书小节／页码 | 最终笔记位置／锚点 | 已保留的机制与案例 |
| --- | --- | --- |
| 章首161—163、图5-1 | 01 compatibility | 滚动升级、离线客户端；两向读写、API请求／响应方向；读改写丢未知字段 |
| Formats for Encoding Data 163—164；Language-Specific Formats 164—165 | 02 representations | 内存／字节、编码与可串行化；零拷贝例外；语言绑定、安全、长期演化 |
| JSON, XML, and Binary Variants 165—167；JSON Schema 166—167 | 03 json-contract | 大整数、Base64、文本交换；开放／封闭模型、数字字符串键例子 |
| Binary encodings 167—169；图5-2 | 04 bytes | Martin／1337／两个兴趣；81与66字节构成、fixstr位数 |
| Protocol Buffers 169—170；图5-3 | 04 bytes | tag、wire type、varint逐字节、33字节；int64／sint64修正 |
| Field tags and schema evolution 171 | 05 protobuf-evolution | 新增／删除／reserved／改名／扩宽；未知字段与转换链 |
| Avro 172—173；图5-4 | 06 avro-resolution | 无tag、32字节、union索引、ZigZag与数组结束标记 |
| The writer’s schema and the reader’s schema 173—174；图5-5—5-6 | 06 avro-resolution | 按writer读取，按reader投影；重排、忽略、填默认 |
| Schema evolution rules 175 | 07 avro-evolution | 双向新增／删除条件；alias／union／类型提升；null默认值版本差异 |
| But what is the writer’s schema? 175—176 | 07 avro-evolution | 文件头、逐记录schema ID、连接协商与历史schema寿命 |
| Dynamically generated schemas 176—177；The Merits of Schemas 177—178 | 08 schema-value | 数据库导出动态生成；稳定编号成本；schema文档／代码生成／检查边界 |
| Modes of Dataflow／Dataflow Through Databases 178—179 | 09 database | 多进程两向兼容、数据比代码长寿 |
| Different values written at different times／Archival storage 179—180 | 09 database | 五年前与五毫秒前、逻辑／物理schema、迁移与归档 |
| Dataflow Through Services: REST and RPC 180；Web services 181—183 | 10 services | 封装、HTTP／REST／IDL、OpenAPI与实现／客户端生成关系 |
| The problems with remote procedure calls 183—184 | 11 rpc-failure | 超时两种世界、重复副作用、延迟／参数／语言差异 |
| Load balancers, service discovery, and service meshes 184—186 | 11 rpc-failure | 发现与均衡区别、DNS缓存、注册与代理、mesh不解决业务幂等 |
| Data encoding and evolution for RPC 186 | 10 services | 服务端先升级的前提、请求／响应兼容与长期API版本 |
| Durable Execution and Workflows 187—189；图5-7、例5-5 | 12 durable-execution、13 durable-boundary | 调度／执行；正常历史、重放、未记录完成的活动重试；幂等键、确定性、旧实例版本 |
| Event-Driven Architectures 189—190；Message brokers 190—191 | 14 messages | 缓冲与确认边界、队列／主题、重投、保留与未知字段 |
| Distributed actor frameworks 191 | 14 messages | 单actor状态、异步消息、位置透明与演化 |
| Summary 191—192 | 15 conclusion | 用实际数据流复核版本、字段与失败语义；衔接复制与事务 |

## 交付文件与规模

全部项目写入限定于本章所有权，共16个文件：

- `notes/ch05.md`：15节，正文汉字粗计11,861（主Agent按来源区前、去围栏代码、保留标题／表格／图注／替代文本统一复计；初报11,863），1张正文表，5个代码／说明块。略超最初8—11千估计，增加部分用于逐字节推演、四处原书技术修正和持久化执行失败边界，没有补产品目录凑长。
- `notes/ch05-report.md`：本报告，含写前覆盖表、核查、旧稿取舍及交接。
- `chapters/ch05.html`：与Markdown同步，15个语义section、双端目录、来源折叠、主题开关、上一章ch04、下一章ch06。
- 三组 `diagrams/sources/ch05-{compatibility,avro-resolution,durable-boundary}.excalidraw`：真实原生元素63个（分别19／18／26），可编辑。
- 对应三组 `diagrams/exports/ch05-*.svg`：官方Excalidraw导出，附主题／无障碍信息；三图分别回答兼容方向、Avro双模式投影、完成记录与副作用边界。
- 三份 `diagrams/sources/ch05-*.skeleton.json`：初次生成的简写定义；已有场景修改时应从.excalidraw重新导出，不用旧skeleton覆盖。
- `diagrams/sources/ch05-diagrams.mjs`、`ch05-render.py`、`ch05-check.py`、`ch05-verify.mjs`：本章制作／验证工具。网站不依赖这些工具运行。

复用共享 `export-excalidraw.mjs`／`excalidraw-browser.js`，没有修改共享工具、其他章节、README／PLAN／CONTINUE或外部旧稿。参考了三本书指定笔记，并沿用已完成第4章页面外壳。

## 保留、修正与舍弃旧稿

### 保留并展开

- 新旧代码共存的原因、读写两向兼容、API请求和响应方向。
- 原书Martin／1337／两个兴趣的81、66、33、32字节记录，补上完整分组与字节复算。
- 字段编号、reserved、未知字段、32→64位扩宽；Avro writer／reader schema、默认值、别名与动态导出。
- “给未来的自己发消息”、数据比代码长寿、逻辑模式与历史存储、归档。
- REST／RPC、IDL与实现、服务发现与负载均衡、持久化执行、消息与actor。
- 支付风控→扣款→入账与拒绝分支，进一步区分完成已记录和完成报告丢失两条路径。

### 纠错记录（正文就地保留原表述→依据→修正）

| 对象／原表述 | 依据与问题 | 修正解释／正文 |
| --- | --- | --- |
| 原书168及旧稿：fixstr高4位类型、低4位长度 | PDF确有该文字；MessagePack规范为101xxxxx | 低5位长度，0—31；b8代表24，不是8。04 |
| 原书170及旧稿：示例int64的−64—63一字节 | 原图1337确为b9 0a；Protobuf规范区分int与sint | int64负数值编码10字节；该对称范围属于ZigZag sint。04 |
| 原书图5-6：writer union(null,long)→reader union(null,int) | 回看174原图；Avro1.12只允许规定方向提升，long不能缩int | 实际long分支即使1337也不支持；本文原创图两侧用long。06 |
| 原书175及旧稿：null必须为union第一分支才可default null | 本章引的Avro1.12.0规范允许默认值匹配union的相应分支 | 使用null-first写法便于旧工具，但不当作1.12通用限制。07 |
| 原书188广义“跳过任务此前所有成功RPC”，旧稿“不会再扣一次” | 原书189已要求幂等；Temporal活动文档明确未报告完成会重试，活动内部步骤会整体重跑 | 历史已确认完成的活动才复用结果，外部效果另靠幂等协议；非共同原子提交。13 |
| 旧稿：Protobuf／Avro都自动保留未知字段 | Avro Schema Resolution定义忽略；Protobuf转JSON也会丢失 | 区分可读、投影和无损读改写；保留整条记录需完整转换链。05—06 |
| 旧稿：响应新增字段、旧客户端忽略是向后兼容 | 本章按写者／读者方向定义 | 该响应是新写旧读，即向前兼容；还须旧校验允许字段。10 |
| 旧稿：竞争消费者之一收到，故每条只处理一次 | 原书190强调配置／投递语义不同 | 正常分配不排除故障重投和重复副作用。14 |

另在正文限定大整数为“不再能精确区分全部整数”，避免“所有>2⁵³均不能表示”及“JS只有double”绝对说法；限定tag改名的二进制／JSON边界、动态生成不等于任意变更兼容、LSM不自动理解不透明value的业务格式、服务端先升级为假设而非普遍事实、网格不处理业务幂等。

删除旧稿的生产产品大全、面试题、重复总览图与“Avro在Kafka完胜／最佳”等未经论证的排名；压缩ASN.1历史、RPC旧产品清单及服务框架代码，把字数用在机制上。未沿用含未定义`order_id`且无完整契约的Stripe请求片段；以明确标注的工作流伪代码说明稳定业务键，不冒充可运行支付实现。

以上原书纠错均为笔记依据规范所作修正，不宣称出版社已确认勘误。

## 实际阅读、外部核查与原图

- 原文1431行、旧稿818行完整读取；正文161—192与参考文献193—196已区分。
- PDF实际渲染并查看印刷163、168、170、173、174、175、187、188、189，分别为PDF187、192、194、197、198、199、211、212、213，覆盖全部原图5-1—5-7、字节图和歧义句。
- 实际读取MessagePack规范、Protobuf Encoding与proto3指南、Avro1.12.0规范相关部分、JSON Schema Objects、Temporal Activity Definition与Workflow Definition。正文来源区含链接、用途与2026-11-07核查日期；没有把旧稿文献号直接复制成已读文献。
- 图5-1依据章首兼容方向原创；图5-2重构原图5-5／5-6并修正类型；图5-3依据原书187—189与Temporal文档解释两种失败点，非原图复刻。

## 实际验证与结果

### 编码／兼容的最小执行验证

运行 `python3 diagrams/sources/ch05-check.py` 通过，依赖仅安装于临时 `ddia2-tools/ch05-python`：protobuf6.33.0、msgpack1.1.2、fastavro1.12.1、jsonschema4.25.1。它是小记录库级验证，不是服务或集群测试。

- 紧凑JSON81、MessagePack66、Protobuf33、Avro32字节均实际编码一致；Protobuf与Avro完整期望字节序列断言通过。
- MessagePack `b8` 的24字节字符串；Base64的300→400和1→4复算通过。
- Protobuf int64(-1)值部分10字节、sint64(-1)值部分1字节；2³²+1读入int32得到1。
- 新Protobuf读旧记录email为空；旧读者读新记录、改数字、写回仍保留email；转JSON再还原丢失email，验证转换链边界。
- Avro新增默认、旧读者忽略新字段、字段重排／投影、缺默认失败；原图long→int在1337值下也拒绝，均通过。Avro1.12 union默认值条目以规范核查为依据，没有把fastavro版本等同Apache Avro版本。
- JSON Schema数字字符串键、前导0、错误键、错误值示例通过。
- Chrome实际执行JSON.parse，9007199254740993舍入为9007199254740992；9007199254740994保持精确。

### 图源与静态内容

- 三图由官方@excalidraw/excalidraw0.18.0 API生成；每图保存后重新从.excalidraw加载到真实编辑器，修改一段文字并恢复，返回editable=true。
- 63个原生矩形／文本／箭头，无嵌入截图；JSON与SVG可解析，所有场景文字与SVG对应。
- 15节完整规范化正文、引言、代码／表格／图注与来源区MD／HTML匹配通过；三个图像alt、语义结构、无重复ID、来源折叠与前后页目标核对。
- 页面36个唯一href/src引用中，已有本地目标与锚点通过；同轮ch06.html、ch08.html在验证时尚未落盘，依用户授权预链接，报告为待主Agent接通，未伪报所有链接通过。
- 本站是原生静态页面，无编译步骤，没有虚构构建命令。网页没有引用notes、originals或sources。

### 浏览器与视觉

- 实际运行本章Chrome：1440px桌面／375px手机 × 系统浅色／深色，共4组。全部整页无横向溢出、正文16px／31.2px行高、15节3图、没有捕获JS／HTTP错误。
- 双端目录实际点击定位、来源折叠、手动反向切换主题并刷新保存均通过；手机图示容器333px、内部560px局部滚动，整页仍375px。
- 三幅独立SVG各浅／深色，共6组，无越过SVG边界的文字；实际查看三张代表图、手机深色正文、桌面浅色正文、手机浅色工作流图截图，线条、标签和图注清晰。
- 临时验证服务器在脚本finally中关闭；无后台写作／服务任务。

结果位于 `/private/var/folders/5k/y6qh6sfd2g30js0v0qrv4mfr0000gn/T/opencode/ddia2-tools/`：`ch05-check-results.json`、`ch05-browser-results.json`、`ch05-reader-*`、`ch05-workflow-*`、`ch05-diagram-*`及`ch05-original-*`截图。

## 未解决问题与跨章交接

- 无本章内容、原文或绘图阻塞。唯一接入待办：主Agent在同轮完成后确认ch06与ch08引用，并把第4章下一页改到ch05；本人未修改第4章或共享导航。
- 章间链接：第4章存储与检索→本章；正文连接第8章可串行化／事务与幂等；下一章第6章复制。第9、12章未制作，只保留文字提示，没有提前创建链接。
- 未运行Temporal、支付网关、REST服务、消息代理或actor集群，没有真实故障注入、性能基准或分布式恰好一次证明；工作流正常／失败流程是有官方依据的机制推演。
- 原书尚未提供完整支付补偿、模式治理或所有客户端升级条件，正文保留这些边界；不把假设流程当作真实实施结果。
- 主Agent接管后若改正文，运行`ch05-render.py`同步HTML；图源改动从相应.excalidraw导出。四位负责人都返回后再统一接入与审稿。

本章已完成；返回后停止编辑，不继续制作其他章节。

## 主Agent整合完成（2026-11-07）

四位负责人全部返回并停止编辑后，主Agent已通读本章及来源、回看编码／兼容原页，以官方规范与Temporal资料复核关键纠错，并复跑`ch05-check.py`通过。第6／8章引用及4→5已接通；概览、书架为8／14。接入后10页链接／锚点、本轮73节及来源双端全文匹配、19组图源／导出检查通过；Chrome52组及正反翻页通过，本章3图已目检。上文作者时点的接入待办已关闭，其原始验证范围保留。全轮证据见本书README和根CONTINUE；无新增阻塞或后台写作任务。
