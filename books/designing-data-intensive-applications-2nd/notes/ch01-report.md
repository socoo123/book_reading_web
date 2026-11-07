# 第1章制作与验证报告

> 负责人：第1轮 Agent A；仅第1章，不递归委派。2026-11-07。**已完成并交付主审，返回后停止编辑。** 本会话模型为 GPT-6 Astra；推理档位由主 Agent 的派发配置记录，本子会话未额外查询／切换模型。

## 阅读与范围

- 固定版本：Martin Kleppmann / Chris Riccomini，O’Reilly 英文第二版 February 2026，ISBN 9781098119065。
- 完整读取 `originals/ddia2-ch01.txt` 1—1324行（印刷1—32／PDF25—56；正文1—26，References从26页开始）。
- 原文之后完整读取只读旧稿 `/Users/zy/ai_learn/ddia_2nd/ch01-数据系统架构的权衡取舍.md` 1—889行。
- 已读取根AGENTS、PLAN、本书README及三本指定写作参考、JESA HTML外壳。

## 写前小节覆盖表

| 原书小节／位置（印刷页） | 本笔记锚点 | 应保留的机制、案例与边界 |
| --- | --- | --- |
| 章首，1—3；Terminology: Frontends and Backends，3 | data-intensive | 数据管理困难与计算密集型区分；五种积木；无状态不等于全系统无状态 |
| Operational Versus Analytical Systems，3—4 | oltp-olap | 后端、BI、数据科学、数据与分析工程师；受众和用途不同 |
| Characterizing Transaction Processing and Analytics，5—6；表1-1 | oltp-olap | 点查／聚合、增删改／导入、当前／历史、固定／即席；超市三问；实时分析边界 |
| Data Warehousing，7—9；图1-1 | warehouse-etl | 数据孤岛、布局、资源争用、访问边界；ETL/ELT与SaaS API；HTAP不取消整合 |
| From data warehouse to data lake，9—10 | lake-pipelines | 特征工程、NLP；原始文件供多消费者；非线性替代、治理责任 |
| Beyond the data lake，10 | lake-pipelines | DataOps、流处理、分析结果回流／reverse ETL、模型部署 |
| Systems of Record and Derived Data，10—11 | authority-derived | 权威与重建；缓存／索引／视图／模型；角色与产品无关；更新失败与重建条件 |
| Cloud Versus Self-Hosting，12；图1-2 | cloud-self-hosting | 开发与运维两个决定；本地部署、IaaS、托管光谱 |
| Pros and Cons of Cloud Services，13—14 | cloud-self-hosting | 平稳／突发负载、团队技能、控制权、锁定、地缘与信任 |
| Cloud Native System Architecture，14—15；表1-2 | storage-compute | 云原生与搬到VM区分；产品分类仅作背景，避免产品清单代替机制 |
| Layering of cloud services，15—16 | storage-compute | 基础资源、对象存储、高层服务；抽象匹配与选择代价 |
| Separation of storage and compute，16—17 | storage-compute | 本地盘／RAID、远端块存储、专用存储；扩算、恢复、网络代价与多租户 |
| Operations in the Cloud Era，17—18 | cloud-operations | 自动化、临时实例、频繁发布、复盘、知识；费用、配额与集成 |
| Distributed Versus Single-Node Systems，19—20 | distributed | 九项动机全覆盖；节点与网络；容量之外的可用性／地理约束 |
| Problems with Distributed Systems，20—21 | distributed | 超时不确定性、数据移动、COST、可观测性、跨服务一致性 |
| Microservices and Serverless，21—22 | services-serverless | 组织独立与数据封装、测试／API演进成本；FaaS调度、计费与冷启动 |
| Cloud Computing Versus Supercomputing，23 | hpc | 批作业／持续服务、检查点、RDMA、拓扑、信任、地域；非绝对分类 |
| Data Systems, Law, and Society，24—25 | data-responsibility | 用途、保留、删除传播、不可变日志／训练模型、风险、最小化；法律限定 |
| Summary，25—26 | tradeoff-summary | 四条主线串联；衔接第2—4章及后续机制章节 |

上表19行全部已覆盖，锚点均实际存在。没有省略核心小节；低层标题被组织成13个连贯阅读小节。原表1-2产品清单只保留其架构分类含义，不再整表复制；长参考文献未逐项外读，不冒称全部核实。原书两图均回看，网站使用重新组织的原创图。

