import re
from datetime import date, datetime

path = r"bga_results.html"
with open(path, encoding='utf-8') as f:
    html = f.read()

today = date(2026, 8, 12)

# ── 1. ヘッダー日付更新 ──
html = html.replace('2026-08-05 集計', '2026-08-12 集計')

# ── 2. 相対日付の更新（全タブ対象） ──
def upd_date(m):
    d = datetime.strptime(m.group(1), '%Y-%m-%d').date()
    n = (today - d).days
    label = '本日' if n == 0 else f'{n}日前'
    return f'<td class="date">{m.group(1)}<br>（{label}）</td>'
html = re.sub(r'<td class="date">(\d{4}-\d{2}-\d{2})<br>（[^）]+）</td>', upd_date, html)

# ── 3. プレイヤーカード更新（メイン集計） ──
# 新規2戦: スカルキング(a1/s2/j3), ワンダラス(a1/j2/s3)
# 現在 sasuken 23/31/21, aohige 35/23/17, Jin 19/27/29  →  23/32/22, 37/23/17, 19/28/30
# sasuken: 2位 31→32 (スカルキング2位), 3位 21→22 (ワンダラス3位)
html = html.replace('<span class="rank-count c2">31</span>', '<span class="rank-count c2">32</span>')  # sasuken c2
html = html.replace('<span class="rank-count c3">21</span>', '<span class="rank-count c3">22</span>')  # sasuken c3
# aohige: 1位 35→37 (スカルキング, ワンダラス)
html = html.replace('<span class="rank-count a">35</span>', '<span class="rank-count a">37</span>')
# Jin: 2位 27→28 (ワンダラス2位), 3位 29→30 (スカルキング3位)
html = html.replace('<span class="rank-count c2">27</span>', '<span class="rank-count c2">28</span>')  # Jin c2
html = html.replace('<span class="rank-count c3">29</span>', '<span class="rank-count c3">30</span>')  # Jin c3
# 総対戦数 75→77
html = html.replace('<div class="card-sub">75戦中</div>', '<div class="card-sub">77戦中</div>')
html = html.replace('<div class="total-num">75</div>', '<div class="total-num">77</div>')

# ── 4. ゲーム別成績 ──
# 4a. 新ゲーム ワンダラスクリーチャーズ を先頭（vegetablestock の前）に追加
wc_row = (
    '      <tr>\n'
    '        <td><a href="https://boardgamearena.com/gamepanel?game=wondrouscreatures" target="_blank" rel="noopener">ワンダラスクリーチャーズ</a><br>'
    '<span style="font-weight:400;color:#999;font-size:.75rem">Wondrous Creatures</span></td>\n'
    '        <td>1</td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num s">0</span><div class="bar-bg"></div></div></td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num a">1</span><div class="bar-bg"><div class="bar-fill bar-a" style="width:100%"></div></div></div></td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num j">0</span><div class="bar-bg"></div></div></td>\n'
    '      </tr>\n'
)
html = html.replace(
    '    <tbody>\n'
    '      <tr>\n'
    '        <td><a href="https://boardgamearena.com/gamepanel?game=vegetablestock"',
    '    <tbody>\n'
    + wc_row +
    '      <tr>\n'
    '        <td><a href="https://boardgamearena.com/gamepanel?game=vegetablestock"'
)

# 4b. スカルキング: 3戦(s0 / a1 33% / j2 67%) → 4戦(s0 / a2 50% / j2 50%)
html = html.replace(
    '        <td><a href="https://boardgamearena.com/gamepanel?game=skullking" target="_blank" rel="noopener">スカルキング</a><br><span style="font-weight:400;color:#999;font-size:.75rem">Skull King</span></td>\n'
    '        <td>3</td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num s">0</span><div class="bar-bg"></div></div></td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num a">1</span><div class="bar-bg"><div class="bar-fill bar-a" style="width:33%"></div></div></div></td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num j">2</span><div class="bar-bg"><div class="bar-fill bar-j" style="width:67%"></div></div></div></td>',
    '        <td><a href="https://boardgamearena.com/gamepanel?game=skullking" target="_blank" rel="noopener">スカルキング</a><br><span style="font-weight:400;color:#999;font-size:.75rem">Skull King</span></td>\n'
    '        <td>4</td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num s">0</span><div class="bar-bg"></div></div></td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num a">2</span><div class="bar-bg"><div class="bar-fill bar-a" style="width:50%"></div></div></div></td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num j">2</span><div class="bar-bg"><div class="bar-fill bar-j" style="width:50%"></div></div></div></td>'
)

