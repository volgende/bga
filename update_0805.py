import re
from datetime import date, datetime

path = r"bga_results.html"
with open(path, encoding='utf-8') as f:
    html = f.read()

today = date(2026, 8, 5)

# ── 1. ヘッダー日付更新 ──
html = html.replace('2026-07-29 集計', '2026-08-05 集計')

# ── 2. 相対日付の更新（全タブ対象） ──
def upd_date(m):
    d = datetime.strptime(m.group(1), '%Y-%m-%d').date()
    n = (today - d).days
    label = '本日' if n == 0 else f'{n}日前'
    return f'<td class="date">{m.group(1)}<br>（{label}）</td>'
html = re.sub(r'<td class="date">(\d{4}-\d{2}-\d{2})<br>（[^）]+）</td>', upd_date, html)

# ── 3. プレイヤーカード更新（メイン集計） ──
# 新規6戦の順位内訳:
#   sasuken: 1位+1(ベジ#2), 2位+3(キャッスルコンボ,レース,GWT#2), 3位+2(ベジ#1,ベジ#3)
#   aohige : 1位+4(キャッスルコンボ,ベジ#1,レース同点,GWT#2同点), 2位+2(ベジ#2,ベジ#3), 3位+0
#   Jin    : 1位+3(レース同点,GWT#2同点,ベジ#3), 2位+1(ベジ#1), 3位+2(キャッスルコンボ,ベジ#2)
# 現在 sasuken 22/28/19, aohige 31/21/17, Jin 16/26/27  →  23/31/21, 35/23/17, 19/27/29
html = html.replace('<span class="rank-count s">22</span>', '<span class="rank-count s">23</span>')
html = html.replace('<span class="rank-count c2">28</span>', '<span class="rank-count c2">31</span>')  # sasuken c2
html = html.replace('<span class="rank-count c3">19</span>', '<span class="rank-count c3">21</span>')  # sasuken c3
html = html.replace('<span class="rank-count a">31</span>', '<span class="rank-count a">35</span>')
html = html.replace('<span class="rank-count c2">21</span>', '<span class="rank-count c2">23</span>')  # aohige c2
# aohige c3=17 は変化なし
html = html.replace('<span class="rank-count j">16</span>', '<span class="rank-count j">19</span>')
html = html.replace('<span class="rank-count c2">26</span>', '<span class="rank-count c2">27</span>')  # Jin c2
html = html.replace('<span class="rank-count c3">27</span>', '<span class="rank-count c3">29</span>')  # Jin c3
# 総対戦数 69→75
html = html.replace('<div class="card-sub">69戦中</div>', '<div class="card-sub">75戦中</div>')
html = html.replace('<div class="total-num">69</div>', '<div class="total-num">75</div>')

# ── 4. ゲーム別成績 ──
# 4a. 新ゲーム2タイトル(ベジタブルストック, レース)を先頭に追加
new_game_rows = (
    '      <tr>\n'
    '        <td><a href="https://boardgamearena.com/gamepanel?game=vegetablestock" target="_blank" rel="noopener">ベジタブルストック</a><br>'
    '<span style="font-weight:400;color:#999;font-size:.75rem">Vegetable Stock</span></td>\n'
    '        <td>3</td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num s">1</span><div class="bar-bg"><div class="bar-fill bar-s" style="width:33%"></div></div></div></td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num a">1</span><div class="bar-bg"><div class="bar-fill bar-a" style="width:33%"></div></div></div></td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num j">1</span><div class="bar-bg"><div class="bar-fill bar-j" style="width:33%"></div></div></div></td>\n'
    '      </tr>\n'
    '      <tr>\n'
    '        <td><a href="https://boardgamearena.com/gamepanel?game=raceforthegalaxy" target="_blank" rel="noopener">レース・フォー・ザ・ギャラクシー</a><br>'
    '<span style="font-weight:400;color:#999;font-size:.75rem">Race for the Galaxy</span></td>\n'
    '        <td>1</td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num s">0</span><div class="bar-bg"></div></div></td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num a">1</span><div class="bar-bg"><div class="bar-fill bar-a" style="width:100%"></div></div></div></td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num j">1</span><div class="bar-bg"><div class="bar-fill bar-j" style="width:100%"></div></div></div></td>\n'
    '      </tr>\n'
)
html = html.replace(
    '    <tbody>\n'
    '      <tr>\n'
    '        <td><a href="https://boardgamearena.com/gamepanel?game=greatwesterntrail"',
    '    <tbody>\n'
    + new_game_rows +
    '      <tr>\n'
    '        <td><a href="https://boardgamearena.com/gamepanel?game=greatwesterntrail"'
)

