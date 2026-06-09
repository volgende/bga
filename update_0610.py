import re
from datetime import date, datetime

path = r"bga_results.html"
with open(path, encoding='utf-8') as f:
    html = f.read()

today = date(2026, 6, 10)

# ── 1. ヘッダー日付更新 ──
html = html.replace('2026-05-27 集計', '2026-06-10 集計')

# ── 2. 相対日付の更新 ──
def upd_date(m):
    d = datetime.strptime(m.group(1), '%Y-%m-%d').date()
    n = (today - d).days
    label = '本日' if n == 0 else f'{n}日前'
    return f'<td class="date">{m.group(1)}<br>（{label}）</td>'
html = re.sub(r'<td class="date">(\d{4}-\d{2}-\d{2})<br>（[^）]+）</td>', upd_date, html)

# ── 3. プレイヤーカード更新 ──
# sasuken: 1位 13→15
html = html.replace('<span class="rank-count s">13</span>', '<span class="rank-count s">15</span>')
# sasuken: 3位 13→15
html = html.replace('<span class="rank-count c3">13</span>', '<span class="rank-count c3">15</span>')
# aohige: 1位 24→25
html = html.replace('<span class="rank-count a">24</span>', '<span class="rank-count a">25</span>')
# aohige: 2位 13→15
html = html.replace('<span class="rank-count c2">13</span>', '<span class="rank-count c2">15</span>')
# aohige: 3位 11→12
html = html.replace('<span class="rank-count c3">11</span>', '<span class="rank-count c3">12</span>')
# Jin: 1位 11→12
html = html.replace('<span class="rank-count j">11</span>', '<span class="rank-count j">12</span>')
# Jin: 2位 19→21
html = html.replace('<span class="rank-count c2">19</span>', '<span class="rank-count c2">21</span>')
# Jin: 3位 18→19
html = html.replace('<span class="rank-count c3">18</span>', '<span class="rank-count c3">19</span>')
# 総対戦数 48→52
html = html.replace('<div class="card-sub">48戦中</div>', '<div class="card-sub">52戦中</div>')
html = html.replace('<div class="total-num">48</div>', '<div class="total-num">52</div>')

# ── 4. ゲーム別成績: 新ゲーム3タイトルを先頭に追加 ──
new_game_rows = (
    '      <tr>\n'
    '        <td><a href="https://boardgamearena.com/gamepanel?game=explodingkittens" target="_blank" rel="noopener">こねこばくはつ</a><br>'
    '<span style="font-weight:400;color:#999;font-size:.75rem">Exploding Kittens</span></td>\n'
    '        <td>2</td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num s">2</span><div class="bar-bg"><div class="bar-fill bar-s" style="width:100%"></div></div></div></td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num a">0</span><div class="bar-bg"></div></div></td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num j">0</span><div class="bar-bg"></div></div></td>\n'
    '      </tr>\n'
    '      <tr>\n'
    '        <td><a href="https://boardgamearena.com/gamepanel?game=parks" target="_blank" rel="noopener">パークス:第二版</a><br>'
    '<span style="font-weight:400;color:#999;font-size:.75rem">Parks</span></td>\n'
    '        <td>1</td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num s">0</span><div class="bar-bg"></div></div></td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num a">0</span><div class="bar-bg"></div></div></td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num j">1</span><div class="bar-bg"><div class="bar-fill bar-j" style="width:100%"></div></div></div></td>\n'
    '      </tr>\n'
    '      <tr>\n'
    '        <td><a href="https://boardgamearena.com/gamepanel?game=forestshuffledartmoor" target="_blank" rel="noopener">フォレストシャッフル:ダートムーア</a><br>'
    '<span style="font-weight:400;color:#999;font-size:.75rem">Forest Shuffle: Dartmoor</span></td>\n'
    '        <td>1</td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num s">0</span><div class="bar-bg"></div></div></td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num a">1</span><div class="bar-bg"><div class="bar-fill bar-a" style="width:100%"></div></div></div></td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num j">0</span><div class="bar-bg"></div></div></td>\n'
    '      </tr>\n'
)
html = html.replace(
    '    <tbody>\n'
    '      <tr>\n'
    '        <td><a href="https://boardgamearena.com/gamepanel?game=diceforge"',
    '    <tbody>\n'
    + new_game_rows +
    '      <tr>\n'
    '        <td><a href="https://boardgamearena.com/gamepanel?game=diceforge"'
)

