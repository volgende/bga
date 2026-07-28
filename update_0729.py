import re
from datetime import date, datetime

path = r"bga_results.html"
with open(path, encoding='utf-8') as f:
    html = f.read()

today = date(2026, 7, 29)

# ── 1. ヘッダー日付更新 ──
html = html.replace('2026-07-21 集計', '2026-07-29 集計')

# ── 2. 相対日付の更新（全タブ対象） ──
def upd_date(m):
    d = datetime.strptime(m.group(1), '%Y-%m-%d').date()
    n = (today - d).days
    label = '本日' if n == 0 else f'{n}日前'
    return f'<td class="date">{m.group(1)}<br>（{label}）</td>'
html = re.sub(r'<td class="date">(\d{4}-\d{2}-\d{2})<br>（[^）]+）</td>', upd_date, html)

# ── 3. プレイヤーカード更新（メイン集計） ──
# 新規3戦: スカルキング(J1/a2/s3), YRO(J1/a2/s3), GWT(s1/J2/a3)
# 現在 sasuken 21/28/17, aohige 31/19/16, Jin 14/25/27  →  22/28/19, 31/21/17, 16/26/27
# sasuken: 1位 21→22 (GWT), 3位 17→19 (スカルキング, YRO)
html = html.replace('<span class="rank-count s">21</span>', '<span class="rank-count s">22</span>')
html = html.replace('<span class="rank-count c3">17</span>', '<span class="rank-count c3">19</span>')  # sasuken c3
# aohige: 2位 19→21 (スカルキング, YRO), 3位 16→17 (GWT)  ※c3=17は上でsasukenを先に処理済み
html = html.replace('<span class="rank-count c2">19</span>', '<span class="rank-count c2">21</span>')  # aohige c2
html = html.replace('<span class="rank-count c3">16</span>', '<span class="rank-count c3">17</span>')  # aohige c3
# Jin: 1位 14→16 (スカルキング, YRO), 2位 25→26 (GWT)
html = html.replace('<span class="rank-count j">14</span>', '<span class="rank-count j">16</span>')
html = html.replace('<span class="rank-count c2">25</span>', '<span class="rank-count c2">26</span>')  # Jin c2
# 総対戦数 66→69
html = html.replace('<div class="card-sub">66戦中</div>', '<div class="card-sub">69戦中</div>')
html = html.replace('<div class="total-num">66</div>', '<div class="total-num">69</div>')

# ── 4. ゲーム別成績 ──
# 4a. 新ゲーム GWT を先頭（rumblenation の前）に追加
gwt_row = (
    '      <tr>\n'
    '        <td><a href="https://boardgamearena.com/gamepanel?game=greatwesterntrail" target="_blank" rel="noopener">グレート・ウエスタン・トレイル</a><br>'
    '<span style="font-weight:400;color:#999;font-size:.75rem">Great Western Trail</span></td>\n'
    '        <td>1</td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num s">1</span><div class="bar-bg"><div class="bar-fill bar-s" style="width:100%"></div></div></div></td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num a">0</span><div class="bar-bg"></div></div></td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num j">0</span><div class="bar-bg"></div></div></td>\n'
    '      </tr>\n'
)
html = html.replace(
    '    <tbody>\n'
    '      <tr>\n'
    '        <td><a href="https://boardgamearena.com/gamepanel?game=rumblenation"',
    '    <tbody>\n'
    + gwt_row +
    '      <tr>\n'
    '        <td><a href="https://boardgamearena.com/gamepanel?game=rumblenation"'
)

# 4b. YRO: 2戦(s1 50% / a1 50% / j0) → 3戦(s1 33% / a1 33% / j1 33%)
html = html.replace(
    '        <td><a href="https://boardgamearena.com/gamepanel?game=yro" target="_blank" rel="noopener">YRO</a><br><span style="font-weight:400;color:#999;font-size:.75rem">YRO</span></td>\n'
    '        <td>2</td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num s">1</span><div class="bar-bg"><div class="bar-fill bar-s" style="width:50%"></div></div></div></td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num a">1</span><div class="bar-bg"><div class="bar-fill bar-a" style="width:50%"></div></div></div></td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num j">0</span><div class="bar-bg"></div></div></td>',
    '        <td><a href="https://boardgamearena.com/gamepanel?game=yro" target="_blank" rel="noopener">YRO</a><br><span style="font-weight:400;color:#999;font-size:.75rem">YRO</span></td>\n'
    '        <td>3</td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num s">1</span><div class="bar-bg"><div class="bar-fill bar-s" style="width:33%"></div></div></div></td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num a">1</span><div class="bar-bg"><div class="bar-fill bar-a" style="width:33%"></div></div></div></td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num j">1</span><div class="bar-bg"><div class="bar-fill bar-j" style="width:33%"></div></div></div></td>'
)

