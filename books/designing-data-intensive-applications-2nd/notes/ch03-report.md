# 第3章覆盖与核查报告

版本：Martin Kleppmann、Chris Riccomini，O’Reilly February 2026，ISBN 9781098119065。原文印刷65—114／PDF89—138，正文65—108。2026-11-07已完整读取 `originals/ddia2-ch03.txt`（2011行，含参考文献），随后完整读取只读旧稿（1349行）。不递归委派。

## 写作前原书小节覆盖表（交付时逐项完成）

| 原书小节／印刷页 | 成品锚点 | 已覆盖内容 |
| --- | --- | --- |
| 章首；Declarative Query Languages／65—66 | model-layers | 逻辑模型、API、存储三层；声明式保留执行自由 |
| Relational Versus Document Models／67 | relational-document | 关系模型定义、历史及NoSQL融合背景 |
| The Object-Relational Mismatch；Object-relational mapping／68—69 | relational-document | 对象映射、N+1、ORM收益及不可消除的成本 |
| The document data model for one-to-many relationships／69—71 | relational-document | 简历树、联表行数膨胀、一对少与一对大量 |
| Normalization, Denormalization, and Joins／72—73 | normalization | ID与名称、SQL连接、文档$lookup |
| Trade-offs of normalization／73—74 | normalization | 更新异常、派生数据与恢复责任 |
| Denormalization in the social networking case study／74—75 | normalization | 物化关系而非复制所有内容；hydration |
| Many-to-One and Many-to-Many Relationships／75—77 | relationships | 关联表、双向查询、单份关系及二级索引 |
| Stars and Snowflakes: Schemas for Analytics／77—79 | analytics-schema | 事实粒度、维度、星／雪花／OBT、金额聚合 |
| When to Use Which Model／80 | schema-locality | 嵌套条目标识、列表排序、访问模式 |
| Schema flexibility in the document model／80—82 | schema-locality | 读时／写时模式、迁移成本、混合结构 |
| Data locality for reads and writes／82 | schema-locality | 一起访问前提、部分读取／更新、非模型保证 |
| Query languages for documents／82—83 | document-query | 鲨鱼观测按月求和；SQL／MongoDB逐步结果 |
| Convergence of document and relational databases／83—84 | schema-locality | 关系和JSON组合；不按产品标签选模型 |
| Graph-Like Data Models／84—85 | property-graph | 邻接表／矩阵、异构实体、变长路径 |
| Property Graphs／86—88 | property-graph | 顶点边属性、入边出边、关系表映射、高元关系 |
| The Cypher Query Language／88—90 | cypher-sql | Lucy路径、零跳、模式与计划分开 |
| Graph Queries in SQL／90—92 | cypher-sql | 完整递归CTE、工作集、去重／环及标签一致 |
| Triple Stores and SPARQL／92—93 | triples-sparql | 主谓宾、字面量／实体、与属性图差异 |
| The Semantic Web；The RDF data model／94—95 | triples-sparql | RDF与编码分离、URI／空白节点、语义网遗产 |
| The SPARQL query language／95—96 | triples-sparql | 同一查询的路径表达、变量绑定与连接 |
| Datalog: Recursive Relational Queries／96—98 | datalog | 事实与规则、递归闭包、逐轮推理、固定点 |
| GraphQL／98—101 | graphql-api | API schema、聊天查询／响应、resolver成本边界 |
| Event Sourcing and CQRS／101—105 | events-cqrs；replay-boundaries | 命令／事件、会议座位、读投影、异步／重复／重建及外部副作用 |
| DataFrames, Matrices, and Arrays／105—107 | dataframes | 评分透视、缺失与零、稀疏存储、类别编码、数组 |
| Summary／107—108 | choosing | 模型选择回到查询／变化；其他专门模型简述 |

## 交付文件与统计