# ── 5. 棒グラフ更新 ──
# 20分: s=7(140px)→s=9(180px)
html = html.replace(
    '            <!-- 20分: s=7(140px), a=4(80px), j=7(140px) -->\n'
    '            <div class="pt-group">\n'
    '              <div class="pt-bar bar-s" style="height:140px;background:var(--s)" title="sasuken2999: 7勝"><span class="pt-n">7</span></div>\n'
    '              <div class="pt-bar bar-a" style="height:80px;background:var(--a)" title="aohige nagoya: 4勝"><span class="pt-n">4</span></div>\n'
    '              <div class="pt-bar bar-j" style="height:140px;background:var(--j)" title="Jin2798: 7勝"><span class="pt-n">7</span></div>\n'
    '            </div>',
    '            <!-- 20分: s=9(180px), a=4(80px), j=7(140px) -->\n'
    '            <div class="pt-group">\n'
    '              <div class="pt-bar bar-s" style="height:180px;background:var(--s)" title="sasuken2999: 9勝"><span class="pt-n">9</span></div>\n'
    '              <div class="pt-bar bar-a" style="height:80px;background:var(--a)" title="aohige nagoya: 4勝"><span class="pt-n">4</span></div>\n'
    '              <div class="pt-bar bar-j" style="height:140px;background:var(--j)" title="Jin2798: 7勝"><span class="pt-n">7</span></div>\n'
    '            </div>'
)

# 30分: a=4(80px)→a=5(100px)
html = html.replace(
    '            <!-- 30分: s=1(20px), a=4(80px), j=1(20px) -->\n'
    '            <div class="pt-group">\n'
    '              <div class="pt-bar bar-s" style="height:20px;background:var(--s)" title="sasuken2999: 1勝"><span class="pt-n">1</span></div>\n'
    '              <div class="pt-bar bar-a" style="height:80px;background:var(--a)" title="aohige nagoya: 4勝"><span class="pt-n">4</span></div>\n'
    '              <div class="pt-bar bar-j" style="height:20px;background:var(--j)" title="Jin2798: 1勝"><span class="pt-n">1</span></div>\n'
    '            </div>',
    '            <!-- 30分: s=1(20px), a=5(100px), j=1(20px) -->\n'
    '            <div class="pt-group">\n'
    '              <div class="pt-bar bar-s" style="height:20px;background:var(--s)" title="sasuken2999: 1勝"><span class="pt-n">1</span></div>\n'
    '              <div class="pt-bar bar-a" style="height:100px;background:var(--a)" title="aohige nagoya: 5勝"><span class="pt-n">5</span></div>\n'
    '              <div class="pt-bar bar-j" style="height:20px;background:var(--j)" title="Jin2798: 1勝"><span class="pt-n">1</span></div>\n'
    '            </div>'
)

# 40分: j=1(20px)→j=2(40px)
html = html.replace(
    '            <!-- 40分: s=3(60px), a=2(40px), j=1(20px) -->\n'
    '            <div class="pt-group">\n'
    '              <div class="pt-bar bar-s" style="height:60px;background:var(--s)" title="sasuken2999: 3勝"><span class="pt-n">3</span></div>\n'
    '              <div class="pt-bar bar-a" style="height:40px;background:var(--a)" title="aohige nagoya: 2勝"><span class="pt-n">2</span></div>\n'
    '              <div class="pt-bar bar-j" style="height:20px;background:var(--j)" title="Jin2798: 1勝"><span class="pt-n">1</span></div>\n'
    '            </div>',
    '            <!-- 40分: s=3(60px), a=2(40px), j=2(40px) -->\n'
    '            <div class="pt-group">\n'
    '              <div class="pt-bar bar-s" style="height:60px;background:var(--s)" title="sasuken2999: 3勝"><span class="pt-n">3</span></div>\n'
    '              <div class="pt-bar bar-a" style="height:40px;background:var(--a)" title="aohige nagoya: 2勝"><span class="pt-n">2</span></div>\n'
    '              <div class="pt-bar bar-j" style="height:40px;background:var(--j)" title="Jin2798: 2勝"><span class="pt-n">2</span></div>\n'
    '            </div>'
)

