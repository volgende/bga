import re
from datetime import date, datetime

path = r"bga_results.html"
with open(path, encoding='utf-8') as f:
    html = f.read()

today = date(2026, 8, 19)

# ── 1. ヘッダー日付更新 ──
html = html.replace('2026-08-12 集計', '2026-08-19 集計')

# ── 2. 相対日付の更新（全タブ対象） ──
def upd_date(m):
    d = datetime.strptime(m.group(1), '%Y-%m-%d').date()
    n = (today - d).days
    label = '本日' if n == 0 else f'{n}日前'
    return f'<td class="date">{m.group(1)}<br>（{label}）</td>'
html = re.sub(r'<td class="date">(\d{4}-\d{2}-\d{2})<br>（[^）]+）</td>', upd_date, html)

# ── 3. プレイヤーカード更新（メイン集計、ツォルキン1回目は除外） ──
# メイン +2戦: 郵便馬車(a1/j2/s3), ツォルキン2回目(j1/a2/s3)
# 現在 sasuken 23/32/22, aohige 37/23/17, Jin 19/28/30  →  23/32/24, 38/24/17, 20/29/30
# sasuken: 3位 22→24 (郵便馬車3位, ツォルキン2回目3位)
html = html.replace('<span class="rank-count c3">22</span>', '<span class="rank-count c3">24</span>')  # sasuken c3
# aohige: 1位 37→38 (郵便馬車), 2位 23→24 (ツォルキン2回目2位)
html = html.replace('<span class="rank-count a">37</span>', '<span class="rank-count a">38</span>')
html = html.replace('<span class="rank-count c2">23</span>', '<span class="rank-count c2">24</span>')  # aohige c2
# Jin: 1位 19→20 (ツォルキン2回目), 2位 28→29 (郵便馬車2位)
html = html.replace('<span class="rank-count j">19</span>', '<span class="rank-count j">20</span>')
html = html.replace('<span class="rank-count c2">28</span>', '<span class="rank-count c2">29</span>')  # Jin c2
# 総対戦数 77→79
html = html.replace('<div class="card-sub">77戦中</div>', '<div class="card-sub">79戦中</div>')
html = html.replace('<div class="total-num">77</div>', '<div class="total-num">79</div>')

# ── 4. ゲーム別成績: 新ゲーム2タイトルを先頭に追加（ツォルキンはメイン=2回目のみ1戦） ──
new_game_rows = (
    '      <tr>\n'
    '        <td><a href="https://boardgamearena.com/gamepanel?game=thurnandtaxis" target="_blank" rel="noopener">郵便馬車</a><br>'
    '<span style="font-weight:400;color:#999;font-size:.75rem">Thurn and Taxis</span></td>\n'
    '        <td>1</td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num s">0</span><div class="bar-bg"></div></div></td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num a">1</span><div class="bar-bg"><div class="bar-fill bar-a" style="width:100%"></div></div></div></td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num j">0</span><div class="bar-bg"></div></div></td>\n'
    '      </tr>\n'
    '      <tr>\n'
    '        <td><a href="https://boardgamearena.com/gamepanel?game=tzolkin" target="_blank" rel="noopener">ツォルキン: マヤ神聖歴</a><br>'
    '<span style="font-weight:400;color:#999;font-size:.75rem">Tzolk\'in</span></td>\n'
    '        <td>1</td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num s">0</span><div class="bar-bg"></div></div></td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num a">0</span><div class="bar-bg"></div></div></td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num j">1</span><div class="bar-bg"><div class="bar-fill bar-j" style="width:100%"></div></div></div></td>\n'
    '      </tr>\n'
)
html = html.replace(
    '    <tbody>\n'
    '      <tr>\n'
    '        <td><a href="https://boardgamearena.com/gamepanel?game=wondrouscreatures"',
    '    <tbody>\n'
    + new_game_rows +
    '      <tr>\n'
    '        <td><a href="https://boardgamearena.com/gamepanel?game=wondrouscreatures"'
)

