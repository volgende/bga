import re
from datetime import date, datetime

path = r"bga_results.html"
with open(path, encoding='utf-8') as f:
    html = f.read()

today = date(2026, 9, 4)

# ── 1. ヘッダー日付更新 ──
html = html.replace('2026-08-26 集計', '2026-09-04 集計')

# ── 2. 相対日付の更新（全タブ対象） ──
def upd_date(m):
    d = datetime.strptime(m.group(1), '%Y-%m-%d').date()
    n = (today - d).days
    label = '本日' if n == 0 else f'{n}日前'
    return f'<td class="date">{m.group(1)}<br>（{label}）</td>'
html = re.sub(r'<td class="date">(\d{4}-\d{2}-\d{2})<br>（[^）]+）</td>', upd_date, html)

# ── 3. プレイヤーカード更新（メイン集計 84→88） ──
# 新規4戦(すべて通常集計):
#   digit  : 1位sas / 2位Jin / 2位aohige(タイ)   winner sasuken (10分)
#   coffee : 1位Jin / 2位sas / 3位aohige          winner Jin (30分)
#   dewan  : 1位Jin / 2位aohige / 3位sas          winner Jin (20分)
#   dinos  : 1位sas / 2位aohige / 3位Jin          winner sasuken (10分)
# sasuken 25/33/26 → 27/34/27
html = html.replace('<span class="rank-count s">25</span>', '<span class="rank-count s">27</span>')
html = html.replace('<span class="rank-count c2">33</span>', '<span class="rank-count c2">34</span>')  # sasuken c2
html = html.replace('<span class="rank-count c3">26</span>', '<span class="rank-count c3">27</span>')  # sasuken c3
# Jin 22/30/32 → 24/31/33  (先にJin c2 30→31 を処理し aohige 27→30 との衝突回避)
html = html.replace('<span class="rank-count j">22</span>', '<span class="rank-count j">24</span>')
html = html.replace('<span class="rank-count c2">30</span>', '<span class="rank-count c2">31</span>')  # Jin c2
html = html.replace('<span class="rank-count c3">32</span>', '<span class="rank-count c3">33</span>')  # Jin c3
# aohige 39/27/18 → 39/30/19  (1位は変化なし)
html = html.replace('<span class="rank-count c2">27</span>', '<span class="rank-count c2">30</span>')  # aohige c2
html = html.replace('<span class="rank-count c3">18</span>', '<span class="rank-count c3">19</span>')  # aohige c3
# 総対戦数 84→88
html = html.replace('<div class="card-sub">84戦中</div>', '<div class="card-sub">88戦中</div>')
html = html.replace('<div class="total-num">84</div>', '<div class="total-num">88</div>')

# ── 4. ゲーム別成績: 新4タイトルを先頭に追加（1戦ずつ） ──
new_gs_rows = (
    '      <tr>\n'
    '        <td><a href="https://boardgamearena.com/gamepanel?game=digitcode" target="_blank" rel="noopener">ディジットコード</a><br>'
    '<span style="font-weight:400;color:#999;font-size:.75rem">Digit Code</span></td>\n'
    '        <td>1</td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num s">1</span><div class="bar-bg"><div class="bar-fill bar-s" style="width:100%"></div></div></div></td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num a">0</span><div class="bar-bg"></div></div></td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num j">0</span><div class="bar-bg"></div></div></td>\n'
    '      </tr>\n'
    '      <tr>\n'
    '        <td><a href="https://boardgamearena.com/gamepanel?game=coffeerush" target="_blank" rel="noopener">コーヒーラッシュ</a><br>'
    '<span style="font-weight:400;color:#999;font-size:.75rem">Coffee Rush</span></td>\n'
    '        <td>1</td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num s">0</span><div class="bar-bg"></div></div></td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num a">0</span><div class="bar-bg"></div></div></td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num j">1</span><div class="bar-bg"><div class="bar-fill bar-j" style="width:100%"></div></div></div></td>\n'
    '      </tr>\n'
    '      <tr>\n'
    '        <td><a href="https://boardgamearena.com/gamepanel?game=dewan" target="_blank" rel="noopener">デワン</a><br>'
    '<span style="font-weight:400;color:#999;font-size:.75rem">Dewan</span></td>\n'
    '        <td>1</td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num s">0</span><div class="bar-bg"></div></div></td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num a">0</span><div class="bar-bg"></div></div></td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num j">1</span><div class="bar-bg"><div class="bar-fill bar-j" style="width:100%"></div></div></div></td>\n'
    '      </tr>\n'
    '      <tr>\n'
    '        <td><a href="https://boardgamearena.com/gamepanel?game=diggingfordinos" target="_blank" rel="noopener">ディギング・フォー・ダイノス</a><br>'
    '<span style="font-weight:400;color:#999;font-size:.75rem">Digging For Dinos</span></td>\n'
    '        <td>1</td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num s">1</span><div class="bar-bg"><div class="bar-fill bar-s" style="width:100%"></div></div></div></td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num a">0</span><div class="bar-bg"></div></div></td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num j">0</span><div class="bar-bg"></div></div></td>\n'
    '      </tr>\n'
)
html = html.replace(
    '    <tbody>\n'
    '      <tr>\n'
    '        <td><a href="https://boardgamearena.com/gamepanel?game=pondscape"',
    '    <tbody>\n'
    + new_gs_rows +
    '      <tr>\n'
    '        <td><a href="https://boardgamearena.com/gamepanel?game=pondscape"'
)

