import re
from datetime import date, datetime

path = r"bga_results.html"
with open(path, encoding='utf-8') as f:
    html = f.read()

today = date(2026, 7, 9)

# ── 1. ヘッダー日付更新 ──
html = html.replace('2026-07-02 集計', '2026-07-09 集計')

# ── 2. 相対日付の更新 ──
def upd_date(m):
    d = datetime.strptime(m.group(1), '%Y-%m-%d').date()
    n = (today - d).days
    label = '本日' if n == 0 else f'{n}日前'
    return f'<td class="date">{m.group(1)}<br>（{label}）</td>'
html = re.sub(r'<td class="date">(\d{4}-\d{2}-\d{2})<br>（[^）]+）</td>', upd_date, html)

# ── 3. プレイヤーカード更新 ──
# sasuken: 1位 18→19 (ロレンツォ1位)
html = html.replace('<span class="rank-count s">18</span>', '<span class="rank-count s">19</span>')
# sasuken: 2位 26→28 (ストーンエイジ2位 + TM Dice 2位 +2)
html = html.replace('<span class="rank-count c2">26</span>', '<span class="rank-count c2">28</span>')
# aohige: 1位 27→29 (ストーンエイジ1位 + TM Dice 1位同点 +2)
html = html.replace('<span class="rank-count a">27</span>', '<span class="rank-count a">29</span>')
# aohige: 2位 17→18 (ロレンツォ2位 +1)
html = html.replace('<span class="rank-count c2">17</span>', '<span class="rank-count c2">18</span>')
# Jin: 1位 14→15 (TM Dice 1位同点 +1)
html = html.replace('<span class="rank-count j">14</span>', '<span class="rank-count j">15</span>')
# Jin: 3位 23→25 (ストーンエイジ3位 + ロレンツォ3位 +2)
html = html.replace('<span class="rank-count c3">23</span>', '<span class="rank-count c3">25</span>')
# 総対戦数 59→62
html = html.replace('<div class="card-sub">59戦中</div>', '<div class="card-sub">62戦中</div>')
html = html.replace('<div class="total-num">59</div>', '<div class="total-num">62</div>')

# ── 4. ゲーム別成績: 新ゲーム3タイトルを先頭に追加 ──
new_game_rows = (
    '      <tr>\n'
    '        <td><a href="https://boardgamearena.com/gamepanel?game=stoneage" target="_blank" rel="noopener">ストーンエイジ</a><br>'
    '<span style="font-weight:400;color:#999;font-size:.75rem">Stone Age</span></td>\n'
    '        <td>1</td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num s">0</span><div class="bar-bg"></div></div></td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num a">1</span><div class="bar-bg"><div class="bar-fill bar-a" style="width:100%"></div></div></div></td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num j">0</span><div class="bar-bg"></div></div></td>\n'
    '      </tr>\n'
    '      <tr>\n'
    '        <td><a href="https://boardgamearena.com/gamepanel?game=terraformingmarsthedicegame" target="_blank" rel="noopener">テラフォーミング・マーズ:ダイスゲーム</a><br>'
    '<span style="font-weight:400;color:#999;font-size:.75rem">Terraforming Mars: The Dice Game</span></td>\n'
    '        <td>1</td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num s">0</span><div class="bar-bg"></div></div></td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num a">1</span><div class="bar-bg"><div class="bar-fill bar-a" style="width:100%"></div></div></div></td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num j">1</span><div class="bar-bg"><div class="bar-fill bar-j" style="width:100%"></div></div></div></td>\n'
    '      </tr>\n'
    '      <tr>\n'
    '        <td><a href="https://boardgamearena.com/gamepanel?game=lorenzo" target="_blank" rel="noopener">ロレンツォ・イル・マニーフィコ</a><br>'
    '<span style="font-weight:400;color:#999;font-size:.75rem">Lorenzo il Magnifico</span></td>\n'
    '        <td>1</td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num s">1</span><div class="bar-bg"><div class="bar-fill bar-s" style="width:100%"></div></div></div></td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num a">0</span><div class="bar-bg"></div></div></td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num j">0</span><div class="bar-bg"></div></div></td>\n'
    '      </tr>\n'
)
html = html.replace(
    '    <tbody>\n'
    '      <tr>\n'
    '        <td><a href="https://boardgamearena.com/gamepanel?game=shiftingstones"',
    '    <tbody>\n'
    + new_game_rows +
    '      <tr>\n'
    '        <td><a href="https://boardgamearena.com/gamepanel?game=shiftingstones"'
)

