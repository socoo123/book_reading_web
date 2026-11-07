# 第 4 章交付报告（Agent D）

> 2026-11-07：本章完整成品已落盘，供主 Agent 审稿接管。仅制作本章，未递归委派；下列结果均为本章实际执行范围。

## 制作前覆盖表

依据 Martin Kleppmann、Chris Riccomini，O’Reilly 英文第二版，February 2026，ISBN 9781098119065。已完整读取 `originals/ddia2-ch04.txt`（含参考文献，1753行），随后完整对照只读旧稿 `ch04-存储与检索.md`（1092行）。正文印刷115—151／PDF139—175；含参考文献全章115—160／PDF139—184。

| 原书小节（印刷页） | 笔记实际对应锚点 | 关键展开与取舍 |
| --- | --- | --- |
| 章首；Storage and Indexing for OLTP（115—117） | `log-and-index` | 接口与布局分离；追加日志、最新版本、线性扫描、索引维护代价 |
| Log-Structured Storage（118—119） | `log-and-index` | 内存哈希偏移、缓存、重建、空间与范围查询 |
| The SSTable file format（119） | `sstable` | 有序文件、稀疏块索引、块级压缩 |
| Constructing and merging SSTables（120—122） | `lsm-path` | memtable／WAL／flush／不可变段；小数据归并、墓碑保留、故障时发布边界 |
| Bloom filters（122—123） | `bloom-compaction` | 位数组算例、假阳性、不漏报前提、点查与范围界限 |
| Compaction strategies（124） | `bloom-compaction` | 大小分级与分层、读写空间代价、后台积压与背压 |
| Embedded Storage Engines（125） | `indexes-memory` | 嵌入式是部署方式，保留与底层结构的区别 |
| B-Trees（125—127） | `btree` | 根到叶、范围扫描、插入与分裂、层数与缓存；核算容量例 |
| Making B-trees reliable（127—128） | `wal-recovery` | 多页部分写／撕裂页、WAL先行、缓冲、重做及确认边界 |
| Using B-tree variants（128） | `wal-recovery` | COW安全发布、键前缀、兄弟页、物理布局 |
| Comparing B-Trees and LSM-Trees；Read performance（129） | `amplification` | 点／范围读、命中与未命中、尾延迟、实测前提 |
| Sequential versus random writes；SSD侧栏（129—130） | `amplification` | 闪存擦除／GC、顺序与随机并非定额倍数 |
| Write amplification（130—131） | `amplification` | 统一字节口径、具体算例、缓存合并、键值分离、稳态测试 |
| Disk space usage（131—132） | `amplification` | 旧版本、临时空间、碎片、逻辑／物理删除与快照 |
| Multicolumn and Secondary Indexes；Storing Values Within the Index（132—133） | `indexes-memory` | 复合键、重复值、聚簇／堆／覆盖、更新路径 |
| Keeping Everything in Memory（133—134） | `indexes-memory` | 内存格式收益、缓存区别、日志与快照的持久性范围 |
| Data Storage for Analytics；Cloud Data Warehouses（134—136） | `cloud-analytics` | OLTP／OLAP／HTAP，查询引擎／文件格式／表格式／目录，提交元数据的作用 |
| Column-Oriented Storage（136—138） | `column-layout` | 原例4-1水果糖果问题；小销售表；行序一致、行组与裁剪 |
| Column compression（139—140） | `column-layout` | 位图AND／OR、游程及Roaring边界；不等同列族 |
| Sort order in column storage；Writing to column-oriented storage（140—141） | `column-layout` | 整行排序、压缩收益、批写、增量与历史文件合读 |
| Query Execution: Compilation and Vectorization（142—143） | `execution-cubes` | 逐行解释开销、专用代码、批量算子、CPU与SIMD区别 |
| Materialized Views and Data Cubes（143—145） | `execution-cubes` | 预聚合网格、写入维护、AVG不可直接平均、信息损失 |
| Multidimensional and Full-Text Indexes（145—146） | `spatial-fulltext` | 复合键与二维范围、地图边界、空间索引与候选复查 |
| Full-Text Search（146—147） | `spatial-fulltext` | 倒排列表求交、词位置／短语、n-gram、编辑距离 |
| Vector Embeddings；Flat／IVF／HNSW（147—149） | `vector-search` | 距离算例、IVF漏召回、HNSW多层导航、召回／延迟／资源、语义非事实保证 |
| Summary（150—151） | `workload-conclusion` | 从查询与恢复条件解释选型，不设性能胜负表 |

## 产出与统计