# 4c. スカルキング: 2戦(s0 / a1 50% / j1 50%) → 3戦(s0 / a1 33% / j2 67%)
html = html.replace(
    '        <td><a href="https://boardgamearena.com/gamepanel?game=skullking" target="_blank" rel="noopener">スカルキング</a><br><span style="font-weight:400;color:#999;font-size:.75rem">Skull King</span></td>\n'
    '        <td>2</td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num s">0</span><div class="bar-bg"></div></div></td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num a">1</span><div class="bar-bg"><div class="bar-fill bar-a" style="width:50%"></div></div></div></td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num j">1</span><div class="bar-bg"><div class="bar-fill bar-j" style="width:50%"></div></div></div></td>',
    '        <td><a href="https://boardgamearena.com/gamepanel?game=skullking" target="_blank" rel="noopener">スカルキング</a><br><span style="font-weight:400;color:#999;font-size:.75rem">Skull King</span></td>\n'
    '        <td>3</td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num s">0</span><div class="bar-bg"></div></div></td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num a">1</span><div class="bar-bg"><div class="bar-fill bar-a" style="width:33%"></div></div></div></td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num j">2</span><div class="bar-bg"><div class="bar-fill bar-j" style="width:67%"></div></div></div></td>'
)

# ── 5. 棒グラフ更新 ──
# 5a. 10分: j=1(20px) 追加 (YROでJin 1位)
html = html.replace(
    '            <!-- 10分: s=1(20px), a=1(20px) -->\n'
    '            <div class="pt-group">\n'
    '              <div class="pt-bar bar-s" style="height:20px;background:var(--s)" title="sasuken2999: 1勝"><span class="pt-n">1</span></div>\n'
    '              <div class="pt-bar bar-a" style="height:20px;background:var(--a)" title="aohige nagoya: 1勝"><span class="pt-n">1</span></div>\n'
    '            </div>',
    '            <!-- 10分: s=1(20px), a=1(20px), j=1(20px) -->\n'
    '            <div class="pt-group">\n'
    '              <div class="pt-bar bar-s" style="height:20px;background:var(--s)" title="sasuken2999: 1勝"><span class="pt-n">1</span></div>\n'
    '              <div class="pt-bar bar-a" style="height:20px;background:var(--a)" title="aohige nagoya: 1勝"><span class="pt-n">1</span></div>\n'
    '              <div class="pt-bar bar-j" style="height:20px;background:var(--j)" title="Jin2798: 1勝"><span class="pt-n">1</span></div>\n'
    '            </div>'
)

# 5b. 20分: j=8(160px) → j=9(180px) (スカルキングでJin 1位)
html = html.replace(
    '            <!-- 20分: s=11(220px), a=7(140px), j=8(160px) -->\n'
    '            <div class="pt-group">\n'
    '              <div class="pt-bar bar-s" style="height:220px;background:var(--s)" title="sasuken2999: 11勝"><span class="pt-n">11</span></div>\n'
    '              <div class="pt-bar bar-a" style="height:140px;background:var(--a)" title="aohige nagoya: 7勝"><span class="pt-n">7</span></div>\n'
    '              <div class="pt-bar bar-j" style="height:160px;background:var(--j)" title="Jin2798: 8勝"><span class="pt-n">8</span></div>\n'
    '            </div>',
    '            <!-- 20分: s=11(220px), a=7(140px), j=9(180px) -->\n'
    '            <div class="pt-group">\n'
    '              <div class="pt-bar bar-s" style="height:220px;background:var(--s)" title="sasuken2999: 11勝"><span class="pt-n">11</span></div>\n'
    '              <div class="pt-bar bar-a" style="height:140px;background:var(--a)" title="aohige nagoya: 7勝"><span class="pt-n">7</span></div>\n'
    '              <div class="pt-bar bar-j" style="height:180px;background:var(--j)" title="Jin2798: 9勝"><span class="pt-n">9</span></div>\n'
    '            </div>'
)

# 5c. 60分バケットを新設（50分と80分の間、GWTでsasuken 1位）
html = html.replace(
    '            <!-- 50分: s=3(60px), a=2(40px) -->\n'
    '            <div class="pt-group">\n'
    '              <div class="pt-bar bar-s" style="height:60px;background:var(--s)" title="sasuken2999: 3勝"><span class="pt-n">3</span></div>\n'
    '              <div class="pt-bar bar-a" style="height:40px;background:var(--a)" title="aohige nagoya: 2勝"><span class="pt-n">2</span></div>\n'
    '            </div>\n'
    '            <!-- 80分: j=1(20px) -->',
    '            <!-- 50分: s=3(60px), a=2(40px) -->\n'
    '            <div class="pt-group">\n'
    '              <div class="pt-bar bar-s" style="height:60px;background:var(--s)" title="sasuken2999: 3勝"><span class="pt-n">3</span></div>\n'
    '              <div class="pt-bar bar-a" style="height:40px;background:var(--a)" title="aohige nagoya: 2勝"><span class="pt-n">2</span></div>\n'
    '            </div>\n'
    '            <!-- 60分: s=1(20px) -->\n'
    '            <div class="pt-group">\n'
    '              <div class="pt-bar bar-s" style="height:20px;background:var(--s)" title="sasuken2999: 1勝"><span class="pt-n">1</span></div>\n'
    '            </div>\n'
    '            <!-- 80分: j=1(20px) -->'
)