# ── 5. 棒グラフ更新（スケールは14勝のまま変更なし） ──
# 5a. 10分: s=1→3(60px)  (digitcode, dinos)
html = html.replace(
    '            <!-- 10分: s=1(20px), a=2(40px), j=2(40px) -->\n'
    '            <div class="pt-group">\n'
    '              <div class="pt-bar bar-s" style="height:20px;background:var(--s)" title="sasuken2999: 1勝"><span class="pt-n">1</span></div>\n'
    '              <div class="pt-bar bar-a" style="height:40px;background:var(--a)" title="aohige nagoya: 2勝"><span class="pt-n">2</span></div>\n'
    '              <div class="pt-bar bar-j" style="height:40px;background:var(--j)" title="Jin2798: 2勝"><span class="pt-n">2</span></div>\n'
    '            </div>',
    '            <!-- 10分: s=3(60px), a=2(40px), j=2(40px) -->\n'
    '            <div class="pt-group">\n'
    '              <div class="pt-bar bar-s" style="height:60px;background:var(--s)" title="sasuken2999: 3勝"><span class="pt-n">3</span></div>\n'
    '              <div class="pt-bar bar-a" style="height:40px;background:var(--a)" title="aohige nagoya: 2勝"><span class="pt-n">2</span></div>\n'
    '              <div class="pt-bar bar-j" style="height:40px;background:var(--j)" title="Jin2798: 2勝"><span class="pt-n">2</span></div>\n'
    '            </div>'
)
# 5b. 20分: j=11→12(240px)  (dewan)
html = html.replace(
    '            <!-- 20分: s=14(280px), a=10(200px), j=11(220px) -->\n'
    '            <div class="pt-group">\n'
    '              <div class="pt-bar bar-s" style="height:280px;background:var(--s)" title="sasuken2999: 14勝"><span class="pt-n">14</span></div>\n'
    '              <div class="pt-bar bar-a" style="height:200px;background:var(--a)" title="aohige nagoya: 10勝"><span class="pt-n">10</span></div>\n'
    '              <div class="pt-bar bar-j" style="height:220px;background:var(--j)" title="Jin2798: 11勝"><span class="pt-n">11</span></div>\n'
    '            </div>',
    '            <!-- 20分: s=14(280px), a=10(200px), j=12(240px) -->\n'
    '            <div class="pt-group">\n'
    '              <div class="pt-bar bar-s" style="height:280px;background:var(--s)" title="sasuken2999: 14勝"><span class="pt-n">14</span></div>\n'
    '              <div class="pt-bar bar-a" style="height:200px;background:var(--a)" title="aohige nagoya: 10勝"><span class="pt-n">10</span></div>\n'
    '              <div class="pt-bar bar-j" style="height:240px;background:var(--j)" title="Jin2798: 12勝"><span class="pt-n">12</span></div>\n'
    '            </div>'
)
# 5c. 30分: j=3→4(80px)  (coffee)
html = html.replace(
    '            <!-- 30分: s=1(20px), a=7(140px), j=3(60px) -->\n'
    '            <div class="pt-group">\n'
    '              <div class="pt-bar bar-s" style="height:20px;background:var(--s)" title="sasuken2999: 1勝"><span class="pt-n">1</span></div>\n'
    '              <div class="pt-bar bar-a" style="height:140px;background:var(--a)" title="aohige nagoya: 7勝"><span class="pt-n">7</span></div>\n'
    '              <div class="pt-bar bar-j" style="height:60px;background:var(--j)" title="Jin2798: 3勝"><span class="pt-n">3</span></div>\n'
    '            </div>',
    '            <!-- 30分: s=1(20px), a=7(140px), j=4(80px) -->\n'
    '            <div class="pt-group">\n'
    '              <div class="pt-bar bar-s" style="height:20px;background:var(--s)" title="sasuken2999: 1勝"><span class="pt-n">1</span></div>\n'
    '              <div class="pt-bar bar-a" style="height:140px;background:var(--a)" title="aohige nagoya: 7勝"><span class="pt-n">7</span></div>\n'
    '              <div class="pt-bar bar-j" style="height:80px;background:var(--j)" title="Jin2798: 4勝"><span class="pt-n">4</span></div>\n'
    '            </div>'
)

