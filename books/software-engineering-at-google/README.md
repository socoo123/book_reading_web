# Software Engineering at Google：资料与工作状态

> 本书为「架构提升读书笔记」收录的第一本书。第二章至第二十五章及后记已获用户验收。第一章补写由 1 个 `openai/gpt-6.1-sol#max` 子 Agent 完成，主 Agent 已独立核查、审稿及验证，现停止等待第一章验收；正文沿用 16px。执行方案见 [`../../PLAN.md`](../../PLAN.md)，交接见 [`../../CONTINUE.md`](../../CONTINUE.md)。

## 资料状态

| 项目 | 当前记录 |
| --- | --- |
| 书名 | Software Engineering at Google（用户指定） |
| 书籍署名 | Titus Winters、Tom Manshreck、Hyrum Wright（官方入口使用 curated by） |
| 版本、出版年份、出版社 | 实际依据 Abseil 官方 HTML 版；官方入口记载 2020 年 3 月出版，纸质版出版方为 O’Reilly；未确认与用户 PDF 的对应关系 |
| 使用语言、译本及译者 | 英文原文；本站中文为自主整理的学习笔记，不是出版译本 |
| PDF／原书附件 | 尚未取得可读附件；不声称读过用户 PDF |
| 原书阅读情况 | 已读取官方入口、目录、第 1—25 章及后记的正文与现有脚注；Foreword、Preface 未单独制作笔记 |
| 原书目录、章节对应关系 | 目录共 25 个主体章节及 Afterword，另有 Foreword、Preface；第一章 What Is Software Engineering? |
| 第一章署名 | Written by Titus Winters；Edited by Tom Manshreck |
| 第二章署名 | Written by Brian Fitzpatrick；Edited by Riona MacNamara |
| 第三章署名 | Written by Nina Chen and Mark Barolak；Edited by Riona MacNamara |
| 第四章署名 | Written by Demma Rodriguez；Edited by Riona MacNamara |
| 第五章署名 | Written by Brian Fitzpatrick；Edited by Riona MacNamara |
| 第六章署名 | Written by Ben Collins-Sussman；Edited by Riona MacNamara |
| 第七章署名 | Written by Ciera Jaspan；Edited by Riona Macnamara（原页拼写） |
| 第八章署名 | Written by Shaindel Schwartz；Edited by Tom Manshreck |
| 第九章署名 | Written by Tom Manshreck and Caitlin Sadowski；Edited by Lisa Carey |
| 第十章署名 | Written by Tom Manshreck；Edited by Riona MacNamara |
| 第十一章署名 | Written by Adam Bender；Edited by Tom Manshreck |
| 第十二章署名 | Written by Erik Kuefler；Edited by Tom Manshreck |
| 第十三章署名 | Written by Andrew Trenk and Dillon Bly；Edited by Tom Manshreck |
| 第十四章署名 | Written by Joseph Graves；Edited by Tom Manshreck |
| 第十五章署名 | Written by Hyrum Wright；Edited by Tom Manshreck |
| 第十六章署名 | Written by Titus Winters；Edited by Lisa Carey |
| 第十七章署名 | Written by Alexander Neubeck and Ben St. John；Edited by Lisa Carey |
| 第十八章署名 | Written by Erik Kuefler；Edited by Lisa Carey |
| 第十九章署名 | Written by Caitlin Sadowski, Ilham Kurnia, and Ben Rohlfs；Edited by Lisa Carey |
| 第二十章署名 | Written by Caitlin Sadowski；Edited by Lisa Carey |
| 第二十一章署名 | Written by Titus Winters；Edited by Lisa Carey |
| 第二十二章署名 | Written by Hyrum Wright；Edited by Lisa Carey；Testing LSCs 案例署名 Adam Bender |
| 第二十三章署名 | Written by Rachel Tannenbaum；Edited by Lisa Carey；CI Is Alerting 署名 Titus Winters，TAP 案例署名 Adam Bender |
| 第二十四章署名 | Written by Radha Narayan, Bobbi Jones, Sheri Shipe, and David Owens；Edited by Lisa Carey |
| 第二十五章署名 | Written by Onufry Wojtaszczyk；Edited by Lisa Carey |
| 后记署名 | Asim Husain；原文署名职务 Vice President of Engineering, Google，按出版时记录，不作现任职务断言；未列单独编辑署名 |
| 正文进度 | 25 个主体章节＋后记已整理；第二章至第二十五章及后记已验收；第一章补写已完成审稿验证、待验收 |