# 4b. グレート・ウエスタン・トレイル: 1戦(s1 100%) → 2戦(s1 50% / a1 50% / j1 50%)
html = html.replace(
    '        <td><a href="https://boardgamearena.com/gamepanel?game=greatwesterntrail" target="_blank" rel="noopener">グレート・ウエスタン・トレイル</a><br><span style="font-weight:400;color:#999;font-size:.75rem">Great Western Trail</span></td>\n'
    '        <td>1</td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num s">1</span><div class="bar-bg"><div class="bar-fill bar-s" style="width:100%"></div></div></div></td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num a">0</span><div class="bar-bg"></div></div></td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num j">0</span><div class="bar-bg"></div></div></td>',
    '        <td><a href="https://boardgamearena.com/gamepanel?game=greatwesterntrail" target="_blank" rel="noopener">グレート・ウエスタン・トレイル</a><br><span style="font-weight:400;color:#999;font-size:.75rem">Great Western Trail</span></td>\n'
    '        <td>2</td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num s">1</span><div class="bar-bg"><div class="bar-fill bar-s" style="width:50%"></div></div></div></td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num a">1</span><div class="bar-bg"><div class="bar-fill bar-a" style="width:50%"></div></div></div></td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num j">1</span><div class="bar-bg"><div class="bar-fill bar-j" style="width:50%"></div></div></div></td>'
)

# 4c. キャッスルコンボ: 2戦(a2 100%) → 3戦(a3 100%)
html = html.replace(
    '        <td><a href="https://boardgamearena.com/gamepanel?game=castlecombo" target="_blank" rel="noopener">キャッスルコンボ</a><br><span style="font-weight:400;color:#999;font-size:.75rem">Castle Combo</span></td>\n'
    '        <td>2</td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num s">0</span><div class="bar-bg"></div></div></td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num a">2</span><div class="bar-bg"><div class="bar-fill bar-a" style="width:100%"></div></div></div></td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num j">0</span><div class="bar-bg"></div></div></td>',
    '        <td><a href="https://boardgamearena.com/gamepanel?game=castlecombo" target="_blank" rel="noopener">キャッスルコンボ</a><br><span style="font-weight:400;color:#999;font-size:.75rem">Castle Combo</span></td>\n'
    '        <td>3</td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num s">0</span><div class="bar-bg"></div></div></td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num a">3</span><div class="bar-bg"><div class="bar-fill bar-a" style="width:100%"></div></div></div></td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num j">0</span><div class="bar-bg"></div></div></td>'
)

# ── 5. 棒グラフ更新 ──
# 5a. 10分: a=1→2, j=1→2 (レースでaohige, Jin 同点1位)
html = html.replace(
    '            <!-- 10分: s=1(20px), a=1(20px), j=1(20px) -->\n'
    '            <div class="pt-group">\n'
    '              <div class="pt-bar bar-s" style="height:20px;background:var(--s)" title="sasuken2999: 1勝"><span class="pt-n">1</span></div>\n'
    '              <div class="pt-bar bar-a" style="height:20px;background:var(--a)" title="aohige nagoya: 1勝"><span class="pt-n">1</span></div>\n'
    '              <div class="pt-bar bar-j" style="height:20px;background:var(--j)" title="Jin2798: 1勝"><span class="pt-n">1</span></div>\n'
    '            </div>',
    '            <!-- 10分: s=1(20px), a=2(40px), j=2(40px) -->\n'
    '            <div class="pt-group">\n'
    '              <div class="pt-bar bar-s" style="height:20px;background:var(--s)" title="sasuken2999: 1勝"><span class="pt-n">1</span></div>\n'
    '              <div class="pt-bar bar-a" style="height:40px;background:var(--a)" title="aohige nagoya: 2勝"><span class="pt-n">2</span></div>\n'
    '              <div class="pt-bar bar-j" style="height:40px;background:var(--j)" title="Jin2798: 2勝"><span class="pt-n">2</span></div>\n'
    '            </div>'
)