# ── 5. 棒グラフ更新 ──
# 5a. 20分: a=9(180px) → a=10(200px) (郵便馬車でaohige 1位)
html = html.replace(
    '            <!-- 20分: s=12(240px), a=9(180px), j=10(200px) -->\n'
    '            <div class="pt-group">\n'
    '              <div class="pt-bar bar-s" style="height:240px;background:var(--s)" title="sasuken2999: 12勝"><span class="pt-n">12</span></div>\n'
    '              <div class="pt-bar bar-a" style="height:180px;background:var(--a)" title="aohige nagoya: 9勝"><span class="pt-n">9</span></div>\n'
    '              <div class="pt-bar bar-j" style="height:200px;background:var(--j)" title="Jin2798: 10勝"><span class="pt-n">10</span></div>\n'
    '            </div>',
    '            <!-- 20分: s=12(240px), a=10(200px), j=10(200px) -->\n'
    '            <div class="pt-group">\n'
    '              <div class="pt-bar bar-s" style="height:240px;background:var(--s)" title="sasuken2999: 12勝"><span class="pt-n">12</span></div>\n'
    '              <div class="pt-bar bar-a" style="height:200px;background:var(--a)" title="aohige nagoya: 10勝"><span class="pt-n">10</span></div>\n'
    '              <div class="pt-bar bar-j" style="height:200px;background:var(--j)" title="Jin2798: 10勝"><span class="pt-n">10</span></div>\n'
    '            </div>'
)

# 5b. 30分: j=1(20px) → j=2(40px) (ツォルキン2回目でJin 1位)
html = html.replace(
    '            <!-- 30分: s=1(20px), a=6(120px), j=1(20px) -->\n'
    '            <div class="pt-group">\n'
    '              <div class="pt-bar bar-s" style="height:20px;background:var(--s)" title="sasuken2999: 1勝"><span class="pt-n">1</span></div>\n'
    '              <div class="pt-bar bar-a" style="height:120px;background:var(--a)" title="aohige nagoya: 6勝"><span class="pt-n">6</span></div>\n'
    '              <div class="pt-bar bar-j" style="height:20px;background:var(--j)" title="Jin2798: 1勝"><span class="pt-n">1</span></div>\n'
    '            </div>',
    '            <!-- 30分: s=1(20px), a=6(120px), j=2(40px) -->\n'
    '            <div class="pt-group">\n'
    '              <div class="pt-bar bar-s" style="height:20px;background:var(--s)" title="sasuken2999: 1勝"><span class="pt-n">1</span></div>\n'
    '              <div class="pt-bar bar-a" style="height:120px;background:var(--a)" title="aohige nagoya: 6勝"><span class="pt-n">6</span></div>\n'
    '              <div class="pt-bar bar-j" style="height:40px;background:var(--j)" title="Jin2798: 2勝"><span class="pt-n">2</span></div>\n'
    '            </div>'
)

# ── 6. X軸ラベル ──
# 20分: 18→19タイトル (郵便馬車追加)
html = html.replace(
    '<span class="pt-xg" title="タクタ / シャーロック13 / レフュージ / スシゴー! / アップ・オア・ダウン? / フリップ7 / スカルキング / マウンテンゴーツ / オリフラム / ドラフトサウルス / キャプテン・フリップ / イプソ / こねこばくはつ / 宵と暁の呪文書 / シフティング・ストーンズ / ストーンエイジ / 天下鳴動 / ベジタブルストック">18タイトル ▴</span>',
    '<span class="pt-xg" title="タクタ / シャーロック13 / レフュージ / スシゴー! / アップ・オア・ダウン? / フリップ7 / スカルキング / マウンテンゴーツ / オリフラム / ドラフトサウルス / キャプテン・フリップ / イプソ / こねこばくはつ / 宵と暁の呪文書 / シフティング・ストーンズ / ストーンエイジ / 天下鳴動 / ベジタブルストック / 郵便馬車">19タイトル ▴</span>'
)
# 30分: 5→6タイトル (ツォルキン追加)
html = html.replace(
    '<span class="pt-xg" title="世界の七不思議 / キャッスルコンボ / アクロポリス / ブラッディイン / フォレストシャッフル:ダートムーア">5タイトル ▴</span>',
    '<span class="pt-xg" title="世界の七不思議 / キャッスルコンボ / アクロポリス / ブラッディイン / フォレストシャッフル:ダートムーア / ツォルキン: マヤ神聖歴">6タイトル ▴</span>'
)