- `notes/ch03.md`：正文16节，5张数据／推导表，15个代码块；去除代码块和来源区后含 **12,561个汉字**（含标题、图注及表中文字），19,247个字符；全文25,545个字符。并非用统计替代覆盖审查。
- `chapters/ch03.html`：由同一Markdown生成；正文16节、5表、15代码块与3图。双端目录、面包屑、来源details、共享主题／reader脚本、章2→章3→章4翻页均已配置。
- 图示三组：`ch03-model-representations`、`ch03-location-paths`、`ch03-events-projections`。每组在`diagrams/sources/`保留`.skeleton.json`和原生`.excalidraw`，在`diagrams/exports/`保留官方API导出的`.svg`。原生场景分别29、34、18个元素，共81个元素。
- 独占制作工具：`diagrams/sources/ch03-build.py`（从Markdown生成本章HTML）、`ch03-check.py`（小数据验证）、`ch03-browser-check.mjs`（临时本地HTTP服务＋Chrome检查，结束自动关闭）。它们为本地制作工具，不是网页运行依赖。
- Excalidraw复用已准备的默认DDIA_TOOLS与原书共享导出工具，未安装额外工具链，未修改共享脚本；esbuild内存bundle无并行临时文件冲突。原生场景经官方`restoreElements`与编辑器API重载，并实际改字／恢复，通过可编辑性检查。

## 内容组织、保留案例与取舍

- 原书简历案例的核心论证保留，改用Lin／Mei、两组织和三条任职的笔记假设数据，解释嵌入、共享实体、关联表、双向索引与三种模型映射；补出多分支连接产生`2×2`行的具体原因。
- 规范化与时间线保留原书“只物化帖子／发送者ID、读取时hydrate”的历史实现，明确按原书转述，不声称调查X当前内部架构。
- 星型／雪花／OBT均覆盖，新增3条销售事实并固定“行金额、分为单位”的粒度；演示1800分与800分，补充维度唯一键和历史口径对结果的影响。
- 图查询以原书Lucy／Alain为主线：Lucy完整保留London→England→United Kingdom→Europe；法国路径明确为教学简化，不冒充原图。Cypher、完整递归SQL、Turtle／SPARQL、Datalog均解释中间推理；零跳、两条件绑定同一人、去重／环、固定点和计划选择均已展开。
- GraphQL保留聊天案例，提供缩小查询与完整响应。明确API结构、resolver执行、存储模型三者区别，以及响应冗余不等于持久化冗余。
- 会议事件案例保留命令验证、事实日志、多投影、可重建、顺序和外部输入；增加已写事件但视图滞后、位点与视图不同步、重复取消、并发超卖、重放邮件等失败路径，标为笔记展开。
- DataFrame评分pivot给出实际可运行数据，解释唯一坐标、缺失／0、稠密／稀疏、one-hot／multi-hot与多维数组。未扩写为机器学习教程。
- 不保留旧稿生产产品速查表、面试题、大量重复代码及无依据选型门槛。原书历史产品／工具名称只保留解释模型所需者；RDF/XML冗长编码、次要查询语言、全部参考文献逐条介绍未重列。Codd非简单域脚注不展开为关系理论专题。

## 原图与异常提取回看

实际渲染并查看固定PDF中的以下原页，不仅检查提取文本：

| 印刷页／PDF | 核对内容 |
| --- | --- |
| 70／94 | 图3-1关系履历及例3-1 JSON；用户／任职／教育／地区边界 |
| 71／95 | 图3-2一对多树，确认一对少限制 |
| 76／100、77／101 | 图3-3、3-4关联表及跨文档引用，箭头含义与文档边界 |
| 78／102 | 图3-5星型结构、事实列及外键；本文另用明确金额语义的自拟数据 |
| 86／110 | 图3-6Lucy／Alain；确认England及法国中间行政层级，本文明确何处简化 |
| 90／114、91／115 | 例3-6递归SQL；`Location`与`location`确实不一致，非提取错误 |
| 98／122 | 图3-7Datalog逐轮产生闭包，确认零跳基础规则与推导顺序 |
| 99／123 | GraphQL“不允许昂贵操作”原句及查询，确认原文表述过强 |
| 102／126 | 图3-8事件源与多个读模型，确认不代表共同事务或强制同步更新 |
| 106／130 | 图3-9评分矩阵与NumPy稀疏数组举例；确认缺失坐标及原文表述 |