## 产出与统计

- `notes/ch01.md`：完整中文笔记，13节、2表、2条可执行SQL示例、2幅图及完整来源折叠。
- `chapters/ch01.html`：对应静态阅读页，桌面／手机目录、来源details、主题切换、前后导航、图像大图入口；复用共享本地资源。
- 两组图：`diagrams/sources/ch01-authority-derived.excalidraw` 与 `ch01-storage-compute.excalidraw`，对应同名 `.skeleton.json` 和 `diagrams/exports/*.svg`。分别18／14个原生元素，11／9个文字元素，共32元素。
- 制作辅助：`diagrams/sources/ch01-render.py`（本章Markdown→HTML）、`ch01-verify.mjs`（本章浏览器验证），均位于发布排除目录，只读共享外壳和本机依赖，不改共享文件。
- 本报告：`notes/ch01-report.md`。
- 正文区汉字9986（包含标题、表格、代码注释、图注／替代文本，不含来源与翻页）；叙述段落约9331汉字。较7—9千参考投入略高，主要用于SQL具体结果、ETL口径、派生重建条件、存算分离操作过程与法律修正，没有以产品清单或面试题扩充。
- HTML为49,345字节。正文13节及来源内容逐段标准化文本对比，Markdown／HTML完全对应。

## 原图回看与事实核查

实际以PyMuPDF渲染并打开：

| 印刷页／PDF页序 | 核对内容 |
| --- | --- |
| 6／30 | 表1-1八维比较；OLAP中online含义保留不确定性的原文注释；实时分析 |
| 8／32 | 图1-1：三个运营系统分别提取、转换、加载到共同仓库；分析师查询方向；HTAP边界 |
| 12／36 | 图1-2：自研自运维、现成软件自运维、现成软件外包运维的光谱；控制与投入 |
| 15／39 | 表1-2自建与云原生产品例子；对象存储与分层服务说明 |
| 25／49 | GDPR用途限制原句确为“cannot later be used for any other purpose”，非文本提取错误 |

外部实际读取3项，核查日期2026-11-07，正文来源details保留链接：

1. EUR-Lex官方GDPR英文文本，第5条、第6(4)条、第17条及第44—46条。用于目的限制、数据最小化、存储限制、删除事由／例外和跨境传输边界。
2. AWS Lambda官方Pricing页，事件函数按请求与执行时长、预置并发按配置启用期间计费。只作计费边界核查，不引用价格、不列新版产品规格。
3. USENIX原作者COST报告页摘要，确认COST定义与部分被测系统高于数百核仍未胜单线程的语境；没有声称读完论文或复现实验。

### 纠错与旧稿处理

| 对象与原表述 | 问题／依据 | 成品处理 |
| --- | --- | --- |
| 原书印刷25页：个人数据不能用于任何其他目的 | GDPR 5(1)(b)针对不相容的进一步处理，6(4)规定相容性考量 | §12就地说明原句、依据与修正；非出版社已确认勘误 |
| 旧稿：OLTP／OLAP“必须分开” | 原章同时承认通用库和HTAP | §03改为有负载隔离／整合收益时再分离 |
| 旧稿：分析系统“只看不改” | 原表同时列批量导入与事件流；只读相对上游业务事实 | §02分清读取业务副本与系统接收写入 |
| 旧稿：派生“丢了没关系”；只靠能否恢复判断SoR | 可重建仍有数据、转换与时间成本前提；备份不会取消权威角色 | §05具体说明索引故障、重建成本、历史丢失及模型非字节复现 |
| 旧稿：云盘每次固定4KiB；计算节点无状态、存算彻底分家 | 原文为常见块大小示例，分离不消除缓存与恢复状态 | §07保留云服务分层的收益和网络／缓存代价，不泛化产品内部实现 |
| 旧稿：容量规划本身消失 | 原书17—18页明确费用规划与配额 | §08改为机器级预购减少，资源与费用责任保留 |
| 旧稿：每服务独占数据库是“一条铁律” | 原文为常见安排，目标是API封装和减少干扰 | §10说明逻辑所有权不等于专属物理服务器 |
| 旧稿：Serverless闲时不花一分钱 | Lambda官方预置并发按配置期间计费；依赖各自收费 | §10就地修正，未作跨产品统一费用保证 |
| 旧稿：欧洲用户数据须留欧盟、删除必须无条件级联 | GDPR第五章允许满足条件的传输；第17条有事由与例外 | §12区分驻留和传输、工程追踪范围和法律义务 |