## 已使用来源（2026-11-06 核查）

- 官方书籍入口与出版信息：<https://abseil.io/resources/swe-book>
- 官方目录：<https://abseil.io/resources/swe-book/html/toc.html>
- 第一章原文：<https://abseil.io/resources/swe-book/html/ch01.html>
- 第一章补写核查：重新完整读取正文及全部 17 条脚注；Python 官方文档 <https://docs.python.org/3/library/stdtypes.html#set-types-set-frozenset>、<https://docs.python.org/3/library/stdtypes.html#dict>、<https://docs.python.org/3/reference/datamodel.html#object.__hash__> 用于区分集合顺序、字典插入顺序及哈希随机化的进程边界。主 Agent 另对照 Python 3.11 固定版类型文档；排序示例在 Python 3.11.8 通过。
- 第二章原文：<https://abseil.io/resources/swe-book/html/ch02.html>
- 第三章原文：<https://abseil.io/resources/swe-book/html/ch03.html>
- 第四章原文：<https://abseil.io/resources/swe-book/html/ch04.html>
- 第五章原文：<https://abseil.io/resources/swe-book/html/ch05.html>
- 第六章原文：<https://abseil.io/resources/swe-book/html/ch06.html>
- 第七章原文：<https://abseil.io/resources/swe-book/html/ch07.html>
- 第八章原文：<https://abseil.io/resources/swe-book/html/ch08.html>
- 第九章原文：<https://abseil.io/resources/swe-book/html/ch09.html>
- 第十章原文：<https://abseil.io/resources/swe-book/html/ch10.html>
- 第十一章原文：<https://abseil.io/resources/swe-book/html/ch11.html>
- 第十二章原文：<https://abseil.io/resources/swe-book/html/ch12.html>
- 第十三章原文：<https://abseil.io/resources/swe-book/html/ch13.html>
- 第十四章原文：<https://abseil.io/resources/swe-book/html/ch14.html>
- 第十五章原文：<https://abseil.io/resources/swe-book/html/ch15.html>
- 第十六章原文：<https://abseil.io/resources/swe-book/html/ch16.html>
- 第十七章原文：<https://abseil.io/resources/swe-book/html/ch17.html>
- 第十八章原文：<https://abseil.io/resources/swe-book/html/ch18.html>
- 第十九章原文：<https://abseil.io/resources/swe-book/html/ch19.html>
- 第二十章原文：<https://abseil.io/resources/swe-book/html/ch20.html>
- 第二十一章原文：<https://abseil.io/resources/swe-book/html/ch21.html>
- 第二十二章原文：<https://abseil.io/resources/swe-book/html/ch22.html>
- 第二十三章原文：<https://abseil.io/resources/swe-book/html/ch23.html>
- 第二十四章原文：<https://abseil.io/resources/swe-book/html/ch24.html>
- 第二十五章原文：<https://abseil.io/resources/swe-book/html/ch25.html>
- 后记原文：<https://abseil.io/resources/swe-book/html/ch26.html>，不是第 26 个主体章节。
- 第四章报告作者核查：<https://www.perpetuallineup.org/>；作者应为 Clare Garvie、Alvaro Bedoya、Jonathan Frankle，已在该章记录原书书目错误。
- 第四章图像识别案例的后续报道：<https://www.wired.com/story/when-it-comes-to-gorillas-google-photos-remains-blind/>；用于区分当时案例与后续应对，未据此推断当前产品状态。
- 第五章论文书目核查：<https://api.crossref.org/works/10.1037/0021-9010.93.1.108>；Adam M. Grant 论文出版年份应为 2008，非原书所列 2018。本次只核对书目，未阅读全文。
- 第八章 C++ 语义核查：<https://eel.is/c++draft/unique.ptr.single>、<https://eel.is/c++draft/unique.ptr.single.ctor>。`unique_ptr` 的不可复制与独占所有权不排除 `get()` 取得非拥有指针；按值移动构造后源对象为空，仍可赋值、重置或析构。
- 第八章自动格式化补充：<https://go.dev/blog/gofmt>。Go 官方博客解释统一格式对阅读、维护及机械化改写的作用；正文未将这份补充材料冒充原章论述。
- 第九章评审响应译法核查：<https://google.github.io/eng-practices/review/reviewer/speed.html>。将响应建议表达为“约一个工作日”，区别于连续 24 小时，也不把响应期限写成完成评审期限。
- 第十章教程命令核查：<https://curl.se/docs/manpage.html#-I>、<https://www.gnu.org/software/bash/manual/html_node/Command-Search-and-Execution.html>。原书示例中的 `curl -I` 只请求 HTTP 响应头，不下载包；`cd ~; foobar.sh` 仍依赖命令搜索路径，进入目录不等于能够按裸文件名执行脚本。
- 第十一章历史实现核查：<https://openjdk.org/jeps/486>。原章用 Java SecurityManager 执行小型测试约束是当时实践；JDK 24 已永久禁用该机制，不能直接作为当前 JDK 的实现方案。
- 第十一章 Java 演示条件：<https://docs.oracle.com/javase/8/docs/technotes/guides/language/assert.html#enable-disable>。补齐完整类、入口和 `java -ea`；章节负责人已在 JDK 21.0.2 编译运行，并确认反向减法启用断言后失败。
- 第十二章代码核查：原章例 12-1 的返回类型、12-13 的负数符号、12-16 的多余括号及命名、12-22 的 Python 赋值语法已在来源区记录；与作者有意设计的错误反例分开。原创 Python 示例依据 <https://docs.python.org/3.11/library/unittest.html#basic-example>，四项测试通过；内部实现替换后测试不变，遗漏收款入账被行为测试捕获。
- 第十三章 API 与打桩能力核查：<https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/util/Map.html#put(K,V)>、<https://docs.python.org/3/library/unittest.mock.html#unittest.mock.Mock.side_effect>。Java Map 写入使用 `put`；简单固定返回值不会自动形成读写状态，但框架回调能够实现状态行为，不能笼统说打桩框架无法保存状态。
- 第十三章工具说明：<https://errorprone.info/bugpattern/DoNotMock> 的检查级别为 ERROR；章节负责人已运行文本存储契约、拒付／超时与缓存三个 Python 示例，并验证 `side_effect` 状态回调和 `create_autospec` 签名检查。
- 第十一／十四章原文内部差异：第十一章将 GWS 自动化测试推广转折记为 2005 年，第十四章历史回顾写为 2003 年；当前记录这处不一致，未据此判定真实年份。第十四章的 99% 示例还需区分独立假设下的替身失配概率与系统实际缺陷概率。
- 第十五章 Java 标识核查：<https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/lang/Deprecated.html>。注解为 `@Deprecated`，小写 `@deprecated` 是 Javadoc 标签；两者与迁移执行机制不同。原章脚注工具地址已返回 404，IAEA 报告全文未取得，正文保留转述身份与资料缺口。
- 第十六章 Git 与主干开发核查：<https://git-scm.com/docs/git-clone>、<https://dora.dev/capabilities/trunk-based-development/>。浅克隆、部分克隆与稀疏工作树作用不同；主干开发可使用短分支，DORA 研究不作为单因素因果证明。单一版本政策允许受控升级期短暂双版本，与第十五／十八章迁移说明相连。
- 第十七章研究全文：<https://research.google.com/pubs/archive/43835.pdf>。主 Agent 已读取并核对 27 位参与者、23 个团队及表 1 的 259 条分类回答；比例不是全部查询或工时占比。论文引言与方法存在 396／394 总问卷数差异，本文不依赖该总数。
- 第十七章索引核查：<https://swtch.com/~rsc/regexp/regexp4.html>。三元组提供候选，完整正则再精确匹配；原章的 recall 措辞已澄清。原书脚注的旧外部 Code Search 关闭年份 2013 与 Cox 2012 年 1 月记述及研究论文的 2006—2012 年不一致，已记录差异，不推定准确停服日。
- 第十八章 Bazel 核查：<https://bazel.build/run/build>、<https://bazel.build/docs/sandboxing>、<https://bazel.build/remote/caching>。按目标及依赖闭包加载 BUILD；沙箱不能普遍隐藏全部宿主文件；缓存复用仍需完整输入、受控工具与确定性。原章的强保证表述已收窄。
- 第十八章外部依赖及现代工具：<https://bazel.build/external/migration>、<https://bazel.build/external/overview>、<https://bazel.build/rules/lib/repo/http#http_archive-sha256>、<https://docs.gradle.org/current/userguide/build_cache.html>、<https://maven.apache.org/guides/introduction/introduction-to-dependency-mechanism.html>、<https://maven.apache.org/guides/introduction/introduction-to-the-pom.html>。Bzlmod 自动解析传递模块依赖，外部依赖也可为源码；哈希属性并非语法强制；Gradle 支持缓存；Maven 有确定调解规则且 POM 仍使用 XML。逐项依据及历史边界见该章来源区。
- 第十九章核查：依据原章正文及两条脚注，区分快照与变更、文件阅读进度与 LGTM、注意力集合与参与者名单，以及评审条件与提交检查。工具实现和 Gerrit 对比保持原书历史语境，不作为当前内部产品说明。
- 第二十章 Java 与分析工具：<https://docs.oracle.com/javase/specs/jls/se25/html/jls-15.html#jls-15.19>、<https://errorprone.info/bugpattern/BadShiftAmount>、<https://errorprone.info/docs/flags>。`int >>> 32` 实际位移为零；工具检查、普通编译与组织错误级别政策分开解释。有效误报使用行动口径，不等同统计假阳性率，也不能由不同交互次数相除得出。
- 第二十章协议兼容性：<https://protobuf.dev/best-practices/dos-donts/>、<https://protobuf.dev/programming-guides/proto3/#updating>。原文“只有保存序列化数据才有问题”的概括过宽；滚动升级、回滚与新旧进程通信同样需要兼容性，已在来源区记录修正。
- 第二十一章版本规范与解析：<https://semver.org/spec/v2.0.0.html>、<https://research.swtch.com/version-sat>、<https://go.dev/ref/mod#minimal-version-selection>。SemVer 不规定包管理器范围与选版算法；VERSION 的 NP 完全结论有模型前提；Go MVS 按依赖图中的最高最低要求选版，不自动获取仓库最新版或安全修复。
- 第二十一章兼容性与历史边界：<https://abseil.io/about/compatibility>、<https://gcc.gnu.org/onlinedocs/libstdc++/manual/abi.html>。区分 API、ABI 与具体工具链保证，C++ 标准不提供无条件 ABI 承诺；Abseil 当前政策与原章历史描述分别标注。Live at Head 依赖可见下游、可运行测试与迁移责任，原章未声称跨组织方案已获大规模验证。
- 第二十二章 RoseHub：<https://opensource.googleblog.com/2017/03/operation-rosehub.html> 的报道发表于 2017-03-01，行动始于 2016 年 3 月，50 位员工发现 2,600 个项目并发出补丁，不代表补丁全部合入。<https://commons.apache.org/proper/commons-collections/security.html> 说明漏洞还涉及不可信对象反序列化等条件；原章年份与简写口径已在来源区纠正。
- 第二十二章迁移与测试：核对先调整行为、再建立别名、最后逐批改引用的 `scoped_ptr` 迁移顺序；TAP 每三小时启动一轮与一轮可能超过六小时是不同时间口径；组合测试通过不能逻辑证明每个分片独立正确。
- 第二十三章核查：按原章区分提交前、提交后、发布候选与生产探测；保留 Assistant 运行耗时缩短十四倍、Takeout 配置／部署失败和介入调试等不同统计口径。hotswapping 复杂度指部署副本规模；已知失败标记仍保留观察与清理机制。录制／回放的误报标签极性、脚注 7 错置和环境自足的确定性边界已在来源区说明。补查 <https://www.martinfowler.com/articles/continuousIntegration.html> 当前 2024-01-18 版的定义，不作为 2020 年原句版本。
- 第二十四章书目核查：<https://martinfowler.com/books/continuousDelivery.html> 明确 *Continuous Delivery*（2010）的作者为 Jez Humble 与 David Farley，Martin Fowler 为作序者；原章归为 Fowler 所著有误。
- 第二十四章定义与平台行为：<https://martinfowler.com/bliki/ContinuousDelivery.html> 区分持续交付能力与持续部署；<https://support.google.com/googleplay/android-developer/answer/9845334?hl=en> 核对当前测试轨道说明；<https://support.google.com/googleplay/android-developer/answer/9859252?hl=en> 明确暂停放量不会回退已更新用户、比例不会默认自动增长。正文区分原章自建自动化管道与平台默认行为，部署安慰剂对照不作为整体正确性的统计证明。
- 第二十五章论文书目核查：<https://www.usenix.org/conference/osdi16/technical-sessions/presentation/adya> 将 *Slicer: Auto-Sharding for Datacenter Applications* 列于 OSDI 2016，原章脚注 11 所列 OSDI 2019 有误；此处核查书目与摘要，未将论文全文作为已通读依据。
- 第二十五章现代工具边界：<https://docs.aws.amazon.com/lambda/latest/dg/best-practices.html> 建议复用执行环境中的连接与缓存；<https://kubernetes.io/docs/concepts/workloads/pods/> 说明 Pod 内容器共享网络空间；<https://kubernetes.io/docs/tasks/run-application/scale-deployment/> 明确 Deployment 可缩为零。需分别区分不保证状态保留与不能复用状态、Pod 与单个容器、零副本与按请求自动唤醒。
- 第二十五章补核：<https://knative.dev/docs/serving/autoscaling/scale-to-zero/> 说明 KPA 缩零能力；<https://research.google/pubs/large-scale-cluster-management-at-google-with-borg/> 用于 Borg 书目与摘要核对。原章百万文档、每份一秒、两百台机器的理想耗时应为 83.3 分钟，非一百分钟；脚注 11 的 Slicer 应为 OSDI 2016。各项修正及资料边界已记录在来源区。

