// Chapter-local native scenes. Exports and editor round trips use the shared official tool.
import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { execFileSync } from 'node:child_process';

const dir = path.dirname(fileURLToPath(import.meta.url));
const text = (id,x,y,value,size=19,color='#292824') => ({type:'text',id,x,y,text:value,fontSize:size,fontFamily:2,strokeColor:color});
const box = (id,x,y,width,height,value,dashed=false) => ({type:'rectangle',id,x,y,width,height,strokeColor:'#386d74',backgroundColor:'#f0ece4',fillStyle:'solid',roughness:0.6,strokeWidth:1,strokeStyle:dashed?'dashed':'solid',label:{text:value,fontSize:21,fontFamily:2,strokeColor:'#292824'}});
const arrow = (id,x,y,dx,dy,dashed=false) => ({type:'arrow',id,x,y,width:Math.abs(dx),height:Math.abs(dy),points:[[0,0],[dx,dy]],strokeColor:'#386d74',roughness:0.5,strokeStyle:dashed?'dashed':'solid'});
const line = (id,x,y,dx,dy,dashed=false) => ({type:'line',id,x,y,width:Math.abs(dx),height:Math.abs(dy),points:[[0,0],[dx,dy]],strokeColor:'#66645d',roughness:0.5,strokeStyle:dashed?'dashed':'solid'});
const header = (title,desc) => [text('title',24,18,title,25),text('subtitle',24,62,desc,17,'#66645d')];
const figures = [
  {stem:'ch12-log-groups',title:'日志分片与独立消费者组',description:'组A内A1读P0、A2读P1，组B的B1独立读取两分片；位点表示该组下一条读取位置。',elements:[
    ...header('日志保留数据，消费者组各自保存进度','经典分片分工模型；每个分片内有序，没有跨分片全序。'),
    text('logs',24,112,'同一个主题',21),
    box('p0',24,170,248,104,'分片 P0\n… 40 → 41 → 42 …'),
    box('p1',24,394,248,104,'分片 P1\n… 16 → 17 → 18 …'),
    {...box('a-scope',450,114,334,236,'',true),backgroundColor:'transparent'},
    text('a-name',470,130,'组 A：组内分工',21),
    box('a1',476,174,282,68,'A1 读 P0；next = 42'),
    box('a2',476,260,282,68,'A2 读 P1；next = 18'),
    arrow('p0-a',278,206,192,0),arrow('p1-a',278,412,192,-118),
    {...box('b-scope',450,390,334,174,'',true),backgroundColor:'transparent'},
    text('b-name',470,406,'组 B：独立订阅',21),
    box('b1',476,450,282,86,'B1 读 P0 和 P1\nnext：P0 = 40，P1 = 16'),
    arrow('p0-b',278,250,192,222),arrow('p1-b',278,480,192,32),
    text('note',24,614,'实线：分片被哪个成员读取　　虚线框：消费者组\n读取不删除日志；两组可用不同速度处理同一批事件。',19,'#66645d')
  ]},
  {stem:'ch12-cdc-order',title:'独立双写与CDC的顺序差别',description:'独立双写中数据库最终B、索引最终A；CDC让数据库的A到B顺序成为下游应用的依据，但传播仍然异步。',elements:[
    ...header('全部请求成功，独立双写仍可能分歧','同一键 X；甲想写 A，乙想写 B。箭头表示各系统的应用先后。'),
    text('dual',24,116,'① 应用分别写两边',21),
    text('db-name',24,182,'数据库',21),box('db-a',174,160,184,74,'甲写 A'),box('db-b',448,160,184,74,'乙写 B'),
    arrow('db-order',364,197,78,0),text('db-final',660,184,'最终 B',21),
    text('idx-name',24,304,'索引',21),box('idx-b',174,282,184,74,'乙写 B'),box('idx-a',448,282,184,74,'甲写 A'),
    arrow('idx-order',364,319,78,0),text('idx-final',660,306,'最终 A',21),
    text('pause',174,384,'甲在数据库写成功后暂停；乙先完成索引写入。',19,'#66645d'),
    line('separator',24,440,760,0),text('cdc-name',24,476,'② CDC 从权威提交记录传播',21),
    box('db-log',24,546,236,110,'数据库\n提交顺序 A → B'),box('cdc-log',302,546,196,110,'变更流\nA → B'),box('index',540,546,244,110,'索引依次应用\n最终 B'),
    arrow('capture',266,601,30,0),arrow('propagate',504,601,30,0),
    text('note',24,704,'CDC 路径是异步传播，不是跨系统共同事务。\n下游仍需守住同键顺序、重试和删除语义。',19,'#66645d')
  ]},
  {stem:'ch12-snapshot-cut',title:'一致快照与变更日志在位置100衔接',description:'S100包含A10和B20，依次应用101改A11、102删B、103增C30，最终A11与C30；不能在快照复制后直接跳到104。',elements:[
    ...header('快照是一份基线，日志接着推进它','笔记假设；数字是同一源日志位置，不是墙上时钟。'),
    box('snapshot',24,142,212,132,'一致快照 S100\nA = 10\nB = 20'),
    line('cut',270,106,0,214,true),text('cut-label',248,334,'切点 100',19),
    box('e101',302,156,136,104,'101\nA → 11'),box('e102',474,156,136,104,'102\n删除 B'),box('e103',646,156,136,104,'103\nC → 30'),
    arrow('l1',444,208,24,0),arrow('l2',616,208,24,0),text('keep',320,296,'复制期间保留 100 之后的变化',19,'#66645d'),
    arrow('load',130,280,0,160),box('base',24,446,212,110,'① 装载 S100\n{A:10, B:20}'),
    box('apply',302,446,220,110,'② 顺序应用\n101 → 102 → 103'),box('result',588,446,196,110,'③ 当前结果\n{A:11, C:30}'),
    arrow('a1',242,500,54,0),arrow('a2',528,500,54,0),
    text('failure',24,608,'错误衔接：装载 S100 后直接读 104，会漏掉三次变化。\n错误混合：先应用 A=11，再装入旧快照 A=10，会倒退。',19),
    text('legend',24,696,'虚线：快照切点　　上排箭头：源日志顺序　　下排：目标重建步骤',17,'#66645d')
  ]},
  {stem:'ch12-watermark-late',title:'窗口先输出、迟到更正与最终清理',description:'处理顺序向右；事件时间窗口为10点到10点01分。水位线10点01分输出2，清理前迟到更正3，水位线10点03分清理后进入旁路。',elements:[
    ...header('同一窗口可以先给结果，再接受迟到更正','笔记假设：[10:00, 10:01)；清理界限 W = 10:03。'),
    arrow('time',24,140,760,0),text('time-label',24,104,'处理先后 →',18),
    box('on-time',24,194,162,154,'先到两条\n事件时间\n10:00:10\n10:00:40'),box('first',224,194,162,154,'W = 10:01\n首次输出\n计数 2'),
    box('late',424,194,162,154,'清理前迟到\n事件时间\n10:00:25\n计数改为 3'),box('clean',624,194,162,154,'W = 10:03\n清理状态\n之后不再改'),
    arrow('step1',192,270,26,0),arrow('step2',392,270,26,0),arrow('step3',592,270,26,0),
    box('output',224,420,362,110,'同一个窗口键 K\nK → 2，再更新为 K → 3'),arrow('emit1',305,354,0,60),arrow('emit2',505,354,0,60),
    box('too-late',624,420,162,110,'更晚的旧事件\n旁路或丢弃'),arrow('side',705,354,0,60),
    text('not-add',24,584,'下游必须理解“替换／撤回”：最终是 3，不是 2 + 3 = 5。',20),
    text('legend',24,640,'W 是事件时间进度判断；图中清理时间是教学约定，非产品默认。\n事件标签是发生时间；横轴只表示本次运行的处理次序。',17,'#66645d')
  ]},
  {stem:'ch12-join-state',title:'三类流连接保存什么状态、谁触发输出',description:'流流缓存两侧近期事件；流表由档案CDC维护本地表并由活动触发丰富；表表保存两侧当前表，由任一侧变化维护结果。',elements:[
    ...header('连接的差别：保存什么，什么变化触发输出','三行是语义对照；不是部署拓扑。'),
    text('h1',24,112,'输入／触发',19),text('h2',306,112,'受管理状态',19),text('h3',600,112,'输出',19),
    box('ss-input',24,164,226,128,'流—流\n搜索或点击到来'),box('ss-state',300,164,246,128,'两侧近期事件\n按键、时间索引'),box('ss-out',596,164,190,128,'匹配记录\n到期后判未匹配'),
    arrow('ss1',256,226,38,0),arrow('ss2',552,226,38,0),text('ss-note',24,316,'点击也可能先到；两侧都需要可等待的状态。',18,'#66645d'),
    line('sep1',24,364,762,0),
    box('st-input',24,410,226,128,'流—表\n活动到来触发查询'),box('st-state',300,410,246,128,'本地档案表\nCDC 更新当前值'),box('st-out',596,410,190,128,'丰富后的活动\n通常不追溯改写'),
    arrow('st1',256,472,38,0),arrow('st2',552,472,38,0),text('st-note',24,562,'档案变化只更新表；使用哪个历史版本还需单独约定。',18,'#66645d'),
    line('sep2',24,610,762,0),
    box('tt-input',24,656,226,128,'表—表\n帖子或关注变化'),box('tt-state',300,656,246,128,'两侧当前表\n以及必要索引'),box('tt-out',596,656,190,128,'维护当前时间线\n插入／删除配对'),
    arrow('tt1',256,718,38,0),arrow('tt2',552,718,38,0),text('tt-note',24,808,'任一侧更新都可能改变已有结果；输出必须理解更正。',18,'#66645d'),
    text('legend',24,866,'箭头：由输入经状态计算结果；每类状态都需要一致恢复。',17,'#66645d')
  ]},
  {stem:'ch12-checkpoint-cut',title:'检查点协调源位置与算子状态',description:'两路屏障之前的记录共同形成一致恢复切面；收到屏障只是开始或固定快照，所需持久化确认收齐并记录完成后才可恢复。',elements:[
    ...header('检查点保存的是一致切面，不是任意两份备份','对齐方案；每路从左向右处理。虚线不是共同墙上时刻。'),
    text('alabel',24,132,'输入 A',21),box('a-before',126,108,222,78,'屏障 n 之前'),box('a-after',446,108,222,78,'屏障 n 之后'),arrow('a1',354,146,86,0),
    text('blabel',24,256,'输入 B',21),box('b-before',126,232,222,78,'屏障 n 之前'),box('b-after',446,232,222,78,'屏障 n 之后'),arrow('b1',354,270,86,0),
    line('cut',398,98,0,234,true),text('n',376,350,'屏障 n',19),
    text('align',24,404,'先收到屏障的一路暂缓处理；另一侧追到 n 后，固定状态版本。',19),
    box('snapshot',24,470,322,126,'快照 n\n源位点 + 算子状态\n状态可异步上传'),box('complete',466,470,322,126,'协调者\n收齐必需的持久化确认\n可靠记录 n 完成'),
    arrow('ack',352,530,108,0),text('ack-label',370,500,'确认',18),arrow('recover',626,602,0,64),
    box('restore',24,672,764,102,'故障后同时恢复 n 的源位点与状态\n未完成检查点不能使用；n 之后输入重新处理'),
    text('legend',24,820,'实线：处理或完成确认　　虚线：逻辑恢复切面\n只见到屏障 ≠ 检查点已完成；外部输出还需提交协议。',18,'#66645d')
  ]},
  {stem:'ch12-effect-boundary',title:'恰好一次的保证必须跨越实际提交边界',description:'输入位点、受管状态和输出可由同一处理协议协调；外部邮件支付不自动加入，需稳定业务ID和接收方原子去重或提交合作。',elements:[
    ...header('恰好一次：先标明协议能管理哪些效果','执行可以重试；要约束的是可见效果是否重复。'),
    {...box('scope',24,122,764,286,'',true),backgroundColor:'transparent'},text('scope-title',46,144,'明确的处理／提交协议范围（概念图）',21),
    box('offset',48,218,208,114,'输入位点\n恢复到正确前缀'),box('state',302,218,208,114,'受管状态\n与位点一致'),box('out',556,218,208,114,'输出记录\n提交或原子去重'),
    arrow('inside1',262,274,34,0),arrow('inside2',516,274,34,0),text('inside-note',48,366,'框内不是自动成立：必须有实际事务或恢复协议。',18,'#66645d'),
    arrow('cross',660,414,0,102),text('cross-label',224,450,'跨界调用不会随状态恢复而撤销',18),
    box('external',478,522,310,118,'外部邮件／支付服务\n执行成功但响应丢失\n重试是否再次生效？'),box('receiver',24,522,350,118,'接收方配合\n稳定业务 ID\n原子去重 + 执行动作'),arrow('contract',380,580,92,0),
    text('end',24,700,'保证只能延伸到接收方实际承诺的动作，不能延伸到用户行为。',19),text('legend',24,752,'虚线框：保证范围，不是进程边界　　实线：处理或调用关系',17,'#66645d')
  ]}
];

for (const figure of figures) {
  if (process.argv[2] && process.argv[2] !== figure.stem) continue;
  const input = path.join(dir, `${figure.stem}.skeleton.json`);
  await fs.writeFile(input, JSON.stringify(figure.elements, null, 2) + '\n');
  execFileSync(process.execPath, [path.join(dir, 'export-excalidraw.mjs'), input, figure.title, figure.description], {stdio:'inherit'});
}
