"""Authoring-only: chapter 7 native Excalidraw element skeletons."""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
TEXT, MUTED, SOFT, ACCENT = '#292824', '#66645d', '#f0ece4', '#386d74'

def text(id, x, y, value, size=19, color=TEXT):
    return dict(type='text', id=id, x=x, y=y, text=value, fontSize=size, fontFamily=2, strokeColor=color)

def box(id, x, y, w, h, value, size=20, dashed=False):
    return dict(type='rectangle', id=id, x=x, y=y, width=w, height=h,
                strokeColor=ACCENT, backgroundColor=SOFT, fillStyle='solid', roughness=0.6,
                strokeStyle='dashed' if dashed else 'solid',
                label=dict(text=value, fontSize=size, fontFamily=2, strokeColor=TEXT))

def arrow(id, x, y, dx, dy, start=None, end=None, dashed=False, points=None):
    a = dict(type='arrow', id=id, x=x, y=y, width=abs(dx), height=abs(dy),
             points=points or [[0, 0], [dx, dy]], strokeColor=ACCENT,
             roughness=0.5, strokeStyle='dashed' if dashed else 'solid', endArrowhead='arrow')
    if start: a['start'] = {'id': start}
    if end: a['end'] = {'id': end}
    return a

def save(stem, elements):
    (HERE / f'{stem}.skeleton.json').write_text(json.dumps(elements, ensure_ascii=False, indent=2) + '\n')

e = [text('title', 20, 10, '固定分片：只改变“分片 → 节点”', 25),
     text('rule', 20, 52, '键 → S = hash(key) % 12  始终不变；假设各片等大、等负载。', 18, MUTED),
     text('before', 20, 100, '扩容前：3 个节点，每节点 4 片', 20)]
for i, x in enumerate([20, 285, 550]):
    e.append(box(f'old{i}', x, 145, 220, 100, f'节点 {i}\nS{i*4} · S{i*4+1} · S{i*4+2} · S{i*4+3}', 19))
e += [text('move', 20, 335, '只搬 S3、S7、S11，共 3/12 = 25%', 19),
      arrow('m0', 130, 250, 565, 155, 'old0', 'new3'),
      arrow('m1', 395, 250, 300, 155, 'old1', 'new3'),
      arrow('m2', 660, 250, 35, 155, 'old2', 'new3')]
for i, x in enumerate([20, 220, 420, 620]):
    ids = ['S0 · S1 · S2', 'S4 · S5 · S6', 'S8 · S9 · S10', 'S3 · S7 · S11'][i]
    e.append(box(f'new{i}', x, 410, 170, 100, f'节点 {i}' + ('（新增）' if i == 3 else '') + '\n' + ids, 18))
e += [text('after', 20, 545, '扩容后：4 个节点，每节点 3 片', 20),
      text('legend', 20, 585, '框：物理节点　S：逻辑分片　箭头：整片迁移；其余分片不动。', 18, MUTED)]
save('ch07-fixed-shards', e)

e = [text('title', 20, 10, '迁移 S3：数据追上以后，还要交接写入资格', 25),
     text('sub', 20, 52, '笔记假设协议；阶段从上到下。允许交接窗口内等待或重试。', 18, MUTED),
     text('s1', 20, 100, '01　A 仍是所有者：复制快照并重放增量', 20),
     box('a1', 20, 145, 220, 92, 'A：继续读写\n快照位点 40'),
     box('b1', 550, 145, 220, 92, 'B：准备数据\n尚无写入资格'),
     arrow('copy', 245, 190, 300, 0, 'a1', 'b1'),
     text('copylabel', 285, 155, '快照 + 后续日志', 18),
     text('s2', 20, 285, '02　建立屏障：A 停止接新写，B 追至最终位点', 20),
     box('a2', 20, 330, 220, 92, 'A：排空已接写入\n最终位点 48'),
     box('b2', 550, 330, 220, 92, 'B：已应用到 48\n具备完整基线'),
     arrow('catchup', 245, 375, 300, 0, 'a2', 'b2'),
     text('catchlabel', 290, 340, '最后一段增量', 18),
     text('s3', 20, 470, '03　发布新代次：B 接管，A 的旧写入资格失效', 20),
     box('map', 20, 515, 285, 92, '协调层持久记录\n新代次：S3 → B'),
     box('b3', 550, 515, 220, 92, 'B：新所有者\n开始接受写入'),
     arrow('publish', 310, 560, 235, 0, 'map', 'b3', True),
     text('publishlabel', 350, 525, '发布资格／映射', 18),
     text('stale', 20, 650, '旧路由到 A：拒绝／重定向／转发；不能再在 A 本地提交。', 18),
     text('legend', 20, 690, '实线：数据传递　虚线：权威状态发布　B 未到 48 时不得切换。', 18, MUTED)]