第 1—25 章及后记正文与现有脚注已实际读取。本次笔记以这些实际可获取的资料为依据，不标纸书／PDF 页码；HTML 定位到章节与小节。公开网页未在此核实具体印次与勘误版本，未来用户提供 PDF 时再对照，不默默混用。

官方入口注明数字版采用 CC BY-NC-ND 4.0；本项目保存来源链接，以自主分析、解释和案例形成笔记，不将原书文件或整章译文部署到网站。当前原始 HTML 只作为临时阅读资料，不进入项目部署产物。

## 来源与写作策略

1. 以实际取得并确认的原书版本为主来源；不默默混用不同版本或译本。
2. 原书观点注明章节／小节，用自己的语言整理；直接引文逐字核对并标注位置。页码必须对应明确版本。
3. 明确区分原书观点、笔记解释和外部补充。真实案例附依据，假设案例明确标识，并说明前提、过程、结果与局限。
4. 外部核查优先官方文档、原始论文和权威资料，保留链接；时效性结论记录核查日期。尚无实际获取的来源时，不虚列参考文献。
5. 错误或争议使用“原表述 → 问题及依据 → 修正解释”，区分事实错误、翻译歧义、时代局限、特定前提及观点争议。
6. 按最新反馈写成内容充分、顺畅的文章：展开核心观点、推理与例子的背景、过程、结果，篇幅不限于第一章精简稿。减少反问、反驳和反复限定；少量重点色块和小图服务于理解。自然交代来源身份，文末折叠保存简短来源对应；不默认附练习、决策卡或大型覆盖表。第二章作为已认可的图文风格参考。