# ── 6. X軸ラベル: 60分を新設（50分と80分の間） ──
html = html.replace(
    '          <div class="pt-xlabel">\n'
    '            <span class="pt-xl">50分</span>\n'
    '            <span class="pt-xg" title="チャレンジャーズ! / ダーウィンズ・ジャーニー / アグリコラ">3タイトル ▴</span>\n'
    '          </div>\n'
    '          <div class="pt-xlabel">\n'
    '            <span class="pt-xl">80分</span>',
    '          <div class="pt-xlabel">\n'
    '            <span class="pt-xl">50分</span>\n'
    '            <span class="pt-xg" title="チャレンジャーズ! / ダーウィンズ・ジャーニー / アグリコラ">3タイトル ▴</span>\n'
    '          </div>\n'
    '          <div class="pt-xlabel">\n'
    '            <span class="pt-xl">60分</span>\n'
    '            <span class="pt-xg" title="グレート・ウエスタン・トレイル">1タイトル ▴</span>\n'
    '          </div>\n'
    '          <div class="pt-xlabel">\n'
    '            <span class="pt-xl">80分</span>'
)

# ── 7-8. 履歴シフト＋新規行挿入（メインタブ限定） ──
marker = '</div><!-- /tab-main -->'
idx = html.index(marker)
main_part, rest_part = html[:idx], html[idx:]

# 7. 行番号シフト 66→69, ..., 1→4
for i in range(66, 0, -1):
    main_part = main_part.replace(
        f'<td>{i}</td><td class="date">',
        f'<td>{i+3}</td><td class="date">'
    )

# 8. 新規履歴行3行を先頭に挿入（新しい順: スカルキング→YRO→GWT）
new_rows = (
    '\n'
    '      <tr>\n'
    '        <td>1</td><td class="date">2026-07-29<br>（本日）</td>\n'
    '        <td class="game-name"><a href="https://boardgamearena.com/gamepanel?game=skullking" target="_blank" rel="noopener">スカルキング</a><br>'
    '<span style="font-weight:400;color:#999;font-size:.78rem">Skull King</span></td>\n'
    '        <td class="pt-time">20</td>\n'
    '        <td><div class="rank">\n'
    '          <div class="rrow"><span class="badge b1">1位</span><span class="p-j">Jin2798</span><span class="score">460pt</span></div>\n'
    '          <div class="rrow"><span class="badge b2">2位</span><span class="p-a">aohige nagoya</span><span class="score">360pt</span></div>\n'
    '          <div class="rrow"><span class="badge b3">3位</span><span class="p-s">sasuken2999</span><span class="score">280pt</span></div>\n'
    '        </div></td>\n'
    '      </tr>\n'
    '\n'
    '      <tr>\n'
    '        <td>2</td><td class="date">2026-07-29<br>（本日）</td>\n'
    '        <td class="game-name"><a href="https://boardgamearena.com/gamepanel?game=yro" target="_blank" rel="noopener">YRO</a><br>'
    '<span style="font-weight:400;color:#999;font-size:.78rem">YRO</span></td>\n'
    '        <td class="pt-time">10</td>\n'
    '        <td><div class="rank">\n'
    '          <div class="rrow"><span class="badge b1">1位</span><span class="p-j">Jin2798</span><span class="score">45pt</span></div>\n'
    '          <div class="rrow"><span class="badge b2">2位</span><span class="p-a">aohige nagoya</span><span class="score">36pt</span></div>\n'
    '          <div class="rrow"><span class="badge b3">3位</span><span class="p-s">sasuken2999</span><span class="score">34pt</span></div>\n'
    '        </div></td>\n'
    '      </tr>\n'
    '\n'
    '      <tr>\n'
    '        <td>3</td><td class="date">2026-07-29<br>（本日）</td>\n'
    '        <td class="game-name"><a href="https://boardgamearena.com/gamepanel?game=greatwesterntrail" target="_blank" rel="noopener">グレート・ウエスタン・トレイル</a><br>'
    '<span style="font-weight:400;color:#999;font-size:.78rem">Great Western Trail</span></td>\n'
    '        <td class="pt-time">60</td>\n'
    '        <td><div class="rank">\n'
    '          <div class="rrow"><span class="badge b1">1位</span><span class="p-s">sasuken2999</span><span class="score">32pt</span></div>\n'
    '          <div class="rrow"><span class="badge b2">2位</span><span class="p-j">Jin2798</span><span class="score">18pt</span></div>\n'
    '          <div class="rrow"><span class="badge b3">3位</span><span class="p-a">aohige nagoya</span><span class="score">17pt</span></div>\n'
    '        </div></td>\n'
    '      </tr>\n'
    '\n'
)
main_part = main_part.replace(
    '    <tbody>\n\n      <tr>\n        <td>4</td><td class="date">2026-07-21<br>（8日前）</td>',
    '    <tbody>\n' + new_rows + '      <tr>\n        <td>4</td><td class="date">2026-07-21<br>（8日前）</td>'
)

