import re
from datetime import date, datetime

path = r"bga_results.html"
with open(path, encoding='utf-8') as f:
    html = f.read()

today = date(2026, 6, 25)

# ── 1. ヘッダー日付更新 ──
html = html.replace('2026-06-17 集計', '2026-06-25 集計')

# ── 2. 相対日付の更新 ──
def upd_date(m):
    d = datetime.strptime(m.group(1), '%Y-%m-%d').date()
    n = (today - d).days
    label = '本日' if n == 0 else f'{n}日前'
    return f'<td class="date">{m.group(1)}<br>（{label}）</td>'
html = re.sub(r'<td class="date">(\d{4}-\d{2}-\d{2})<br>（[^）]+）</td>', upd_date, html)

# ── 3. プレイヤーカード更新 ──
# sasuken: 1位 15→16
html = html.replace('<span class="rank-count s">15</span>', '<span class="rank-count s">16</span>')
# sasuken: 2位 24→25
html = html.replace('<span class="rank-count c2">24</span>', '<span class="rank-count c2">25</span>')
# aohige: 2位 15→16
html = html.replace('<span class="rank-count c2">15</span>', '<span class="rank-count c2">16</span>')
# aohige: 3位 13→14
html = html.replace('<span class="rank-count c3">13</span>', '<span class="rank-count c3">14</span>')
# Jin: 1位 13→14
html = html.replace('<span class="rank-count j">13</span>', '<span class="rank-count j">14</span>')
# Jin: 3位 20→21
html = html.replace('<span class="rank-count c3">20</span>', '<span class="rank-count c3">21</span>')
# 総対戦数 54→56
html = html.replace('<div class="card-sub">54戦中</div>', '<div class="card-sub">56戦中</div>')
html = html.replace('<div class="total-num">54</div>', '<div class="total-num">56</div>')

# ── 4. ゲーム別成績: 新ゲーム(マルコポーロ2)を先頭に追加、ワイナリーを更新 ──
# 4a. マルコポーロ2を先頭に追加
new_game_row = (
    '      <tr>\n'
    '        <td><a href="https://boardgamearena.com/gamepanel?game=marcopolotwo" target="_blank" rel="noopener">マルコポーロ2:大いなる帰還</a><br>'
    '<span style="font-weight:400;color:#999;font-size:.75rem">Marco Polo II: In the Service of the Khan</span></td>\n'
    '        <td>1</td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num s">0</span><div class="bar-bg"></div></div></td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num a">0</span><div class="bar-bg"></div></div></td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num j">1</span><div class="bar-bg"><div class="bar-fill bar-j" style="width:100%"></div></div></div></td>\n'
    '      </tr>\n'
)
html = html.replace(
    '    <tbody>\n'
    '      <tr>\n'
    '        <td><a href="https://boardgamearena.com/gamepanel?game=spellbook"',
    '    <tbody>\n'
    + new_game_row +
    '      <tr>\n'
    '        <td><a href="https://boardgamearena.com/gamepanel?game=spellbook"'
)

# 4b. ワイナリーの四季: 1試合(a=1,100%) → 2試合(s=1 50%, a=1 50%)
html = html.replace(
    '        <td><a href="https://boardgamearena.com/gamepanel?game=viticulture" target="_blank" rel="noopener">ワイナリーの四季</a><br><span style="font-weight:400;color:#999;font-size:.75rem">Viticulture</span></td>\n'
    '        <td>1</td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num s">0</span><div class="bar-bg"></div></div></td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num a">1</span><div class="bar-bg"><div class="bar-fill bar-a" style="width:100%"></div></div></div></td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num j">0</span><div class="bar-bg"></div></div></td>',
    '        <td><a href="https://boardgamearena.com/gamepanel?game=viticulture" target="_blank" rel="noopener">ワイナリーの四季</a><br><span style="font-weight:400;color:#999;font-size:.75rem">Viticulture</span></td>\n'
    '        <td>2</td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num s">1</span><div class="bar-bg"><div class="bar-fill bar-s" style="width:50%"></div></div></div></td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num a">1</span><div class="bar-bg"><div class="bar-fill bar-a" style="width:50%"></div></div></div></td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num j">0</span><div class="bar-bg"></div></div></td>'
)

