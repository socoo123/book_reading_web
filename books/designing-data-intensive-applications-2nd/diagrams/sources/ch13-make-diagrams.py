"""Authoring-only native Excalidraw skeletons; export with the shared official tool."""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
INK, MUTED, ACCENT, SOFT = '#292824', '#66645d', '#386d74', '#f0ece4'


def text(id, x, y, value, size=18, color=MUTED):
    return dict(type='text', id=id, x=x, y=y, text=value, fontSize=size,
                fontFamily=2, strokeColor=color)


def box(id, x, y, w, h, value, size=21):
    return dict(type='rectangle', id=id, x=x, y=y, width=w, height=h,
                strokeColor=ACCENT, backgroundColor=SOFT, fillStyle='solid', roughness=0.6,
                label=dict(text=value, fontSize=size, fontFamily=2, strokeColor=INK))


def arrow(id, x, y, dx, dy, start=None, end=None, dashed=False, points=None):
    a = dict(type='arrow', id=id, x=x, y=y, width=abs(dx), height=abs(dy),
             points=points or [[0, 0], [dx, dy]], strokeColor=ACCENT,
             strokeStyle='dashed' if dashed else 'solid', roughness=0.6,
             endArrowhead='arrow')
    if start:
        a['start'] = dict(id=start)
    if end:
        a['end'] = dict(id=end)
    return a


def save(stem, title, subtitle, elements):
    scene = [text('title', 24, 18, title, 25, INK), text('subtitle', 24, 60, subtitle)] + elements
    (HERE / f'ch13-{stem}.skeleton.json').write_text(json.dumps(scene, ensure_ascii=False, indent=2) + '\n')


save('integration', '一种事实，多种派生表示', '先明确输入与顺序，再让各视图独立推进。', [
    box('input', 24, 135, 150, 76, '业务输入'),
    box('record', 250, 135, 195, 76, '权威记录\n决定相关写顺序'),
    box('log', 520, 135, 195, 76, 'CDC / 事件日志\n持久输入与位点'),
    arrow('write', 180, 173, 64, 0, 'input', 'record'),
    arrow('capture', 451, 173, 63, 0, 'record', 'log', True),
    text('cap', 455, 137, '捕获', 17),
    box('search', 24, 365, 195, 86, '转换 → 搜索\n独立进度 p₁'),
    box('view', 274, 365, 195, 86, '转换 → 页面视图\n独立进度 p₂'),
    box('analysis', 524, 365, 195, 86, '转换 → 分析\n独立进度 p₃'),
    arrow('to-search', 550, 218, -430, 140, 'log', 'search', True),
    arrow('to-view', 615, 218, -245, 140, 'log', 'view', True),
    arrow('to-analysis', 685, 218, -65, 140, 'log', 'analysis', True),
    text('derive', 24, 278, '虚线：按契约派生\n允许暂时落后', 18),
    text('read', 24, 490, '读请求访问需要的表示；各进度不必相同。', 19),
    text('boundary', 24, 527, '恢复依赖：输入仍在、转换可重现、输出可靠且可去重。', 18),
])

e = [text('col1', 24, 110, '写路径：提前完成', 20, INK),
     text('col2', 302, 110, '交汇点：保存结果', 20, INK),
     text('col3', 580, 110, '读路径：请求后执行', 20, INK)]
for n, y, left, mid, right in [
    (1, 165, '保存文档', '原始文档', '扫描、匹配'),
    (2, 295, '保存、分词、建索引', '倒排索引', '列表集合运算、排序'),
    (3, 425, '继续维护热门结果', '热门查询物化视图', '取结果、组织响应'),
]:
    e += [box(f'w{n}', 24, y, 230, 75, left, 19), box(f'm{n}', 302, y, 230, 75, mid, 19),
          box(f'r{n}', 580, y, 230, 75, right, 19),
          arrow(f'a{n}', 259, y+37, 37, 0, f'w{n}', f'm{n}'),
          arrow(f'b{n}', 537, y+37, 37, 0, f'm{n}', f'r{n}')]
e += [text('bottom', 24, 545, '三行是替代安排；更多预计算换取更少读时工作，也增加维护成本。', 18)]
save('read-boundary', '移动读写边界，而非消灭计算', '从上到下，越来越多的工作提前到写路径。', e)

save('client-subscribe', '客户端也是需要恢复的小订阅者', '先取得一致初态，再接增量；断线之后按保存的游标补读。', [
    box('snapshot', 24, 130, 230, 82, '服务端快照\n对应游标 40'),
    box('initial', 540, 130, 220, 82, '客户端初始化\n本地状态 @40'),
    arrow('init', 260, 171, 274, 0, 'snapshot', 'initial'),
    text('initlabel', 320, 135, '① 初始化读', 18),
    box('log', 24, 280, 230, 82, '订阅事件流\n41 → 42 → 43 …'),
    box('local', 540, 280, 220, 82, '状态与游标一致保存\n已应用到 42', 19),
    arrow('push', 260, 321, 274, 0, 'log', 'local', True),
    text('pushlabel', 297, 278, '② 推送 41、42', 18),
    arrow('localapply', 650, 218, 0, 56, 'initial', 'local'),
    text('disconnect', 540, 394, '离线：本地仍可阅读', 18),
    arrow('resume', 534, 450, -274, 0, None, None, True),
    text('resumelabel', 278, 413, '③ 重连：携带游标 42', 18),
    text('replay', 24, 433, '从 43 补读', 20, INK),
    text('bottom', 24, 510, '游标过期 → 重新取得快照并衔接增量；长连接本身不保证重放。', 18),
])