# ── 5. 棒グラフ更新 ──
# 5a. 20分: a=8(160px) → a=9(180px) (スカルキングでaohige 1位)
html = html.replace(
    '            <!-- 20分: s=12(240px), a=8(160px), j=10(200px) -->\n'
    '            <div class="pt-group">\n'
    '              <div class="pt-bar bar-s" style="height:240px;background:var(--s)" title="sasuken2999: 12勝"><span class="pt-n">12</span></div>\n'
    '              <div class="pt-bar bar-a" style="height:160px;background:var(--a)" title="aohige nagoya: 8勝"><span class="pt-n">8</span></div>\n'
    '              <div class="pt-bar bar-j" style="height:200px;background:var(--j)" title="Jin2798: 10勝"><span class="pt-n">10</span></div>\n'
    '            </div>',
    '            <!-- 20分: s=12(240px), a=9(180px), j=10(200px) -->\n'
    '            <div class="pt-group">\n'
    '              <div class="pt-bar bar-s" style="height:240px;background:var(--s)" title="sasuken2999: 12勝"><span class="pt-n">12</span></div>\n'
    '              <div class="pt-bar bar-a" style="height:180px;background:var(--a)" title="aohige nagoya: 9勝"><span class="pt-n">9</span></div>\n'
    '              <div class="pt-bar bar-j" style="height:200px;background:var(--j)" title="Jin2798: 10勝"><span class="pt-n">10</span></div>\n'
    '            </div>'
)

# 5b. 40分: a=2(40px) → a=3(60px) (ワンダラスでaohige 1位)
html = html.replace(
    '            <!-- 40分: s=4(80px), a=2(40px), j=3(60px) -->\n'
    '            <div class="pt-group">\n'
    '              <div class="pt-bar bar-s" style="height:80px;background:var(--s)" title="sasuken2999: 4勝"><span class="pt-n">4</span></div>\n'
    '              <div class="pt-bar bar-a" style="height:40px;background:var(--a)" title="aohige nagoya: 2勝"><span class="pt-n">2</span></div>\n'
    '              <div class="pt-bar bar-j" style="height:60px;background:var(--j)" title="Jin2798: 3勝"><span class="pt-n">3</span></div>\n'
    '            </div>',
    '            <!-- 40分: s=4(80px), a=3(60px), j=3(60px) -->\n'
    '            <div class="pt-group">\n'
    '              <div class="pt-bar bar-s" style="height:80px;background:var(--s)" title="sasuken2999: 4勝"><span class="pt-n">4</span></div>\n'
    '              <div class="pt-bar bar-a" style="height:60px;background:var(--a)" title="aohige nagoya: 3勝"><span class="pt-n">3</span></div>\n'
    '              <div class="pt-bar bar-j" style="height:60px;background:var(--j)" title="Jin2798: 3勝"><span class="pt-n">3</span></div>\n'
    '            </div>'
)

# ── 6. X軸ラベル: 40分 6→7タイトル (ワンダラスクリーチャーズ追加) ──
html = html.replace(
    '<span class="pt-xg" title="ファイブ・トライブズ / リビング・フォレスト / ダイスフォージ / パークス:第二版 / マルコポーロ2:大いなる帰還 / ロレンツォ・イル・マニーフィコ">6タイトル ▴</span>',
    '<span class="pt-xg" title="ファイブ・トライブズ / リビング・フォレスト / ダイスフォージ / パークス:第二版 / マルコポーロ2:大いなる帰還 / ロレンツォ・イル・マニーフィコ / ワンダラスクリーチャーズ">7タイトル ▴</span>'
)

# ── 7-8. 履歴シフト＋新規行挿入（メインタブ限定） ──
marker = '</div><!-- /tab-main -->'
idx = html.index(marker)
main_part, rest_part = html[:idx], html[idx:]

# 7. 行番号シフト 75→77, ..., 1→3
for i in range(75, 0, -1):
    main_part = main_part.replace(
        f'<td>{i}</td><td class="date">',
        f'<td>{i+2}</td><td class="date">'
    )

