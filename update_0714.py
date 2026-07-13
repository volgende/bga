import re
from datetime import date, datetime

path = r"bga_results.html"
with open(path, encoding='utf-8') as f:
    html = f.read()

today = date(2026, 7, 14)

# ── 1. 相対日付の更新 ──
def upd_date(m):
    d = datetime.strptime(m.group(1), '%Y-%m-%d').date()
    n = (today - d).days
    label = '本日' if n == 0 else f'{n}日前'
    return f'<td class="date">{m.group(1)}<br>（{label}）</td>'
html = re.sub(r'<td class="date">(\d{4}-\d{2}-\d{2})<br>（[^）]+）</td>', upd_date, html)

# ── 2. 4人集計: プレイヤーカード更新 ──
# sasuken: 1位=1(タクタ同点), 2位=1(TM), 3位=1(シフティング), 4位=1(スカルキング)
html = html.replace('<span class="rank-count s" id="f-s1">0</span>', '<span class="rank-count s" id="f-s1">1</span>')
html = html.replace('<span class="rank-count c2" id="f-s2">0</span>', '<span class="rank-count c2" id="f-s2">1</span>')
html = html.replace('<span class="rank-count c3" id="f-s3">0</span>', '<span class="rank-count c3" id="f-s3">1</span>')
html = html.replace('<span class="rank-count c4" id="f-s4">0</span>', '<span class="rank-count c4" id="f-s4">1</span>')
# aohige: 1位=1(タクタ同点), 2位=1(スカルキング), 3位=1(TM), 4位=0
html = html.replace('<span class="rank-count a" id="f-a1">0</span>', '<span class="rank-count a" id="f-a1">1</span>')
html = html.replace('<span class="rank-count c2" id="f-a2">0</span>', '<span class="rank-count c2" id="f-a2">1</span>')
html = html.replace('<span class="rank-count c3" id="f-a3">0</span>', '<span class="rank-count c3" id="f-a3">1</span>')
# ponytailthes: 1位=4(全試合1位!), 2/3/4位=0
html = html.replace('<span class="rank-count p" id="f-p1">0</span>', '<span class="rank-count p" id="f-p1">4</span>')
# Jin: 1位=1(シフティング同点), 2位=1(タクタ), 3位=1(スカルキング), 4位=1(TM)
html = html.replace('<span class="rank-count j" id="f-j1">0</span>', '<span class="rank-count j" id="f-j1">1</span>')
html = html.replace('<span class="rank-count c2" id="f-j2">0</span>', '<span class="rank-count c2" id="f-j2">1</span>')
html = html.replace('<span class="rank-count c3" id="f-j3">0</span>', '<span class="rank-count c3" id="f-j3">1</span>')
html = html.replace('<span class="rank-count c4" id="f-j4">0</span>', '<span class="rank-count c4" id="f-j4">1</span>')
# 総対戦数・各プレイヤー「N戦中」
html = html.replace('<div class="total-num" id="f-total">0</div>', '<div class="total-num" id="f-total">4</div>')
html = html.replace('<div class="card-sub" id="f-sub-s">0戦中</div>', '<div class="card-sub" id="f-sub-s">4戦中</div>')
html = html.replace('<div class="card-sub" id="f-sub-a">0戦中</div>', '<div class="card-sub" id="f-sub-a">4戦中</div>')
html = html.replace('<div class="card-sub" id="f-sub-p">0戦中</div>', '<div class="card-sub" id="f-sub-p">4戦中</div>')
html = html.replace('<div class="card-sub" id="f-sub-j">0戦中</div>', '<div class="card-sub" id="f-sub-j">4戦中</div>')