# ── 6. X軸ラベル更新 ──
# 20分: 12→13タイトル (こねこばくはつ追加)
html = html.replace(
    '<span class="pt-xg" title="タクタ / シャーロック13 / レフュージ / スシゴー! / アップ・オア・ダウン? / フリップ7 / スカルキング / マウンテンゴーツ / オリフラム / ドラフトサウルス / キャプテン・フリップ / イプソ">12タイトル ▴</span>',
    '<span class="pt-xg" title="タクタ / シャーロック13 / レフュージ / スシゴー! / アップ・オア・ダウン? / フリップ7 / スカルキング / マウンテンゴーツ / オリフラム / ドラフトサウルス / キャプテン・フリップ / イプソ / こねこばくはつ">13タイトル ▴</span>'
)
# 30分: 4→5タイトル (フォレストシャッフル:ダートムーア追加)
html = html.replace(
    '<span class="pt-xg" title="世界の七不思議 / キャッスルコンボ / アクロポリス / ブラッディイン">4タイトル ▴</span>',
    '<span class="pt-xg" title="世界の七不思議 / キャッスルコンボ / アクロポリス / ブラッディイン / フォレストシャッフル:ダートムーア">5タイトル ▴</span>'
)
# 40分: 3→4タイトル (パークス:第二版追加)
html = html.replace(
    '<span class="pt-xg" title="ファイブ・トライブズ / リビング・フォレスト / ダイスフォージ">3タイトル ▴</span>',
    '<span class="pt-xg" title="ファイブ・トライブズ / リビング・フォレスト / ダイスフォージ / パークス:第二版">4タイトル ▴</span>'
)

# ── 7. 履歴行番号シフト 48→52, ..., 1→5 ──
for i in range(48, 0, -1):
    html = html.replace(
        f'<td>{i}</td><td class="date">',
        f'<td>{i+4}</td><td class="date">'
    )