# ── 5. 棒グラフ更新 ──
# 20分: a=5(100px)→a=6(120px) (ストーンエイジでaohige 1位)
html = html.replace(
    '            <!-- 20分: s=10(200px), a=5(100px), j=8(160px) -->\n'
    '            <div class="pt-group">\n'
    '              <div class="pt-bar bar-s" style="height:200px;background:var(--s)" title="sasuken2999: 10勝"><span class="pt-n">10</span></div>\n'
    '              <div class="pt-bar bar-a" style="height:100px;background:var(--a)" title="aohige nagoya: 5勝"><span class="pt-n">5</span></div>\n'
    '              <div class="pt-bar bar-j" style="height:160px;background:var(--j)" title="Jin2798: 8勝"><span class="pt-n">8</span></div>\n'
    '            </div>',
    '            <!-- 20分: s=10(200px), a=6(120px), j=8(160px) -->\n'
    '            <div class="pt-group">\n'
    '              <div class="pt-bar bar-s" style="height:200px;background:var(--s)" title="sasuken2999: 10勝"><span class="pt-n">10</span></div>\n'
    '              <div class="pt-bar bar-a" style="height:120px;background:var(--a)" title="aohige nagoya: 6勝"><span class="pt-n">6</span></div>\n'
    '              <div class="pt-bar bar-j" style="height:160px;background:var(--j)" title="Jin2798: 8勝"><span class="pt-n">8</span></div>\n'
    '            </div>'
)

# 40分: s=3(60px)→s=4(80px) (ロレンツォでsasuken 1位)
html = html.replace(
    '            <!-- 40分: s=3(60px), a=2(40px), j=3(60px) -->\n'
    '            <div class="pt-group">\n'
    '              <div class="pt-bar bar-s" style="height:60px;background:var(--s)" title="sasuken2999: 3勝"><span class="pt-n">3</span></div>\n'
    '              <div class="pt-bar bar-a" style="height:40px;background:var(--a)" title="aohige nagoya: 2勝"><span class="pt-n">2</span></div>\n'
    '              <div class="pt-bar bar-j" style="height:60px;background:var(--j)" title="Jin2798: 3勝"><span class="pt-n">3</span></div>\n'
    '            </div>',
    '            <!-- 40分: s=4(80px), a=2(40px), j=3(60px) -->\n'
    '            <div class="pt-group">\n'
    '              <div class="pt-bar bar-s" style="height:80px;background:var(--s)" title="sasuken2999: 4勝"><span class="pt-n">4</span></div>\n'
    '              <div class="pt-bar bar-a" style="height:40px;background:var(--a)" title="aohige nagoya: 2勝"><span class="pt-n">2</span></div>\n'
    '              <div class="pt-bar bar-j" style="height:60px;background:var(--j)" title="Jin2798: 3勝"><span class="pt-n">3</span></div>\n'
    '            </div>'
)

# 50分: a=2(40px)→a=3(60px), j=1(20px)追加 (TM Diceで同点1位 Jin/aohige)
html = html.replace(
    '            <!-- 50分: s=3(60px), a=2(40px) -->\n'
    '            <div class="pt-group">\n'
    '              <div class="pt-bar bar-s" style="height:60px;background:var(--s)" title="sasuken2999: 3勝"><span class="pt-n">3</span></div>\n'
    '              <div class="pt-bar bar-a" style="height:40px;background:var(--a)" title="aohige nagoya: 2勝"><span class="pt-n">2</span></div>\n'
    '            </div>',
    '            <!-- 50分: s=3(60px), a=3(60px), j=1(20px) -->\n'
    '            <div class="pt-group">\n'
    '              <div class="pt-bar bar-s" style="height:60px;background:var(--s)" title="sasuken2999: 3勝"><span class="pt-n">3</span></div>\n'
    '              <div class="pt-bar bar-a" style="height:60px;background:var(--a)" title="aohige nagoya: 3勝"><span class="pt-n">3</span></div>\n'
    '              <div class="pt-bar bar-j" style="height:20px;background:var(--j)" title="Jin2798: 1勝"><span class="pt-n">1</span></div>\n'
    '            </div>'
)

