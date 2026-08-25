import re
from datetime import date, datetime

path = r"bga_results.html"
with open(path, encoding='utf-8') as f:
    html = f.read()

today = date(2026, 8, 26)

# ── 1. ヘッダー日付更新 ──
html = html.replace('2026-08-19 集計', '2026-08-26 集計')

# ── 2. 相対日付の更新（全タブ対象） ──
def upd_date(m):
    d = datetime.strptime(m.group(1), '%Y-%m-%d').date()
    n = (today - d).days
    label = '本日' if n == 0 else f'{n}日前'
    return f'<td class="date">{m.group(1)}<br>（{label}）</td>'
html = re.sub(r'<td class="date">(\d{4}-\d{2}-\d{2})<br>（[^）]+）</td>', upd_date, html)

# ── 3. プレイヤーカード更新（メイン集計） ──
# 新規5戦: ポンド2(j1/s2/a3), ポンド1(a1/j2/s3), クィブ2(s1/a2/j3), クィブ1(j1/a2/s3), 郵便馬車(s1/a2/j3)
# 現在 sasuken 23/32/24, aohige 38/24/17, Jin 20/29/30  →  25/33/26, 39/27/18, 22/30/32
# sasuken: 1位 23→25 (クィブ2, 郵便馬車), 2位 32→33 (ポンド2), 3位 24→26 (ポンド1, クィブ1)
html = html.replace('<span class="rank-count s">23</span>', '<span class="rank-count s">25</span>')
html = html.replace('<span class="rank-count c2">32</span>', '<span class="rank-count c2">33</span>')  # sasuken c2
html = html.replace('<span class="rank-count c3">24</span>', '<span class="rank-count c3">26</span>')  # sasuken c3
# aohige: 1位 38→39 (ポンド1), 2位 24→27 (クィブ2, クィブ1, 郵便馬車), 3位 17→18 (ポンド2)
html = html.replace('<span class="rank-count a">38</span>', '<span class="rank-count a">39</span>')
html = html.replace('<span class="rank-count c2">24</span>', '<span class="rank-count c2">27</span>')  # aohige c2
html = html.replace('<span class="rank-count c3">17</span>', '<span class="rank-count c3">18</span>')  # aohige c3
# Jin: 1位 20→22 (ポンド2, クィブ1), 2位 29→30 (ポンド1), 3位 30→32 (クィブ2, 郵便馬車)
html = html.replace('<span class="rank-count j">20</span>', '<span class="rank-count j">22</span>')
html = html.replace('<span class="rank-count c2">29</span>', '<span class="rank-count c2">30</span>')  # Jin c2
html = html.replace('<span class="rank-count c3">30</span>', '<span class="rank-count c3">32</span>')  # Jin c3
# 総対戦数 79→84
html = html.replace('<div class="card-sub">79戦中</div>', '<div class="card-sub">84戦中</div>')
html = html.replace('<div class="total-num">79</div>', '<div class="total-num">84</div>')

# ── 4. ゲーム別成績 ──
# 4a. 新ゲーム2タイトル(ポンドスケープ, クィブルス)を先頭に追加
new_game_rows = (
    '      <tr>\n'
    '        <td><a href="https://boardgamearena.com/gamepanel?game=pondscape" target="_blank" rel="noopener">ポンドスケープ</a><br>'
    '<span style="font-weight:400;color:#999;font-size:.75rem">Pondscape</span></td>\n'
    '        <td>2</td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num s">0</span><div class="bar-bg"></div></div></td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num a">1</span><div class="bar-bg"><div class="bar-fill bar-a" style="width:50%"></div></div></div></td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num j">1</span><div class="bar-bg"><div class="bar-fill bar-j" style="width:50%"></div></div></div></td>\n'
    '      </tr>\n'
    '      <tr>\n'
    '        <td><a href="https://boardgamearena.com/gamepanel?game=quibbles" target="_blank" rel="noopener">クィブルス</a><br>'
    '<span style="font-weight:400;color:#999;font-size:.75rem">Quibbles</span></td>\n'
    '        <td>2</td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num s">1</span><div class="bar-bg"><div class="bar-fill bar-s" style="width:50%"></div></div></div></td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num a">0</span><div class="bar-bg"></div></div></td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num j">1</span><div class="bar-bg"><div class="bar-fill bar-j" style="width:50%"></div></div></div></td>\n'
    '      </tr>\n'
)
html = html.replace(
    '    <tbody>\n'
    '      <tr>\n'
    '        <td><a href="https://boardgamearena.com/gamepanel?game=thurnandtaxis"',
    '    <tbody>\n'
    + new_game_rows +
    '      <tr>\n'
    '        <td><a href="https://boardgamearena.com/gamepanel?game=thurnandtaxis"'
)

