"""Create small native Excalidraw skeletons; export with the shared official API tool."""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
INK, MUTED, ACCENT, SOFT = '#292824', '#66645d', '#386d74', '#f0ece4'


def text(id, x, y, value, size=19, color=INK):
    return dict(type='text', id=id, x=x, y=y, text=value, fontSize=size,
                fontFamily=2, strokeColor=color)


def box(id, x, y, w, h, label='', dashed=False, fill=True):
    item = dict(type='rectangle', id=id, x=x, y=y, width=w, height=h,
                strokeColor=ACCENT, backgroundColor=SOFT if fill else 'transparent',
                fillStyle='solid', roughness=0.7, strokeWidth=1.5,
                strokeStyle='dashed' if dashed else 'solid')
    if label:
        item['label'] = dict(text=label, fontSize=21, fontFamily=2, strokeColor=INK)
    return item


def arrow(id, start, end, a, b, dashed=False, both=False):
    x, y = a
    dx, dy = b[0] - x, b[1] - y
    item = dict(type='arrow', id=id, x=x, y=y, width=abs(dx), height=abs(dy),
                points=[[0, 0], [dx, dy]], strokeColor=ACCENT, roughness=0.5,
                strokeStyle='dashed' if dashed else 'solid', endArrowhead='arrow')
    if start:
        item['start'] = {'id': start}
    if end:
        item['end'] = {'id': end}
    if both:
        item['startArrowhead'] = 'arrow'
    return item


def save(stem, elements):
    (HERE / f'ch06-{stem}.skeleton.json').write_text(json.dumps(elements, ensure_ascii=False, indent=2) + '\n')


save('sync-ack', [
    text('title', 20, 20, '成功响应等待哪条复制路径？', 25),
    text('sub', 20, 62, '单次写 W；从上向下读依赖顺序，不表示实际耗时。', 18, MUTED),
    box('leader', 250, 120, 240, 75, 'L 接收并保存 W'),
    box('f1', 20, 290, 300, 85, 'F1 完成约定确认'),
    box('f2', 430, 290, 300, 85, 'F2 稍后完成复制', True),
    box('reply', 20, 465, 300, 75, 'L 回复客户端：成功'),
    arrow('to-f1', 'leader', 'f1', (285, 200), (190, 284)),
    arrow('to-f2', 'leader', 'f2', (455, 200), (560, 284), True),
    arrow('to-reply', 'f1', 'reply', (170, 381), (170, 459)),
    text('sync', 35, 222, '同步：必须等待', 18),
    text('async', 535, 222, '异步：本次不等', 18),
    text('ack', 190, 410, '收到 F1 确认后', 18, MUTED),
    text('f2note', 430, 440, '此时 F2 仍可能落后\n不等待 ≠ 永远不传播', 19, MUTED),
    text('legend', 20, 587, '确认层次另行约定：收到 / 可靠保存 / 查询可见。', 19),
])

save('local-first', [
    text('title', 20, 20, '本地完成编辑，联网后传播与合并', 25),
    text('sub', 20, 62, '实线：设备内部操作　虚线：可延后的网络同步', 18, MUTED),
    box('phone', 20, 120, 330, 355, fill=False),
    box('laptop', 410, 120, 330, 355, fill=False),
    text('phone-label', 40, 140, '手机 · 可写副本', 20),
    text('laptop-label', 430, 140, '电脑 · 可写副本', 20),
    box('ui1', 65, 195, 240, 60, '界面'),
    box('ui2', 455, 195, 240, 60, '界面'),
    box('data1', 65, 365, 240, 75, '持久本地数据\n与待同步修改'),
    box('data2', 455, 365, 240, 75, '持久本地数据\n与待同步修改'),
    arrow('edit1', 'ui1', 'data1', (185, 261), (185, 359), both=True),
    arrow('edit2', 'ui2', 'data2', (575, 261), (575, 359), both=True),
    text('local1', 205, 284, '编辑↓\n刷新↑', 18, MUTED),
    text('local2', 595, 284, '编辑↓\n刷新↑', 18, MUTED),
    box('relay', 240, 585, 280, 75, '同步中转服务'),
    arrow('sync1', 'data1', 'relay', (185, 446), (275, 579), True, True),
    arrow('sync2', 'data2', 'relay', (575, 446), (485, 579), True, True),
    text('s1', 30, 515, '发送 / 接收\n断网后再继续', 18, MUTED),
    text('s2', 590, 515, '发送 / 接收\n到达后合并', 18, MUTED),
    text('legend', 20, 704, '本地保存 ≠ 已同步其他设备；中转不预设唯一排序主节点。', 18),
])

