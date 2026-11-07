// Chapter-local native scenes; all exports go through the shared official API.
import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { execFileSync } from 'node:child_process';

const dir = path.dirname(fileURLToPath(import.meta.url));
const text = (id,x,y,value,size=19,color='#292824') => ({type:'text',id,x,y,text:value,fontSize:size,fontFamily:2,strokeColor:color});
const box = (id,x,y,width,height,value,dashed=false,bold=false) => ({type:'rectangle',id,x,y,width,height,strokeColor:'#386d74',backgroundColor:'#f0ece4',fillStyle:'solid',roughness:0.6,strokeWidth:bold?3:1,strokeStyle:dashed?'dashed':'solid',label:{text:value,fontSize:21,fontFamily:2,strokeColor:'#292824'}});
const arrow = (id,x,y,dx,dy,dashed=false) => ({type:'arrow',id,x,y,width:Math.abs(dx),height:Math.abs(dy),points:[[0,0],[dx,dy]],strokeColor:'#386d74',roughness:0.5,strokeStyle:dashed?'dashed':'solid'});
const line = (id,x,y,dx,dy,dashed=false) => ({type:'line',id,x,y,width:Math.abs(dx),height:Math.abs(dy),points:[[0,0],[dx,dy]],strokeColor:'#66645d',roughness:0.5,strokeStyle:dashed?'dashed':'solid'});
const header = (title,desc) => [text('title',24,18,title,25),text('subtitle',24,62,desc,17,'#66645d')];
const figures = [
  {stem:'ch08-read-skew',title:'一次原子转账，两次读取拼出不存在的总额',description:'时间向下，读者的查询跨过同一个转账提交点，读到旧账户1余额500和新账户2余额400。',elements:[
    ...header('读偏斜：一次提交，两次观察','时间向下；每次查询只读已提交值，合起来却不是同一时刻。'),
    text('reader',48,108,'读取事务',21),text('database',470,108,'数据库状态',21),
    box('read1',48,158,246,92,'① 读账户 1\n得到 500'),
    box('before',470,158,300,92,'账户 1 = 500\n账户 2 = 500'),
    arrow('query1',300,204,164,0),text('q1label',324,174,'命中旧状态',17),
    box('transfer',470,298,300,156,'同一个转账事务\n账户 1 → 600\n账户 2 → 400\n② 整体 COMMIT',false,true),
    arrow('advance1',620,256,0,36),
    line('readtimeline',26,256,0,240,true),
    text('gap',42,348,'两次查询之间，\n转账已经完成',20),
    box('read2',48,504,246,92,'③ 读账户 2\n得到 400'),
    box('after',470,504,300,92,'账户 1 = 600\n账户 2 = 400'),
    arrow('advance2',620,460,0,38),arrow('query2',300,550,164,0),
    text('q2label',324,520,'命中新状态',17),
    box('mixed',48,650,722,80,'读者：500 + 400 = 900\n实际提交前后：总额始终为 1000'),
    text('legend',24,764,'粗框：一个事务的整体提交　　横箭头：本次查询命中的状态',17,'#66645d')
  ]},
  {stem:'ch08-mvcc',title:'MVCC按快照选择版本',description:'旧快照读取500并忽略事务13的删除和插入，新快照读取400；插入删除标记是教学模型。',elements:[
    ...header('MVCC：同一行的两个版本','插入／删除标记为教学模型；事务 13 已提交，但旧快照不因此改变。'),
    box('oldreader',24,132,248,112,'旧快照\n在事务 13 开始前取点'),
    box('oldversion',478,132,300,112,'余额 500\ninserted_by = 5\ndeleted_by = 13'),
    arrow('oldvisible',278,182,194,0),text('oldvislabel',300,152,'可见：500',19),
    text('deletion',480,270,'旧快照也忽略删除标记 13，\n因此 500 仍可见。',18,'#66645d'),
    {...arrow('filtered',148,250,324,174,true),points:[[0,0],[0,90],[324,90],[324,174]],width:324,height:174},
    text('filterlabel',178,306,'旧快照忽略新版本',17,'#66645d'),
    box('newreader',24,382,248,112,'新快照\n在事务 13 提交后取点'),
    box('newversion',478,382,300,112,'余额 400\ninserted_by = 13\ndeleted_by = 空'),
    arrow('newvisible',278,446,194,0),text('newvislabel',300,456,'可见：400',19),
    text('note',24,552,'实线：当前快照可见　　虚线：被旧快照过滤\n版本能否回收，取决于是否仍有有效快照需要它。',19)
  ]},
  {stem:'ch08-write-skew',title:'写不同的行仍可能违反共同规则',description:'两名医生各自从快照读到两人在岗，各自离岗，无同行写冲突，最后无人值班。',elements:[
    ...header('写偏斜：两个局部正确决定，共同出错','规则：同一班次至少一人在岗。初始甲、乙都在岗。'),
    {...box('scope',24,118,752,212,'',true),backgroundColor:'transparent'},
    text('scope-label',44,136,'规则与读取都涉及两行',19),
    box('aread',52,190,300,106,'T甲读：甲在、乙在\n人数 2 → 可以离岗'),
    box('bread',448,190,300,106,'T乙读：甲在、乙在\n人数 2 → 可以离岗'),
    arrow('astep',202,302,0,72),arrow('bstep',598,302,0,72),
    box('awrite',52,380,300,108,'T甲：只改甲行\n甲离岗，然后提交'),
    box('bwrite',448,380,300,108,'T乙：只改乙行\n乙离岗，然后提交'),
    arrow('aend',202,494,160,74),arrow('bend',598,494,-160,74),
    box('result',122,574,556,90,'最终：甲不在、乙不在\n写集合不同，却违反“至少一人”'),
    text('note',24,706,'任何合法串行次序都会让后执行者看到只剩一人，从而拒绝离岗。',18,'#66645d')
  ]},
  {stem:'ch08-ssi-cycle',title:'SSI医生示例中的读写反依赖环',description:'甲读乙的旧状态要求甲排乙前，乙读甲的旧状态又要求乙排甲前，两要求成环；中止一方并重新读取。',elements:[
    ...header('SSI：串行顺序的要求形成环','箭头是等价串行顺序约束，不是消息，也不是实际时间。'),
    box('a',48,232,252,104,'T甲\n读乙在岗，改甲离岗'),
    box('b',500,232,252,104,'T乙\n读甲在岗，改乙离岗'),
    {...arrow('ab',180,226,440,0),points:[[0,0],[0,-80],[440,-80],[440,0]],width:440,height:80},
    text('ab-label',264,108,'甲读乙旧值：甲必须在乙前',19),
    {...arrow('ba',620,342,-440,0),points:[[0,0],[0,80],[-440,80],[-440,0]],width:440,height:80},
    text('ba-label',264,444,'乙读甲旧值：乙必须在甲前',19),
    box('retry',48,522,704,110,'两个顺序要求无法同时满足\n示意：甲提交，乙中止 → 乙重读后发现只剩一人'),
    text('note',24,670,'rw 反依赖：旧版本读者 → 改变该值的写者。\n这里只画最小环；实际 SSI 还使用危险结构与提交顺序规则。',18,'#66645d')
  ]},
  {stem:'ch08-2pc-normal',title:'两阶段提交中的持久承诺和持久决定',description:'时间向下。参与者持久保存prepared再投YES，协调者收齐YES后持久决定COMMIT，再将决定发给参与者。',elements:[
    ...header('2PC：先持久承诺，再持久决定','简化成功路径；P、Q 已经完成尚未提交的业务读写。'),
    text('ptitle',62,110,'参与者 P',21),text('ctitle',350,110,'协调者 C',21),text('qtitle',652,110,'参与者 Q',21),
    line('p-life',120,146,0,584,true),line('c-life',414,146,0,584,true),line('q-life',710,146,0,584,true),
    arrow('prep-p',408,178,-282,0),arrow('prep-q',420,178,284,0),
    text('prep-label1',204,150,'① prepare',18),text('prep-label2',508,150,'① prepare',18),
    box('p-durable',24,230,192,90,'② 持久保存\nPREPARED',false,true),
    box('q-durable',614,230,192,90,'② 持久保存\nPREPARED',false,true),
    arrow('yes-p',126,362,282,0,true),arrow('yes-q',704,362,-284,0,true),
    text('yeslabel1',208,332,'③ YES',18),text('yeslabel2',522,332,'③ YES',18),
    box('c-durable',294,406,240,94,'④ 收齐 YES 后\n持久决定 COMMIT',false,true),
    arrow('commit-p',408,548,-282,0),arrow('commit-q',420,548,284,0),
    text('commitlabel1',178,518,'⑤ COMMIT',18),text('commitlabel2',510,518,'⑤ COMMIT',18),
    box('p-done',24,598,192,90,'⑥ 记录提交\n释放事务资源'),
    box('q-done',614,598,192,90,'⑥ 记录提交\n释放事务资源'),
    arrow('ack-p',126,728,282,0,true),arrow('ack-q',704,728,-284,0,true),
    text('acklabel1',218,698,'完成响应',17),text('acklabel2',520,698,'完成响应',17),
    text('legend',24,780,'粗框：持久化边界　　实线：请求　　虚线：响应／时间线\n参与者答 YES 后、协调者作决定后，都不能随意反悔。',18,'#66645d')
  ]},
  {stem:'ch08-2pc-recovery',title:'协调者恢复后重发同一个决定',description:'C持久记录COMMIT，Q完成但P未获通知，C崩溃；P保留prepared和锁，恢复的C读原日志并重发COMMIT。',elements:[
    ...header('2PC 恢复：超时不能替代缺失的决定','时间向下；同一事务 T。以下是已持久决定 COMMIT 的历史。'),
    text('p-head',50,112,'参与者 P',21),text('c-head',352,112,'协调者 C',21),text('q-head',652,112,'参与者 Q',21),
    box('p-prepared',24,170,192,86,'已 PREPARED\n已回复 YES'),
    box('decision',294,170,240,86,'持久日志\nT → COMMIT',false,true),
    box('q-commit',614,170,192,86,'已收到决定\n完成 COMMIT'),
    arrow('q-delivered',540,210,68,0),
    arrow('p-undelivered',288,210,-66,0,true),text('notreceived',218,270,'未送达 P',17),
    arrow('c-crash',414,262,0,52),box('crashed',294,320,240,80,'C 崩溃'),
    box('p-wait',24,320,192,148,'P 仍然存疑\n保留修改和锁\n不能超时中止',true),
    text('q-note',610,336,'Q 已提交，\n不会因 C 崩溃\n自动回滚。',19),
    arrow('c-restart',414,406,0,78),
    box('recovery',294,490,240,94,'恢复者读取原日志\n仍为 T → COMMIT',false,true),
    {...arrow('resend',288,540,-168,78),points:[[0,0],[-168,0],[-168,78]],width:168,height:78},
    text('resend-label',24,500,'重发原决定',17),
    box('p-complete',24,624,192,86,'P 完成提交\n释放锁'),
    text('other-history',286,642,'若从未形成持久 COMMIT，\n完整恢复日志可支持中止；\n日志损坏不等于“从未提交”。',19),
    text('legend',24,758,'实线：已送达／恢复步骤　　虚线：未送达／等待状态',17,'#66645d')
  ]},
  {stem:'ch08-idempotent',title:'消息ID、业务写和结果在同一个数据库事务内',description:'先用唯一消息ID去重，首次处理写业务和结果，重复处理读取原结果；两分支提交后都确认，提交后确认前崩溃通过重投恢复。',elements:[
    ...header('幂等消费：让重投递只重复交接，不重复生效','假设稳定消息 ID、唯一约束，且去重记录仍保留。'),
    box('delivery',260,110,300,72,'接收消息 ID = m'),
    {...box('transaction',24,232,772,360,'',false,true),backgroundColor:'transparent'},
    text('txn-label',44,246,'同一个数据库事务',21),
    box('claim',240,292,340,72,'尝试插入唯一 ID = m'),arrow('begin',410,188,0,98),
    box('first',52,432,300,98,'首次：插入成功\n更新业务，并保存结果'),
    box('duplicate',448,432,300,98,'重复：ID 已存在\n读取原结果，跳过业务写'),
    arrow('first-path',310,370,-108,56),arrow('duplicate-path',510,370,88,56),
    text('commit-label',312,550,'整体 COMMIT',21),
    arrow('ack-path',410,598,0,60),box('ack',260,664,300,76,'确认当前投递（ack）'),
    {...arrow('retry',676,618,0,-420,true),points:[[0,0],[88,0],[88,-420],[-90,-420],[-90,-472],[-110,-472]],width:198,height:472},
    text('crash',468,610,'此处崩溃 → 重投',17),
    text('legend',24,786,'粗框：数据库原子边界　　虚线：提交后确认前故障引起重投\n两条分支都在提交后 ack；外部邮件不在此事务框内。',18,'#66645d')
  ]}
];

for (const figure of figures) {
  if (process.argv[2] && process.argv[2] !== figure.stem) continue;
  const input = path.join(dir, `${figure.stem}.skeleton.json`);
  await fs.writeFile(input, JSON.stringify(figure.elements, null, 2) + '\n');
  execFileSync(process.execPath, [path.join(dir, 'export-excalidraw.mjs'), input, figure.title, figure.description], {stdio:'inherit'});
}