# ── 8. 新規履歴行4行を先頭に挿入 ──
new_rows = (
    '\n'
    '      <tr>\n'
    '        <td>1</td><td class="date">2026-06-10<br>（本日）</td>\n'
    '        <td class="game-name"><a href="https://boardgamearena.com/gamepanel?game=explodingkittens" target="_blank" rel="noopener">こねこばくはつ</a><br>'
    '<span style="font-weight:400;color:#999;font-size:.78rem">Exploding Kittens</span></td>\n'
    '        <td class="pt-time">20</td>\n'
    '        <td><div class="rank">\n'
    '          <div class="rrow"><span class="badge b1">1位</span><span class="p-s">sasuken2999</span><span class="score">3pt</span></div>\n'
    '          <div class="rrow"><span class="badge b2">2位</span><span class="p-a">aohige nagoya</span><span class="score">2pt</span></div>\n'
    '          <div class="rrow"><span class="badge b3">3位</span><span class="p-j">Jin2798</span><span class="score">1pt</span></div>\n'
    '        </div></td>\n'
    '      </tr>\n'
    '\n'
    '      <tr>\n'
    '        <td>2</td><td class="date">2026-06-10<br>（本日）</td>\n'
    '        <td class="game-name"><a href="https://boardgamearena.com/gamepanel?game=parks" target="_blank" rel="noopener">パークス:第二版</a><br>'
    '<span style="font-weight:400;color:#999;font-size:.78rem">Parks</span></td>\n'
    '        <td class="pt-time">40</td>\n'
    '        <td><div class="rank">\n'
    '          <div class="rrow"><span class="badge b1">1位</span><span class="p-j">Jin2798</span><span class="score">70pt</span></div>\n'
    '          <div class="rrow"><span class="badge b2">2位</span><span class="p-a">aohige nagoya</span><span class="score">43pt</span></div>\n'
    '          <div class="rrow"><span class="badge b3">3位</span><span class="p-s">sasuken2999</span><span class="score">41pt</span></div>\n'
    '        </div></td>\n'
    '      </tr>\n'
    '\n'
    '      <tr>\n'
    '        <td>3</td><td class="date">2026-06-10<br>（本日）</td>\n'
    '        <td class="game-name"><a href="https://boardgamearena.com/gamepanel?game=forestshuffledartmoor" target="_blank" rel="noopener">フォレストシャッフル:ダートムーア</a><br>'
    '<span style="font-weight:400;color:#999;font-size:.78rem">Forest Shuffle: Dartmoor</span></td>\n'
    '        <td class="pt-time">30</td>\n'
    '        <td><div class="rank">\n'
    '          <div class="rrow"><span class="badge b1">1位</span><span class="p-a">aohige nagoya</span><span class="score">121pt</span></div>\n'
    '          <div class="rrow"><span class="badge b2">2位</span><span class="p-j">Jin2798</span><span class="score">79pt</span></div>\n'
    '          <div class="rrow"><span class="badge b3">3位</span><span class="p-s">sasuken2999</span><span class="score">73pt</span></div>\n'
    '        </div></td>\n'
    '      </tr>\n'
    '\n'
    '      <tr>\n'
    '        <td>4</td><td class="date">2026-06-10<br>（本日）</td>\n'
    '        <td class="game-name"><a href="https://boardgamearena.com/gamepanel?game=explodingkittens" target="_blank" rel="noopener">こねこばくはつ</a><br>'
    '<span style="font-weight:400;color:#999;font-size:.78rem">Exploding Kittens</span></td>\n'
    '        <td class="pt-time">20</td>\n'
    '        <td><div class="rank">\n'
    '          <div class="rrow"><span class="badge b1">1位</span><span class="p-s">sasuken2999</span><span class="score">3pt</span></div>\n'
    '          <div class="rrow"><span class="badge b2">2位</span><span class="p-j">Jin2798</span><span class="score">2pt</span></div>\n'
    '          <div class="rrow"><span class="badge b3">3位</span><span class="p-a">aohige nagoya</span><span class="score">1pt</span></div>\n'
    '        </div></td>\n'
    '      </tr>\n'
    '\n'
)
html = html.replace(
    '    <tbody>\n\n      <tr>\n        <td>5</td><td class="date">2026-05-27<br>（14日前）</td>',
    '    <tbody>\n' + new_rows + '      <tr>\n        <td>5</td><td class="date">2026-05-27<br>（14日前）</td>'
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

chk('header 2026-06-10',          '2026-06-10 集計' in h)
chk('total-num 52',                '<div class="total-num">52</div>' in h)
chk('card-sub 52 x3',             h.count('<div class="card-sub">52戦中</div>') == 3)
chk('sasuken s=15',               '<span class="rank-count s">15</span>' in h)
chk('sasuken c2=22',              '<span class="rank-count c2">22</span>' in h)
chk('sasuken c3=15',              '<span class="rank-count c3">15</span>' in h)
chk('aohige a=25',                '<span class="rank-count a">25</span>' in h)
chk('aohige c2=15',               '<span class="rank-count c2">15</span>' in h)
chk('aohige c3=12',               '<span class="rank-count c3">12</span>' in h)
chk('Jin j=12',                   '<span class="rank-count j">12</span>' in h)
chk('Jin c2=21',                  '<span class="rank-count c2">21</span>' in h)
chk('Jin c3=19',                  '<span class="rank-count c3">19</span>' in h)
chk('explodingkittens in gamestats','game=explodingkittens' in h)
chk('parks in gamestats',         'game=parks' in h)
chk('forestshuffledartmoor in gamestats','game=forestshuffledartmoor' in h)
chk('20min s=9 180px',            '<!-- 20分: s=9(180px), a=4(80px), j=7(140px) -->' in h)
chk('30min a=5 100px',            '<!-- 30分: s=1(20px), a=5(100px), j=1(20px) -->' in h)
chk('40min j=2 40px',             '<!-- 40分: s=3(60px), a=2(40px), j=2(40px) -->' in h)
chk('20min 13titles',             '13タイトル' in h and 'こねこばくはつ' in h)
chk('30min 5titles',              '5タイトル' in h and 'フォレストシャッフル:ダートムーア' in h)
chk('40min 4titles',              '4タイトル' in h and 'パークス:第二版' in h)
chk('row#1 explodingkittens today','<td>1</td><td class="date">2026-06-10<br>（本日）</td>' in h)
chk('row#2 parks today',          '<td>2</td><td class="date">2026-06-10<br>（本日）</td>' in h)
chk('row#3 forestshuffle today',  '<td>3</td><td class="date">2026-06-10<br>（本日）</td>' in h)
chk('row#4 explodingkittens today','<td>4</td><td class="date">2026-06-10<br>（本日）</td>' in h)
chk('row#5 = former#1 diceforge', '<td>5</td><td class="date">2026-05-27<br>（14日前）</td>' in h)
row_count = len(__import__('re').findall(r'<td>\d+</td><td class="date">', h))
chk(f'52 history rows (found {row_count})', row_count == 52)
chk('no old header date',         '2026-05-27 集計' not in h)
chk('no 48 total',                '<div class="total-num">48</div>' not in h)

print(f'\nResult: {ok} OK / {ng} NG')