# 5b. 20分: s=11→12(240px), a=7→8(160px), j=9→10(200px) (ベジ#2 s, ベジ#1 a, ベジ#3 j)
html = html.replace(
    '            <!-- 20分: s=11(220px), a=7(140px), j=9(180px) -->\n'
    '            <div class="pt-group">\n'
    '              <div class="pt-bar bar-s" style="height:220px;background:var(--s)" title="sasuken2999: 11勝"><span class="pt-n">11</span></div>\n'
    '              <div class="pt-bar bar-a" style="height:140px;background:var(--a)" title="aohige nagoya: 7勝"><span class="pt-n">7</span></div>\n'
    '              <div class="pt-bar bar-j" style="height:180px;background:var(--j)" title="Jin2798: 9勝"><span class="pt-n">9</span></div>\n'
    '            </div>',
    '            <!-- 20分: s=12(240px), a=8(160px), j=10(200px) -->\n'
    '            <div class="pt-group">\n'
    '              <div class="pt-bar bar-s" style="height:240px;background:var(--s)" title="sasuken2999: 12勝"><span class="pt-n">12</span></div>\n'
    '              <div class="pt-bar bar-a" style="height:160px;background:var(--a)" title="aohige nagoya: 8勝"><span class="pt-n">8</span></div>\n'
    '              <div class="pt-bar bar-j" style="height:200px;background:var(--j)" title="Jin2798: 10勝"><span class="pt-n">10</span></div>\n'
    '            </div>'
)

# 5c. 30分: a=5→6(120px) (キャッスルコンボでaohige 1位)
html = html.replace(
    '            <!-- 30分: s=1(20px), a=5(100px), j=1(20px) -->\n'
    '            <div class="pt-group">\n'
    '              <div class="pt-bar bar-s" style="height:20px;background:var(--s)" title="sasuken2999: 1勝"><span class="pt-n">1</span></div>\n'
    '              <div class="pt-bar bar-a" style="height:100px;background:var(--a)" title="aohige nagoya: 5勝"><span class="pt-n">5</span></div>\n'
    '              <div class="pt-bar bar-j" style="height:20px;background:var(--j)" title="Jin2798: 1勝"><span class="pt-n">1</span></div>\n'
    '            </div>',
    '            <!-- 30分: s=1(20px), a=6(120px), j=1(20px) -->\n'
    '            <div class="pt-group">\n'
    '              <div class="pt-bar bar-s" style="height:20px;background:var(--s)" title="sasuken2999: 1勝"><span class="pt-n">1</span></div>\n'
    '              <div class="pt-bar bar-a" style="height:120px;background:var(--a)" title="aohige nagoya: 6勝"><span class="pt-n">6</span></div>\n'
    '              <div class="pt-bar bar-j" style="height:20px;background:var(--j)" title="Jin2798: 1勝"><span class="pt-n">1</span></div>\n'
    '            </div>'
)

# 5d. 60分: s=1 → s=1, a=1, j=1 (GWT#2でaohige, Jin 同点1位)
html = html.replace(
    '            <!-- 60分: s=1(20px) -->\n'
    '            <div class="pt-group">\n'
    '              <div class="pt-bar bar-s" style="height:20px;background:var(--s)" title="sasuken2999: 1勝"><span class="pt-n">1</span></div>\n'
    '            </div>',
    '            <!-- 60分: s=1(20px), a=1(20px), j=1(20px) -->\n'
    '            <div class="pt-group">\n'
    '              <div class="pt-bar bar-s" style="height:20px;background:var(--s)" title="sasuken2999: 1勝"><span class="pt-n">1</span></div>\n'
    '              <div class="pt-bar bar-a" style="height:20px;background:var(--a)" title="aohige nagoya: 1勝"><span class="pt-n">1</span></div>\n'
    '              <div class="pt-bar bar-j" style="height:20px;background:var(--j)" title="Jin2798: 1勝"><span class="pt-n">1</span></div>\n'
    '            </div>'
)