- `notes/ch04.md`：完整中文内容源；正文约 **1.29万汉字**（来源区前的汉字粗计，含标题、图注和替代文本；不含来源与翻页）。机制与案例深度优先于机械长度。
- `chapters/ch04.html`：完整静态阅读页；**14个主小节、4个次级标题、正文2张数据表、来源1张对应表、1段小数据文本示意、5张原创图**。前页 `ch03.html`，后页回 `../index.html` 并注明第5章待制作。仅与当前已制作的第1—3章互链。
- 5组可编辑原生 `.excalidraw` 与官方导出 `.svg`，名称为 `ch04-lsm-path`、`ch04-merge-tombstone`、`ch04-btree-recovery`、`ch04-column-mask`、`ch04-ivf-boundary`，分别在 `diagrams/sources/`、`diagrams/exports/`。保留相应 `.skeleton.json`。
- 本章制作脚本位于 `diagrams/sources/ch04-diagrams.mjs`、`ch04-render.py`、`ch04-verify.mjs`；这些是本地制作／核对工具，不是网站运行依赖。HTML从MD生成，以保持内容同步。
- Excalidraw复用默认 `DDIA_TOOLS` 与官方0.18.0 API，无独立安装。最终场景元素数分别 **22、16、16、72、20，共146个**；列式图元素较多来自6列×5行的简单对齐数据格，不是密集架构关系图。
- 未修改共享文件、其他章节或外部旧稿。没有后台服务、浏览器或写作任务遗留。

## 原文与原图实际阅读

制作前先完整读原文1753行，再完整对照旧稿1092行；不是从旧稿翻译。原书章末104条参考文献的条目信息随章通读，未声称逐篇阅读这些文献。

| 原图 | 印刷页／PDF页序 | 实际核对内容 |
| --- | --- | --- |
| 4-1 | 118／142 | 哈希偏移与字节布局 |
| 4-2 | 119／143 | 稀疏首键、块边界与压缩块 |
| 4-3 | 121／145 | 多段归并、同键的新版本选择 |
| 4-4 | 123／147 | 位数组从0起、hash位置、确定不存在与假阳性 |
| 4-5 | 126／150 | 根到叶查询251及范围边界 |
| 4-6 | 127／151 | 插入334、337处分裂及父页引用；同页容量算例 |
| 4-7 | 138／162 | 列式布局与跨列相同行序 |
| 4-8 | 139／163 | 位图与游程编码示意 |
| 4-9 | 143／167 | 两个位图AND与匹配位置 |
| 4-10 | 144／168 | 日期×商品聚合及沿维度汇总 |
| 4-11 | 149／173 | HNSW逐层图导航，不把底层解释为全局精确保证 |

另回看印刷129／PDF153（暂停读写原表述）、131／155（vacuum原表述）、140／164（Roaring原表述）。原文中没有需复原的独立复杂公式；容量、向量距离、位图与平均值均做了数值核查。

## 旧稿利用、修正与扩展边界

保留旧稿有助理解的“日志→有序文件→合并”思路、字节偏移、位图小数据与索引入口解释，但重新组织成连贯文章，增加发布失败、墓碑复活和页分裂崩溃路径。未继承旧稿产品速查、面试推荐、强行类比、RUM“三选二”口号或固定性能胜负表。

### 原书层面的校正／补足（均在正文就地说明）

1. **p127四层／4KiB／500→250TB**：按根叶共四层及数据存叶的明确口径，叶页数量为500³，容量512,000,000,000字节≈512GB；500⁴叶页≈256TB需五层。若叶中引用树外记录，容量另算。属于本笔记复算校正，不宣称出版社已确认。
2. **p129 RocksDB“暂停所有读写”**：官方Write Stalls描述写入减速／阻塞。正文改为写背压，读可能被竞争和读放大间接拖慢；不说整个读取协议被统一暂停。
3. **p131 vacuum移动页／重新摆放**：PostgreSQL17普通VACUUM主要回收死版本供复用，通常不归还中间空洞；VACUUM FULL才重写压紧，且有锁／临时空间代价。
4. **p140 Roaring仅逐位与游程两种形式**：官方还有稀疏整数数组，并按块选择数组／位图／游程。正文补足三种容器，不把简化当完整算法定义。

### 旧稿中进一步纠正的过度简化

- “B-tree删除立即彻底”：逻辑不可见、版本回收、WAL／备份与物理字节清除不能混同。
- “HNSW底层精确找到最近向量”“保证大概率近／固定数量级提升”：原书明确近似；按实际数据、搜索预算与召回测量，不附无依据概率或速度保证。
- “内存库省掉全部编码及恢复格式”：省部分面向磁盘主存储布局的开销，日志编码、快照和恢复仍可能存在；不按产品名固定强弱持久性。
- `flush()`即持久化、SSTable函数返回即截断WAL：区分语言缓冲、设备同步与可恢复文件集合发布；不交付缺少发布协议的“数据库实现”。
- “后台合并不阻塞／快照免费”：并发进行仍有CPU、IO与缓存争用；共享快照仍占保留空间，也不能替代独立备份。
- “每次更新独立整页写、B-tree放大固定≥2x”：缓冲合并、日志编码和观测口径会影响实际放大，正文使用统一字节窗口算例。
- “任意列式新写入立即可查”“查询只要用了位运算就瞬间完成”：改为按提交可见性及硬件／数据分布判断。

