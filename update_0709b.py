import re
from datetime import date, datetime

path = r"bga_results.html"
with open(path, encoding='utf-8') as f:
    html = f.read()

# ── 1. プレイヤーカード更新 (TM Dice除外による差し戻し) ──
# sasuken: 2位 28→27
html = html.replace('<span class="rank-count c2">28</span>', '<span class="rank-count c2">27</span>')
# aohige: 1位 29→28
html = html.replace('<span class="rank-count a">29</span>', '<span class="rank-count a">28</span>')
# Jin: 1位 15→14
html = html.replace('<span class="rank-count j">15</span>', '<span class="rank-count j">14</span>')
# 総対戦数 62→61
html = html.replace('<div class="card-sub">62戦中</div>', '<div class="card-sub">61戦中</div>')
html = html.replace('<div class="total-num">62</div>', '<div class="total-num">61</div>')

# ── 2. ゲーム別成績: TM Dice行を削除 ──
html = html.replace(
    '      <tr>\n'
    '        <td><a href="https://boardgamearena.com/gamepanel?game=terraformingmarsthedicegame" target="_blank" rel="noopener">テラフォーミング・マーズ:ダイスゲーム</a><br>'
    '<span style="font-weight:400;color:#999;font-size:.75rem">Terraforming Mars: The Dice Game</span></td>\n'
    '        <td>1</td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num s">0</span><div class="bar-bg"></div></div></td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num a">1</span><div class="bar-bg"><div class="bar-fill bar-a" style="width:100%"></div></div></div></td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num j">1</span><div class="bar-bg"><div class="bar-fill bar-j" style="width:100%"></div></div></div></td>\n'
    '      </tr>\n',
    ''
)

# ── 3. 棒グラフ: 50分を差し戻し ──
html = html.replace(
    '            <!-- 50分: s=3(60px), a=3(60px), j=1(20px) -->\n'
    '            <div class="pt-group">\n'
    '              <div class="pt-bar bar-s" style="height:60px;background:var(--s)" title="sasuken2999: 3勝"><span class="pt-n">3</span></div>\n'
    '              <div class="pt-bar bar-a" style="height:60px;background:var(--a)" title="aohige nagoya: 3勝"><span class="pt-n">3</span></div>\n'
    '              <div class="pt-bar bar-j" style="height:20px;background:var(--j)" title="Jin2798: 1勝"><span class="pt-n">1</span></div>\n'
    '            </div>',
    '            <!-- 50分: s=3(60px), a=2(40px) -->\n'
    '            <div class="pt-group">\n'
    '              <div class="pt-bar bar-s" style="height:60px;background:var(--s)" title="sasuken2999: 3勝"><span class="pt-n">3</span></div>\n'
    '              <div class="pt-bar bar-a" style="height:40px;background:var(--a)" title="aohige nagoya: 2勝"><span class="pt-n">2</span></div>\n'
    '            </div>'
)

# ── 4. X軸ラベル: 50分 4→3タイトル (TM Dice除外) ──
html = html.replace(
    '<span class="pt-xg" title="チャレンジャーズ! / ダーウィンズ・ジャーニー / アグリコラ / テラフォーミング・マーズ:ダイスゲーム">4タイトル ▴</span>',
    '<span class="pt-xg" title="チャレンジャーズ! / ダーウィンズ・ジャーニー / アグリコラ">3タイトル ▴</span>'
)

# ── 5. 履歴: TM Dice行(#2)を削除 ──
html = html.replace(
    '\n'
    '      <tr>\n'
    '        <td>2</td><td class="date">2026-07-09<br>（本日）</td>\n'
    '        <td class="game-name"><a href="https://boardgamearena.com/gamepanel?game=terraformingmarsthedicegame" target="_blank" rel="noopener">テラフォーミング・マーズ:ダイスゲーム</a><br>'
    '<span style="font-weight:400;color:#999;font-size:.78rem">Terraforming Mars: The Dice Game</span></td>\n'
    '        <td class="pt-time">50</td>\n'
    '        <td><div class="rank">\n'
    '          <div class="rrow"><span class="badge b1">1位</span><span class="p-j">Jin2798</span><span class="score">1pt</span></div>\n'
    '          <div class="rrow"><span class="badge b1">1位</span><span class="p-a">aohige nagoya</span><span class="score">1pt</span></div>\n'
    '          <div class="rrow"><span class="badge b2">2位</span><span class="p-s">sasuken2999</span><span class="score">0pt</span></div>\n'
    '        </div></td>\n'
    '      </tr>\n',
    ''
)

# ── 6. 履歴行番号シフト: 3→2, 4→3, ..., 62→61 ──
for i in range(3, 63):
    html = html.replace(
        f'<td>{i}</td><td class="date">',
        f'<td>{i-1}</td><td class="date">'
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

chk('header 2026-07-09',                   '2026-07-09 集計' in h)
chk('total-num 61',                         '<div class="total-num">61</div>' in h)
chk('card-sub 61 x3',                       h.count('<div class="card-sub">61戦中</div>') == 3)
chk('sasuken s=19',                         '<span class="rank-count s">19</span>' in h)
chk('sasuken c2=27',                        '<span class="rank-count c2">27</span>' in h)
chk('sasuken c3=15',                        '<span class="rank-count c3">15</span>' in h)
chk('aohige a=28',                          '<span class="rank-count a">28</span>' in h)
chk('aohige c2=18',                         '<span class="rank-count c2">18</span>' in h)
chk('aohige c3=15',                         '<span class="rank-count c3">15</span>' in h)
chk('Jin j=14',                             '<span class="rank-count j">14</span>' in h)
chk('Jin c2=22',                            '<span class="rank-count c2">22</span>' in h)
chk('Jin c3=25',                            '<span class="rank-count c3">25</span>' in h)
chk('stoneage in gamestats',                'game=stoneage" target="_blank"' in h)
chk('terraformingmarsthedicegame removed',  'game=terraformingmarsthedicegame' not in h)
chk('lorenzo in gamestats',                 'game=lorenzo" target="_blank"' in h)
chk('50min reverted s=3 a=2',              '<!-- 50分: s=3(60px), a=2(40px) -->' in h)
chk('50min no j bar',                       '<!-- 50分: s=3(60px), a=3' not in h)
chk('50min 3titles',                        '3タイトル' in h and 'アグリコラ' in h)
chk('50min no tmdice title',               'テラフォーミング・マーズ:ダイスゲーム' not in h)
chk('row#1 stoneage today',                 '<td>1</td><td class="date">2026-07-09<br>（本日）</td>' in h)
chk('row#2 lorenzo today',                  '<td>2</td><td class="date">2026-07-09<br>（本日）</td>' in h)
chk('row#3 = 2026-06-30',                   '<td>3</td><td class="date">2026-06-30' in h)
row_count = len(__import__('re').findall(r'<td>\d+</td><td class="date">', h))
chk(f'61 history rows (found {row_count})', row_count == 61)
chk('no 62 total',                          '<div class="total-num">62</div>' not in h)

print(f'\nResult: {ok} OK / {ng} NG')
