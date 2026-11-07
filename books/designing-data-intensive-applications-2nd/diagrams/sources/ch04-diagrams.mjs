// Chapter-local authoring source. Uses the shared official Excalidraw exporter.
import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { execFileSync } from 'node:child_process';

const dir = path.dirname(fileURLToPath(import.meta.url));
const text = (id, x, y, value, size = 19, color = '#292824') => ({ type:'text', id, x, y, text:value, fontSize:size, fontFamily:2, strokeColor:color });
const box = (id, x, y, width, height, value, dashed = false) => ({ type:'rectangle', id, x, y, width, height, strokeColor:'#386d74', backgroundColor:'#f0ece4', fillStyle:'solid', roughness:0.7, strokeStyle:dashed?'dashed':'solid', label:{ text:value, fontSize:21, fontFamily:2, strokeColor:'#292824' } });
const arrow = (id, x, y, dx, dy, start, end, dashed = false) => ({ type:'arrow', id, x, y, width:Math.abs(dx), height:Math.abs(dy), points:[[0,0],[dx,dy]], strokeColor:'#386d74', roughness:0.6, strokeStyle:dashed?'dashed':'solid', ...(start?{start:{id:start}}:{}), ...(end?{end:{id:end}}:{}) });
const line = (id, x, y, dx, dy, dashed = false) => ({ type:'line', id, x, y, width:Math.abs(dx), height:Math.abs(dy), points:[[0,0],[dx,dy]], strokeColor:'#66645d', roughness:0.5, strokeStyle:dashed?'dashed':'solid' });
const header = (title, desc) => [text('title',24,18,title,25),text('subtitle',24,60,desc,17,'#66645d')];
const figures = [
  { stem:'ch04-lsm-path', title:'LSM：恢复依据与有序文件分别负责什么', description:'实线为写入及发布步骤，虚线为读取范围。SSTable完整持久化并发布后才能回收对应WAL。', elements:[
    ...header('LSM：恢复依据与有序文件','示意同步持久化；步骤可以流水化，成功确认需满足持久性约定。'),
    box('wal',24,120,220,96,'追加 WAL\n保留恢复依据'),
    box('mem',292,120,220,96,'内存表\n活动 / 冻结'),
    box('read',560,120,200,96,'读请求\n检查有效状态'),
    arrow('write',250,168,36,0,'wal','mem'),
    arrow('readmem',554,168,-36,0,'read','mem',true),
    box('temp',292,284,220,96,'冻结表按序写出\n临时 SSTable'),
    arrow('flush',402,222,0,56,'mem','temp'),
    text('flush-label',420,240,'落盘',17,'#66645d'),
    box('published',292,448,220,96,'已发布 SSTables\n合并新旧版本读取'),
    arrow('publish',402,386,0,56,'temp','published'),
    text('publish-label',420,403,'持久化并发布',17,'#66645d'),
    { ...arrow('readfiles',660,222,0,274,'read','published',true), points:[[0,0],[0,274],[-142,274]], width:142, height:274 },
    text('failure',24,302,'写到一半崩溃：\n保留 WAL\n丢弃未发布半成品',18,'#66645d'),
    text('release',24,464,'发布完成后，才回收\n对应更新的 WAL',18,'#66645d'),
    text('legend',24,582,'实线：写入 / 发布　　虚线：读取　　文件集合还须可恢复',17,'#66645d')
  ]},
  { stem:'ch04-merge-tombstone', title:'局部合并为什么必须保留删除标记', description:'S1和S2合并后保留b的墓碑，未参加合并的S0仍保存b等于2。', elements:[
    ...header('局部合并：删除标记仍有工作要做','S0 最旧，S2 最新；† 表示删除。本例不保留历史快照。'),
    box('old',24,116,210,108,'S0（未参与）\nb = 2',true),
    box('mid',292,116,210,108,'S1\na=1，b=4，d=6'),
    box('new',550,116,210,108,'S2\nb=†，c=5'),
    text('outside',24,263,'更旧的 b 仍在这里。\n虚线框表示它不参加\n这一次压缩合并。',18,'#66645d'),
    box('result',316,334,420,100,'合并输出\na=1，b=†，c=5，d=6'),
    arrow('midmerge',397,230,50,98,'mid','result'),
    arrow('newmerge',655,230,-50,98,'new','result'),
    text('pick',452,269,'同键保留较新版本',17,'#66645d'),
    text('risk',24,484,'若输出不保留 †，读取可能继续命中 S0 的 b=2，让旧值复活。',19),
    text('rule',24,524,'只有确认旧版本已处理、且无需保留历史状态，才能移除墓碑。',17,'#66645d')
  ]},
  { stem:'ch04-btree-recovery', title:'B-tree的日志持久化、部分刷页与恢复', description:'时间向下。WAL先可靠保存，即使数据页只刷出一部分，重启也可按恢复协议修复页和引用关系。', elements:[
    ...header('B-tree：数据页落后时，日志保留恢复依据','时间向下；示意已提交更新，不表示盲目重做所有未提交记录。'),
    text('one',24,131,'① WAL 已同步',21),
    box('wal',240,112,500,92,'页修改与分裂的恢复信息\n已可靠保存'),
    arrow('advance',490,210,0,62,'wal',null),
    text('two',24,295,'② 部分页刷盘\n    此时崩溃',21),
    box('newpage',240,278,235,98,'部分子页\n已是新状态'),
    box('oldparent',505,278,235,98,'父页引用\n可能仍是旧状态'),
    arrow('redo',490,389,0,61,null,'restored'),
    text('three',24,478,'③ 重启恢复',21),
    box('restored',240,456,500,94,'依据 WAL 重做必要修改\n恢复页内容与引用关系'),
    text('note',24,594,'不变量：相关 WAL 先持久化，数据页才可写入持久存储。',19)
  ]},
  { stem:'ch04-column-mask', title:'同一行位置使跨列位图求交成立', description:'商品31位图101010与门店3位图110110相与得到100010，选中数量2和5，求和为7。', elements:(()=>{
    const e=header('列式筛选：位的位置必须指向同一行','六行笔记假设数据；按位 AND 选择第 1、5 行。');
    const rows=[['行位置',[1,2,3,4,5,6]],['商品 = 31',[1,0,1,0,1,0]],['门店 = 3',[1,1,0,1,1,0]],['两个条件 AND',[1,0,0,0,1,0]],['数量',[2,1,4,3,5,2]]];
    for(let r=0;r<rows.length;r++){
      const y=112+r*64;
      e.push(text(`row-${r}`,24,y+8,rows[r][0],20));
      rows[r][1].forEach((v,i)=>e.push(box(`cell-${r}-${i}`,225+i*82,y,68,42,String(v),r===4&&i!==0&&i!==4)));
    }
    e.push(box('sum',225,474,478,76,'选中第 1、5 项：2 + 5 = 7'));
    e.push(arrow('q1',259,416,0,52,'cell-4-0','sum'));
    e.push(arrow('q5',587,416,0,52,'cell-4-4','sum'));
    e.push(text('note',24,586,'实线数量格为命中项；虚线格不参与本次求和。',17,'#66645d'));
    return e;
  })()},
  { stem:'ch04-ivf-boundary', title:'IVF边界附近的近邻遗漏', description:'中心0和10，查询4.9更靠近左中心，但数据点5.1在右簇，距离仅0.2。只搜左簇会漏掉真正近邻。', elements:[
    ...header('IVF：最近的中心，不保证包含最近的数据点','一维笔记反例；只探查一个簇时，右侧近邻可能没有参加比较。'),
    box('space',24,116,700,270,'',false),
    text('left-title',48,136,'左簇（本次被探查）',21),
    text('right-title',410,136,'右簇（本次未探查）',21),
    line('axis',64,297,620,0), line('boundary',374,183,0,176,true),
    {type:'ellipse',id:'a',x:55,y:288,width:18,height:18,strokeColor:'#386d74',backgroundColor:'#386d74',fillStyle:'solid',roughness:0.5},
    {type:'ellipse',id:'q',x:355,y:288,width:18,height:18,strokeColor:'#292824',backgroundColor:'#292824',fillStyle:'solid',roughness:0.5},
    {type:'ellipse',id:'b',x:376,y:288,width:18,height:18,strokeColor:'#386d74',backgroundColor:'#386d74',fillStyle:'solid',roughness:0.5},
    {type:'ellipse',id:'center-right',x:675,y:288,width:18,height:18,strokeColor:'#386d74',backgroundColor:'#f0ece4',fillStyle:'solid',roughness:0.5},
    text('a-label',45,327,'A=0\n左中心',18),
    text('q-label',239,214,'查询 q=4.9',19), line('q-guide',329,246,35,35),
    text('b-label',421,214,'B=5.1',19), line('b-guide',443,245,-58,36),
    text('c-label',627,327,'右中心\n10',18),
    text('border-label',331,405,'簇边界 5',18,'#66645d'),
    text('distances',24,459,'只搜左簇：返回 A，距离 4.9\n真实最近：B，距离 0.2，却在未探查的右簇',21),
    text('legend',24,536,'横轴为坐标；虚线为分界。扩大探查范围才能纳入 B。',17,'#66645d')
  ]}
];

for(const f of figures){
  if(process.argv[2] && process.argv[2]!==f.stem)continue;
  const input=path.join(dir,`${f.stem}.skeleton.json`);
  await fs.writeFile(input,JSON.stringify(f.elements,null,2)+'\n');
  execFileSync(process.execPath,[path.join(dir,'export-excalidraw.mjs'),input,f.title,f.description],{stdio:'inherit'});
}