必要书外补充都标为笔记解释或假设：WAL持久发布边界、PostgreSQL仅索引扫描的可见性条件、加权平均合并、短语与n-gram候选复核、ANN过滤及recall@k、语义相似不证明事实。未扩大成完整事务／搜索引擎教程。

## 外部核查资料

2026-11-07实际访问并阅读相关段落：

- PostgreSQL17官方WAL简介：<https://www.postgresql.org/docs/17/wal-intro.html>。
- RocksDB官方Write Stalls wiki：<https://github.com/facebook/rocksdb/wiki/Write-Stalls>；按核查当日页面，不声称针对全部历史版本。
- PostgreSQL17官方Routine Vacuuming §24.1.1／24.1.2／24.1.4：<https://www.postgresql.org/docs/17/routine-vacuuming.html>。
- Roaring官方About：<https://roaringbitmap.org/about/>，重点数据分块与三类表示。
- pgvector官方README：<https://github.com/pgvector/pgvector>，页面安装版本0.8.7；读取HNSW／IVFFlat／Filtering／Monitoring段落。

## 实际验证结果

### 数值与关键步骤

Python小数据核对通过：

- S1／S2归并顺序、b的墓碑保留、过早去除墓碑后从S0读到b=2的反例。
- B-tree插入334后键序、337处分段；四／五层容量分别512GB／256TB（十进制）。
- 位图商品31=`101010`、门店3=`110110`、AND=`100010`；商品31 OR 68=`111011`；数量求和7。
- 日期×商品立方体两行分别 `[6,1,0]`、`[5,2,3]`，总数17。
- 写放大4；两组不同样本量平均值合并19。
- 原书嵌入坐标欧氏距离0.3226453161与1.2722814154。
- IVF q=4.9更近左中心0，而数据B=5.1距离0.2，确认跨簇遗漏；recall@5=0.6。

这是算法／算术级核查，不是引擎故障注入、持久性压力测试或真实ANN基准。

### 静态内容与资源

- MD与HTML **14个正文section和来源区的规范化文本逐段一致**；正文／示例／图注／来源同步。
- 页面35个去重href／src引用中，所有本地文件与锚点存在；无重复ID；网页未链接notes／originals／sources／本地PDF。
- 所有5份SVG XML可解析，场景文字均能在对应SVG找到。官方导出后均实际重载场景到编辑器，修改并恢复一段文字，返回 `editable:true`。
- 按现有Pages白名单，本章发布产物为 **1 HTML＋5 SVG**；MD、场景、骨架与制作脚本均位于排除目录。本站没有编译步骤，没有声称“构建通过”。

### 浏览器与阅读

- 本地Google Chrome／Playwright检查 **1440×960、375×960各浅／深色，共4组**；正文16px、行高31.2px；桌面正文720px；页面无横向溢出，5图均加载，无捕获到的JS／HTTP错误。
- 系统主题跟随、手动反向切换及刷新后的localStorage保存通过。
- 手机目录展开／折叠、来源details展开／折叠通过；首个键盘Tab到“跳到主要内容”，焦点outline为solid。
- 手机列式图链接容器实际局部滚动：client333px、scroll560px，scrollLeft可到227px，overflow-x:auto；没有撑宽整页。
- 实际查看桌面浅色页首、手机浅色页首、手机深色图文、桌面深色列式图，以及5张独立浅色SVG和1张独立深色SVG截图。全部标签清晰、未裁切；独立图手动主题读取通过。
- 检查发现IVF原先两个相邻框的实线边界遮住虚线分界，已改为一个外框＋独立虚线，并同步图注；只重新导出该图并定点回看通过。
- 独立SVG第一次使用Playwright `fullPage:true`截图超时；改为足够容纳SVG的900×740固定视口后全部截图成功。此为截图方式问题，无网页运行错误。

核对JSON与截图位于本机临时目录：`/private/var/folders/5k/y6qh6sfd2g30js0v0qrv4mfr0000gn/T/opencode/ddia2-ch04/`。关键结果为 `numerical-checks.json`、`browser-checks.json`、`supplemental-checks.json`；原页PNG也存于同目录。

## 交接与遗留

- 无资料、绘图、正文或页面阻塞。主 Agent 可按覆盖表逐节审稿，重点复核原书四处技术校正的措辞。
- 概览接入、共享制作状态与全书导航由主 Agent 统一维护；本章后页按本轮约定暂回概览，第5章后续轮次完成再由主 Agent接续。
- 没有部署，没有执行真实数据库性能或故障测试；这不是未完成内容，而是本次静态读书笔记的验证边界。
- 本报告提交后本章负责人返回并停止编辑；主 Agent 接管前不再更改本章文件。