# ── 5. 棒グラフ更新 ──
# 40分: j=2(40px)→j=3(60px) (マルコポーロ2でJin 1位)
html = html.replace(
    '            <!-- 40分: s=3(60px), a=2(40px), j=2(40px) -->\n'
    '            <div class="pt-group">\n'
    '              <div class="pt-bar bar-s" style="height:60px;background:var(--s)" title="sasuken2999: 3勝"><span class="pt-n">3</span></div>\n'
    '              <div class="pt-bar bar-a" style="height:40px;background:var(--a)" title="aohige nagoya: 2勝"><span class="pt-n">2</span></div>\n'
    '              <div class="pt-bar bar-j" style="height:40px;background:var(--j)" title="Jin2798: 2勝"><span class="pt-n">2</span></div>\n'
    '            </div>',
    '            <!-- 40分: s=3(60px), a=2(40px), j=3(60px) -->\n'
    '            <div class="pt-group">\n'
    '              <div class="pt-bar bar-s" style="height:60px;background:var(--s)" title="sasuken2999: 3勝"><span class="pt-n">3</span></div>\n'
    '              <div class="pt-bar bar-a" style="height:40px;background:var(--a)" title="aohige nagoya: 2勝"><span class="pt-n">2</span></div>\n'
    '              <div class="pt-bar bar-j" style="height:60px;background:var(--j)" title="Jin2798: 3勝"><span class="pt-n">3</span></div>\n'
    '            </div>'
)

# 90分: s=0→s=1(20px) 追加 (ワイナリーの四季でsasuken 1位)
html = html.replace(
    '            <!-- 90分: a=9(180px) -->\n'
    '            <div class="pt-group">\n'
    '              <div class="pt-bar bar-a" style="height:180px;background:var(--a)" title="aohige nagoya: 9勝"><span class="pt-n">9</span></div>\n'
    '            </div>',
    '            <!-- 90分: s=1(20px), a=9(180px) -->\n'
    '            <div class="pt-group">\n'
    '              <div class="pt-bar bar-s" style="height:20px;background:var(--s)" title="sasuken2999: 1勝"><span class="pt-n">1</span></div>\n'
    '              <div class="pt-bar bar-a" style="height:180px;background:var(--a)" title="aohige nagoya: 9勝"><span class="pt-n">9</span></div>\n'
    '            </div>'
)

# ── 6. X軸ラベル更新 ──
# 40分: 4→5タイトル (マルコポーロ2追加)
html = html.replace(
    '<span class="pt-xg" title="ファイブ・トライブズ / リビング・フォレスト / ダイスフォージ / パークス:第二版">4タイトル ▴</span>',
    '<span class="pt-xg" title="ファイブ・トライブズ / リビング・フォレスト / ダイスフォージ / パークス:第二版 / マルコポーロ2:大いなる帰還">5タイトル ▴</span>'
)

# ── 7. 履歴行番号シフト 54→56, ..., 1→3 ──
for i in range(54, 0, -1):
    html = html.replace(
        f'<td>{i}</td><td class="date">',
        f'<td>{i+2}</td><td class="date">'
    )