## 文件分工与同步

- `index.html`：书籍概览、已核对的书籍信息与阅读目录。
- `chapters/reading-template.html`：阅读布局演示，不是正式章节。
- `notes/ch01.md`、`chapters/ch01.html` 和 `diagrams/{sources,exports}/ch01-*`：本轮第一章补写，由唯一章节负责人独占写入。
- `notes/ch02.md`、`chapters/ch02.html`：第二章新版图文样稿。
- `notes/ch03.md` 至 `notes/ch06.md` 及对应 `chapters/ch03.html` 至 `chapters/ch06.html`：已验收四章。
- `notes/ch07.md` 至 `notes/ch10.md` 及对应 `chapters/ch07.html` 至 `chapters/ch10.html`：已验收四章。
- `notes/ch11.md` 至 `notes/ch14.md` 及对应 `chapters/ch11.html` 至 `chapters/ch14.html`：已验收四章。
- `notes/ch15.md` 至 `notes/ch18.md` 及对应 `chapters/ch15.html` 至 `chapters/ch18.html`：已验收四章。
- `notes/ch19.md` 至 `notes/ch22.md` 及对应 `chapters/ch19.html` 至 `chapters/ch22.html`：已验收四章。
- `notes/ch23.md` 至 `notes/ch25.md` 及对应 `chapters/ch23.html` 至 `chapters/ch25.html`：已验收三个主体章节。
- `notes/afterword.md`、`chapters/afterword.html`：已验收后记，按实际原文篇幅整理。
- `notes/<chapter-id>.md`：获批章节的内容源。
- `chapters/<chapter-id>.html`：对应的静态阅读页。
- `diagrams/sources/<figure-id>.d2`、`.excalidraw` 或 `.mmd`：按场景保存可编辑图源。
- `diagrams/exports/<figure-id>.svg`：网页使用的导出图，与图源使用相同基础名称；图文对应，兼顾浅深色与手机阅读。