# ── 6. X軸ラベル ──
# 10分: 1→2タイトル (レース追加)
html = html.replace(
    '            <span class="pt-xl">10分</span>\n'
    '            <span class="pt-xg" title="YRO">1タイトル ▴</span>',
    '            <span class="pt-xl">10分</span>\n'
    '            <span class="pt-xg" title="YRO / レース・フォー・ザ・ギャラクシー">2タイトル ▴</span>'
)
# 20分: 17→18タイトル (ベジタブルストック追加)
html = html.replace(
    '<span class="pt-xg" title="タクタ / シャーロック13 / レフュージ / スシゴー! / アップ・オア・ダウン? / フリップ7 / スカルキング / マウンテンゴーツ / オリフラム / ドラフトサウルス / キャプテン・フリップ / イプソ / こねこばくはつ / 宵と暁の呪文書 / シフティング・ストーンズ / ストーンエイジ / 天下鳴動">17タイトル ▴</span>',
    '<span class="pt-xg" title="タクタ / シャーロック13 / レフュージ / スシゴー! / アップ・オア・ダウン? / フリップ7 / スカルキング / マウンテンゴーツ / オリフラム / ドラフトサウルス / キャプテン・フリップ / イプソ / こねこばくはつ / 宵と暁の呪文書 / シフティング・ストーンズ / ストーンエイジ / 天下鳴動 / ベジタブルストック">18タイトル ▴</span>'
)

# ── 7-8. 履歴シフト＋新規行挿入（メインタブ限定） ──
marker = '</div><!-- /tab-main -->'
idx = html.index(marker)
main_part, rest_part = html[:idx], html[idx:]

# 7. 行番号シフト 69→75, ..., 1→7
for i in range(69, 0, -1):
    main_part = main_part.replace(
        f'<td>{i}</td><td class="date">',
        f'<td>{i+6}</td><td class="date">'
    )