原页PNG仅保存在批准的临时目录`.../T/opencode/ddia2-ch03/`，不发布原书图。本站三张图是教学重组，不复刻原书图全部数据。

## 纠错与边界记录

以下均在正文就地解释，出版社未确认者不称为官方勘误。

| 对象与原表述 | 问题及依据 | 本章修正 |
| --- | --- | --- |
| 旧稿座位代码：500，订3、订5、取消3，输出497 | 算术及实际执行结果为495 | 表、代码和图统一为495，并展示500→497→492→495 |
| 原书例3-6／90—91页：同类地点标签分别写`Location`和`location` | PDF确有混写，普通区分大小写文本比较不等价 | 记录不一致；教学SQL用独立地点表与统一样本 |
| 原书99页及旧稿：GraphQL不允许昂贵操作，限制递归即可避免昂贵查询 | 官方Demand control列出深度、宽度、分页、成本分析；resolver自身也可能昂贵 | 区分没有任意长度递归路径与允许有限嵌套；成本需显式管理 |
| 原书106页／旧稿：NumPy作为稀疏数组库，DataFrame轻松处理宽矩阵 | 普通NumPy ndarray为稠密；SciPy提供专用稀疏结构，pivot也可能占用大量内存 | 区分逻辑矩阵、缺失语义与稀疏表示，不将转换视作免费 |
| 旧稿：文档更新要整篇重写、嵌套项不能有独立引用 | 将常见实现／默认寻址方式误当模型绝对限制 | 给嵌套任职ID；说明实际读写单位与引用保证取决于系统 |
| 旧稿：事件入日志时视图同步更新 | 原书允许独立读模型与下游追赶，没有共同提交保证 | 明确异步滞后及消费位点与视图提交的故障窗口 |
| 旧稿：销毁密钥即等于删除、重放时关闭副作用即可 | 派生副本／备份、已解密信息和实时重试仍需处理 | 不作法律合规保证；区分纯投影、重放与外部幂等责任 |
| 旧稿：数仓数据不可变，更新一致性问题基本不存在 | 历史更正、迟到数据和维度变化仍会改变查询口径 | 限定更新压力通常较小，要求说明当时／当前维度 |
| 旧稿：多对多就图、4行比31行意味着量级优势 | 关系模型直接支持多对多；代码行数不是性能证据 | 用变长路径／异构关系及实际查询需求讨论图的收益 |
| 旧稿：GraphQL客户端加字段即服务端零修改 | 只有字段已暴露在schema时成立 | 明确接口能力边界；失败时也不保证返回全部字段值 |

## 外部依据（2026-11-07实际读取）

1. PostgreSQL 18，`WITH Queries`：<https://www.postgresql.org/docs/18/queries-with.html>。本次通过current入口取得18版内容，核对递归工作表、UNION、环检测和SEARCH排序；来源区采用固定18版链接。
2. GraphQL，Security／Demand control：<https://graphql.org/learn/security/>。核对深度、宽度、分页与复杂度控制，作为原书过强表述的修正依据。
3. Pandas，DataFrame.pivot：<https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.pivot.html>。核对重塑而非聚合、重复坐标报错；本机实际执行版本2.3.3，不将网页版本当作本机版本。
4. SciPy，Sparse arrays：<https://docs.scipy.org/doc/scipy/reference/sparse.html>。核对CSR／COO等稀疏结构及其与NumPy的区别。

其余技术主线以实际通读原书为依据。没有为未访问的原书参考文献制造“已阅读”记录。

## 实际验证

### 内容与代码