# ── 3. 4人集計: ゲーム別成績テーブルを追加 ──
new_gamestats = (
    '      <tr>\n'
    '        <td><a href="https://boardgamearena.com/gamepanel?game=terraformingmars" target="_blank" rel="noopener">テラフォーミング・マーズ</a><br>'
    '<span style="font-weight:400;color:#999;font-size:.75rem">Terraforming Mars</span></td>\n'
    '        <td>1</td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num s">0</span><div class="bar-bg"></div></div></td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num a">0</span><div class="bar-bg"></div></div></td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num p">1</span><div class="bar-bg"><div class="bar-fill bar-p" style="width:100%"></div></div></div></td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num j">0</span><div class="bar-bg"></div></div></td>\n'
    '      </tr>\n'
    '      <tr>\n'
    '        <td><a href="https://boardgamearena.com/gamepanel?game=shiftingstones" target="_blank" rel="noopener">シフティング・ストーンズ</a><br>'
    '<span style="font-weight:400;color:#999;font-size:.75rem">Shifting Stones</span></td>\n'
    '        <td>1</td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num s">0</span><div class="bar-bg"></div></div></td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num a">0</span><div class="bar-bg"></div></div></td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num p">1</span><div class="bar-bg"><div class="bar-fill bar-p" style="width:100%"></div></div></div></td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num j">1</span><div class="bar-bg"><div class="bar-fill bar-j" style="width:100%"></div></div></div></td>\n'
    '      </tr>\n'
    '      <tr>\n'
    '        <td><a href="https://boardgamearena.com/gamepanel?game=skullking" target="_blank" rel="noopener">スカルキング</a><br>'
    '<span style="font-weight:400;color:#999;font-size:.75rem">Skull King</span></td>\n'
    '        <td>1</td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num s">0</span><div class="bar-bg"></div></div></td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num a">0</span><div class="bar-bg"></div></div></td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num p">1</span><div class="bar-bg"><div class="bar-fill bar-p" style="width:100%"></div></div></div></td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num j">0</span><div class="bar-bg"></div></div></td>\n'
    '      </tr>\n'
    '      <tr>\n'
    '        <td><a href="https://boardgamearena.com/gamepanel?game=tacta" target="_blank" rel="noopener">タクタ</a><br>'
    '<span style="font-weight:400;color:#999;font-size:.75rem">Tacta</span></td>\n'
    '        <td>1</td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num s">1</span><div class="bar-bg"><div class="bar-fill bar-s" style="width:100%"></div></div></div></td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num a">1</span><div class="bar-bg"><div class="bar-fill bar-a" style="width:100%"></div></div></div></td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num p">1</span><div class="bar-bg"><div class="bar-fill bar-p" style="width:100%"></div></div></div></td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num j">0</span><div class="bar-bg"></div></div></td>\n'
    '      </tr>\n'
)
html = html.replace(
    '    <tbody id="f-gamestats-body">\n'
    '      <tr><td colspan="6" style="text-align:center;color:#aaa;padding:24px;">まだ対戦記録がありません</td></tr>\n'
    '    </tbody>',
    '    <tbody id="f-gamestats-body">\n'
    + new_gamestats +
    '    </tbody>'
)

# ── 4. 4人集計: 履歴行を追加（新しい順: タクタ→スカルキング→シフティング→TM） ──
new_history = (
    '\n'
    '      <tr>\n'
    '        <td>1</td><td class="date">2026-07-14<br>（本日）</td>\n'
    '        <td class="game-name"><a href="https://boardgamearena.com/gamepanel?game=tacta" target="_blank" rel="noopener">タクタ</a><br>'
    '<span style="font-weight:400;color:#999;font-size:.78rem">Tacta</span></td>\n'
    '        <td class="pt-time">20</td>\n'
    '        <td><div class="rank">\n'
    '          <div class="rrow"><span class="badge b1">1位</span><span class="p-a">aohige nagoya</span><span class="score">50pt</span></div>\n'
    '          <div class="rrow"><span class="badge b1">1位</span><span class="p-p">ponytailthes</span><span class="score">50pt</span></div>\n'
    '          <div class="rrow"><span class="badge b1">1位</span><span class="p-s">sasuken2999</span><span class="score">50pt</span></div>\n'
    '          <div class="rrow"><span class="badge b2">2位</span><span class="p-j">Jin2798</span><span class="score">48pt</span></div>\n'
    '        </div></td>\n'
    '      </tr>\n'
    '\n'
    '      <tr>\n'
    '        <td>2</td><td class="date">2026-07-14<br>（本日）</td>\n'
    '        <td class="game-name"><a href="https://boardgamearena.com/gamepanel?game=skullking" target="_blank" rel="noopener">スカルキング</a><br>'
    '<span style="font-weight:400;color:#999;font-size:.78rem">Skull King</span></td>\n'
    '        <td class="pt-time">20</td>\n'
    '        <td><div class="rank">\n'
    '          <div class="rrow"><span class="badge b1">1位</span><span class="p-p">ponytailthes</span><span class="score">170pt</span></div>\n'
    '          <div class="rrow"><span class="badge b2">2位</span><span class="p-a">aohige nagoya</span><span class="score">120pt</span></div>\n'
    '          <div class="rrow"><span class="badge b3">3位</span><span class="p-j">Jin2798</span><span class="score">110pt</span></div>\n'
    '          <div class="rrow"><span class="badge b4">4位</span><span class="p-s">sasuken2999</span><span class="score">-10pt</span></div>\n'
    '        </div></td>\n'
    '      </tr>\n'
    '\n'
    '      <tr>\n'
    '        <td>3</td><td class="date">2026-07-14<br>（本日）</td>\n'
    '        <td class="game-name"><a href="https://boardgamearena.com/gamepanel?game=shiftingstones" target="_blank" rel="noopener">シフティング・ストーンズ</a><br>'
    '<span style="font-weight:400;color:#999;font-size:.78rem">Shifting Stones</span></td>\n'
    '        <td class="pt-time">20</td>\n'
    '        <td><div class="rank">\n'
    '          <div class="rrow"><span class="badge b1">1位</span><span class="p-p">ponytailthes</span><span class="score">15pt</span></div>\n'
    '          <div class="rrow"><span class="badge b1">1位</span><span class="p-j">Jin2798</span><span class="score">15pt</span></div>\n'
    '          <div class="rrow"><span class="badge b2">2位</span><span class="p-a">aohige nagoya</span><span class="score">14pt</span></div>\n'
    '          <div class="rrow"><span class="badge b3">3位</span><span class="p-s">sasuken2999</span><span class="score">11pt</span></div>\n'
    '        </div></td>\n'
    '      </tr>\n'
    '\n'
    '      <tr>\n'
    '        <td>4</td><td class="date">2026-07-14<br>（本日）</td>\n'
    '        <td class="game-name"><a href="https://boardgamearena.com/gamepanel?game=terraformingmars" target="_blank" rel="noopener">テラフォーミング・マーズ</a><br>'
    '<span style="font-weight:400;color:#999;font-size:.78rem">Terraforming Mars</span></td>\n'
    '        <td class="pt-time">120</td>\n'
    '        <td><div class="rank">\n'
    '          <div class="rrow"><span class="badge b1">1位</span><span class="p-p">ponytailthes</span><span class="score">74pt</span></div>\n'
    '          <div class="rrow"><span class="badge b2">2位</span><span class="p-s">sasuken2999</span><span class="score">57pt</span></div>\n'
    '          <div class="rrow"><span class="badge b3">3位</span><span class="p-a">aohige nagoya</span><span class="score">57pt</span></div>\n'
    '          <div class="rrow"><span class="badge b4">4位</span><span class="p-j">Jin2798</span><span class="score">50pt</span></div>\n'
    '        </div></td>\n'
    '      </tr>\n'
    '\n'
)
html = html.replace(
    '    <tbody id="f-history-body">\n'
    '      <tr><td colspan="5" style="text-align:center;color:#aaa;padding:24px;">まだ対戦記録がありません</td></tr>\n'
    '    </tbody>',
    '    <tbody id="f-history-body">\n'
    + new_history +
    '    </tbody>'
)