save('quorum-intersection', [
    text('title', 20, 20, '固定三副本：写二、读二必有交集', 25),
    text('sub', 20, 62, '前提：写已完成，副本没有丢失版本，随后再读。', 18, MUTED),
    box('universe', 20, 112, 740, 380, fill=False),
    text('universe-label', 40, 128, '同一副本集合 N = {A, B, C}', 19),
    box('writes', 45, 178, 450, 170, fill=False),
    box('reads', 285, 223, 450, 204, dashed=True, fill=False),
    text('write-label', 65, 190, '实线：完成写的集合 {A, B}', 18),
    text('read-label', 310, 390, '虚线：本次读的集合 {B, C}', 18),
    box('a', 80, 265, 140, 60, 'A · 新值'),
    box('b', 320, 265, 140, 60, 'B · 新值'),
    box('c', 560, 265, 140, 60, 'C · 旧值'),
    text('intersect', 305, 448, '交集 B 提供已完成写', 19),
    text('formula', 20, 535, '|交集| ≥ w + r − n = 2 + 2 − 3 = 1', 22),
    text('scope', 20, 580, '按版本选值，不是对值投票；交集不等于完整一致性协议。', 18, MUTED),
])

items = [text('title', 20, 20, '未完成写：两次 quorum 读仍可能倒退', 25),
         text('sub', 20, 62, 'n=3，w=2，r=2；读响应前不等待写回修复。', 18, MUTED)]
for name, x in [('A', 275), ('B', 445), ('C', 615)]:
    items.append(text('head-' + name, x + 40, 104, name, 23))
for i, (y, label, active) in enumerate([
    (152, '① 写仅到 A\n尚未取得两个确认', 'none'),
    (302, '② R1 读取 A、B\n返回 1；修复未完成', 'ab'),
    (452, '③ 随后 R2 读 B、C\n返回 0', 'bc'),
]):
    items.append(text(f'row-{i}', 20, y + 9, label, 19))
    for name, x, value in [('A', 275, 1), ('B', 445, 0), ('C', 615, 0)]:
        selected = name.lower() in active
        items.append(box(f'{name}-{i}', x, y, 125, 75, f'{name} = {value}', not selected, selected))
    if i < 2:
        items.append(arrow(f'step-{i}', None, None, (110, y + 86), (110, y + 133)))
items += [text('legend', 20, 565, '实线格：本次读响应　虚线格：未入本次读 / 尚未完成写', 18, MUTED),
          text('why', 20, 610, '新写只有一份；不能套用“写已在 w 个副本完成”的前提。', 19)]
save('quorum-inflight', items)

save('causal-versions', [
    text('title', 20, 20, '购物车：版本编号不等于因果先后', 25),
    text('sub', 20, 62, '箭头：后项已经知道前项；未连线仍需检查有无传递路径。', 18, MUTED),
    box('v1', 20, 155, 200, 85, 'v1 · 加奶\n上下文：空'),
    box('v2', 20, 405, 200, 85, 'v2 · 加蛋\n上下文：空'),
    box('v3', 300, 125, 200, 85, 'v3 · 加面粉\n上下文：1'),
    box('v4', 590, 405, 200, 85, 'v4 · 加火腿\n上下文：2'),
    box('v5', 590, 125, 200, 85, 'v5 · 加培根\n上下文：3'),
    arrow('e13', 'v1', 'v3', (226, 175), (294, 167)),
    arrow('e14', 'v1', 'v4', (225, 225), (584, 422)),
    arrow('e24', 'v2', 'v4', (226, 448), (584, 448)),
    arrow('e25', 'v2', 'v5', (225, 418), (584, 195)),
    arrow('e35', 'v3', 'v5', (506, 167), (584, 167)),
    text('cross', 20, 513, '交叉线没有连接点', 17, MUTED),
    text('concurrent', 20, 555, 'v3 ∥ v4；v4 ∥ v5（∥ 表示并发，不是同时到达）', 21),
    text('result', 20, 605, '步骤 5 后保留 v4、v5 两个候选，等待知道两者的后续合并。', 18, MUTED),
])
print('Wrote 5 ch06 skeletons; use the shared exporter for native scenes and SVGs.')
