// Chapter-local native scenes. Reuse the shared official Excalidraw exporter.
import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { execFileSync } from 'node:child_process';

const dir = path.dirname(fileURLToPath(import.meta.url));
const text = (id,x,y,value,size=19,color='#292824') => ({type:'text',id,x,y,text:value,fontSize:size,fontFamily:2,strokeColor:color});
const box = (id,x,y,width,height,value,dashed=false,bold=false) => ({type:'rectangle',id,x,y,width,height,strokeColor:'#386d74',backgroundColor:'#f0ece4',fillStyle:'solid',roughness:0.6,strokeWidth:bold?3:1,strokeStyle:dashed?'dashed':'solid',...(value?{label:{text:value,fontSize:21,fontFamily:2,strokeColor:'#292824'}}:{})});
const arrow = (id,x,y,dx,dy,dashed=false) => ({type:'arrow',id,x,y,width:Math.abs(dx),height:Math.abs(dy),points:[[0,0],[dx,dy]],strokeColor:'#386d74',roughness:0.5,strokeStyle:dashed?'dashed':'solid'});
const line = (id,x,y,dx,dy,dashed=false) => ({type:'line',id,x,y,width:Math.abs(dx),height:Math.abs(dy),points:[[0,0],[dx,dy]],strokeColor:'#66645d',roughness:0.5,strokeStyle:dashed?'dashed':'solid'});
const header = (title,desc) => [text('title',24,18,title,25),text('subtitle',24,62,desc,17,'#66645d')];
const figures = [
  {stem:'ch10-linearization',title:'与写并发的两次读，也必须共享同一个顺序',description:'写W在2到10之间，A在3到4返回1，B在5到6若返回0则矛盾；W必须先于A，而A实时先于B。',elements:[
    ...header('线性化：区间可以重叠，解释不能互相矛盾','初值 x = 0，只有 W 写入 1；时间向右，数值为假设。'),
    arrow('time',150,140,640,0),text('time-label',150,108,'时间',17),
    ...[2,3,4,5,6,10].flatMap(t=>[line('tick'+t,150+60*t,135,0,10),text('number'+t,143+60*t,108,String(t),17)]),
    text('w-label',24,203,'W：写入 1',21),box('w',270,194,480,42,''),
    line('w-point',342,185,0,60),text('w-end',588,249,'10：写才返回',18),
    text('a-label',24,300,'A：读到 1',21),box('a',330,290,60,42,''),line('a-point',360,281,0,60),
    text('a-note',422,300,'A 返回时，W 必须已生效',19),
    text('b-label',24,397,'B：若读到 0',21),box('b',450,386,60,42,'',true),line('b-point',480,377,0,60),
    text('b-note',542,397,'无法解释！',21),
    box('order-w',150,498,150,72,'W 生效'),box('order-a',390,498,150,72,'A 读到 1'),box('order-b',630,498,150,72,'B 必须读 1'),
    arrow('wa',306,534,78,0),arrow('ab',546,534,78,0),
    text('forced',24,608,'横条：调用—返回区间　短竖线：候选线性化点\n箭头：读结果与实时先后强制的顺序；B 返回 0 时不存在合法排法。',18,'#66645d')
  ]},
  {stem:'ch10-cross-channel',title:'通知路径快于文件复制，转码器可能读到旧版本',description:'先写文件并获得确认，再发队列通知。文件内部复制仍未完成时，转码器已收到通知并读取落后副本。',elements:[
    ...header('跨通道竞态：消息到了，新文件还没到','沿编号阅读；实线为应用操作，虚线为仍在途中的复制。'),
    box('web',24,170,180,120,'Web 服务'),box('primary',314,170,210,120,'写入副本\n已保存新视频'),box('replica',624,170,190,120,'读取副本\n仍是旧版本'),
    arrow('write',210,208,98,0),text('write-label',214,177,'① 写文件',17),
    arrow('ack',308,266,-98,0),text('ack-label',214,272,'② 已确认',17),
    arrow('replication',530,226,88,0,true),text('replication-label',544,185,'复制中',17),
    arrow('enqueue',114,296,0,178),text('enqueue-label',130,356,'③ 发通知',19),
    box('queue',24,480,180,90,'消息队列'),box('worker',624,480,190,90,'转码器'),
    arrow('delivery',210,526,408,0),text('delivery-label',318,491,'通知先到达',19),
    arrow('read',718,474,0,-178),text('read-label',500,356,'④ 读：拿到旧版本',19),
    box('failure',24,632,790,90,'结果：对旧原片转码，或读到“文件不存在”\n等待固定几秒，不能证明复制已经完成'),
    text('legend',24,758,'修复方向：线性一致存储；或传递版本／进度依赖，并等待目标版本可读。',18,'#66645d')
  ]},
  {stem:'ch10-clock-orders',title:'已传播的因果依赖，与系统不知道的现实先后',description:'上图B接收A和C时间戳后生成更大时间戳；下图权限更新15在现实中先于照片12，快照13却只看见照片。',elements:[
    ...header('逻辑时钟：知道的依赖才能进入顺序','上半部传播依赖；下半部只存在用户跨设备的现实先后。'),
    box('a',24,132,250,86,'A 发消息\n(1, A)'),box('c',24,272,250,86,'C 独立发消息\n(1, C)'),
    box('b',494,202,320,112,'B 收到两条消息\n计数器提升到 1\n回复：(2, B)'),
    arrow('a-b',280,176,208,62),arrow('c-b',280,316,208,-42),
    text('visible',326,348,'箭头携带时间戳：回复排在原因之后',18),
    line('divider',24,410,790,0,true),
    box('privacy',24,472,280,106,'笔记本：改为私密\n账号库时间戳 15'),
    box('photo',514,472,300,106,'手机：上传照片\n照片库时间戳 12'),
    arrow('real-order',310,524,198,0),text('real-label',338,470,'先完成，再开始',17),
    text('no-context',310,552,'未传递时钟上下文',17),
    box('snapshot',24,634,790,96,'快照 13：照片 12 已可见，私密设置 15 却不可见\n系统仍读到先前的“公开”，违背用户的实际操作顺序'),
    text('legend',24,766,'上方箭头：系统消息依赖　下方箭头：用户行动顺序，非数据库消息。',18,'#66645d')
  ]},
  {stem:'ch10-log-handoff',title:'多数派交接必须保留已提交历史',description:'任期7的A和B保存当前任期条目X并提交，任期8由携带X的B与C接管；共同节点B需要遵循持久记忆和日志继承规则。',elements:[
    ...header('日志接管：交集是证据相遇的地方','固定三投票节点，多数派为 2；X 是任期 7、槽位 8 的条目。'),
    text('old-term',24,118,'任期 7：A + B 持久保存当前任期的 X → 可以提交',21),
    box('a-old',54,184,210,116,'主节点 A\n保存 X',false,true),box('b-old',334,184,210,116,'节点 B\n保存 X',false,true),box('c-old',614,184,210,116,'节点 C\n尚未收到 X',true),
    line('ab-evidence',270,244,58,0),
    arrow('memory',439,306,0,148),text('memory-label',460,350,'B 保留 X\n并遵守继承规则',19),
    text('a-crash',72,354,'A 与其余节点失联',18),
    box('a-new',54,460,210,116,'旧主 A\n无法独自提交',true),box('b-new',334,460,210,116,'新主 B\n携带 X 接管',false,true),box('c-new',614,460,210,116,'节点 C\n从 B 补齐 X',false,true),
    arrow('copy-x',550,518,58,0),
    text('new-term',24,620,'任期 8：B + C 形成新多数派；已提交 X 不能被推翻',21),
    text('legend',24,680,'粗框：该阶段多数派　虚框：落后／失联节点\n交集还需持久任期、投票限制与日志继承；不是“碰到同一节点就安全”。',18,'#66645d')
  ]},
  {stem:'ch10-read-barrier',title:'线性一致读的三类证据',description:'新主先建立当前任期提交依据，为当前读记录读位置并获得匹配的多数派确认，再等待状态机应用到读位置，才返回。',elements:[
    ...header('安全读取：资格、提交知识、应用进度缺一不可','无租约的 Raft ReadIndex 路径；箭头表示完成条件的依赖。'),
    box('term',24,126,452,100,'① 新主建立当前任期提交依据\n常用方式：提交当前任期空操作'),
    text('term-note',514,146,'通常每任期建立一次，\n不是每次读都写空操作。',19),
    arrow('to-confirm',250,232,0,54),
    box('confirm',24,292,452,120,'② 为当前读记录安全读位置\n等待与该读匹配的多数派确认\n得到可使用的 readIndex'),
    text('isolated',514,316,'隔离旧主：拿不到确认\n→ 不能凭“我是主”返回',19),
    arrow('to-apply',250,418,0,54),
    box('apply',24,478,452,100,'③ 等待本地状态机追上\nappliedIndex ≥ readIndex'),
    text('lagging',514,496,'日志到 50，应用到 48：\n→ 仍须等条目 49、50 执行',19),
    arrow('to-read',250,584,0,54),box('return',24,644,452,76,'读取状态机，然后返回'),
    text('follower',514,652,'从节点也可取得安全读位置，\n等自己应用完成后服务读。',18),
    text('legend',24,764,'租约读可摊销资格确认，但必须另外证明时间与租约假设。',18,'#66645d')
  ]},
  {stem:'ch10-coordination',title:'小型控制面提供归属，资源端落实隔离',description:'协调服务保存分片归属和代次42，通知异步更新路由缓存；业务数据直接从工作节点到存储，存储拒绝小于已接受代次42的旧请求。',elements:[
    ...header('协调服务：控制决定小，业务数据流大','实线：控制请求／业务访问　虚线：异步变更通知。'),
    box('control',24,124,790,162,'',false,true),
    text('control-label',44,138,'小型控制面：3 个投票副本保存同一份决定',21),
    box('r1',54,188,178,70,'副本 1'),box('r2',330,188,178,70,'副本 2'),box('r3',606,188,178,70,'副本 3'),
    line('r12',238,223,86,0),line('r23',514,223,86,0),
    text('state',238,308,'分片 7 → 工作节点 B，代次 42',21),
    arrow('lease',190,292,0,148),text('lease-label',36,354,'授予归属\n与令牌 42',18),
    arrow('watch',686,292,0,148,true),text('watch-label',700,354,'变更\n通知',18),
    box('worker',24,446,332,100,'工作节点 B\n持有代次 42'),box('cache',560,446,254,100,'路由缓存\n稍后才更新'),
    arrow('business',190,552,0,108),text('business-label',210,590,'业务写：携带 42',19),
    box('storage',24,666,332,100,'业务数据存储\n原子检查并记录代次'),
    box('old',560,666,254,100,'恢复的旧节点 A\n仍携带 41',true),
    arrow('stale',554,716,-192,0),text('stale-label',386,678,'41：拒绝',19),
    text('legend',24,808,'资源已接受 42 后拒绝旧代次 41；通知到达，不等于旧节点已经停机。',18,'#66645d')
  ]}
];

for (const figure of figures) {
  if (process.argv[2] && process.argv[2] !== figure.stem) continue;
  const input = path.join(dir, `${figure.stem}.skeleton.json`);
  await fs.writeFile(input, JSON.stringify(figure.elements, null, 2) + '\n');
  execFileSync(process.execPath, [path.join(dir, 'export-excalidraw.mjs'), input, figure.title, figure.description], {stdio:'inherit'});
}