with open(path, 'w', encoding='utf-8') as f:
    f.write(html)

print("Done!")

# ── 検証 ──
with open(path, encoding='utf-8') as f:
    h = f.read()

ok = ng = 0
def chk(name, cond):
    global ok, ng
    if cond: ok += 1; print(f'OK {name}')
    else:    ng += 1; print(f'NG {name}')

chk('f-total=4',           '<div class="total-num" id="f-total">4</div>' in h)
chk('f-sub x4 = 4戦中',    h.count('>4戦中<') == 4)
chk('f-s1=1',              'id="f-s1">1</span>' in h)
chk('f-s2=1',              'id="f-s2">1</span>' in h)
chk('f-s3=1',              'id="f-s3">1</span>' in h)
chk('f-s4=1',              'id="f-s4">1</span>' in h)
chk('f-a1=1',              'id="f-a1">1</span>' in h)
chk('f-a2=1',              'id="f-a2">1</span>' in h)
chk('f-a3=1',              'id="f-a3">1</span>' in h)
chk('f-a4=0 (unchanged)',  'id="f-a4">0</span>' in h)
chk('f-p1=4',              'id="f-p1">4</span>' in h)
chk('f-p2=0 (unchanged)',  'id="f-p2">0</span>' in h)
chk('f-j1=1',              'id="f-j1">1</span>' in h)
chk('f-j2=1',              'id="f-j2">1</span>' in h)
chk('f-j3=1',              'id="f-j3">1</span>' in h)
chk('f-j4=1',              'id="f-j4">1</span>' in h)
chk('gamestats terraformingmars', 'game=terraformingmars" target="_blank" rel="noopener">テラフォーミング・マーズ' in h)
chk('gamestats shiftingstones',   'game=shiftingstones" target="_blank" rel="noopener">シフティング・ストーンズ' in h)
chk('gamestats skullking',        'game=skullking" target="_blank" rel="noopener">スカルキング' in h)
chk('gamestats tacta',            'game=tacta" target="_blank" rel="noopener">タクタ' in h)
chk('no placeholder gamestats',   'まだ対戦記録がありません' not in h)
chk('history row#1 tacta',        '<td>1</td><td class="date">2026-07-14<br>（本日）</td>' in h)
chk('history row#4 TM',           '<td>4</td><td class="date">2026-07-14<br>（本日）</td>' in h)
chk('main tab total unchanged',   '<div class="total-num">61</div>' in h)

print(f'\nResult: {ok} OK / {ng} NG')