# ── 7. 初見ゲームセクション: ツォルキン1回目を先頭に追加（メイン集計から除外） ──
# 既存ダーウィンズ shinken-num 1 → 2
html = html.replace('<td class="shinken-num">1</td>', '<td class="shinken-num">2</td>')
# 先頭に新規行を挿入（tbody直後）
shinken_new = (
    '\n'
    '      <tr>\n'
    '        <td class="shinken-num">1</td><td class="date">2026-08-19<br>（本日）</td>\n'
    '        <td class="game-name"><a href="https://boardgamearena.com/gamepanel?game=tzolkin" target="_blank" rel="noopener">ツォルキン: マヤ神聖歴</a><br>'
    '<span style="font-weight:400;color:#999;font-size:.78rem">Tzolk\'in</span></td>\n'
    '        <td><div class="rank">\n'
    '          <div class="rrow"><span class="badge b1">1位</span><span class="p-a">aohige nagoya</span><span class="score">1pt</span></div>\n'
    '          <div class="rrow"><span class="badge b1">1位</span><span class="p-j">Jin2798</span><span class="score">1pt</span></div>\n'
    '          <div class="rrow"><span class="badge b2">2位</span><span class="p-s">sasuken2999</span><span class="score">0pt</span></div>\n'
    '        </div></td>\n'
    '      </tr>\n'
)
html = html.replace(
    '      <tr><th>#</th><th>日時</th><th>ゲーム</th><th>結果（順位・スコア）</th></tr>\n'
    '    </thead>\n'
    '    <tbody>\n'
    '\n'
    '      <tr>\n'
    '        <td class="shinken-num">2</td><td class="date">2026-05-27',
    '      <tr><th>#</th><th>日時</th><th>ゲーム</th><th>結果（順位・スコア）</th></tr>\n'
    '    </thead>\n'
    '    <tbody>\n'
    + shinken_new +
    '\n'
    '      <tr>\n'
    '        <td class="shinken-num">2</td><td class="date">2026-05-27'
)

# ── 8-9. メイン履歴シフト＋新規行挿入（メインタブ限定） ──
marker = '</div><!-- /tab-main -->'
idx = html.index(marker)
main_part, rest_part = html[:idx], html[idx:]

# 8. 行番号シフト 77→79, ..., 1→3
for i in range(77, 0, -1):
    main_part = main_part.replace(
        f'<td>{i}</td><td class="date">',
        f'<td>{i+2}</td><td class="date">'
    )