# ── 8. 新規履歴行2行を先頭に挿入 ──
new_rows = (
    '\n'
    '      <tr>\n'
    '        <td>1</td><td class="date">2026-06-25<br>（本日）</td>\n'
    '        <td class="game-name"><a href="https://boardgamearena.com/gamepanel?game=marcopolotwo" target="_blank" rel="noopener">マルコポーロ2:大いなる帰還</a><br>'
    '<span style="font-weight:400;color:#999;font-size:.78rem">Marco Polo II: In the Service of the Khan</span></td>\n'
    '        <td class="pt-time">40</td>\n'
    '        <td><div class="rank">\n'
    '          <div class="rrow"><span class="badge b1">1位</span><span class="p-j">Jin2798</span><span class="score">109pt</span></div>\n'
    '          <div class="rrow"><span class="badge b2">2位</span><span class="p-s">sasuken2999</span><span class="score">76pt</span></div>\n'
    '          <div class="rrow"><span class="badge b3">3位</span><span class="p-a">aohige nagoya</span><span class="score">68pt</span></div>\n'
    '        </div></td>\n'
    '      </tr>\n'
    '\n'
    '      <tr>\n'
    '        <td>2</td><td class="date">2026-06-25<br>（本日）</td>\n'
    '        <td class="game-name"><a href="https://boardgamearena.com/gamepanel?game=viticulture" target="_blank" rel="noopener">ワイナリーの四季</a><br>'
    '<span style="font-weight:400;color:#999;font-size:.78rem">Viticulture</span></td>\n'
    '        <td class="pt-time">90</td>\n'
    '        <td><div class="rank">\n'
    '          <div class="rrow"><span class="badge b1">1位</span><span class="p-s">sasuken2999</span><span class="score">32pt</span></div>\n'
    '          <div class="rrow"><span class="badge b2">2位</span><span class="p-a">aohige nagoya</span><span class="score">31pt</span></div>\n'
    '          <div class="rrow"><span class="badge b3">3位</span><span class="p-j">Jin2798</span><span class="score">25pt</span></div>\n'
    '        </div></td>\n'
    '      </tr>\n'
    '\n'
)
html = html.replace(
    '    <tbody>\n\n      <tr>\n        <td>3</td><td class="date">2026-06-17<br>（8日前）</td>',
    '    <tbody>\n' + new_rows + '      <tr>\n        <td>3</td><td class="date">2026-06-17<br>（8日前）</td>'
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

chk('header 2026-06-25',            '2026-06-25 集計' in h)
chk('total-num 56',                  '<div class="total-num">56</div>' in h)
chk('card-sub 56 x3',               h.count('<div class="card-sub">56戦中</div>') == 3)
chk('sasuken s=16',                 '<span class="rank-count s">16</span>' in h)
chk('sasuken c2=25',                '<span class="rank-count c2">25</span>' in h)
chk('sasuken c3=15',                '<span class="rank-count c3">15</span>' in h)
chk('aohige a=26',                  '<span class="rank-count a">26</span>' in h)
chk('aohige c2=16',                 '<span class="rank-count c2">16</span>' in h)
chk('aohige c3=14',                 '<span class="rank-count c3">14</span>' in h)
chk('Jin j=14',                     '<span class="rank-count j">14</span>' in h)
chk('Jin c2=21',                    '<span class="rank-count c2">21</span>' in h)
chk('Jin c3=21',                    '<span class="rank-count c3">21</span>' in h)
chk('marcopolotwo in gamestats',    'game=marcopolotwo' in h)
chk('viticulture plays=2',          'game=viticulture" target="_blank" rel="noopener">ワイナリーの四季</a>' in h and '<td>2</td>' in h)
chk('viticulture s=1 50%',         'win-num s">1</span><div class="bar-bg"><div class="bar-fill bar-s" style="width:50%' in h)
chk('40min j=3 60px',              '<!-- 40分: s=3(60px), a=2(40px), j=3(60px) -->' in h)
chk('90min s=1 added',             '<!-- 90分: s=1(20px), a=9(180px) -->' in h)
chk('40min 5titles',               '5タイトル' in h and 'マルコポーロ2' in h)
chk('row#1 marcopolotwo today',    '<td>1</td><td class="date">2026-06-25<br>（本日）</td>' in h)
chk('row#2 viticulture today',     '<td>2</td><td class="date">2026-06-25<br>（本日）</td>' in h)
chk('row#3 = former#1 (06-17)',    '<td>3</td><td class="date">2026-06-17<br>（8日前）</td>' in h)
row_count = len(__import__('re').findall(r'<td>\d+</td><td class="date">', h))
chk(f'56 history rows (found {row_count})', row_count == 56)
chk('no old header date',          '2026-06-17 集計' not in h)
chk('no 54 total',                 '<div class="total-num">54</div>' not in h)

print(f'\nResult: {ok} OK / {ng} NG')