# 4b. 郵便馬車: 1戦(a1 100%) → 2戦(s1 50% / a1 50% / j0)
html = html.replace(
    '        <td><a href="https://boardgamearena.com/gamepanel?game=thurnandtaxis" target="_blank" rel="noopener">郵便馬車</a><br><span style="font-weight:400;color:#999;font-size:.75rem">Thurn and Taxis</span></td>\n'
    '        <td>1</td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num s">0</span><div class="bar-bg"></div></div></td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num a">1</span><div class="bar-bg"><div class="bar-fill bar-a" style="width:100%"></div></div></div></td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num j">0</span><div class="bar-bg"></div></div></td>',
    '        <td><a href="https://boardgamearena.com/gamepanel?game=thurnandtaxis" target="_blank" rel="noopener">郵便馬車</a><br><span style="font-weight:400;color:#999;font-size:.75rem">Thurn and Taxis</span></td>\n'
    '        <td>2</td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num s">1</span><div class="bar-bg"><div class="bar-fill bar-s" style="width:50%"></div></div></div></td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num a">1</span><div class="bar-bg"><div class="bar-fill bar-a" style="width:50%"></div></div></div></td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num j">0</span><div class="bar-bg"></div></div></td>'
)

# ── 5. グラフスケール拡張 12勝 → 14勝（20px/勝維持） ──
# 5a. CSS
html = html.replace(
    '    /* align with bar zone: top padding 20px + bar area 200px */\n'
    '    padding-top: 0; height: 220px; padding-bottom: 0; box-sizing: border-box;',
    '    /* align with bar zone: top padding 20px + bar area 240px */\n'
    '    padding-top: 0; height: 260px; padding-bottom: 0; box-sizing: border-box;'
)
html = html.replace(
    '    height: 260px; position: relative; border-left: 2px solid #ccc;',
    '    height: 300px; position: relative; border-left: 2px solid #ccc;'
)
html = html.replace(
    '  /* gridlines at 2,4,6,8,10,12 wins (each 2 wins = 40px) */',
    '  /* gridlines at 2,4,6,8,10,12,14 wins (each 2 wins = 40px) */'
)
html = html.replace(
    '    display: flex; height: 240px; align-items: flex-end;',
    '    display: flex; height: 280px; align-items: flex-end;'
)
html = html.replace(
    '  .pt-group { flex: 1; display: flex; align-items: flex-end; justify-content: center; gap: 4px; height: 240px; }',
    '  .pt-group { flex: 1; display: flex; align-items: flex-end; justify-content: center; gap: 4px; height: 280px; }'
)

# 5b. Y軸ラベル: 12,10,8,6,4,2 → 14,12,10,8,6,4,2
html = html.replace(
    '      <!-- Y軸ラベル: 上から 12,10,8,6,4,2（240px ÷ 6段階 = 40px/段） -->\n'
    '      <div class="pt-yaxis">\n'
    '        <span class="pt-yl">12</span>\n'
    '        <span class="pt-yl">10</span>\n'
    '        <span class="pt-yl">8</span>\n'
    '        <span class="pt-yl">6</span>\n'
    '        <span class="pt-yl">4</span>\n'
    '        <span class="pt-yl">2</span>\n'
    '      </div>',
    '      <!-- Y軸ラベル: 上から 14,12,10,8,6,4,2（280px ÷ 7段階 = 40px/段） -->\n'
    '      <div class="pt-yaxis">\n'
    '        <span class="pt-yl">14</span>\n'
    '        <span class="pt-yl">12</span>\n'
    '        <span class="pt-yl">10</span>\n'
    '        <span class="pt-yl">8</span>\n'
    '        <span class="pt-yl">6</span>\n'
    '        <span class="pt-yl">4</span>\n'
    '        <span class="pt-yl">2</span>\n'
    '      </div>'
)

