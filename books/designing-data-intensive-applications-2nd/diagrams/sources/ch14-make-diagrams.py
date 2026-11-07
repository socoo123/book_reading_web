"""Authoring helpers for three original chapter-14 Excalidraw scenes."""
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent
TEXT, MUTED, ACCENT, SOFT = '#292824', '#66645d', '#386d74', '#f0ece4'


def text(id, x, y, value, size=18, color=MUTED):
    return dict(type='text', id=id, x=x, y=y, text=value, fontSize=size,
                fontFamily=2, strokeColor=color)


def box(id, x, y, value, width=240, height=90):
    return dict(type='rectangle', id=id, x=x, y=y, width=width, height=height,
                strokeColor=ACCENT, backgroundColor=SOFT, fillStyle='solid', roughness=0.7,
                label=dict(text=value, fontSize=21, fontFamily=2, strokeColor=TEXT))


def arrow(id, x, y, dx, dy, start, end, dashed=False):
    return dict(type='arrow', id=id, x=x, y=y, width=abs(dx), height=abs(dy),
                points=[[0, 0], [dx, dy]], strokeColor=ACCENT, roughness=0.7,
                strokeStyle='dashed' if dashed else 'solid',
                start={'id': start}, end={'id': end})


def save(stem, elements):
    (HERE / f'{stem}.skeleton.json').write_text(json.dumps(elements, ensure_ascii=False, indent=2) + '\n')


save('ch14-responsibility-overview', [
    text('title', 24, 20, '把责任从数据管道接回人的生活', 25, TEXT),
    text('subtitle', 24, 66, '顺时针读：技术输出会成为人的实际处境。'),
    box('person', 24, 130, '人的行为\n身份、兴趣与处境'),
    box('collect', 410, 130, '采集与保留\n记录、关联与保存'),
    box('decide', 410, 340, '分析与决策\n预测、筛选与推荐'),
    box('impact', 24, 340, '生活中的结果\n机会、成本与自主权'),
    arrow('capture', 274, 175, 126, 0, 'person', 'collect'),
    arrow('process', 530, 230, 0, 100, 'collect', 'decide'),
    arrow('act', 400, 385, -126, 0, 'decide', 'impact'),
    arrow('return', 144, 330, 0, -100, 'impact', 'person', True),
    text('capture-label', 302, 142, '采集'),
    text('process-label', 548, 270, '加工'),
    text('act-label', 300, 351, '行动'),
    text('return-label', 164, 270, '影响'),
    text('question-collect', 24, 480, '采集责任：是否必要？谁能选择用途与保留？'),
    text('question-decide', 24, 515, '决策责任：谁受影响？谁解释、纠错并承担后果？'),
])

save('ch14-credit-feedback', [
    text('title', 24, 20, '一次不幸，怎样被反馈循环延长', 25, TEXT),
    text('subtitle', 24, 66, '前提：雇主使用信用分筛选；外部冲击先造成还款困难。', 17),
    box('payments', 24, 140, '还款困难\n错过账单'),
    box('score', 410, 140, '信用分下降\n被标记为更高风险'),
    box('jobs', 410, 350, '就业机会减少\n雇主按信用筛选'),
    box('income', 24, 350, '收入更难恢复\n处境继续恶化'),
    arrow('record', 274, 185, 126, 0, 'payments', 'score'),
    arrow('screen', 530, 240, 0, 100, 'score', 'jobs'),
    arrow('earning', 400, 395, -126, 0, 'jobs', 'income'),
    arrow('feedback', 144, 340, 0, -100, 'income', 'payments', True),
    text('record-label', 294, 150, '记入记录'),
    text('screen-label', 549, 279, '筛选'),
    text('earning-label', 294, 360, '影响收入'),
    text('feedback-label', 164, 265, '影响后续\n还款'),
    text('lesson', 24, 485, '后续数据也包含先前决策的影响。', 20, TEXT),
    text('boundary', 24, 524, '实线：本例影响路径　虚线：处境返回输入；不是普遍因果定律。', 17),
])

save('ch14-purpose-choice', [
    text('title', 24, 20, '同一份病历，不同用途需要不同判断', 25, TEXT),
    text('subtitle', 24, 66, '原书罕见病案例：愿意帮助研究，不等于放弃用途选择。', 17),
    box('patient', 24, 150, '患者的病历\n由本人作出知情选择', 250, 100),
    box('research', 455, 150, '研究者\n用于约定研究', 250, 100),
    box('other-purpose', 455, 365, '就业／保险判断\n另一种用途', 250, 100),
    arrow('share', 284, 200, 161, 0, 'patient', 'research'),
    arrow('reuse', 580, 260, 0, 95, 'research', 'other-purpose', True),
    text('share-label', 310, 163, '愿意分享'),
    text('reuse-label', 600, 291, '用途扩展'),
    text('choice', 24, 355, '研究同意\n不自动涵盖另一个用途', 20, TEXT),
    text('legend', 24, 515, '实线：约定分享　虚线：需另行判断的用途，不表示已获许可。', 17),
    text('law', 24, 550, '本图说明个人选择；不把同意写成唯一法律依据。', 17),
])

print('Wrote three ch14 skeletons; export with the shared official Excalidraw tool.')