# ── 6. X軸ラベル（タイトル追加） ──
# 10分: 2→4 (ディジットコード, ディギング・フォー・ダイノス)
html = html.replace(
    '<span class="pt-xg" title="YRO / レース・フォー・ザ・ギャラクシー">2タイトル ▴</span>',
    '<span class="pt-xg" title="YRO / レース・フォー・ザ・ギャラクシー / ディジットコード / ディギング・フォー・ダイノス">4タイトル ▴</span>'
)
# 20分: 20→21 (デワン)
html = html.replace(
    '/ ベジタブルストック / 郵便馬車 / クィブルス">20タイトル ▴</span>',
    '/ ベジタブルストック / 郵便馬車 / クィブルス / デワン">21タイトル ▴</span>'
)
# 30分: 7→8 (コーヒーラッシュ)
html = html.replace(
    '/ ツォルキン: マヤ神聖歴 / ポンドスケープ">7タイトル ▴</span>',
    '/ ツォルキン: マヤ神聖歴 / ポンドスケープ / コーヒーラッシュ">8タイトル ▴</span>'
)

# ── 7-8. メイン履歴シフト＋新規行挿入（メインタブ限定） ──
marker = '</div><!-- /tab-main -->'
idx = html.index(marker)
main_part, rest_part = html[:idx], html[idx:]

# 7. 行番号シフト 84→88, ..., 1→5
for i in range(84, 0, -1):
    main_part = main_part.replace(
        f'<td>{i}</td><td class="date">',
        f'<td>{i+4}</td><td class="date">'
    )