当前无 Markdown 生成器。正式章节由页面 Agent 根据内容源手工同步 HTML，每次修订同批交付源稿、网页与相关资源，由主 Agent 对照关键内容后才标记交付。未同步稿件不计为已发布章节。每批交付后停止，等待用户验收并批准下一批，不自动推进全书。

第 3—18 章已完成审稿验证并获验收。上批第 15—18 章共约 3.33 万汉字、38 节、7 张原创 SVG，主 Agent 已通读原文、稿件、页面与图源；正文和代码同步、本地链接、来源锚点及折叠区、图注、图源／导出检查通过。Chrome 下四章在 375px／1440px、浅／深色组合中均正常，正文和重点 16px，无页面横向溢出；全部 7 张图独立打开时跟随已保存主题，章节、概览及全部图示截图已审阅。第十八章 Python 缓存演示及遗漏输入反例已由负责人运行，主 Agent 已审阅代码与脚本；BUILD 片段仅核对结构，未在 Bazel 中构建。

上批第 19—22 章共约 3.27 万汉字、37 节、8 张原创 SVG，已完成主 Agent 审稿与整合验证并获用户验收。正文及代码、来源、图源与导出同步，本地链接与原文锚点通过；Chrome 桌面／手机、浅／深色及独立大图检查通过，章节、概览与全部图示截图已审阅。Java 位移演示、C++11 兼容桥及三个分离编译迁移阶段已由负责人实际运行，主 Agent 已审阅脚本与结果；版本区间／MVS 表格由负责人以 Python 验证，主 Agent 已审阅脚本与结果。完整记录见 `../../CONTINUE.md`。