# 8. 新規履歴行2行を先頭に挿入（新しい順: スカルキング→ワンダラス）
new_rows = (
    '\n'
    '      <tr>\n'
    '        <td>1</td><td class="date">2026-08-12<br>（本日）</td>\n'
    '        <td class="game-name"><a href="https://boardgamearena.com/gamepanel?game=skullking" target="_blank" rel="noopener">スカルキング</a><br>'
    '<span style="font-weight:400;color:#999;font-size:.78rem">Skull King</span></td>\n'
    '        <td class="pt-time">20</td>\n'
    '        <td><div class="rank">\n'
    '          <div class="rrow"><span class="badge b1">1位</span><span class="p-a">aohige nagoya</span><span class="score">270pt</span></div>\n'
    '          <div class="rrow"><span class="badge b2">2位</span><span class="p-s">sasuken2999</span><span class="score">50pt</span></div>\n'
    '          <div class="rrow"><span class="badge b3">3位</span><span class="p-j">Jin2798</span><span class="score">-40pt</span></div>\n'
    '        </div></td>\n'
    '      </tr>\n'
    '\n'
    '      <tr>\n'
    '        <td>2</td><td class="date">2026-08-12<br>（本日）</td>\n'
    '        <td class="game-name"><a href="https://boardgamearena.com/gamepanel?game=wondrouscreatures" target="_blank" rel="noopener">ワンダラスクリーチャーズ</a><br>'
    '<span style="font-weight:400;color:#999;font-size:.78rem">Wondrous Creatures</span></td>\n'
    '        <td class="pt-time">40</td>\n'
    '        <td><div class="rank">\n'
    '          <div class="rrow"><span class="badge b1">1位</span><span class="p-a">aohige nagoya</span><span class="score">144pt</span></div>\n'
    '          <div class="rrow"><span class="badge b2">2位</span><span class="p-j">Jin2798</span><span class="score">139pt</span></div>\n'
    '          <div class="rrow"><span class="badge b3">3位</span><span class="p-s">sasuken2999</span><span class="score">102pt</span></div>\n'
    '        </div></td>\n'
    '      </tr>\n'
    '\n'
)
main_part = main_part.replace(
    '    <tbody>\n\n      <tr>\n        <td>3</td><td class="date">2026-08-05<br>（7日前）</td>',
    '    <tbody>\n' + new_rows + '      <tr>\n        <td>3</td><td class="date">2026-08-05<br>（7日前）</td>'
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

chk('header 2026-08-12',            '2026-08-12 集計' in h)
chk('total-num 77',                  '<div class="total-num">77</div>' in h)
chk('card-sub 77 x3',               h.count('<div class="card-sub">77戦中</div>') == 3)
chk('sasuken s=23',                 '<span class="rank-count s">23</span>' in h)
chk('sasuken c2=32',                '<span class="rank-count c2">32</span>' in h)
chk('sasuken c3=22',                '<span class="rank-count c3">22</span>' in h)
chk('aohige a=37',                  '<span class="rank-count a">37</span>' in h)
chk('aohige c2=23',                 '<span class="rank-count c2">23</span>' in h)
chk('aohige c3=17',                 '<span class="rank-count c3">17</span>' in h)
chk('Jin j=19',                     '<span class="rank-count j">19</span>' in h)
chk('Jin c2=28',                    '<span class="rank-count c2">28</span>' in h)
chk('Jin c3=30',                    '<span class="rank-count c3">30</span>' in h)
chk('sum sasuken 23+32+22=77',      23+32+22 == 77)
chk('sum aohige 37+23+17=77',       37+23+17 == 77)
chk('sum Jin 19+28+30=77',          19+28+30 == 77)
chk('wondrouscreatures in gamestats', 'game=wondrouscreatures" target="_blank" rel="noopener">ワンダラスクリーチャーズ' in h)
chk('skullking plays=4 a=2',        'game=skullking" target="_blank" rel="noopener">スカルキング</a><br><span style="font-weight:400;color:#999;font-size:.75rem">Skull King</span></td>\n        <td>4</td>' in h)
chk('20min a=9 180px',              '<!-- 20分: s=12(240px), a=9(180px), j=10(200px) -->' in h)
chk('40min a=3 60px',               '<!-- 40分: s=4(80px), a=3(60px), j=3(60px) -->' in h)
chk('xaxis 40min 7titles',          '7タイトル' in h and 'ワンダラスクリーチャーズ">7タイトル' in h)
chk('row#1 skullking today',        '<td>1</td><td class="date">2026-08-12<br>（本日）</td>' in main_h)
chk('row#2 wondrous today',         '<td>2</td><td class="date">2026-08-12<br>（本日）</td>' in main_h)
chk('row#3 = former#1 (08-05)',     '<td>3</td><td class="date">2026-08-05<br>（7日前）</td>' in main_h)
main_rows = len(re.findall(r'<td>\d+</td><td class="date">', main_h))
chk(f'77 main history rows (found {main_rows})', main_rows == 77)
four_rows = len(re.findall(r'<td>\d+</td><td class="date">', four_h))
chk(f'4-player tab still 4 rows (found {four_rows})', four_rows == 4)
chk('no old header date',           '2026-08-05 集計' not in h)
chk('no 75 total',                  '<div class="total-num">75</div>' not in h)

print(f'\nResult: {ok} OK / {ng} NG')