# 5c. グリッドライン: top = 20 + (14-n)*20
html = html.replace(
    '          <!-- グリッドライン (padding-top:20px 分を加算: top = 20 + (12-n)*20) -->\n'
    '          <div class="pt-gl" style="top:20px"  title="12勝ライン"></div><!-- 12wins -->\n'
    '          <div class="pt-gl" style="top:60px"  title="10勝ライン"></div><!-- 10wins -->\n'
    '          <div class="pt-gl" style="top:100px" title="8勝ライン"></div><!-- 8wins -->\n'
    '          <div class="pt-gl" style="top:140px" title="6勝ライン"></div><!-- 6wins -->\n'
    '          <div class="pt-gl" style="top:180px" title="4勝ライン"></div><!-- 4wins -->\n'
    '          <div class="pt-gl" style="top:220px" title="2勝ライン"></div><!-- 2wins -->',
    '          <!-- グリッドライン (padding-top:20px 分を加算: top = 20 + (14-n)*20) -->\n'
    '          <div class="pt-gl" style="top:20px"  title="14勝ライン"></div><!-- 14wins -->\n'
    '          <div class="pt-gl" style="top:60px"  title="12勝ライン"></div><!-- 12wins -->\n'
    '          <div class="pt-gl" style="top:100px" title="10勝ライン"></div><!-- 10wins -->\n'
    '          <div class="pt-gl" style="top:140px" title="8勝ライン"></div><!-- 8wins -->\n'
    '          <div class="pt-gl" style="top:180px" title="6勝ライン"></div><!-- 6wins -->\n'
    '          <div class="pt-gl" style="top:220px" title="4勝ライン"></div><!-- 4wins -->\n'
    '          <div class="pt-gl" style="top:260px" title="2勝ライン"></div><!-- 2wins -->'
)

# ── 6. 棒グラフ更新 ──
# 6a. 20分: s=12→14(280px), j=10→11(220px) (クィブ2+郵便馬車でsasuken, クィブ1でJin)
html = html.replace(
    '            <!-- 20分: s=12(240px), a=10(200px), j=10(200px) -->\n'
    '            <div class="pt-group">\n'
    '              <div class="pt-bar bar-s" style="height:240px;background:var(--s)" title="sasuken2999: 12勝"><span class="pt-n">12</span></div>\n'
    '              <div class="pt-bar bar-a" style="height:200px;background:var(--a)" title="aohige nagoya: 10勝"><span class="pt-n">10</span></div>\n'
    '              <div class="pt-bar bar-j" style="height:200px;background:var(--j)" title="Jin2798: 10勝"><span class="pt-n">10</span></div>\n'
    '            </div>',
    '            <!-- 20分: s=14(280px), a=10(200px), j=11(220px) -->\n'
    '            <div class="pt-group">\n'
    '              <div class="pt-bar bar-s" style="height:280px;background:var(--s)" title="sasuken2999: 14勝"><span class="pt-n">14</span></div>\n'
    '              <div class="pt-bar bar-a" style="height:200px;background:var(--a)" title="aohige nagoya: 10勝"><span class="pt-n">10</span></div>\n'
    '              <div class="pt-bar bar-j" style="height:220px;background:var(--j)" title="Jin2798: 11勝"><span class="pt-n">11</span></div>\n'
    '            </div>'
)