html = main_part + rest_part

with open(path, 'w', encoding='utf-8') as f:
    f.write(html)

print("Done!")

# ── 検証 ──
with open(path, encoding='utf-8') as f:
    h = f.read()

main_h = h[:h.index(marker)]
four_h = h[h.index(marker):]

ok = ng = 0
def chk(name, cond):
    global ok, ng
    if cond: ok += 1; print(f'OK {name}')
    else:    ng += 1; print(f'NG {name}')

chk('header 2026-07-29',            '2026-07-29 集計' in h)
chk('total-num 69',                  '<div class="total-num">69</div>' in h)
chk('card-sub 69 x3',               h.count('<div class="card-sub">69戦中</div>') == 3)
chk('sasuken s=22',                 '<span class="rank-count s">22</span>' in h)
chk('sasuken c2=28',                '<span class="rank-count c2">28</span>' in h)
chk('sasuken c3=19',                '<span class="rank-count c3">19</span>' in h)
chk('aohige a=31',                  '<span class="rank-count a">31</span>' in h)
chk('aohige c2=21',                 '<span class="rank-count c2">21</span>' in h)
chk('aohige c3=17',                 '<span class="rank-count c3">17</span>' in h)
chk('Jin j=16',                     '<span class="rank-count j">16</span>' in h)
chk('Jin c2=26',                    '<span class="rank-count c2">26</span>' in h)
chk('Jin c3=27',                    '<span class="rank-count c3">27</span>' in h)
chk('sum sasuken 22+28+19=69',      22+28+19 == 69)
chk('sum aohige 31+21+17=69',       31+21+17 == 69)
chk('sum Jin 16+26+27=69',          16+26+27 == 69)
chk('gwt in gamestats',             'game=greatwesterntrail" target="_blank" rel="noopener">グレート・ウエスタン・トレイル' in h)
chk('yro plays=3',                  'game=yro" target="_blank" rel="noopener">YRO</a><br><span style="font-weight:400;color:#999;font-size:.75rem">YRO</span></td>\n        <td>3</td>' in h)
chk('skullking plays=3 j=2',        'game=skullking" target="_blank" rel="noopener">スカルキング</a><br><span style="font-weight:400;color:#999;font-size:.75rem">Skull King</span></td>\n        <td>3</td>' in h and '<span class="win-num j">2</span>' in h)
chk('10min j added',                '<!-- 10分: s=1(20px), a=1(20px), j=1(20px) -->' in h)
chk('20min j=9 180px',              '<!-- 20分: s=11(220px), a=7(140px), j=9(180px) -->' in h)
chk('60min bucket added',           '<!-- 60分: s=1(20px) -->' in h)
chk('xaxis 60min label',            '<span class="pt-xl">60分</span>' in h)
chk('xaxis 60min gwt title',        'title="グレート・ウエスタン・トレイル">1タイトル' in h)
chk('row#1 skullking today',        '<td>1</td><td class="date">2026-07-29<br>（本日）</td>' in main_h)
chk('row#3 gwt today',              '<td>3</td><td class="date">2026-07-29<br>（本日）</td>' in main_h)
chk('row#4 = former#1 (07-21)',     '<td>4</td><td class="date">2026-07-21<br>（8日前）</td>' in main_h)
main_rows = len(re.findall(r'<td>\d+</td><td class="date">', main_h))
chk(f'69 main history rows (found {main_rows})', main_rows == 69)
four_rows = len(re.findall(r'<td>\d+</td><td class="date">', four_h))
chk(f'4-player tab still 4 rows (found {four_rows})', four_rows == 4)
chk('4-player total unchanged',     '<div class="total-num" id="f-total">4</div>' in four_h)
chk('no old header date',           '2026-07-21 集計' not in h)
chk('no 66 total',                  '<div class="total-num">66</div>' not in h)

print(f'\nResult: {ok} OK / {ng} NG')