# 8. 新規履歴行6行を先頭に挿入（新しい順）
new_rows = (
    '\n'
    '      <tr>\n'
    '        <td>1</td><td class="date">2026-08-05<br>（本日）</td>\n'
    '        <td class="game-name"><a href="https://boardgamearena.com/gamepanel?game=castlecombo" target="_blank" rel="noopener">キャッスルコンボ</a><br>'
    '<span style="font-weight:400;color:#999;font-size:.78rem">Castle Combo</span></td>\n'
    '        <td class="pt-time">30</td>\n'
    '        <td><div class="rank">\n'
    '          <div class="rrow"><span class="badge b1">1位</span><span class="p-a">aohige nagoya</span><span class="score">87pt</span></div>\n'
    '          <div class="rrow"><span class="badge b2">2位</span><span class="p-s">sasuken2999</span><span class="score">76pt</span></div>\n'
    '          <div class="rrow"><span class="badge b3">3位</span><span class="p-j">Jin2798</span><span class="score">69pt</span></div>\n'
    '        </div></td>\n'
    '      </tr>\n'
    '\n'
    '      <tr>\n'
    '        <td>2</td><td class="date">2026-08-05<br>（本日）</td>\n'
    '        <td class="game-name"><a href="https://boardgamearena.com/gamepanel?game=vegetablestock" target="_blank" rel="noopener">ベジタブルストック</a><br>'
    '<span style="font-weight:400;color:#999;font-size:.78rem">Vegetable Stock</span></td>\n'
    '        <td class="pt-time">20</td>\n'
    '        <td><div class="rank">\n'
    '          <div class="rrow"><span class="badge b1">1位</span><span class="p-a">aohige nagoya</span><span class="score">57pt</span></div>\n'
    '          <div class="rrow"><span class="badge b2">2位</span><span class="p-j">Jin2798</span><span class="score">56pt</span></div>\n'
    '          <div class="rrow"><span class="badge b3">3位</span><span class="p-s">sasuken2999</span><span class="score">54pt</span></div>\n'
    '        </div></td>\n'
    '      </tr>\n'
    '\n'
    '      <tr>\n'
    '        <td>3</td><td class="date">2026-08-05<br>（本日）</td>\n'
    '        <td class="game-name"><a href="https://boardgamearena.com/gamepanel?game=raceforthegalaxy" target="_blank" rel="noopener">レース・フォー・ザ・ギャラクシー</a><br>'
    '<span style="font-weight:400;color:#999;font-size:.78rem">Race for the Galaxy</span></td>\n'
    '        <td class="pt-time">10</td>\n'
    '        <td><div class="rank">\n'
    '          <div class="rrow"><span class="badge b1">1位</span><span class="p-a">aohige nagoya</span><span class="score">1pt</span></div>\n'
    '          <div class="rrow"><span class="badge b1">1位</span><span class="p-j">Jin2798</span><span class="score">1pt</span></div>\n'
    '          <div class="rrow"><span class="badge b2">2位</span><span class="p-s">sasuken2999</span><span class="score">0pt</span></div>\n'
    '        </div></td>\n'
    '      </tr>\n'
    '\n'
    '      <tr>\n'
    '        <td>4</td><td class="date">2026-08-05<br>（本日）</td>\n'
    '        <td class="game-name"><a href="https://boardgamearena.com/gamepanel?game=greatwesterntrail" target="_blank" rel="noopener">グレート・ウエスタン・トレイル</a><br>'
    '<span style="font-weight:400;color:#999;font-size:.78rem">Great Western Trail</span></td>\n'
    '        <td class="pt-time">60</td>\n'
    '        <td><div class="rank">\n'
    '          <div class="rrow"><span class="badge b1">1位</span><span class="p-j">Jin2798</span><span class="score">62pt</span></div>\n'
    '          <div class="rrow"><span class="badge b1">1位</span><span class="p-a">aohige nagoya</span><span class="score">62pt</span></div>\n'
    '          <div class="rrow"><span class="badge b2">2位</span><span class="p-s">sasuken2999</span><span class="score">46pt</span></div>\n'
    '        </div></td>\n'
    '      </tr>\n'
    '\n'
    '      <tr>\n'
    '        <td>5</td><td class="date">2026-08-05<br>（本日）</td>\n'
    '        <td class="game-name"><a href="https://boardgamearena.com/gamepanel?game=vegetablestock" target="_blank" rel="noopener">ベジタブルストック</a><br>'
    '<span style="font-weight:400;color:#999;font-size:.78rem">Vegetable Stock</span></td>\n'
    '        <td class="pt-time">20</td>\n'
    '        <td><div class="rank">\n'
    '          <div class="rrow"><span class="badge b1">1位</span><span class="p-s">sasuken2999</span><span class="score">50pt</span></div>\n'
    '          <div class="rrow"><span class="badge b2">2位</span><span class="p-a">aohige nagoya</span><span class="score">39pt</span></div>\n'
    '          <div class="rrow"><span class="badge b3">3位</span><span class="p-j">Jin2798</span><span class="score">38pt</span></div>\n'
    '        </div></td>\n'
    '      </tr>\n'
    '\n'
    '      <tr>\n'
    '        <td>6</td><td class="date">2026-08-05<br>（本日）</td>\n'
    '        <td class="game-name"><a href="https://boardgamearena.com/gamepanel?game=vegetablestock" target="_blank" rel="noopener">ベジタブルストック</a><br>'
    '<span style="font-weight:400;color:#999;font-size:.78rem">Vegetable Stock</span></td>\n'
    '        <td class="pt-time">20</td>\n'
    '        <td><div class="rank">\n'
    '          <div class="rrow"><span class="badge b1">1位</span><span class="p-j">Jin2798</span><span class="score">83pt</span></div>\n'
    '          <div class="rrow"><span class="badge b2">2位</span><span class="p-a">aohige nagoya</span><span class="score">80pt</span></div>\n'
    '          <div class="rrow"><span class="badge b3">3位</span><span class="p-s">sasuken2999</span><span class="score">78pt</span></div>\n'
    '        </div></td>\n'
    '      </tr>\n'
    '\n'
)
main_part = main_part.replace(
    '    <tbody>\n\n      <tr>\n        <td>7</td><td class="date">2026-07-29<br>（7日前）</td>',
    '    <tbody>\n' + new_rows + '      <tr>\n        <td>7</td><td class="date">2026-07-29<br>（7日前）</td>'
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

chk('header 2026-08-05',            '2026-08-05 集計' in h)
chk('total-num 75',                  '<div class="total-num">75</div>' in h)
chk('card-sub 75 x3',               h.count('<div class="card-sub">75戦中</div>') == 3)
chk('sasuken s=23',                 '<span class="rank-count s">23</span>' in h)
chk('sasuken c2=31',                '<span class="rank-count c2">31</span>' in h)
chk('sasuken c3=21',                '<span class="rank-count c3">21</span>' in h)
chk('aohige a=35',                  '<span class="rank-count a">35</span>' in h)
chk('aohige c2=23',                 '<span class="rank-count c2">23</span>' in h)
chk('aohige c3=17',                 '<span class="rank-count c3">17</span>' in h)
chk('Jin j=19',                     '<span class="rank-count j">19</span>' in h)
chk('Jin c2=27',                    '<span class="rank-count c2">27</span>' in h)
chk('Jin c3=29',                    '<span class="rank-count c3">29</span>' in h)
chk('sum sasuken 23+31+21=75',      23+31+21 == 75)
chk('sum aohige 35+23+17=75',       35+23+17 == 75)
chk('sum Jin 19+27+29=75',          19+27+29 == 75)
chk('vegetablestock in gamestats',  'game=vegetablestock" target="_blank" rel="noopener">ベジタブルストック' in h)
chk('race in gamestats',            'game=raceforthegalaxy" target="_blank" rel="noopener">レース・フォー・ザ・ギャラクシー' in h)
chk('gwt plays=2',                  'game=greatwesterntrail" target="_blank" rel="noopener">グレート・ウエスタン・トレイル</a><br><span style="font-weight:400;color:#999;font-size:.75rem">Great Western Trail</span></td>\n        <td>2</td>' in h)
chk('castlecombo plays=3 a=3',      'game=castlecombo" target="_blank" rel="noopener">キャッスルコンボ</a><br><span style="font-weight:400;color:#999;font-size:.75rem">Castle Combo</span></td>\n        <td>3</td>' in h and '<span class="win-num a">3</span>' in h)
chk('10min a=2 j=2',                '<!-- 10分: s=1(20px), a=2(40px), j=2(40px) -->' in h)
chk('20min s=12 240px',             '<!-- 20分: s=12(240px), a=8(160px), j=10(200px) -->' in h)
chk('30min a=6 120px',              '<!-- 30分: s=1(20px), a=6(120px), j=1(20px) -->' in h)
chk('60min a=1 j=1 added',          '<!-- 60分: s=1(20px), a=1(20px), j=1(20px) -->' in h)
chk('xaxis 10min 2titles',          '2タイトル' in h and 'YRO / レース・フォー・ザ・ギャラクシー' in h)
chk('xaxis 20min 18titles',         '18タイトル' in h and 'ベジタブルストック">18タイトル' in h)
chk('row#1 castlecombo today',      '<td>1</td><td class="date">2026-08-05<br>（本日）</td>' in main_h)
chk('row#6 vegetablestock today',   '<td>6</td><td class="date">2026-08-05<br>（本日）</td>' in main_h)
chk('row#7 = former#1 (07-29)',     '<td>7</td><td class="date">2026-07-29<br>（7日前）</td>' in main_h)
main_rows = len(re.findall(r'<td>\d+</td><td class="date">', main_h))
chk(f'75 main history rows (found {main_rows})', main_rows == 75)
four_rows = len(re.findall(r'<td>\d+</td><td class="date">', four_h))
chk(f'4-player tab still 4 rows (found {four_rows})', four_rows == 4)
chk('no old header date',           '2026-07-29 集計' not in h)
chk('no 69 total',                  '<div class="total-num">69</div>' not in h)

print(f'\nResult: {ok} OK / {ng} NG')