保留旧稿有价值的超市访问模式、ETL职责、源与派生及云外包思路，并以原章重新组织。未沿用其Lakehouse扩展、未经验证CDC伪代码、生产产品速查与面试架构；这些并非原章完成内容。本文新增算例、故障过程和团队场景均显式标为笔记假设／解释，未冒称实际生产案例。

## 实际验证

### 内容和静态资源

- SQL在Python自带SQLite内存数据库实际运行：点查得到`('A',1200)`，一月份聚合得到`('A',2000),('B',1500)`，二月记录排除。没有声称使用PostgreSQL或部署数据库。
- 容量示例复算：40×24＝960单元小时；40×0.5＝20单元小时；比值48。正文明确不是价格比。
- HTML无重复ID；56项href/src检查全部本地目标或锚点可解析。第一次检查时同轮ch03/ch04尚未落盘，最终已在它们落盘后定点复核为可访问。
- 网页没有PDF、notes、originals、sources目录链接；章1上一页为概览，下一页为ch02；正文仅链接本轮第2—4章，其他章为纯文字。
- 两个SVG XML可解析，源场景20个文字元素与导出逐行一致。官方Excalidraw 0.18.0导出后重载编辑器，实际改字／恢复均`editable:true`。
- 已检查导出工具`esbuild write:false`，按主 Agent 补充共用默认DDIA_TOOLS依赖，bundle不写共享临时文件，章stem分离；无额外安装。
- 按现有Pages白名单与排除规则，本章公开产物为1 HTML＋2 SVG；笔记、图源和工具被排除。网站没有编译步骤，未把内容渲染称为框架构建或部署。

### 浏览器

运行`node .../diagrams/sources/ch01-verify.mjs`，由脚本启动仅本次检查使用的本地HTTP服务，结束已关闭服务和Chrome：

- 1440×900／375×900分别覆盖系统浅色、系统深色，共4组；正文16px、31.2px行高，页面宽度恰为1440／375，无整页横向溢出。
- 双端目录按断点切换；手机目录实际展开并点击锚点；来源details实际展开和键盘聚焦。
- 手动切换到与系统相反的主题，再刷新，DOM与localStorage选择均保持；截图回到系统主题。
- 两图实际滚动到可见位置并完成加载；手机图宽560、容器333，局部横向滚动；两张表及代码块均验证`overflow-x:auto`，手机内容确实宽于容器。
- 独立打开两张SVG，所有文字边界在viewBox内，无裁切；浅色派生图、深色存算图和375px深色文章截图已实际查看，节点文字与箭头无重叠，对比可读。
- 捕获到的JS／HTTP错误为0。截图与`browser-results.json`位于`/private/var/folders/5k/y6qh6sfd2g30js0v0qrv4mfr0000gn/T/opencode/ddia2-ch01/`。
- 制作期修正两项工具问题：初次渲染在chapters目录尚不存在时不能解析`chapters/../diagrams`，改为规范化绝对路径；初版浏览器脚本等待全部懒加载图导致超时，改为逐图滚入后等待当前图。均为制作脚本问题，修复后上述验证通过。

## 跨章衔接与遗留

- 第2章接性能／可靠性／可扩展性／可维护性，第3章接模型与查询，第4章接物理布局与存储；这些页面链接已存在。
- 第8章事务、第9章网络失败、第11—13章批流与集成、第14章责任仅作文字衔接，不提前建未完成章链接。
- 术语沿用本书README：运营型／分析型、权威记录系统／派生数据、复制／分片、吞吐量、存算分离等。未发现需主Agent调整共用术语的冲突。
- 本章无资料、图示或验证阻塞。待主Agent逐章主审、共享概览／书架接入与全轮交接；未修改这些共享文件，也未部署。
- 内容边界：法规核查仅支撑本文指定条文；训练数据删除对既有模型的完整技术方案留待后续问题，正文没有假称解决。COST仅核对摘要，未读其全文。

**交付完成。Agent A 返回后停止编辑，主Agent可接管以上文件。**
