# Designing Data-Intensive Applications · 第二版概览

Martin Kleppmann、Chris Riccomini；O’Reilly 英文第二版，February 2026，First Release 2026-02-18；ISBN 978-1-098-11906-5。副标题：The Big Ideas Behind Reliable, Scalable, and Maintainable Systems。依据用户提供的673页英文原书PDF，中文章名与术语为本站译法，不对应特定中文出版译本。

一次数据库写入怎样成为可靠的记录？数据分到多台机器以后，读者会看到什么，故障又留下什么？本书沿数据模型、存储、复制、事务和共识逐层解释这些问题，再把批处理与流处理连接成应用的数据流，最后讨论系统对人的影响。

适合有基本编程与 Web 应用经验、了解关系数据库和 SQL，希望补充分布式系统基础的读者。了解 TCP、HTTP 有助于阅读。笔记会用具体操作、数据与失败情境解释机制，保留原书的推理、权衡和适用边界。

第二版新增或重写云原生与对象存储、向量索引、DataFrames、GraphQL、本地优先与同步引擎、持久化执行、形式化方法和随机化测试；一致性与共识、现代批处理也有较大调整。本站按第二版十四章组织。

## 阅读目录

已收录全部14章，14／14章，共250节、64幅章节解释图；[全书专题导航](guide.md)已整合。以下是本站学习分组，不是原书正式分部。当前目录见[概览](../index.html#chapters)，可从[第1章](ch01.md)开始阅读。

按问题复习可进入五条路线：[选型与性能](guide.md#selection-performance)、[一致性与故障](guide.md#consistency-failure)、[演化与数据流](guide.md#evolution-dataflow)、[端到端正确性](guide.md#end-to-end)、[数据责任](guide.md#data-responsibility)；另有[术语](guide.md#terms)、[案例](guide.md#cases)、[来源](guide.md#chapter-sources)与[纠错](guide.md#corrections)索引。

- 架构选择与数据基础：[1 数据系统架构的权衡取舍](ch01.md)；[2 定义非功能性需求](ch02.md)；[3 数据模型与查询语言](ch03.md)；[4 存储与检索](ch04.md)；[5 编码与演化](ch05.md)。
- 分布式数据与正确性：[6 复制](ch06.md)；[7 分片](ch07.md)；[8 事务](ch08.md)；[9 分布式系统的困难](ch09.md)；[10 一致性与共识](ch10.md)。
- 数据流与系统责任：[11 批处理](ch11.md)；[12 流处理](ch12.md)；[13 流系统的哲学](ch13.md)；[14 做正确的事](ch14.md)。

## 先辨认：哪份数据负责记录事实？

第 1 章把权威记录系统与派生数据区分开来。前者保存某项数据的权威版本，后者为某种读取用途，从已有数据生成另一种表示。例如，同一批业务记录可以供给搜索索引和分析聚合；它们属于派生数据，不因为采用不同数据库就各自成为事实来源。

从图中左侧沿实线读到权威记录，再沿虚线读到派生视图：两种箭头分别表示业务写入和派生更新。派生更新可能滞后，因此“原记录已保存”和“所有查询视图已更新”是两个状态。图示是笔记的原创概念说明，未指定具体同步协议。

![业务输入通过实线写入权威记录系统；权威记录通过虚线的提取、转换与更新形成派生视图。更新可能滞后，重建依赖源数据和转换条件。](../diagrams/exports/overview-dataflow.svg)

概览图：区分事实记录与为读取生成的表示，不表示一次共同提交。依据第 1 章 Systems of Record and Derived Data，印刷 10—11／PDF 34—35；重建条件为笔记解释。点击[查看大图](../diagrams/exports/overview-dataflow.svg)。

“可重建”也有前提：所需源数据仍被保留，转换逻辑、必要版本与其他输入条件能够恢复。这个条件提醒我们，派生不等于可以无条件删除；第 [11](ch11.md#publish)—[13 章](ch13.md#reprocessing)会进一步讨论重处理、[数据传播](ch12.md#snapshot-handoff)与正确性。

<details id="sources">
<summary>概览来源与整理说明</summary>

版本信息来自英文第二版版权页（PDF 6）。读者背景与第二版变化来自前言（印刷 xvii—xix／PDF 19—21）；十四章顺序与名称已对照原书目录。概览图根据第 1 章印刷 10—11 页重新组织，未照描原图。三个学习分组与中文表述由本站整理。

2026-11-07 实际访问[出版社已确认勘误页](https://www.oreilly.com/catalog/errata.csp?isbn=9781098119065)，页面显示未找到已确认勘误；这不代表原书没有错误。[作者参考文献仓库](https://github.com/ept/ddia2-references)用于后续定位原始材料，各章会记录实际阅读与核查范围。

</details>
