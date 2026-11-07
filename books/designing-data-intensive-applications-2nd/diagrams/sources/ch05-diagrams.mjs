// Chapter-local authoring source; official shared exporter performs scene/editor round-trip.
import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { execFileSync } from 'node:child_process';

const dir = path.dirname(fileURLToPath(import.meta.url));
const text = (id,x,y,value,size=19,color='#292824') => ({type:'text',id,x,y,text:value,fontSize:size,fontFamily:2,strokeColor:color});
const box = (id,x,y,width,height,value,dashed=false) => ({type:'rectangle',id,x,y,width,height,strokeColor:'#386d74',backgroundColor:'#f0ece4',fillStyle:'solid',roughness:0.6,strokeStyle:dashed?'dashed':'solid',label:{text:value,fontSize:21,fontFamily:2,strokeColor:'#292824'}});
const arrow = (id,x,y,dx,dy,start,end,dashed=false) => ({type:'arrow',id,x,y,width:Math.abs(dx),height:Math.abs(dy),points:[[0,0],[dx,dy]],strokeColor:'#386d74',roughness:0.5,strokeStyle:dashed?'dashed':'solid',...(start?{start:{id:start}}:{}),...(end?{end:{id:end}}:{})});
const header = (title,description) => [text('title',24,18,title,25),text('subtitle',24,60,description,17,'#66645d')];
const figures = [
  {stem:'ch05-compatibility',title:'兼容方向：先标写者与读者',description:'向后兼容是旧写者到新读者；向前兼容是新写者到旧读者。旧版读改写还需保留未知字段。',elements:[
    ...header('兼容方向：先标写者与读者','箭头 = 数据流向；版本新旧与箭头朝向分别标明。'),
    text('backward',24,108,'向后兼容 backward',21),
    box('old-writer',24,150,250,90,'旧代码写入\nv1 数据'),
    box('new-reader',480,150,250,90,'新代码读取\n理解旧格式'),
    arrow('old-to-new',280,195,194,0,'old-writer','new-reader'),
    text('old-data',320,158,'旧数据',18,'#66645d'),
    text('forward',24,282,'向前兼容 forward',21),
    box('new-writer',24,324,250,90,'新代码写入\nv2 数据'),
    box('old-reader',480,324,250,90,'旧代码读取\n容忍新增内容'),
    arrow('new-to-old',280,369,194,0,'new-writer','old-reader'),
    text('new-data',320,332,'新数据',18,'#66645d'),
    box('writeback',24,466,706,112,'读得懂 ≠ 无损写回\n旧版若重新构造整条记录，未知 photoURL 仍可能丢失',true),
    text('api',24,614,'旧客户端 → 新服务：请求向后兼容；响应向前兼容。',19)
  ]},
  {stem:'ch05-avro-resolution',title:'Avro：用写者模式读字节，用读者模式生成结果',description:'按写者顺序读取姓名、long数字、头像，按读者模式重排数字和姓名、忽略头像，并将缺失locale填成zh-CN。',elements:[
    ...header('Avro：两份模式，各负一项责任','笔记假设；Person 名称相同，favoriteNumber 两侧均为 long。'),
    box('writer',24,116,320,152,'写者模式\n① userName : string\n② favoriteNumber : long\n③ photoURL : string'),
    box('reader',414,116,320,152,'读者模式\n① favoriteNumber : long\n② userName : string\n③ locale : string = "zh-CN"',true),
    box('bytes',24,344,240,100,'原始字节\n按写者顺序连接值'),
    box('resolve',354,344,380,100,'按写者模式识别边界\n按字段名映射到读者结构'),
    arrow('writer-input',184,274,0,64,'writer','bytes'),
    arrow('data',270,394,78,0,'bytes','resolve'),
    arrow('reader-input',574,274,0,64,'reader','resolve',true),
    box('result',354,516,380,132,'读者得到的对象\nfavoriteNumber = 1337\nuserName = "Martin"\nlocale = "zh-CN"'),
    arrow('output',544,450,0,60,'resolve','result'),
    text('discard',24,530,'photoURL 被投影忽略。\n这不承诺保留它，\n再按旧模式写回仍可能丢失。',18,'#66645d'),
    text('legend',24,688,'实线：读取与投影　　虚线：读者期望的结构与默认值',17,'#66645d')
  ]},
  {stem:'ch05-durable-boundary',title:'持久化执行：完成记录决定恢复路径',description:'完成已入历史时重放旧结果；外部扣款已发生但活动完成报告丢失时可能重试，支付方须以同一幂等键去重。',elements:[
    ...header('持久化执行：完成记录决定恢复路径','两行是两种故障时点；框架历史与外部副作用没有共同提交点。'),
    text('case-a',24,110,'A　完成结果已入历史，随后工作流进程重启',21),
    box('a-history',24,158,214,112,'引擎历史\n扣款完成\n结果 = charge-9'),
    box('a-replay',292,158,204,112,'重放工作流\n返回历史中的\ncharge-9'),
    box('a-next',550,158,210,112,'继续后续步骤\n银行入账'),
    arrow('a1',244,214,42,0,'a-history','a-replay'),
    arrow('a2',502,214,42,0,'a-replay','a-next'),
    text('a-note',24,300,'这次恢复不用再次执行已记录完成的扣款活动。',18,'#66645d'),
    text('case-b',24,362,'B　外部已扣款，完成报告未进入历史',21),
    box('b-external',24,410,214,112,'支付方\n已执行扣款\n保存键 K 的结果'),
    box('b-history',292,410,204,112,'引擎历史\n活动已安排\n无完成结果',true),
    arrow('gap',244,466,42,0,'b-external','b-history',true),
    text('gap-label',243,538,'完成报告丢失',17,'#66645d'),
    box('b-retry',550,410,210,112,'超时后重试活动\n仍使用同一个 K'),
    arrow('b1',502,466,42,0,'b-history','b-retry'),
    box('b-dedup',292,608,468,90,'支付方识别 K，返回既有 charge-9\n不新增第二笔扣款'),
    arrow('retry-call',655,528,0,74,'b-retry','b-dedup'),
    text('b-note',24,746,'K = payment-742:debit；去重效果依赖支付方协议、作用域与保留期。',17,'#66645d')
  ]}
];
for (const f of figures) {
  const input = path.join(dir,`${f.stem}.skeleton.json`);
  await fs.writeFile(input,JSON.stringify(f.elements,null,2)+'\n');
  execFileSync(process.execPath,[path.join(dir,'export-excalidraw.mjs'),input,f.title,f.description],{stdio:'inherit'});
}