# 8. 新規履歴行4行を先頭に挿入（新しい順）
new_rows = (
    '\n'
    '      <tr>\n'
    '        <td>1</td><td class="date">2026-09-04<br>（本日）</td>\n'
    '        <td class="game-name"><a href="https://boardgamearena.com/gamepanel?game=digitcode" target="_blank" rel="noopener">ディジットコード</a><br>'
    '<span style="font-weight:400;color:#999;font-size:.78rem">Digit Code</span></td>\n'
    '        <td class="pt-time">10</td>\n'
    '        <td><div class="rank">\n'
    '          <div class="rrow"><span class="badge b1">1位</span><span class="p-s">sasuken2999</span><span class="score">1pt</span></div>\n'
    '          <div class="rrow"><span class="badge b2">2位</span><span class="p-j">Jin2798</span><span class="score">0pt</span></div>\n'
    '          <div class="rrow"><span class="badge b2">2位</span><span class="p-a">aohige nagoya</span><span class="score">0pt</span></div>\n'
    '        </div></td>\n'
    '      </tr>\n'
    '\n'
    '      <tr>\n'
    '        <td>2</td><td class="date">2026-09-04<br>（本日）</td>\n'
    '        <td class="game-name"><a href="https://boardgamearena.com/gamepanel?game=coffeerush" target="_blank" rel="noopener">コーヒーラッシュ</a><br>'
    '<span style="font-weight:400;color:#999;font-size:.78rem">Coffee Rush</span></td>\n'
    '        <td class="pt-time">30</td>\n'
    '        <td><div class="rank">\n'
    '          <div class="rrow"><span class="badge b1">1位</span><span class="p-j">Jin2798</span><span class="score">6pt</span></div>\n'
    '          <div class="rrow"><span class="badge b2">2位</span><span class="p-s">sasuken2999</span><span class="score">6pt</span></div>\n'
    '          <div class="rrow"><span class="badge b3">3位</span><span class="p-a">aohige nagoya</span><span class="score">6pt</span></div>\n'
    '        </div></td>\n'
    '      </tr>\n'
    '\n'
    '      <tr>\n'
    '        <td>3</td><td class="date">2026-09-04<br>（本日）</td>\n'
    '        <td class="game-name"><a href="https://boardgamearena.com/gamepanel?game=dewan" target="_blank" rel="noopener">デワン</a><br>'
    '<span style="font-weight:400;color:#999;font-size:.78rem">Dewan</span></td>\n'
    '        <td class="pt-time">20</td>\n'
    '        <td><div class="rank">\n'
    '          <div class="rrow"><span class="badge b1">1位</span><span class="p-j">Jin2798</span><span class="score">39pt</span></div>\n'
    '          <div class="rrow"><span class="badge b2">2位</span><span class="p-a">aohige nagoya</span><span class="score">38pt</span></div>\n'
    '          <div class="rrow"><span class="badge b3">3位</span><span class="p-s">sasuken2999</span><span class="score">32pt</span></div>\n'
    '        </div></td>\n'
    '      </tr>\n'
    '\n'
    '      <tr>\n'
    '        <td>4</td><td class="date">2026-09-04<br>（本日）</td>\n'
    '        <td class="game-name"><a href="https://boardgamearena.com/gamepanel?game=diggingfordinos" target="_blank" rel="noopener">ディギング・フォー・ダイノス</a><br>'
    '<span style="font-weight:400;color:#999;font-size:.78rem">Digging For Dinos</span></td>\n'
    '        <td class="pt-time">10</td>\n'
    '        <td><div class="rank">\n'
    '          <div class="rrow"><span class="badge b1">1位</span><span class="p-s">sasuken2999</span><span class="score">85pt</span></div>\n'
    '          <div class="rrow"><span class="badge b2">2位</span><span class="p-a">aohige nagoya</span><span class="score">79pt</span></div>\n'
    '          <div class="rrow"><span class="badge b3">3位</span><span class="p-j">Jin2798</span><span class="score">66pt</span></div>\n'
    '        </div></td>\n'
    '      </tr>\n'
    '\n'
)
main_part = main_part.replace(
    '    <tbody>\n\n      <tr>\n        <td>5</td><td class="date">2026-08-26<br>（9日前）</td>',
    '    <tbody>\n' + new_rows + '      <tr>\n        <td>5</td><td class="date">2026-08-26<br>（9日前）</td>'
)

html = main_part + rest_part

with open(path, 'w', encoding='utf-8') as f:
    f.write(html)

print("Done!")

# ── 検証 ──
with open(path, encoding='utf-8') as f:
    h = f.read()
main_h = h[:h.index(marker)]
rest_h = h[h.index(marker):]

ok = ng = 0
def chk(name, cond):
    global ok, ng
    if cond: ok += 1; print(f'OK {name}')
    else:    ng += 1; print(f'NG {name}')