上批第 23—25 章及后记共约 3.02 万汉字、36 节、6 张原创 SVG，主 Agent 已完成原文核查、图文审稿与导航整合。29 个 HTML 页本地链接／锚点、本批正文与来源同步、图源／导出检查通过；Chrome 四篇桌面／手机、浅／深色及全部 6 图独立查看通过，页面与图示截图已审阅。后记单独使用 `afterword` 文件名。**本批已验收；本轮仅授权第一章补写，全书整合和部署另行授权。**

第一章补写共 8028 汉字、9 节、4 处重点、2 张原创 SVG，保留原有六个锚点。主 Agent 已通读原文、稿件、HTML 和两张图源，独立核查意见已纳入正文与来源区。29 页本地链接／锚点、正文与来源同步、图源／导出检查通过；Chrome 桌面／手机 × 浅／深色、主题保存及两图独立查看通过，章节与全部图示截图已审阅。代码示例实际运行通过。**第一章补写待验收；全书整合、Foreword／Preface 笔记与部署另行授权。**

## 2026-11-06 阅读体验优化（待验收）

用户要求优化本书笔记，范围为第 2—25 章及后记；第一章补写与第二本书不在范围内（第一章只接入了目录高亮并补上图注里的大图链接，正文未动）。用户指定子 Agent 使用 Claude Opus 5.5（项目约定的 GPT-6.1 Sol · max 在当前环境不可用）。第 5、11 章先试点，经主 Agent 审阅后其余 23 篇各由 1 名负责人并行完成，主 Agent 逐篇审阅改动、核对关键改写与新图的原文依据。

- 正文：精简核查式限定与重复归属，脚本统计的候选句由 367 句降到 110 句，余下多为原书论证或影响读者做法的限定；事实、案例、纠错不变，正文总量基本持平。按原文收紧了第 4、11、15、19、23 章等处的若干措辞。
- 来源区：删去读取过程、PDF 版本、SVG 制作等工作记录，保留原文链接、小节对应和全部纠错（统一为“原表述 → 问题及依据 → 修正”），汉字量减少约 19%。
- 图示：新增 35 张原创解释图（全书由 48 张增至 83 张），图号随之顺延；全部 SVG 统一可在单独打开时跟随已保存主题，HTML 图注的“查看大图”均为链接。
- 页面：书架与概览移除流程状态文字，概览目录按原书五个部分分组；新增 `assets/reader.js`，桌面侧栏目录高亮当前小节。
- 验证：26 篇静态检查（正文／来源区双向同步、链接与锚点、图号、SVG 副本）通过；Chrome 375px／1440px × 浅／深色、目录高亮、主题保存检查通过；35 张新图浅深色截图已审阅。改前备份与检查脚本在项目外 `/tmp/swe-opt/`。

## 本地预览

在项目根目录运行 `python3 -m http.server 8000`，访问 `http://localhost:8000/`。采用原生 HTML／CSS／JavaScript，无依赖安装或构建步骤。