save('request-id', '网络重试，仍是同一次业务操作', 'r7 在客户端创建；所有重试保持 r7。', [
    box('client', 24, 125, 180, 76, '客户端\n意图 r7'),
    box('app', 300, 125, 180, 76, '应用服务器\n传递 r7'),
    box('db', 580, 125, 220, 76, '数据库\n唯一请求记录'),
    arrow('first', 210, 163, 84, 0, 'client', 'app'),
    arrow('forward', 486, 163, 88, 0, 'app', 'db'),
    box('tx', 510, 250, 290, 105, '本地事务共同提交\n请求 r7 ＋ 余额修改', 21),
    arrow('execute', 690, 207, 0, 37, 'db', 'tx'),
    arrow('lost', 504, 303, -294, 0, 'tx', None, True),
    text('loss', 30, 270, '× 成功响应丢失\n客户端不知道结果', 19),
    box('retry', 24, 420, 220, 76, '仍用 r7 重试'),
    box('result', 510, 420, 290, 76, '重复插入失败并回滚\n读取 r7 的原结果', 20),
    arrow('again', 250, 458, 254, 0, 'retry', 'result'),
    text('againlabel', 300, 423, '不重新扣款', 18),
    text('bottom', 24, 550, '新业务意图才用新 ID；唯一约束失败后不能继续执行余额更新。', 18),
])

save('payment', '批准在 A，效果传播到各账户', '假设：A 有 100 元；B 可接受入账；转 30 元，手续费 1 元。', [
    text('request', 24, 120, '客户端请求 r7', 20, INK),
    box('source', 24, 270, 190, 100, 'A 账户日志\n统一该账户顺序'),
    box('processor', 305, 270, 215, 100, 'A 处理器\n检查并预留 31', 21),
    arrow('submit', 118, 155, 0, 109, None, 'source'),
    arrow('consume', 220, 320, 79, 0, 'source', 'processor'),
    text('local', 305, 410, '可用余额：100 → 69\n出账后：账面 69、预留 0', 18),
    box('dest', 655, 210, 195, 88, 'B 日志与处理器\n入账 +30', 20),
    box('fee', 655, 400, 195, 88, 'F 日志与处理器\n入账 +1', 20),
    arrow('incoming', 526, 296, 123, -42, 'processor', 'dest', True),
    arrow('fees', 526, 347, 123, 97, 'processor', 'fee', True),
    arrow('outgoing', 412, 264, -232, 0, 'processor', 'source', True,
          [[0,0],[0,-65],[-232,-65],[-232,0]]),
    text('looplabel', 190, 157, 'r7 出账 −31：回到 A 日志', 18),
    text('roles', 590, 335, '都带 r7\n区分分录角色', 18),
    text('bottom', 24, 535, '各分片按序应用、按效果去重；没有跨账户的即时共同可见点。', 18),
    text('done', 24, 574, '全部完成后：69 + 30 + 1 = 100。', 20, INK),
])

save('recovery', '恢复的是尚未完成的输出责任', '工程补充：持久待发清单；另一条路径是状态与位点一致恢复后重放。', [
    box('tx', 24, 135, 320, 140, '一个本地事务\n批准 r7、预留 31、输入位点\n待发：A−31 / B+30 / F+1', 20),
    box('publish', 440, 155, 190, 100, '发布器\n逐条可靠交接'),
    arrow('scan', 350, 205, 84, 0, 'tx', 'publish'),
    box('b', 710, 155, 190, 100, 'B 已收到 +30\n确认可能丢失', 20),
    arrow('sendb', 636, 205, 68, 0, 'publish', 'b', True),
    text('crash', 440, 295, '× 只发 B 后崩溃', 20, INK),
    box('resume', 24, 395, 320, 110, '重启读取持久待发记录\n补齐未确认的责任', 21),
    arrow('recover', 184, 281, 0, 108, 'tx', 'resume'),
    box('a', 440, 385, 190, 100, 'A：补发 −31\n完成预留出账', 20),
    box('f', 710, 385, 190, 100, 'F：补发 +1\n手续费入账', 20),
    arrow('senda', 350, 430, 84, 0, 'resume', 'a', True),
    arrow('sendf', 350, 480, 354, 0, 'resume', 'f', True,
          [[0,0],[35,60],[340,60],[354,0]]),
    text('duplicate', 440, 560, 'B 若重复收到：同一分录只生效一次。', 18),
    text('bottom', 24, 620, '不能只记 seen(r7) 就跳过；确认前的发送责任必须可恢复。', 19),
])

print('wrote 6 chapter-13 skeletons')
