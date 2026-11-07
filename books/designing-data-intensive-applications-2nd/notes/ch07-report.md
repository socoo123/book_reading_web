# 第7章分片 · 覆盖与交付报告

## 写作前覆盖表（2026-11-07）

已先完整阅读 `originals/ddia2-ch07.txt`（含References，913行），再完整对照只读旧稿 `/Users/zy/ai_learn/ddia_2nd/ch07-分片.md`（1041行）。固定英文第二版：Martin Kleppmann、Chris Riccomini，O’Reilly February 2026；本章正文印刷251—272／PDF275—296，参考文献273—275，276空白。

| 原书小节 | 印刷页 | 计划笔记锚点与展开 |
| --- | --- | --- |
| 章首；Sharding and Partitioning | 251—253 | `shards-and-replicas`：逻辑归属、物理副本、节点可持多片、术语 |
| Pros and Cons of Sharding | 253—254 | `scaling-boundary`：容量、吞吐、局部性、跨片事务与单机分片 |
| Sharding for Multitenancy | 254—255 | `multitenancy`：七类收益、三类限制，租户与个人区分 |
| Sharding of Key-Value Data；Sharding by Key Range | 255—257 | `range-and-compound`：百科边界、传感器时间热点、复合键 |
| Rebalancing key-range sharded data | 257—258 | `range-splitting`：预分裂、拆分合并、分裂与迁移分开 |
| Sharding by Hash of Key；Hash modulo number of nodes | 258—259 | `hash-and-fixed`：稳定哈希、0—11取模手算 |
| Fixed number of shards | 259—261 | `hash-and-fixed`：12片／3→4节点、粒度／恢复／重分片 |
| Sharding by hash range；Partitioning and Range Queries in Data Warehouses | 261—263 | `hash-range-and-consistent`：哈希范围、分区与片内排序、虚拟范围 |
| Consistent hashing | 263 | `hash-range-and-consistent`：最少移动、环区间小例、非副本一致性 |
| Skewed Workloads and Relieving Hot Spots | 263—264 | `hot-keys`：数据／请求倾斜、隔离与拆写、读放大 |
| Operations: Automatic Versus Manual Rebalancing | 264—265 | `migration`：自动／人工权衡、级联失效、假设协调迁移时序 |
| Request Routing | 265—268 | `routing`：三条路径、权威映射、过期路由、共识／gossip、分析查询 |
| Sharding and Secondary Indexes；Local Secondary Indexes | 268—270 | `local-index`：二手车、局部写、scatter-gather、尾延迟 |
| Global Secondary Indexes | 270—271 | `global-index`：词项分片、ID→记录第二跳、多条件交集、跨片更新 |
| Summary | 271—272 | `design-check`：将分片键、热点、迁移与索引代价连成判断，衔接第8章 |

优先保留传感器和二手车原书案例；压缩词源、历史新闻、产品清单与默认值。旧稿的环形例、取模例有教学价值，但区间方向和统计前提须修正。迁移将明确为笔记假设协议，不把双写＋回填写成通用正确方案。

## 交付状态与文件

**已完成，交还主Agent后停止编辑。** 本会话仅负责第7章，未递归委派，未修改共享文件、其他章或外部旧稿。上述覆盖表所有核心项已完成，锚点保持不变。页面入口：`chapters/ch07.html`。

共19个本章文件：

- `notes/ch07.md`：正文与来源。
- `notes/ch07-report.md`：本报告。
- `chapters/ch07.html`：静态阅读页。
- `diagrams/sources/ch07-{fixed-shards,migration,local-index,global-index}.excalidraw`：4份原生场景。
- 同stem的 `diagrams/sources/*.skeleton.json`：4份简写输入。
- 同stem的 `diagrams/exports/*.svg`：4份官方导出。
- `diagrams/sources/ch07-diagrams.py`：创建本章简写图源；已有场景如手工修改，应从`.excalidraw`导出，避免由skeleton覆盖。
- `diagrams/sources/ch07-build.py`：从本章MD生成HTML，复用ch01外壳及共享CSS／JS。
- `diagrams/sources/ch07-verify.py`：小数据与静态内容核对，使用Python标准库及已有markdown包。
- `diagrams/sources/ch07-browser.mjs`：Chrome阅读与SVG验证，临时HTTP服务在结束时关闭。

统计：**13节，4图，1张正文表，1个说明性text代码块；正文汉字8,080。** 汉字口径与第一轮一致：来源区前、去围栏代码、保留标题／图注／表格／替代文本，不机械换算英文词数。略超过初估8千上界，主要用于迁移的正常／迟到请求顺序及就地纠错。页面正文16px、行高1.95、720px最大行宽，双端目录、来源折叠、面包屑、前后章导航齐全。