# 9. 新規履歴行2行を先頭に挿入（新しい順: 郵便馬車→ツォルキン2回目）
new_rows = (
    '\n'
    '      <tr>\n'
    '        <td>1</td><td class="date">2026-08-19<br>（本日）</td>\n'
    '        <td class="game-name"><a href="https://boardgamearena.com/gamepanel?game=thurnandtaxis" target="_blank" rel="noopener">郵便馬車</a><br>'
    '<span style="font-weight:400;color:#999;font-size:.78rem">Thurn and Taxis</span></td>\n'
    '        <td class="pt-time">20</td>\n'
    '        <td><div class="rank">\n'
    '          <div class="rrow"><span class="badge b1">1位</span><span class="p-a">aohige nagoya</span><span class="score">18pt</span></div>\n'
    '          <div class="rrow"><span class="badge b2">2位</span><span class="p-j">Jin2798</span><span class="score">5pt</span></div>\n'
    '          <div class="rrow"><span class="badge b3">3位</span><span class="p-s">sasuken2999</span><span class="score">-9pt</span></div>\n'
    '        </div></td>\n'
    '      </tr>\n'
    '\n'
    '      <tr>\n'
    '        <td>2</td><td class="date">2026-08-19<br>（本日）</td>\n'
    '        <td class="game-name"><a href="https://boardgamearena.com/gamepanel?game=tzolkin" target="_blank" rel="noopener">ツォルキン: マヤ神聖歴</a><br>'
    '<span style="font-weight:400;color:#999;font-size:.78rem">Tzolk\'in</span></td>\n'
    '        <td class="pt-time">30</td>\n'
    '        <td><div class="rank">\n'
    '          <div class="rrow"><span class="badge b1">1位</span><span class="p-j">Jin2798</span><span class="score">66pt</span></div>\n'
    '          <div class="rrow"><span class="badge b2">2位</span><span class="p-a">aohige nagoya</span><span class="score">44pt</span></div>\n'
    '          <div class="rrow"><span class="badge b3">3位</span><span class="p-s">sasuken2999</span><span class="score">35pt</span></div>\n'
    '        </div></td>\n'
    '      </tr>\n'
    '\n'
)
main_part = main_part.replace(
    '    <tbody>\n\n      <tr>\n        <td>3</td><td class="date">2026-08-12<br>（7日前）</td>',
    '    <tbody>\n' + new_rows + '      <tr>\n        <td>3</td><td class="date">2026-08-12<br>（7日前）</td>'
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
shinken_h = rest_h[rest_h.index('初見ゲーム戦績'):rest_h.index('/tab-shinken')]

ok = ng = 0
def chk(name, cond):
    global ok, ng
    if cond: ok += 1; print(f'OK {name}')
    else:    ng += 1; print(f'NG {name}')

chk('header 2026-08-19',            '2026-08-19 集計' in h)
chk('total-num 79',                  '<div class="total-num">79</div>' in h)
chk('card-sub 79 x3',               h.count('<div class="card-sub">79戦中</div>') == 3)
chk('sasuken s=23',                 '<span class="rank-count s">23</span>' in h)
chk('sasuken c2=32',                '<span class="rank-count c2">32</span>' in h)
chk('sasuken c3=24',                '<span class="rank-count c3">24</span>' in h)
chk('aohige a=38',                  '<span class="rank-count a">38</span>' in h)
chk('aohige c2=24',                 '<span class="rank-count c2">24</span>' in h)
chk('aohige c3=17',                 '<span class="rank-count c3">17</span>' in h)
chk('Jin j=20',                     '<span class="rank-count j">20</span>' in h)
chk('Jin c2=29',                    '<span class="rank-count c2">29</span>' in h)
chk('Jin c3=30',                    '<span class="rank-count c3">30</span>' in h)
chk('sum sasuken 23+32+24=79',      23+32+24 == 79)
chk('sum aohige 38+24+17=79',       38+24+17 == 79)
chk('sum Jin 20+29+30=79',          20+29+30 == 79)
chk('thurnandtaxis in gamestats',   'game=thurnandtaxis" target="_blank" rel="noopener">郵便馬車' in h)
chk('tzolkin in gamestats',         'game=tzolkin" target="_blank" rel="noopener">ツォルキン: マヤ神聖歴' in main_h)
chk('20min a=10 200px',             '<!-- 20分: s=12(240px), a=10(200px), j=10(200px) -->' in h)
chk('30min j=2 40px',               '<!-- 30分: s=1(20px), a=6(120px), j=2(40px) -->' in h)
chk('xaxis 20min 19titles',         '19タイトル' in h and '郵便馬車">19タイトル' in h)
chk('xaxis 30min 6titles',          'ツォルキン: マヤ神聖歴">6タイトル' in h)
# 初見セクション
chk('shinken tzolkin #1',           '<td class="shinken-num">1</td><td class="date">2026-08-19' in shinken_h and 'game=tzolkin' in shinken_h)
chk('shinken darwins #2',           '<td class="shinken-num">2</td>' in shinken_h and 'game=darwinsjourney' in shinken_h)
chk('shinken 2 rows',               shinken_h.count('class="shinken-num"') == 2)
chk('shinken tzolkin tie 1st',      shinken_h.count('<span class="badge b1">1位</span>') == 2)
# メイン履歴
chk('row#1 thurnandtaxis today',    '<td>1</td><td class="date">2026-08-19<br>（本日）</td>' in main_h)
chk('row#2 tzolkin today',          '<td>2</td><td class="date">2026-08-19<br>（本日）</td>' in main_h)
chk('row#3 = former#1 (08-12)',     '<td>3</td><td class="date">2026-08-12<br>（7日前）</td>' in main_h)
main_rows = len(re.findall(r'<td>\d+</td><td class="date">', main_h))
chk(f'79 main history rows (found {main_rows})', main_rows == 79)
# ツォルキン1回目がメイン履歴に無いこと（スコア 0pt の sasuken 2位 = 除外分）
chk('tzolkin 1st NOT in main (only 1 tzolkin row)', main_h.count('game=tzolkin') == 1)
four_rows = len(re.findall(r'<td>\d+</td><td class="date">', rest_h[rest_h.index('/tab-shinken'):]))
chk(f'4-player tab still 4 rows (found {four_rows})', four_rows == 4)
chk('no old header date',           '2026-08-12 集計' not in h)
chk('no 77 total',                  '<div class="total-num">77</div>' not in h)

print(f'\nResult: {ok} OK / {ng} NG')