save('ch07-migration', e)

e = [text('title', 20, 10, '本地索引：完整搜索需要分发—汇集', 25),
     text('sub', 20, 52, '假设按车辆 ID 分片；每片只索引自己的记录。', 18, MUTED),
     box('query', 265, 105, 250, 85, '查询方\n查全部红车'),
     box('d0', 20, 305, 340, 175, '数据片 D0\n101：红色 Ford\n202：蓝色 Honda\n本地 color:red → [101]', 19),
     box('d1', 430, 305, 340, 175, '数据片 D1\n501：红色 Honda\n本地 color:red → [501]', 19),
     arrow('q0', 300, 195, -165, 105, 'query', 'd0'),
     arrow('q1', 480, 195, 165, 105, 'query', 'd1'),
     text('scatter0', 100, 240, '查 color:red', 18),
     text('scatter1', 610, 240, '查 color:red', 18),
     box('result', 265, 600, 250, 85, '汇集完整结果\n101 和 501'),
     arrow('r0', 190, 485, 120, 110, 'd0', 'result', True),
     arrow('r1', 600, 485, -120, 110, 'd1', 'result', True),
     text('return0', 80, 530, '返回记录 101', 18),
     text('return1', 620, 530, '返回记录 501', 18),
     text('legend', 20, 730, '实线：查询请求　虚线：查询结果　每片仍用索引，不是全表逐行扫描。', 18, MUTED)]
save('ch07-local-index', e)

e = [text('title', 20, 10, '全局索引：先取 ID，再按 ID 取记录', 25),
     text('sub', 20, 52, '索引按词项分片；记录按车辆 ID 分片。框表示逻辑边界。', 18, MUTED),
     box('i0', 20, 115, 340, 100, '索引片 I0\ncolor:red → [101, 501]', 20),
     box('i1', 430, 115, 340, 100, '索引片 I1（本次不查）\nmake:Honda → [202, 501]', 19, True),
     box('query', 265, 355, 250, 90, '查询方\n先定位词项，再定位 ID'),
     arrow('term', 295, 350, -195, -130, 'query', 'i0'),
     text('termlabel', 30, 280, '① 查 color:red', 18),
     arrow('ids', 285, 220, 105, 130, 'i0', 'query', True),
     text('idslabel', 350, 280, '得到 [101, 501]', 18),
     box('d0', 20, 600, 340, 100, '数据片 D0\n101：红色 Ford（原记录）', 19),
     box('d1', 430, 600, 340, 100, '数据片 D1\n501：红色 Honda（原记录）', 19),
     arrow('fetch0', 300, 450, -165, 145, 'query', 'd0'),
     arrow('fetch1', 480, 450, 165, 145, 'query', 'd1'),
     text('fetch0label', 65, 515, '② 按 ID 取 101', 18),
     text('fetch1label', 620, 500, '② 按 ID 取 501', 18),
     text('legend', 20, 750, '实线：请求　虚线：ID 响应；原记录响应省略。取记录仍可能跨片。', 18, MUTED)]
save('ch07-global-index', e)
print('Wrote four chapter-7 skeletons; export with the shared official API tool.')