### 图示与原书对应

| 笔记图 | 主题／原书对应 | 原生元素 |
| --- | --- | ---: |
| 图7-1／fixed-shards | 12个分片、3→4节点，键到分片不变；对应原图7-4及259—261页 | 23 |
| 图7-2／migration | 快照40→增量48→交接资格；依据260、265—267页问题作假设展开 | 25 |
| 图7-3／local-index | 两个数据片及本地索引的scatter-gather；对应原图7-9 | 19 |
| 图7-4／global-index | 索引取ID后再按ID跨片取记录；对应原图7-10及271页 | 21 |

合计88个原生矩形、文本、绑定箭头元素。均复用共享工具，使用Excalidraw 0.18.0官方convert／export／restore及实际编辑器API；每份保存场景都重载、改字、恢复，输出`editable:true`。四图均有图例、读法、alt、独立大图入口、浅深主题及手机局部滚动，没有仅画SVG冒充场景。

## 原书、旧稿与补充的处理

### 完整阅读与回看

- 先读根AGENTS、PLAN、本书README、CONTINUE，再通读分章913行原文与1041行只读旧稿；写作前覆盖表先落盘。
- 实际渲染并查看印刷252、256、258—263、266—267、269—271共13页，覆盖全部原图7-1—7-10；核对16位哈希值域、范围边界、复制与分片、迁移路由、全局索引的两段读取。
- 原书印刷258第二段的`Unfortunately`在收益语境里不协调，正文按分片数随数据量适应的机制说明，来源区记录语词疑点；没有把它误解为额外技术缺陷。
- 写作参考已读Google ch02、JESA ch03与ch02阅读外壳、Hard Parts ch09；核对本站DDIA ch01—04页面外壳，采用现有文章式解释与就地纠错。

### 保留

- 原书复制／分片区分、多租户七类收益及三类限制，传感器范围查询／时间写热点，固定分片的两层映射，热键拆写的读代价，三种路由方式，以及二手车本地／全局索引。
- 旧稿的取模手算、环形小例与分片大小权衡有解释价值，重写为有明确前提的少量键算例；没有直接移植旧稿Mermaid、Obsidian链接及产品清单。

### 修正与限定

| 对象／原表述 | 问题与依据 | 本章处理 |
| --- | --- | --- |
| 原书258页及旧稿：分裂须全量重写新文件 | HBase官方实现段说明先建父文件引用、后续压缩合并 | 就地保留原表述→依据→“是否立即重写依实现” |
| 旧稿：MongoDB `{sensorId,timestamp}` 只有sensorId定片 | 官方完整复合键值空间可按范围划分 | 区分完整复合分片键与分片键＋排序键模型 |
| 旧稿：“几乎所有键都搬”“加一个节点约75%” | 75%只适用于所列3→4及均匀条件，不能泛化 | 0—11全部列出；9/12对比固定分片3/12 |
| 旧稿：2048适合多种非二次幂节点数 | 2048的因子只有2的幂 | 明确整除是分配粒度便利，非硬条件 |
| 旧稿图：插入标记之后的键转新节点 | 顺时针取首个标记规则下方向相反 | 新标记550接管401—550；150/1024并不均分负载 |
| 旧稿：jump O(1)时间／零内存 | 原论文1—6页：预期循环<ln(n)+1；仅不需持久映射结构 | 明确预期O(log n)、常数额外空间及连续桶约束 |
| 旧稿：双写＋回填＋灰度切读是通用零停机迁移 | 独立双写部分失败、回填覆盖新值、旧在途写未处理 | 假设快照／有序日志／屏障／新代次协议，允许切换等待 |
| 旧稿：全局索引无尾延迟放大、吞吐随分片增加 | 原书271页明确多词项与回表仍可能跨片 | 单词项取列表与端到端取记录分开；保留热点与异步滞后 |
| 旧稿：云自动热管理等同透明应用加盐 | 原书明确不展开内部细节，不能据名称等同 | 只保留自动调整的动机，不代入未经证实机制 |

另限定“读瓶颈加副本即可”、租户分片等同完整法规实现、任意分片即可给出部分查询结果、无主库无条件容忍冲突位置表等过强说法。原书中的自动管理产品／默认分片数、Scylla vnode版本差异、公司规模和历史新闻未作为当前操作指南重现，不另造事实。

### 实际外部核查

日期2026-11-07。正文来源details含可访问链接及用途：