`python3 diagrams/sources/ch03-check.py`（从本书目录执行）通过：

- SQLite 3.51.0实际运行正文通用SQL：地区连接结果`(7, Lin, 杭州)`；销售按类别汇总乳品1800／烘焙800分；完整递归SQL返回Lucy。
- 对递归SQL补两个直接相关边界：出生／居住直接指向根地点时零跳匹配；ID-only `UNION` 在增加一条环边后终止且结果正确。不据此声称任意携带深度的递归都安全。
- Datalog两条正向闭包规则以Python集合求固定点，新事实轮次为7、4、1，确认Idaho→North America、London→Europe及Alain出生条件不成立。**没有运行Datalog产品引擎。**
- 正文事件Python原样执行，四个前缀结果500／497／492／495，完整重放一致；重复取消的增量算术495+3=498已复核。
- Pandas 2.3.3原样执行评分pivot，验证缺失值、已知均分4、补零均分8/3与重复坐标`ValueError`。
- 海洋观测通过Python小数据复算1月5／2月1；**未运行PostgreSQL日期函数或MongoDB聚合服务**。两者语法按原书示例及UTC约定编写。
- JSON代码块全部解析通过；原生Excalidraw每条文字与对应SVG逐行匹配，三份SVG XML解析通过。
- Cypher、SPARQL、GraphQL未连接相应服务端运行；图查询已按同一小数据和关系闭包核对语义，不声称已做产品集成验证。

### 页面与资源

- Markdown与HTML **16节逐节规范化全文文本匹配**，包括示例、表、图注；来源由同一内容源生成。
- 检查63条页面引用：本地文件均存在、HTML目标锚点存在，无重复ID；无指向PDF、originals、notes或图源的网页链接。无构建步骤，本次为静态生成与检查，不虚称框架构建。
- Chrome实际运行 **1440px／375px × 浅／深色** 四组：正文16px、行高31.2px、16节、3图，图像全部加载，无页面横向溢出，无JS／HTTP错误；宽代码、表格、图像保持局部滚动。
- 实际点击手机目录与来源details；手动切深色、刷新后localStorage及页面主题均保存。浅／深系统偏好各自截图确认。
- 实际目视桌面浅色、手机深色首页，关系／文档／图浅色图、地点路径浅色图、事件投影深色图：文字、线条、箭头均无裁切或遮挡。源码与官方导出保持对应。
- 浏览器检查首次因测试脚本等待未进入视口的懒加载图片`decode()`而超时，随后仅将检查脚本中图片临时设为eager，四组通过；页面懒加载行为没有修改。此为验证脚本问题，不是页面资源加载失败。
- 截图与`browser-results.json`保存在`/private/var/folders/5k/y6qh6sfd2g30js0v0qrv4mfr0000gn/T/opencode/ddia2-ch03/`，HTTP服务与Chrome均已退出。

## 交接与遗留

- 第1—4章仅链接本轮页面，其他章节只有文字提示；章3上翻第2章、下翻第4章。共享书籍概览、书架、README、PLAN及CONTINUE交由主Agent整合，本Agent未改动。
- 无资料缺口、图示工具阻塞或已知未解决内容问题。产品服务端集成未做，范围已如实列明，不影响静态笔记交付。
- 当前为主审前成品；需要主Agent依计划通读审稿并维护整体制作状态。交付返回后停止编辑，不自动继续其他章。

## 主Agent接管补记（2026-11-07）

四位负责人全部返回后，主Agent通读本章并修正一处术语：原稿“社交图、网页图和道路图只是同构例子”容易与数学上的图同构混淆；原书印刷84—85的homogeneous data指各例内部顶点／关系类型同质，已改为“同质数据”并解释区别。运行`ch03-build.py`同步HTML；复跑`ch03-check.py`以及全轮内容／资源和浏览器检查通过。修正后按来源前去围栏代码、保留图注／替代文本等统一口径为12,589汉字。原始交付统计保留以区分负责人交付与主审后状态。