# 6b. 30分: a=6→7(140px), j=2→3(60px) (ポンド1でaohige, ポンド2でJin)
html = html.replace(
    '            <!-- 30分: s=1(20px), a=6(120px), j=2(40px) -->\n'
    '            <div class="pt-group">\n'
    '              <div class="pt-bar bar-s" style="height:20px;background:var(--s)" title="sasuken2999: 1勝"><span class="pt-n">1</span></div>\n'
    '              <div class="pt-bar bar-a" style="height:120px;background:var(--a)" title="aohige nagoya: 6勝"><span class="pt-n">6</span></div>\n'
    '              <div class="pt-bar bar-j" style="height:40px;background:var(--j)" title="Jin2798: 2勝"><span class="pt-n">2</span></div>\n'
    '            </div>',
    '            <!-- 30分: s=1(20px), a=7(140px), j=3(60px) -->\n'
    '            <div class="pt-group">\n'
    '              <div class="pt-bar bar-s" style="height:20px;background:var(--s)" title="sasuken2999: 1勝"><span class="pt-n">1</span></div>\n'
    '              <div class="pt-bar bar-a" style="height:140px;background:var(--a)" title="aohige nagoya: 7勝"><span class="pt-n">7</span></div>\n'
    '              <div class="pt-bar bar-j" style="height:60px;background:var(--j)" title="Jin2798: 3勝"><span class="pt-n">3</span></div>\n'
    '            </div>'
)

# ── 7. X軸ラベル ──
# 20分: 19→20タイトル (クィブルス追加)
html = html.replace(
    '<span class="pt-xg" title="タクタ / シャーロック13 / レフュージ / スシゴー! / アップ・オア・ダウン? / フリップ7 / スカルキング / マウンテンゴーツ / オリフラム / ドラフトサウルス / キャプテン・フリップ / イプソ / こねこばくはつ / 宵と暁の呪文書 / シフティング・ストーンズ / ストーンエイジ / 天下鳴動 / ベジタブルストック / 郵便馬車">19タイトル ▴</span>',
    '<span class="pt-xg" title="タクタ / シャーロック13 / レフュージ / スシゴー! / アップ・オア・ダウン? / フリップ7 / スカルキング / マウンテンゴーツ / オリフラム / ドラフトサウルス / キャプテン・フリップ / イプソ / こねこばくはつ / 宵と暁の呪文書 / シフティング・ストーンズ / ストーンエイジ / 天下鳴動 / ベジタブルストック / 郵便馬車 / クィブルス">20タイトル ▴</span>'
)
# 30分: 6→7タイトル (ポンドスケープ追加)
html = html.replace(
    '<span class="pt-xg" title="世界の七不思議 / キャッスルコンボ / アクロポリス / ブラッディイン / フォレストシャッフル:ダートムーア / ツォルキン: マヤ神聖歴">6タイトル ▴</span>',
    '<span class="pt-xg" title="世界の七不思議 / キャッスルコンボ / アクロポリス / ブラッディイン / フォレストシャッフル:ダートムーア / ツォルキン: マヤ神聖歴 / ポンドスケープ">7タイトル ▴</span>'
)

# ── 8-9. メイン履歴シフト＋新規行挿入（メインタブ限定） ──
marker = '</div><!-- /tab-main -->'
idx = html.index(marker)
main_part, rest_part = html[:idx], html[idx:]

# 8. 行番号シフト 79→84, ..., 1→6
for i in range(79, 0, -1):
    main_part = main_part.replace(
        f'<td>{i}</td><td class="date">',
        f'<td>{i+5}</td><td class="date">'
    )