1. Apache HBase官方参考指南，`RegionServer Splitting Implementation`；返回legacy页面、4.0.0-alpha-1-SNAPSHOT，明确只作为“并非所有分裂都当场全量重写”的实现反例，不当作当前稳定版全流程说明。
2. MongoDB官方`Shard Keys`页面，完整复合键与不重叠键范围；不声称运行了对应服务端。
3. Lamping／Veach 2014 jump论文PDF 1—6页，包含原算法、环映射、连续编号限制和Performance Analysis；HTML入口404后改读原PDF，依据已取得。
4. AWS DynamoDB GSI官方文档，投影字段、索引读取和异步同步段；未把本章抽象索引片解释成该托管服务所有内部实现。

## 实际验证

### 数值与操作小例

运行 `python3 .../diagrams/sources/ch07-verify.py`：

- 哈希0—11从模3到模4，9条移动；固定12片只迁S3/S7/S11，四节点各3片；hash=15始终在S3，owner从0变3。
- 环0—1023加入550，只移动401—550共150个位置，分布424/300/150/150，比例0.146484375。
- A传感器10:00—10:02范围读数[21,22]；1500写/5桶=300，200次全量读产生1000次子读请求。
- 本地红车列表D0=[101]、D1=[501]；全局red∩Honda=[501]；红车原记录涉及D0和D1；异步改色不等于索引即时更新。
- 迁移模型先装位点40快照，再顺序应用41—48更新与删除；B到47或A未停写均不能切换；B到48且旧写停止才具备切换条件；新代次不接受A旧资格。此为显式假设下的内存模型，**不是实际分布式协议／故障恢复证明**。

### 内容与静态资源

- 13节正文、导读、代码、表格、全部图注和来源区规范化全文MD／HTML匹配。
- 54项当时可用本地引用／锚点检查通过；无重复ID，图像均有alt，HTML不链接notes／originals／sources／PDF。
- **同轮`ch06.html`、`ch08.html`在本次核对时尚未落盘，按任务保留前后链接，明确列为主Agent整合后需补验项。** 未把它们报告为已经通过。
- 4份JSON场景与SVG XML及全部文本对应通过，共88原生元素；1个说明性text块不冒称产品SQL执行。
- 第一次静态检查因本机无bs4停止，已将检查器改用标准库HTMLParser，随后通过；未新增网站或全局Python依赖。

### 页面与图示

运行 `node .../diagrams/sources/ch07-browser.mjs`，本机Google Chrome：

- 1440px桌面／375px手机 × 浅／深色，共4组页面检查通过。
- 系统主题跟随、手动主题选择与刷新保存、桌面／手机目录跳转、来源details打开通过。
- 正文16px／31.2px行高；页面宽度分别1440／375，无整页横向溢出；手机图容器333px、图像最小560px，在图内局部滚动。
- 四个独立SVG各浅／深色共8组，主题文字颜色及所有文字边界检查通过，无裁切。
- 页面捕获的JS／HTTP错误为0，四图均完成实际加载。人工查看全部四图（含深色迁移图）、桌面浅色与手机深色阅读截图，连线与文字无碰撞、流程方向正确。
- 验证输出／截图位于临时工具目录`.../T/opencode/ddia2-tools/`：`ch07-static-results.json`、`ch07-browser-results.json`、`ch07-reader-*.png`、四图stem的浅深色PNG。临时HTTP服务和浏览器已关闭。

站点为静态HTML，不存在部署构建命令；仅执行本章制作渲染与上述验证，没有声称编译／部署成功。

## 遗留、衔接与停止

- 本章内容／图示无已知阻塞。主Agent待四人全部返回后接管，需将本章接入概览、进度和翻页，并在第6／8章落盘后复核`ch06.html`、`ch08.html`链接。
- 上接第6章复制及复制延迟，下接第8章跨片原子性／事务；已完成第2、4章有链接。第9／10／11章只作文字提示，无未来章失效链接。
- 没有运行真实MongoDB、HBase、DynamoDB服务，未作实际集群迁移、数据库并发／网络故障注入或吞吐基准；范围明确保留。没有通读本章33篇参考文献。
- 已保留全部源文件与可重跑工具；所有文件仅在本章所有权范围，外部旧稿只读。**本章交付完成，返回并停止编辑。**

## 主Agent整合完成（2026-11-07）

四位负责人全部返回并停止编辑后，主Agent已通读本章及来源，回看分裂与索引原页，以HBase官方实现复核无需立即全量重写的反例，并复跑`ch07-verify.py`通过。第6／8章引用与6→7→8已接通；概览、书架为8／14。接入后10页链接／锚点、本轮73节及来源双端全文匹配、19组图源／导出检查通过；Chrome52组及正反翻页通过，本章4图已目检。上文作者时点的接入待办已关闭，其原始验证范围保留。全轮证据见本书README和根CONTINUE；无新增阻塞或后台写作任务。