# ── 6. X軸ラベル更新 ──
# 20分: 15→16タイトル (ストーンエイジ追加)
html = html.replace(
    '<span class="pt-xg" title="タクタ / シャーロック13 / レフュージ / スシゴー! / アップ・オア・ダウン? / フリップ7 / スカルキング / マウンテンゴーツ / オリフラム / ドラフトサウルス / キャプテン・フリップ / イプソ / こねこばくはつ / 宵と暁の呪文書 / シフティング・ストーンズ">15タイトル ▴</span>',
    '<span class="pt-xg" title="タクタ / シャーロック13 / レフュージ / スシゴー! / アップ・オア・ダウン? / フリップ7 / スカルキング / マウンテンゴーツ / オリフラム / ドラフトサウルス / キャプテン・フリップ / イプソ / こねこばくはつ / 宵と暁の呪文書 / シフティング・ストーンズ / ストーンエイジ">16タイトル ▴</span>'
)
# 40分: 5→6タイトル (ロレンツォ追加)
html = html.replace(
    '<span class="pt-xg" title="ファイブ・トライブズ / リビング・フォレスト / ダイスフォージ / パークス:第二版 / マルコポーロ2:大いなる帰還">5タイトル ▴</span>',
    '<span class="pt-xg" title="ファイブ・トライブズ / リビング・フォレスト / ダイスフォージ / パークス:第二版 / マルコポーロ2:大いなる帰還 / ロレンツォ・イル・マニーフィコ">6タイトル ▴</span>'
)
# 50分: 3→4タイトル (TM Dice追加)
html = html.replace(
    '<span class="pt-xg" title="チャレンジャーズ! / ダーウィンズ・ジャーニー / アグリコラ">3タイトル ▴</span>',
    '<span class="pt-xg" title="チャレンジャーズ! / ダーウィンズ・ジャーニー / アグリコラ / テラフォーミング・マーズ:ダイスゲーム">4タイトル ▴</span>'
)

# ── 7. 履歴行番号シフト 59→62, ..., 1→4 ──
for i in range(59, 0, -1):
    html = html.replace(
        f'<td>{i}</td><td class="date">',
        f'<td>{i+3}</td><td class="date">'
    )