# 9. 新規履歴行5行を先頭に挿入（新しい順）
new_rows = (
    '\n'
    '      <tr>\n'
    '        <td>1</td><td class="date">2026-08-26<br>（本日）</td>\n'
    '        <td class="game-name"><a href="https://boardgamearena.com/gamepanel?game=pondscape" target="_blank" rel="noopener">ポンドスケープ</a><br>'
    '<span style="font-weight:400;color:#999;font-size:.78rem">Pondscape</span></td>\n'
    '        <td class="pt-time">30</td>\n'
    '        <td><div class="rank">\n'
    '          <div class="rrow"><span class="badge b1">1位</span><span class="p-j">Jin2798</span><span class="score">115pt</span></div>\n'
    '          <div class="rrow"><span class="badge b2">2位</span><span class="p-s">sasuken2999</span><span class="score">93pt</span></div>\n'
    '          <div class="rrow"><span class="badge b3">3位</span><span class="p-a">aohige nagoya</span><span class="score">91pt</span></div>\n'
    '        </div></td>\n'
    '      </tr>\n'
    '\n'
    '      <tr>\n'
    '        <td>2</td><td class="date">2026-08-26<br>（本日）</td>\n'
    '        <td class="game-name"><a href="https://boardgamearena.com/gamepanel?game=pondscape" target="_blank" rel="noopener">ポンドスケープ</a><br>'
    '<span style="font-weight:400;color:#999;font-size:.78rem">Pondscape</span></td>\n'
    '        <td class="pt-time">30</td>\n'
    '        <td><div class="rank">\n'
    '          <div class="rrow"><span class="badge b1">1位</span><span class="p-a">aohige nagoya</span><span class="score">84pt</span></div>\n'
    '          <div class="rrow"><span class="badge b2">2位</span><span class="p-j">Jin2798</span><span class="score">60pt</span></div>\n'
    '          <div class="rrow"><span class="badge b3">3位</span><span class="p-s">sasuken2999</span><span class="score">49pt</span></div>\n'
    '        </div></td>\n'
    '      </tr>\n'
    '\n'
    '      <tr>\n'
    '        <td>3</td><td class="date">2026-08-26<br>（本日）</td>\n'
    '        <td class="game-name"><a href="https://boardgamearena.com/gamepanel?game=quibbles" target="_blank" rel="noopener">クィブルス</a><br>'
    '<span style="font-weight:400;color:#999;font-size:.78rem">Quibbles</span></td>\n'
    '        <td class="pt-time">20</td>\n'
    '        <td><div class="rank">\n'
    '          <div class="rrow"><span class="badge b1">1位</span><span class="p-s">sasuken2999</span><span class="score">21pt</span></div>\n'
    '          <div class="rrow"><span class="badge b2">2位</span><span class="p-a">aohige nagoya</span><span class="score">15pt</span></div>\n'
    '          <div class="rrow"><span class="badge b3">3位</span><span class="p-j">Jin2798</span><span class="score">12pt</span></div>\n'
    '        </div></td>\n'
    '      </tr>\n'
    '\n'
    '      <tr>\n'
    '        <td>4</td><td class="date">2026-08-26<br>（本日）</td>\n'
    '        <td class="game-name"><a href="https://boardgamearena.com/gamepanel?game=quibbles" target="_blank" rel="noopener">クィブルス</a><br>'
    '<span style="font-weight:400;color:#999;font-size:.78rem">Quibbles</span></td>\n'
    '        <td class="pt-time">20</td>\n'
    '        <td><div class="rank">\n'
    '          <div class="rrow"><span class="badge b1">1位</span><span class="p-j">Jin2798</span><span class="score">21pt</span></div>\n'
    '          <div class="rrow"><span class="badge b2">2位</span><span class="p-a">aohige nagoya</span><span class="score">17pt</span></div>\n'
    '          <div class="rrow"><span class="badge b3">3位</span><span class="p-s">sasuken2999</span><span class="score">13pt</span></div>\n'
    '        </div></td>\n'
    '      </tr>\n'
    '\n'
    '      <tr>\n'
    '        <td>5</td><td class="date">2026-08-26<br>（本日）</td>\n'
    '        <td class="game-name"><a href="https://boardgamearena.com/gamepanel?game=thurnandtaxis" target="_blank" rel="noopener">郵便馬車</a><br>'
    '<span style="font-weight:400;color:#999;font-size:.78rem">Thurn and Taxis</span></td>\n'
    '        <td class="pt-time">20</td>\n'
    '        <td><div class="rank">\n'
    '          <div class="rrow"><span class="badge b1">1位</span><span class="p-s">sasuken2999</span><span class="score">16pt</span></div>\n'
    '          <div class="rrow"><span class="badge b2">2位</span><span class="p-a">aohige nagoya</span><span class="score">12pt</span></div>\n'
    '          <div class="rrow"><span class="badge b3">3位</span><span class="p-j">Jin2798</span><span class="score">4pt</span></div>\n'
    '        </div></td>\n'
    '      </tr>\n'
    '\n'
)
main_part = main_part.replace(
    '    <tbody>\n\n      <tr>\n        <td>6</td><td class="date">2026-08-19<br>（7日前）</td>',
    '    <tbody>\n' + new_rows + '      <tr>\n        <td>6</td><td class="date">2026-08-19<br>（7日前）</td>'
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

chk('header 2026-08-26',            '2026-08-26 集計' in h)
chk('total-num 84',                  '<div class="total-num">84</div>' in h)
chk('card-sub 84 x3',               h.count('<div class="card-sub">84戦中</div>') == 3)
chk('sasuken s=25',                 '<span class="rank-count s">25</span>' in h)
chk('sasuken c2=33',                '<span class="rank-count c2">33</span>' in h)
chk('sasuken c3=26',                '<span class="rank-count c3">26</span>' in h)
chk('aohige a=39',                  '<span class="rank-count a">39</span>' in h)
chk('aohige c2=27',                 '<span class="rank-count c2">27</span>' in h)
chk('aohige c3=18',                 '<span class="rank-count c3">18</span>' in h)
chk('Jin j=22',                     '<span class="rank-count j">22</span>' in h)
chk('Jin c2=30',                    '<span class="rank-count c2">30</span>' in h)
chk('Jin c3=32',                    '<span class="rank-count c3">32</span>' in h)
chk('sum sasuken 25+33+26=84',      25+33+26 == 84)
chk('sum aohige 39+27+18=84',       39+27+18 == 84)
chk('sum Jin 22+30+32=84',          22+30+32 == 84)
chk('pondscape in gamestats',       'game=pondscape" target="_blank" rel="noopener">ポンドスケープ' in h)
chk('quibbles in gamestats',        'game=quibbles" target="_blank" rel="noopener">クィブルス' in h)
chk('thurnandtaxis plays=2',        'game=thurnandtaxis" target="_blank" rel="noopener">郵便馬車</a><br><span style="font-weight:400;color:#999;font-size:.75rem">Thurn and Taxis</span></td>\n        <td>2</td>' in h)
# スケール拡張
chk('yaxis 14 added',               '<span class="pt-yl">14</span>' in h)
chk('yaxis 7 labels',               h.count('<span class="pt-yl">') == 7)
chk('barzone 300px',                'height: 300px; position: relative;' in h)
chk('pt-groups 280px',              'display: flex; height: 280px; align-items: flex-end;' in h)
chk('pt-group 280px',               'gap: 4px; height: 280px; }' in h)
chk('yaxis height 260px',           'padding-top: 0; height: 260px;' in h)
chk('gridline 14 at 20px',          'style="top:20px"  title="14勝ライン"' in h)
chk('gridline 2 at 260px',          'style="top:260px" title="2勝ライン"' in h)
chk('20min s=14 280px',             '<!-- 20分: s=14(280px), a=10(200px), j=11(220px) -->' in h)
chk('30min a=7 j=3',                '<!-- 30分: s=1(20px), a=7(140px), j=3(60px) -->' in h)
chk('no bar exceeds 280px',         'height:300px;background' not in h)
chk('xaxis 20min 20titles',         '20タイトル' in h and 'クィブルス">20タイトル' in h)
chk('xaxis 30min 7titles',          'ポンドスケープ">7タイトル' in h)
chk('row#1 pondscape today',        '<td>1</td><td class="date">2026-08-26<br>（本日）</td>' in main_h)
chk('row#5 thurnandtaxis today',    '<td>5</td><td class="date">2026-08-26<br>（本日）</td>' in main_h)
chk('row#6 = former#1 (08-19)',     '<td>6</td><td class="date">2026-08-19<br>（7日前）</td>' in main_h)
main_rows = len(re.findall(r'<td>\d+</td><td class="date">', main_h))
chk(f'84 main history rows (found {main_rows})', main_rows == 84)
four_rows = len(re.findall(r'<td>\d+</td><td class="date">', rest_h[rest_h.index('/tab-shinken'):]))
chk(f'4-player tab still 4 rows (found {four_rows})', four_rows == 4)
chk('shinken still 2 rows',         rest_h.count('class="shinken-num"') == 2)
chk('no old header date',           '2026-08-19 集計' not in h)
chk('no 79 total',                  '<div class="total-num">79</div>' not in h)

print(f'\nResult: {ok} OK / {ng} NG')
