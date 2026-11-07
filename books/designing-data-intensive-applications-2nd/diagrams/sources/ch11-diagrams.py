"""Chapter 11 authoring skeletons; export with the shared official Excalidraw tool."""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
TEXT, MUTED, SOFT, ACCENT = '#292824', '#66645d', '#f0ece4', '#386d74'


def text(id, x, y, value, size=19, color=TEXT):
    return dict(type='text', id=id, x=x, y=y, text=value, fontSize=size,
                fontFamily=2, strokeColor=color)


def box(id, x, y, w, h, value, size=21, dashed=False):
    return dict(type='rectangle', id=id, x=x, y=y, width=w, height=h,
                strokeColor=ACCENT, backgroundColor=SOFT, fillStyle='solid',
                roughness=0.5, strokeStyle='dashed' if dashed else 'solid',
                label=dict(text=value, fontSize=size, fontFamily=2, strokeColor=TEXT))


def arrow(id, x, y, dx, dy, start, end, dashed=False):
    return dict(type='arrow', id=id, x=x, y=y, width=abs(dx), height=abs(dy),
                points=[[0, 0], [dx, dy]], strokeColor=ACCENT, roughness=0.5,
                strokeStyle='dashed' if dashed else 'solid', endArrowhead='arrow',
                start={'id': start}, end={'id': end})


def save(stem, elements):
    (HERE / f'ch11-{stem}.skeleton.json').write_text(
        json.dumps(elements, ensure_ascii=False, indent=2) + '\n')


save('layers', [
    text('title', 20, 10, '同一条批管道，三个不同职责', 26),
    text('sub', 20, 55, '虚线是运行控制；实线是数据读写。方框表示逻辑角色。', 18, MUTED),
    box('workflow', 20, 125, 280, 100, '工作流编排\n依赖就绪才提交作业'),
    box('scheduler', 510, 125, 280, 100, '资源调度\n分配 CPU／内存／GPU'),
    arrow('submit', 305, 175, 200, 0, 'workflow', 'scheduler', True),
    text('submit-label', 350, 140, '提交作业', 18),
    box('input', 20, 335, 280, 100, '存储：输入快照\n固定清单，只读'),
    box('compute', 510, 335, 280, 100, '计算任务\n扫描 → 连接 → 聚合'),
    arrow('allocate', 650, 230, 0, 100, 'scheduler', 'compute', True),
    text('allocate-label', 680, 265, '分配／启动', 18),
    arrow('read', 305, 385, 200, 0, 'input', 'compute'),
    text('read-label', 345, 350, '读取记录', 18),
    box('output', 510, 550, 280, 100, '存储：新版本输出\n完整确认后交给下游'),
    arrow('write', 650, 440, 0, 105, 'compute', 'output'),
    text('write-label', 680, 475, '写入结果', 18),
    text('note', 20, 555, '工作流决定“何时可消费”。\n计算引擎决定“如何计算”。\n存储保存数据与版本。', 19),
    text('legend', 20, 700, '三种职责可由多个工具协作，也可集成于同一托管服务。', 18, MUTED),
])

e = [text('title', 20, 10, 'Shuffle 细节：只展开 reducer 2 的入边', 25),
     text('sub', 20, 55, 'm_i,r2 是逻辑分区，不承诺一个分区对应一个物理文件。', 18, MUTED)]
for i, (y, values) in enumerate([(120, '(A,1)  (C,1)'), (275, '(A,1)  (B,1)'), (430, '(B,1)  (C,1)')], 1):
    e += [box(f'm{i}', 20, y, 175, 85, f'Mapper {i}', 21),
          box(f'p{i}', 290, y, 240, 85, f'm{i},r2：有序段\n{values}', 19),
          arrow(f'local{i}', 200, y+42, 85, 0, f'm{i}', f'p{i}'),
          arrow(f'fetch{i}', 535, y+42, 105, 317-(y+42), f'p{i}', 'merge')]
e += [box('merge', 645, 235, 240, 165, 'r2 拉取并归并\nA A B B C C\n同键相邻的输入', 21),
      box('output', 645, 485, 240, 85, '逐键求和\nA:2　B:2　C:2', 21),
      arrow('reduce', 765, 405, 0, 75, 'merge', 'output'),
      text('local-label', 225, 92, '本地', 18, MUTED),
      text('network-label', 565, 170, '网络', 18, MUTED),
      text('note', 20, 605, '教学假设：A、B、C 都分给 r2；其余 reducer 路径省略。', 19),
      text('legend', 20, 645, '箭头：数据传送　有序仅指 r2 的输入；不是所有输出的全局顺序。', 18, MUTED)]
save('shuffle', e)

save('join', [
    text('title', 20, 10, '一个用户组：先读档案，再顺序处理事件', 25),
    text('sub', 20, 55, '笔记假设：每个 user_id 恰有一份档案；本图只展示用户 104。', 18, MUTED),
    box('sorted', 20, 145, 260, 200, '按复合键排序后\n104 · 档案 · 1989-01-30\n104 · 事件 · /x\n104 · 事件 · /z', 19),
    box('join', 365, 145, 225, 200, '连接循环\n保存一份出生日期\n事件逐条读取\n不逐行查远端库', 20),
    box('joined', 675, 145, 240, 200, '输出两条记录\n/x · 1989-01-30\n/z · 1989-01-30', 20),
    arrow('input', 285, 245, 75, 0, 'sorted', 'join'),
    arrow('emit', 595, 245, 75, 0, 'join', 'joined'),
    text('keys', 20, 410, '分片键／分组键：user_id\n排序键：(user_id, type, event_time)\n档案的 type 排在事件前。', 19),
    box('group-url', 675, 450, 240, 105, '下一阶段\n改按 URL 分片聚合', 21),
    arrow('reshuffle', 795, 350, 0, 95, 'joined', 'group-url'),
    text('legend', 20, 620, '实线：记录流动　两侧有重复键时，需另行处理版本或多对多配对。', 18, MUTED),
])

save('publish', [
    text('title', 20, 10, '发布 V18：先完整，再切换', 26),
    text('sub', 20, 55, '笔记教学协议；实线为数据访问，虚线为完成证据与发布控制。', 18, MUTED),
    box('build', 20, 125, 235, 100, '批任务／导入器\n输出带版本 V18'),
    box('staging', 435, 125, 340, 100, 'V18 暂存空间\n对在线查询不可见'),
    arrow('load', 260, 175, 170, 0, 'build', 'staging'),
    text('load-label', 300, 140, '文件或日志', 18),
    box('gate', 435, 330, 340, 125, '完整性屏障\n全部预期分片已完成\n消费位点／清单已核对', 21),
    arrow('ready', 605, 230, 0, 95, 'staging', 'gate', True),
    text('ready-label', 635, 265, '提交完成证据', 18),
    text('failure', 20, 340, '构建失败或数据未齐：\n继续服务 V17。\n收到完成通知，不等于\n已经应用所有分片。', 19),
    box('pointer', 435, 565, 340, 95, '当前版本引用\nV17 → V18（原子切换）', 21),
    arrow('commit', 605, 460, 0, 100, 'gate', 'pointer', True),
    text('commit-label', 635, 495, '核对通过才切换', 18),
    box('reader', 20, 565, 235, 95, '在线读者\n每次查询固定一个版本'),
    arrow('select', 260, 612, 170, 0, 'reader', 'pointer'),
    text('select-label', 300, 580, '选择版本', 18),
    text('legend', 20, 710, 'V17 在旧读者退出且回滚保留期结束后清理；不是多个系统共同事务。', 18, MUTED),
])
print('Wrote four chapter-11 native-element skeletons.')