# ── 8. 新規履歴行3行を先頭に挿入 ──
new_rows = (
    '\n'
    '      <tr>\n'
    '        <td>1</td><td class="date">2026-07-09<br>（本日）</td>\n'
    '        <td class="game-name"><a href="https://boardgamearena.com/gamepanel?game=stoneage" target="_blank" rel="noopener">ストーンエイジ</a><br>'
    '<span style="font-weight:400;color:#999;font-size:.78rem">Stone Age</span></td>\n'
    '        <td class="pt-time">20</td>\n'
    '        <td><div class="rank">\n'
    '          <div class="rrow"><span class="badge b1">1位</span><span class="p-a">aohige nagoya</span><span class="score">236pt</span></div>\n'
    '          <div class="rrow"><span class="badge b2">2位</span><span class="p-s">sasuken2999</span><span class="score">211pt</span></div>\n'
    '          <div class="rrow"><span class="badge b3">3位</span><span class="p-j">Jin2798</span><span class="score">151pt</span></div>\n'
    '        </div></td>\n'
    '      </tr>\n'
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
    '      </tr>\n'
    '\n'
    '      <tr>\n'
    '        <td>3</td><td class="date">2026-07-09<br>（本日）</td>\n'
    '        <td class="game-name"><a href="https://boardgamearena.com/gamepanel?game=lorenzo" target="_blank" rel="noopener">ロレンツォ・イル・マニーフィコ</a><br>'
    '<span style="font-weight:400;color:#999;font-size:.78rem">Lorenzo il Magnifico</span></td>\n'
    '        <td class="pt-time">40</td>\n'
    '        <td><div class="rank">\n'
    '          <div class="rrow"><span class="badge b1">1位</span><span class="p-s">sasuken2999</span><span class="score">70pt</span></div>\n'
    '          <div class="rrow"><span class="badge b2">2位</span><span class="p-a">aohige nagoya</span><span class="score">70pt</span></div>\n'
    '          <div class="rrow"><span class="badge b3">3位</span><span class="p-j">Jin2798</span><span class="score">68pt</span></div>\n'
    '        </div></td>\n'
    '      </tr>\n'
    '\n'
)
html = html.replace(
    '    <tbody>\n\n      <tr>\n        <td>4</td><td class="date">2026-06-30<br>（9日前）</td>',
    '    <tbody>\n' + new_rows + '      <tr>\n        <td>4</td><td class="date">2026-06-30<br>（9日前）</td>'
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
chk('total-num 62',                         '<div class="total-num">62</div>' in h)
chk('card-sub 62 x3',                       h.count('<div class="card-sub">62戦中</div>') == 3)
chk('sasuken s=19',                         '<span class="rank-count s">19</span>' in h)
chk('sasuken c2=28',                        '<span class="rank-count c2">28</span>' in h)
chk('sasuken c3=15',                        '<span class="rank-count c3">15</span>' in h)
chk('aohige a=29',                          '<span class="rank-count a">29</span>' in h)
chk('aohige c2=18',                         '<span class="rank-count c2">18</span>' in h)
chk('aohige c3=15',                         '<span class="rank-count c3">15</span>' in h)
chk('Jin j=15',                             '<span class="rank-count j">15</span>' in h)
chk('Jin c2=22',                            '<span class="rank-count c2">22</span>' in h)
chk('Jin c3=25',                            '<span class="rank-count c3">25</span>' in h)
chk('stoneage in gamestats',                'game=stoneage" target="_blank"' in h)
chk('terraformingmarsthedicegame in gamestats', 'game=terraformingmarsthedicegame' in h)
chk('lorenzo in gamestats',                 'game=lorenzo" target="_blank"' in h)
chk('20min a=6 120px',                      '<!-- 20分: s=10(200px), a=6(120px), j=8(160px) -->' in h)
chk('40min s=4 80px',                       '<!-- 40分: s=4(80px), a=2(40px), j=3(60px) -->' in h)
chk('50min j=1 added',                      '<!-- 50分: s=3(60px), a=3(60px), j=1(20px) -->' in h)
chk('20min 16titles',                       '16タイトル' in h and 'ストーンエイジ' in h)
chk('40min 6titles',                        '6タイトル' in h and 'ロレンツォ' in h)
chk('50min 4titles',                        '4タイトル' in h and 'テラフォーミング・マーズ:ダイスゲーム' in h)
chk('row#1 stoneage today',                 '<td>1</td><td class="date">2026-07-09<br>（本日）</td>' in h)
chk('row#2 tmdice today',                   '<td>2</td><td class="date">2026-07-09<br>（本日）</td>' in h)
chk('row#3 lorenzo today',                  '<td>3</td><td class="date">2026-07-09<br>（本日）</td>' in h)
chk('row#4 = former#1 (06-30 9days)',       '<td>4</td><td class="date">2026-06-30<br>（9日前）</td>' in h)
row_count = len(__import__('re').findall(r'<td>\d+</td><td class="date">', h))
chk(f'62 history rows (found {row_count})', row_count == 62)
chk('no old header date',                   '2026-07-02 集計' not in h)
chk('no 59 total',                          '<div class="total-num">59</div>' not in h)

print(f'\nResult: {ok} OK / {ng} NG')