chk('header 2026-09-04',             '2026-09-04 集計' in h)
chk('no old header 08-26',           '2026-08-26 集計' not in h)
chk('total-num 88',                  '<div class="total-num">88</div>' in h)
chk('card-sub 88 x3',                h.count('<div class="card-sub">88戦中</div>') == 3)
chk('sasuken s=27',                  '<span class="rank-count s">27</span>' in h)
chk('sasuken c2=34',                 '<span class="rank-count c2">34</span>' in h)
chk('sasuken c3=27',                 '<span class="rank-count c3">27</span>' in h)
chk('aohige a=39',                   '<span class="rank-count a">39</span>' in h)
chk('aohige c2=30',                  '<span class="rank-count c2">30</span>' in h)
chk('aohige c3=19',                  '<span class="rank-count c3">19</span>' in h)
chk('Jin j=24',                      '<span class="rank-count j">24</span>' in h)
chk('Jin c2=31',                     '<span class="rank-count c2">31</span>' in h)
chk('Jin c3=33',                     '<span class="rank-count c3">33</span>' in h)
chk('sum sasuken 27+34+27=88',       27+34+27 == 88)
chk('sum aohige 39+30+19=88',        39+30+19 == 88)
chk('sum Jin 24+31+33=88',           24+31+33 == 88)
chk('no stale s=25',                 '<span class="rank-count s">25</span>' not in h)
chk('no stale j=22',                 '<span class="rank-count j">22</span>' not in h)
chk('digitcode gamestats',           'game=digitcode" target="_blank" rel="noopener">ディジットコード' in h)
chk('coffeerush gamestats',          'game=coffeerush" target="_blank" rel="noopener">コーヒーラッシュ' in h)
chk('dewan gamestats',               'game=dewan" target="_blank" rel="noopener">デワン' in h)
chk('dinos gamestats',               'game=diggingfordinos" target="_blank" rel="noopener">ディギング・フォー・ダイノス' in h)
# 棒グラフ
chk('10min s=3 60px',                '<!-- 10分: s=3(60px), a=2(40px), j=2(40px) -->' in h)
chk('20min j=12 240px',              '<!-- 20分: s=14(280px), a=10(200px), j=12(240px) -->' in h)
chk('30min j=4 80px',                '<!-- 30分: s=1(20px), a=7(140px), j=4(80px) -->' in h)
chk('no bar over 280px',             'height:300px;background' not in h)
chk('scale still 14 (yaxis)',        h.count('<span class="pt-yl">') == 7 and '<span class="pt-yl">14</span>' in h)
chk('barzone still 300px',           'height: 300px; position: relative;' in h)
# 棒グラフ勝利数合計 = プレイヤー1位数
def bar_sum(cls, h):
    return sum(int(x) for x in re.findall(r'pt-bar '+cls+r'[^>]*title="[^"]*: (\d+)勝"', h))
chk('bar sum sasuken=27',            bar_sum('bar-s', h) == 27)
chk('bar sum aohige=39',             bar_sum('bar-a', h) == 39)
chk('bar sum Jin=24',                bar_sum('bar-j', h) == 24)
# X軸
chk('xaxis 10min 4titles',           'ディギング・フォー・ダイノス">4タイトル' in h)
chk('xaxis 20min 21titles',          'クィブルス / デワン">21タイトル' in h)
chk('xaxis 30min 8titles',           'ポンドスケープ / コーヒーラッシュ">8タイトル' in h)
# 履歴
chk('row#1 digitcode today',         '<td>1</td><td class="date">2026-09-04<br>（本日）</td>' in main_h)
chk('row#4 dinos today',             '<td>4</td><td class="date">2026-09-04<br>（本日）</td>' in main_h)
chk('row#5 = former#1 (08-26)',      '<td>5</td><td class="date">2026-08-26<br>（9日前）</td>' in main_h)
chk('digit tie two b2',              main_h.count('<span class="p-j">Jin2798</span><span class="score">0pt</span>') == 1)
main_rows = len(re.findall(r'<td>\d+</td><td class="date">', main_h))
chk(f'88 main history rows (found {main_rows})', main_rows == 88)
four_rows = len(re.findall(r'<td>\d+</td><td class="date">', rest_h[rest_h.index('/tab-shinken'):]))
chk(f'post-shinken rows unchanged=4 (found {four_rows})', four_rows == 4)
chk('shinken still 2 rows',          h.count('class="shinken-num"') == 2)
chk('relative date 08-26 = 9日前',   '2026-08-26<br>（9日前）' in h)

print(f'\nResult: {ok} OK / {ng} NG')
