// Chapter 9 native Excalidraw scenes. Run once to author; later edit/re-export .excalidraw.
import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { execFileSync } from 'node:child_process';
const dir=path.dirname(fileURLToPath(import.meta.url));
const text=(id,x,y,value,size=19,muted=false)=>({type:'text',id,x,y,text:value,fontSize:size,fontFamily:2,strokeColor:muted?'#66645d':'#292824'});
const box=(id,x,y,width,height,value,dashed=false)=>({type:'rectangle',id,x,y,width,height,strokeColor:'#386d74',backgroundColor:'#f0ece4',fillStyle:'solid',roughness:0.5,strokeWidth:1.5,strokeStyle:dashed?'dashed':'solid',label:{text:value,fontSize:21,fontFamily:2,strokeColor:'#292824'}});
const arrow=(id,x,y,dx,dy,start,end,dashed=false)=>({type:'arrow',id,x,y,width:Math.abs(dx),height:Math.abs(dy),points:[[0,0],[dx,dy]],strokeColor:'#386d74',roughness:0.4,strokeStyle:dashed?'dashed':'solid',...(start?{start:{id:start}}:{}),...(end?{end:{id:end}}:{})});
const header=(title,desc)=>[text('title',24,20,title,25),text('subtitle',24,66,desc,17,true)];
const figures=[
 {stem:'ch09-timeout',title:'一个超时观察，多种远端事实',description:'请求未到、远端暂停、执行后响应丢失都可表现为客户端没有响应；超时无法判断是否已执行。',elements:[
  ...header('超时：没有响应，不等于没有执行','从左到右读；× 表示未送达，虚线表示仍在等待。'),
  box('lost',24,126,338,94,'请求在途中丢失 ×\n远端尚未执行'),
  box('paused',24,272,338,94,'请求已到，服务端暂停\n稍后可能继续执行',true),
  box('done',24,418,338,94,'远端已执行\n成功响应丢失 ×'),
  box('observation',548,272,276,100,'客户端超时\n仍然不知道业务结果'),
  arrow('a',368,173,174,116,'lost','observation'),
  arrow('b',368,319,174,0,'paused','observation',true),
  arrow('c',368,465,174,-111,'done','observation'),
  text('note',24,564,'超时结束的是本次等待；原请求仍可能排队、执行或已经提交。',19)
 ]},
 {stem:'ch09-clock-order',title:'墙上时钟顺序可以违背因果顺序',description:'节点3收到节点1的x等于1后加一为2，但本地42.003小于原写42.004，节点2的LWW选择1。',elements:[
  ...header('LWW：更大的时间戳，未必是后一次写','上方实线表示因果依赖；下方虚线表示复制，不表示到达先后。'),
  box('n1',24,142,296,118,'节点 1：A 写入\nx = 1\n时间戳 42.004'),
  box('n3',514,142,310,118,'节点 3：收到 1 后加一\nx = 2\n时间戳 42.003'),
  arrow('causal',326,201,182,0,'n1','n3'),text('causal-label',346,166,'先复制 x = 1',18),
  box('n2',228,392,394,118,'节点 2 比较 LWW\n42.004 > 42.003\n保留 1，丢掉后来的加一'),
  arrow('copy1',172,266,142,120,'n1','n2',true),
  arrow('copy3',669,266,-142,120,'n3','n2',true),
  text('c1',70,322,'x=1 / 42.004',18),text('c3',646,322,'x=2 / 42.003',18),
  text('note',24,554,'B 明确依赖 A；收敛到同一个值，仍可能丢失因果上更新的结果。',19)
 ]},
 {stem:'ch09-lease-gap',title:'授权转移后，两条陈旧写路径仍然存在',description:'锁服务将租约从A转移给B，但A恢复的写或A崩溃前已发送的延迟写仍能到达资源。',elements:[
  ...header('租约服务正确，资源仍可能被旧写覆盖','上方表示授权转移；下方表示陈旧请求，箭头不是精确时间比例。'),
  box('old',24,126,240,88,'① A 持有租约'),
  box('expired',326,126,180,88,'② 到期'),
  box('new',568,126,256,88,'③ B 获得新租约'),
  arrow('expire',270,170,50,0,'old','expired'),arrow('grant',512,170,50,0,'expired','new'),
  box('pause',24,304,332,96,'路径一：A 暂停后恢复\n仍携旧认识发写入'),
  box('delay',24,470,332,96,'路径二：A 已崩溃\n此前发出的写入迟到'),
  box('storage',570,358,254,138,'资源已接受 B 的写\n又收到 A 的旧写\n凭什么拒绝？'),
  arrow('b-write',696,220,0,132,'new','storage'),text('b-write-label',712,264,'先完成新写',17),
  arrow('zombie',362,352,202,44,'pause','storage',true),
  arrow('late',362,518,202,-44,'delay','storage',true),
  text('note',24,620,'停止旧进程不能撤回在途消息；资源入口也必须识别旧授权。',19)
 ]},
 {stem:'ch09-fencing',title:'隔离在资源接受新代次后生效',description:'A持有33，B取得34后在资源完成代次推进；资源保存34并拒绝33，同代次后续写可继续。',elements:[
  ...header('隔离令牌：授权在服务端，拒绝在资源端','按 ①—⑤ 读；每次资源操作的检查与修改必须原子、持久。'),
  box('locks',280,120,300,88,'租约服务\n每次新授权递增令牌'),
  box('a',24,300,280,100,'① A 得到 33\n暂停／请求延迟'),
  box('b',554,300,280,100,'② B 得到 34\n准备建立隔离'),
  arrow('grant33',310,214,-146,80,'locks','a'),arrow('grant34',548,214,146,80,'locks','b'),
  box('resource',280,494,300,132,'③ 成功记录 max = 34\n④ 之后拒绝 33\n⑤ 允许同代次 34'),
  arrow('advance',694,406,-156,82,'b','resource'),text('adv-label',620,446,'推进代次 34',18),
  arrow('stale',164,406,156,82,'a','resource',true),text('stale-label',42,446,'迟到的 33：拒绝',18),
  text('barrier',24,680,'③ 完成是交接屏障；B 应在此后读取最新状态并继续业务。',19),
  text('note',24,716,'只发令牌、不检查资源，无法阻挡陈旧写；同代次乱序另需处理。',17,true)
 ]},
 {stem:'ch09-replica-fencing',title:'多数副本的新代次决定法定人数读结果',description:'R1和R2已保存34，R3可能接受33；任意两副本读取均包含34，按代次优先比较胜出，再异步修复R3。',elements:[
  ...header('多副本隔离：局部旧写，不成为读取胜者','假设固定 3 副本，成功写 2、读取 2，读者取最大版本。'),
  box('r1',24,136,234,104,'R1：保存 (34,1)\n拒绝后来的 33'),
  box('r2',308,136,234,104,'R2：保存 (34,1)\n拒绝后来的 33'),
  box('r3',592,136,234,104,'R3：暂存 (33,999)\n还没见过 34',true),
  text('order',24,286,'比较规则：(代次, 代内序号)；先比代次，故 (34,1) > (33,999)。',19),
  box('q12',24,358,234,90,'读 R1 + R2\n选 (34,1)'),
  box('q13',308,358,234,90,'读 R1 + R3\n选 (34,1)'),
  box('q23',592,358,234,90,'读 R2 + R3\n选 (34,1)'),
  arrow('repair',430,246,274,0,'r2','r3',true),
  text('repair-label',552,262,'之后修复 R3',17,true),
  text('note',24,506,'每组读集合都与新写集合 {R1,R2} 相交；只读 R3 没有此保证。',19),
  text('boundary',24,542,'图中保护的是可归并的存储状态，不回滚外部邮件等副作用。',17,true)
 ]},
 {stem:'ch09-dst',title:'随机探索，确定性重放',description:'种子和故障计划控制模拟网络时钟磁盘调度，实际协议代码产生历史，性质检查器记录失败并通过相同环境重放。',elements:[
  ...header('确定性模拟测试：控制环境，检查真实代码','实线：本次执行与记录；虚线：保留条件后重放失败历史。'),
  box('seed',24,132,254,108,'种子 + 初始状态\n版本 + 故障计划'),
  box('env',494,132,330,108,'确定性环境\n网络／时钟／磁盘／调度'),
  arrow('control',284,186,204,0,'seed','env'),text('control-label',330,154,'决定事件顺序',18),
  box('code',494,340,330,100,'实际协议代码\n生成操作与响应历史'),
  arrow('execute',658,246,0,88,'env','code'),
  box('check',24,340,254,100,'性质检查器\n例如：接受代次不回退'),
  arrow('history',488,390,-204,0,'code','check'),text('history-label',340,356,'检查历史',18),
  arrow('replay',150,334,0,-88,'check','seed',true),text('replay-label',170,278,'失败重放',18),
  text('note',24,496,'随机选择用于发现新路径；相同受控输入用于复现同一条路径。',19),
  text('limit',24,532,'模拟通过不等于全部执行已证明，也不代替真实硬件性能测试。',17,true)
 ]}
];
for(const f of figures){
 if(process.argv[2]&&process.argv[2]!==f.stem)continue;
 const input=path.join(dir,`${f.stem}.skeleton.json`);
 await fs.writeFile(input,JSON.stringify(f.elements,null,2)+'\n');
 execFileSync(process.execPath,[path.join(dir,'export-excalidraw.mjs'),input,f.title,f.description],{stdio:'inherit'});
}
