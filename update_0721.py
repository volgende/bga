import re
from datetime import date, datetime

path = r"bga_results.html"
with open(path, encoding='utf-8') as f:
    html = f.read()

today = date(2026, 7, 21)

# ── 1. ヘッダー日付更新 ──
html = html.replace('2026-07-09 集計', '2026-07-21 集計')

# ── 2. 相対日付の更新（全タブ対象） ──
def upd_date(m):
    d = datetime.strptime(m.group(1), '%Y-%m-%d').date()
    n = (today - d).days
    label = '本日' if n == 0 else f'{n}日前'
    return f'<td class="date">{m.group(1)}<br>（{label}）</td>'
html = re.sub(r'<td class="date">(\d{4}-\d{2}-\d{2})<br>（[^）]+）</td>', upd_date, html)

# ── 3. プレイヤーカード更新（メイン集計） ──
# sasuken: 1位 19→21 (天下鳴動1位, YRO1位), 2位 27→28 (YRO2位), 3位 15→17 (オルレアン3位, 天下鳴動3位)
html = html.replace('<span class="rank-count s">19</span>', '<span class="rank-count s">21</span>')
html = html.replace('<span class="rank-count c2">27</span>', '<span class="rank-count c2">28</span>')
# aohige: 1位 28→31 (オルレアン, 天下鳴動, YRO), 2位 18→19 (YRO2位), 3位 15→16 (天下鳴動3位)
html = html.replace('<span class="rank-count a">28</span>', '<span class="rank-count a">31</span>')
html = html.replace('<span class="rank-count c2">18</span>', '<span class="rank-count c2">19</span>')
# c3=15 は sasuken と aohige で重複するため、出現順に1件ずつ置換（sasuken→17, aohige→16）
html = html.replace('<span class="rank-count c3">15</span>', '<span class="rank-count c3">17</span>', 1)
html = html.replace('<span class="rank-count c3">15</span>', '<span class="rank-count c3">16</span>', 1)
# Jin: 1位 14 据置, 2位 22→25 (オルレアン, 天下鳴動×2), 3位 25→27 (YRO×2)
html = html.replace('<span class="rank-count c2">22</span>', '<span class="rank-count c2">25</span>')
html = html.replace('<span class="rank-count c3">25</span>', '<span class="rank-count c3">27</span>')
# 総対戦数 61→66
html = html.replace('<div class="card-sub">61戦中</div>', '<div class="card-sub">66戦中</div>')
html = html.replace('<div class="total-num">61</div>', '<div class="total-num">66</div>')

# ── 4. ゲーム別成績 ──
# 4a. オルレアン: 1戦(a=1) → 2戦(a=2) ※既存のタイポ <\span> も修正
html = html.replace(
    '        <td><a href="https://boardgamearena.com/gamepanel?game=orleans" target="_blank" rel="noopener">オルレアン</a><br><span style="font-weight:400;color:#999;font-size:.75rem">Orléans</span></td>\n'
    '        <td>1</td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num s">0</span><div class="bar-bg"></div></div></td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num a">1<\\span><div class="bar-bg"><div class="bar-fill bar-a" style="width:100%"></div></div></div></td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num j">0</span><div class="bar-bg"></div></div></td>',
    '        <td><a href="https://boardgamearena.com/gamepanel?game=orleans" target="_blank" rel="noopener">オルレアン</a><br><span style="font-weight:400;color:#999;font-size:.75rem">Orléans</span></td>\n'
    '        <td>2</td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num s">0</span><div class="bar-bg"></div></div></td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num a">2</span><div class="bar-bg"><div class="bar-fill bar-a" style="width:100%"></div></div></div></td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num j">0</span><div class="bar-bg"></div></div></td>'
)

# 4b. 新ゲーム2タイトル(天下鳴動, YRO)を先頭に追加
new_game_rows = (
    '      <tr>\n'
    '        <td><a href="https://boardgamearena.com/gamepanel?game=rumblenation" target="_blank" rel="noopener">天下鳴動</a><br>'
    '<span style="font-weight:400;color:#999;font-size:.75rem">Rumble Nation</span></td>\n'
    '        <td>2</td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num s">1</span><div class="bar-bg"><div class="bar-fill bar-s" style="width:50%"></div></div></div></td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num a">1</span><div class="bar-bg"><div class="bar-fill bar-a" style="width:50%"></div></div></div></td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num j">0</span><div class="bar-bg"></div></div></td>\n'
    '      </tr>\n'
    '      <tr>\n'
    '        <td><a href="https://boardgamearena.com/gamepanel?game=yro" target="_blank" rel="noopener">YRO</a><br>'
    '<span style="font-weight:400;color:#999;font-size:.75rem">YRO</span></td>\n'
    '        <td>2</td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num s">1</span><div class="bar-bg"><div class="bar-fill bar-s" style="width:50%"></div></div></div></td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num a">1</span><div class="bar-bg"><div class="bar-fill bar-a" style="width:50%"></div></div></div></td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num j">0</span><div class="bar-bg"></div></div></td>\n'
    '      </tr>\n'
)
html = html.replace(
    '    <tbody>\n'
    '      <tr>\n'
    '        <td><a href="https://boardgamearena.com/gamepanel?game=stoneage"',
    '    <tbody>\n'
    + new_game_rows +
    '      <tr>\n'
    '        <td><a href="https://boardgamearena.com/gamepanel?game=stoneage"'
)

# ── 5. グラフのスケール拡張（最大10勝 → 12勝, 20px/勝は維持） ──
# 5a. CSS: 各高さを 12勝(240px) 基準に拡張
html = html.replace(
    '    padding-top: 0; height: 180px; padding-bottom: 0; box-sizing: border-box;',
    '    padding-top: 0; height: 220px; padding-bottom: 0; box-sizing: border-box;'
)
html = html.replace(
    '    height: 220px; position: relative; border-left: 2px solid #ccc;',
    '    height: 260px; position: relative; border-left: 2px solid #ccc;'
)
html = html.replace(
    '    display: flex; height: 200px; align-items: flex-end;',
    '    display: flex; height: 240px; align-items: flex-end;'
)
html = html.replace(
    '  .pt-group { flex: 1; display: flex; align-items: flex-end; justify-content: center; gap: 4px; height: 200px; }',
    '  .pt-group { flex: 1; display: flex; align-items: flex-end; justify-content: center; gap: 4px; height: 240px; }'
)
html = html.replace(
    '  /* gridlines at 0,2,4,6,8 wins (each 2 wins = 40px) */',
    '  /* gridlines at 2,4,6,8,10,12 wins (each 2 wins = 40px) */'
)
html = html.replace(
    '    /* align with bar zone: top padding 20px + bar area 160px */',
    '    /* align with bar zone: top padding 20px + bar area 200px */'
)

# 5b. Y軸ラベル: 10,8,6,4,2 → 12,10,8,6,4,2
html = html.replace(
    '      <!-- Y軸ラベル: 上から 10,8,6,4,2（200px ÷ 5段階 = 40px/段） -->\n'
    '      <div class="pt-yaxis">\n'
    '        <span class="pt-yl">10</span>\n'
    '        <span class="pt-yl">8</span>\n'
    '        <span class="pt-yl">6</span>\n'
    '        <span class="pt-yl">4</span>\n'
    '        <span class="pt-yl">2</span>\n'
    '      </div>',
    '      <!-- Y軸ラベル: 上から 12,10,8,6,4,2（240px ÷ 6段階 = 40px/段） -->\n'
    '      <div class="pt-yaxis">\n'
    '        <span class="pt-yl">12</span>\n'
    '        <span class="pt-yl">10</span>\n'
    '        <span class="pt-yl">8</span>\n'
    '        <span class="pt-yl">6</span>\n'
    '        <span class="pt-yl">4</span>\n'
    '        <span class="pt-yl">2</span>\n'
    '      </div>'
)

# 5c. グリッドライン: top = 20 + (12-n)*20
html = html.replace(
    '          <!-- グリッドライン (padding-top:20px 分を加算: top = 20 + (10-n)*20) -->\n'
    '          <div class="pt-gl" style="top:20px"  title="10勝ライン"></div><!-- 10wins -->\n'
    '          <div class="pt-gl" style="top:60px"  title="8勝ライン"></div><!-- 8wins -->\n'
    '          <div class="pt-gl" style="top:100px" title="6勝ライン"></div><!-- 6wins -->\n'
    '          <div class="pt-gl" style="top:140px" title="4勝ライン"></div><!-- 4wins -->\n'
    '          <div class="pt-gl" style="top:180px" title="2勝ライン"></div><!-- 2wins -->',
    '          <!-- グリッドライン (padding-top:20px 分を加算: top = 20 + (12-n)*20) -->\n'
    '          <div class="pt-gl" style="top:20px"  title="12勝ライン"></div><!-- 12wins -->\n'
    '          <div class="pt-gl" style="top:60px"  title="10勝ライン"></div><!-- 10wins -->\n'
    '          <div class="pt-gl" style="top:100px" title="8勝ライン"></div><!-- 8wins -->\n'
    '          <div class="pt-gl" style="top:140px" title="6勝ライン"></div><!-- 6wins -->\n'
    '          <div class="pt-gl" style="top:180px" title="4勝ライン"></div><!-- 4wins -->\n'
    '          <div class="pt-gl" style="top:220px" title="2勝ライン"></div><!-- 2wins -->'
)

# ── 6. 棒グラフ: 10分バケット新設 + 20分/90分の更新 ──
# 6a. 10分バケットを先頭に追加、20分を s=11, a=7 に更新
html = html.replace(
    '            <!-- 20分: s=10(200px), a=6(120px), j=8(160px) -->\n'
    '            <div class="pt-group">\n'
    '              <div class="pt-bar bar-s" style="height:200px;background:var(--s)" title="sasuken2999: 10勝"><span class="pt-n">10</span></div>\n'
    '              <div class="pt-bar bar-a" style="height:120px;background:var(--a)" title="aohige nagoya: 6勝"><span class="pt-n">6</span></div>\n'
    '              <div class="pt-bar bar-j" style="height:160px;background:var(--j)" title="Jin2798: 8勝"><span class="pt-n">8</span></div>\n'
    '            </div>',
    '            <!-- 10分: s=1(20px), a=1(20px) -->\n'
    '            <div class="pt-group">\n'
    '              <div class="pt-bar bar-s" style="height:20px;background:var(--s)" title="sasuken2999: 1勝"><span class="pt-n">1</span></div>\n'
    '              <div class="pt-bar bar-a" style="height:20px;background:var(--a)" title="aohige nagoya: 1勝"><span class="pt-n">1</span></div>\n'
    '            </div>\n'
    '            <!-- 20分: s=11(220px), a=7(140px), j=8(160px) -->\n'
    '            <div class="pt-group">\n'
    '              <div class="pt-bar bar-s" style="height:220px;background:var(--s)" title="sasuken2999: 11勝"><span class="pt-n">11</span></div>\n'
    '              <div class="pt-bar bar-a" style="height:140px;background:var(--a)" title="aohige nagoya: 7勝"><span class="pt-n">7</span></div>\n'
    '              <div class="pt-bar bar-j" style="height:160px;background:var(--j)" title="Jin2798: 8勝"><span class="pt-n">8</span></div>\n'
    '            </div>'
)

# 6b. 90分: a=9(180px) → a=10(200px) (オルレアンでaohige 1位)
html = html.replace(
    '            <!-- 90分: s=1(20px), a=9(180px) -->\n'
    '            <div class="pt-group">\n'
    '              <div class="pt-bar bar-s" style="height:20px;background:var(--s)" title="sasuken2999: 1勝"><span class="pt-n">1</span></div>\n'
    '              <div class="pt-bar bar-a" style="height:180px;background:var(--a)" title="aohige nagoya: 9勝"><span class="pt-n">9</span></div>\n'
    '            </div>',
    '            <!-- 90分: s=1(20px), a=10(200px) -->\n'
    '            <div class="pt-group">\n'
    '              <div class="pt-bar bar-s" style="height:20px;background:var(--s)" title="sasuken2999: 1勝"><span class="pt-n">1</span></div>\n'
    '              <div class="pt-bar bar-a" style="height:200px;background:var(--a)" title="aohige nagoya: 10勝"><span class="pt-n">10</span></div>\n'
    '            </div>'
)

# ── 7. X軸ラベル: 10分を新設、20分に天下鳴動を追加 ──
html = html.replace(
    '          <div class="pt-xlabel">\n'
    '            <span class="pt-xl">20分</span>\n'
    '            <span class="pt-xg" title="タクタ / シャーロック13 / レフュージ / スシゴー! / アップ・オア・ダウン? / フリップ7 / スカルキング / マウンテンゴーツ / オリフラム / ドラフトサウルス / キャプテン・フリップ / イプソ / こねこばくはつ / 宵と暁の呪文書 / シフティング・ストーンズ / ストーンエイジ">16タイトル ▴</span>\n'
    '          </div>',
    '          <div class="pt-xlabel">\n'
    '            <span class="pt-xl">10分</span>\n'
    '            <span class="pt-xg" title="YRO">1タイトル ▴</span>\n'
    '          </div>\n'
    '          <div class="pt-xlabel">\n'
    '            <span class="pt-xl">20分</span>\n'
    '            <span class="pt-xg" title="タクタ / シャーロック13 / レフュージ / スシゴー! / アップ・オア・ダウン? / フリップ7 / スカルキング / マウンテンゴーツ / オリフラム / ドラフトサウルス / キャプテン・フリップ / イプソ / こねこばくはつ / 宵と暁の呪文書 / シフティング・ストーンズ / ストーンエイジ / 天下鳴動">17タイトル ▴</span>\n'
    '          </div>'
)

# ── 8-9. 履歴の行番号シフトと新規行挿入（メインタブ限定） ──
# ※4人集計タブにも同形式の行番号があるため、tab-main 内だけを対象にする
marker = '</div><!-- /tab-main -->'
idx = html.index(marker)
main_part, rest_part = html[:idx], html[idx:]

# 8. 行番号シフト 61→66, ..., 1→6
for i in range(61, 0, -1):
    main_part = main_part.replace(
        f'<td>{i}</td><td class="date">',
        f'<td>{i+5}</td><td class="date">'
    )

# 9. 新規履歴行5行を先頭に挿入（新しい順）
new_rows = (
    '\n'
    '      <tr>\n'
    '        <td>1</td><td class="date">2026-07-21<br>（本日）</td>\n'
    '        <td class="game-name"><a href="https://boardgamearena.com/gamepanel?game=orleans" target="_blank" rel="noopener">オルレアン</a><br>'
    '<span style="font-weight:400;color:#999;font-size:.78rem">Orléans</span></td>\n'
    '        <td class="pt-time">90</td>\n'
    '        <td><div class="rank">\n'
    '          <div class="rrow"><span class="badge b1">1位</span><span class="p-a">aohige nagoya</span><span class="score">154pt</span></div>\n'
    '          <div class="rrow"><span class="badge b2">2位</span><span class="p-j">Jin2798</span><span class="score">125pt</span></div>\n'
    '          <div class="rrow"><span class="badge b3">3位</span><span class="p-s">sasuken2999</span><span class="score">116pt</span></div>\n'
    '        </div></td>\n'
    '      </tr>\n'
    '\n'
    '      <tr>\n'
    '        <td>2</td><td class="date">2026-07-21<br>（本日）</td>\n'
    '        <td class="game-name"><a href="https://boardgamearena.com/gamepanel?game=rumblenation" target="_blank" rel="noopener">天下鳴動</a><br>'
    '<span style="font-weight:400;color:#999;font-size:.78rem">Rumble Nation</span></td>\n'
    '        <td class="pt-time">20</td>\n'
    '        <td><div class="rank">\n'
    '          <div class="rrow"><span class="badge b1">1位</span><span class="p-a">aohige nagoya</span><span class="score">38pt</span></div>\n'
    '          <div class="rrow"><span class="badge b2">2位</span><span class="p-j">Jin2798</span><span class="score">34pt</span></div>\n'
    '          <div class="rrow"><span class="badge b3">3位</span><span class="p-s">sasuken2999</span><span class="score">32pt</span></div>\n'
    '        </div></td>\n'
    '      </tr>\n'
    '\n'
    '      <tr>\n'
    '        <td>3</td><td class="date">2026-07-21<br>（本日）</td>\n'
    '        <td class="game-name"><a href="https://boardgamearena.com/gamepanel?game=rumblenation" target="_blank" rel="noopener">天下鳴動</a><br>'
    '<span style="font-weight:400;color:#999;font-size:.78rem">Rumble Nation</span></td>\n'
    '        <td class="pt-time">20</td>\n'
    '        <td><div class="rank">\n'
    '          <div class="rrow"><span class="badge b1">1位</span><span class="p-s">sasuken2999</span><span class="score">43pt</span></div>\n'
    '          <div class="rrow"><span class="badge b2">2位</span><span class="p-j">Jin2798</span><span class="score">34pt</span></div>\n'
    '          <div class="rrow"><span class="badge b3">3位</span><span class="p-a">aohige nagoya</span><span class="score">22pt</span></div>\n'
    '        </div></td>\n'
    '      </tr>\n'
    '\n'
    '      <tr>\n'
    '        <td>4</td><td class="date">2026-07-21<br>（本日）</td>\n'
    '        <td class="game-name"><a href="https://boardgamearena.com/gamepanel?game=yro" target="_blank" rel="noopener">YRO</a><br>'
    '<span style="font-weight:400;color:#999;font-size:.78rem">YRO</span></td>\n'
    '        <td class="pt-time">10</td>\n'
    '        <td><div class="rank">\n'
    '          <div class="rrow"><span class="badge b1">1位</span><span class="p-a">aohige nagoya</span><span class="score">51pt</span></div>\n'
    '          <div class="rrow"><span class="badge b2">2位</span><span class="p-s">sasuken2999</span><span class="score">46pt</span></div>\n'
    '          <div class="rrow"><span class="badge b3">3位</span><span class="p-j">Jin2798</span><span class="score">40pt</span></div>\n'
    '        </div></td>\n'
    '      </tr>\n'
    '\n'
    '      <tr>\n'
    '        <td>5</td><td class="date">2026-07-21<br>（本日）</td>\n'
    '        <td class="game-name"><a href="https://boardgamearena.com/gamepanel?game=yro" target="_blank" rel="noopener">YRO</a><br>'
    '<span style="font-weight:400;color:#999;font-size:.78rem">YRO</span></td>\n'
    '        <td class="pt-time">10</td>\n'
    '        <td><div class="rank">\n'
    '          <div class="rrow"><span class="badge b1">1位</span><span class="p-s">sasuken2999</span><span class="score">47pt</span></div>\n'
    '          <div class="rrow"><span class="badge b2">2位</span><span class="p-a">aohige nagoya</span><span class="score">38pt</span></div>\n'
    '          <div class="rrow"><span class="badge b3">3位</span><span class="p-j">Jin2798</span><span class="score">26pt</span></div>\n'
    '        </div></td>\n'
    '      </tr>\n'
    '\n'
)
main_part = main_part.replace(
    '    <tbody>\n\n      <tr>\n        <td>6</td><td class="date">2026-07-09<br>（12日前）</td>',
    '    <tbody>\n' + new_rows + '      <tr>\n        <td>6</td><td class="date">2026-07-09<br>（12日前）</td>'
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

chk('header 2026-07-21',            '2026-07-21 集計' in h)
chk('total-num 66',                  '<div class="total-num">66</div>' in h)
chk('card-sub 66 x3',               h.count('<div class="card-sub">66戦中</div>') == 3)
chk('sasuken s=21',                 '<span class="rank-count s">21</span>' in h)
chk('sasuken c2=28',                '<span class="rank-count c2">28</span>' in h)
chk('sasuken c3=17',                '<span class="rank-count c3">17</span>' in h)
chk('aohige a=31',                  '<span class="rank-count a">31</span>' in h)
chk('aohige c2=19',                 '<span class="rank-count c2">19</span>' in h)
chk('aohige c3=16',                 '<span class="rank-count c3">16</span>' in h)
chk('Jin j=14',                     '<span class="rank-count j">14</span>' in h)
chk('Jin c2=25',                    '<span class="rank-count c2">25</span>' in h)
chk('Jin c3=27',                    '<span class="rank-count c3">27</span>' in h)
# 各カードの合計が66であること
chk('sum sasuken 21+28+17=66',      21+28+17 == 66)
chk('sum aohige 31+19+16=66',       31+19+16 == 66)
chk('sum Jin 14+25+27=66',          14+25+27 == 66)
# ゲーム別成績
chk('rumblenation in gamestats',    'game=rumblenation" target="_blank" rel="noopener">天下鳴動' in h)
chk('yro in gamestats',             'game=yro" target="_blank" rel="noopener">YRO' in h)
chk('orleans plays=2',              'game=orleans" target="_blank" rel="noopener">オルレアン</a><br><span style="font-weight:400;color:#999;font-size:.75rem">Orléans</span></td>\n        <td>2</td>' in h)
chk('orleans a=2 typo fixed',       '<span class="win-num a">2</span>' in h)
chk('no broken <\\span> typo',      '<\\span>' not in h)
# グラフスケール
chk('yaxis 12 added',               '<span class="pt-yl">12</span>' in h)
chk('yaxis 6 labels',               h.count('<span class="pt-yl">') == 6)
chk('barzone 260px',                'height: 260px; position: relative;' in h)
chk('pt-groups 240px',              'display: flex; height: 240px; align-items: flex-end;' in h)
chk('pt-group 240px',               'gap: 4px; height: 240px; }' in h)
chk('yaxis height 220px',           'padding-top: 0; height: 220px;' in h)
chk('gridline 12 at 20px',          'style="top:20px"  title="12勝ライン"' in h)
chk('gridline 2 at 220px',          'style="top:220px" title="2勝ライン"' in h)
# 棒グラフ
chk('10min bucket added',           '<!-- 10分: s=1(20px), a=1(20px) -->' in h)
chk('20min s=11 220px',             '<!-- 20分: s=11(220px), a=7(140px), j=8(160px) -->' in h)
chk('90min a=10 200px',             '<!-- 90分: s=1(20px), a=10(200px) -->' in h)
chk('no bar exceeds 240px',         'height:260px;background' not in h and 'height:240px;background' not in h)
# X軸
chk('xaxis 10min label',            '<span class="pt-xl">10分</span>' in h)
chk('xaxis 20min 17titles',         '17タイトル' in h and '天下鳴動">17タイトル' in h)
chk('xaxis 10 groups',              h.count('<div class="pt-xlabel">') == 10)
chk('chart 10 groups',              main_h.count('<div class="pt-group">') == 10)
# 履歴
chk('row#1 orleans today',          '<td>1</td><td class="date">2026-07-21<br>（本日）</td>' in main_h)
chk('row#5 yro today',              '<td>5</td><td class="date">2026-07-21<br>（本日）</td>' in main_h)
chk('row#6 = former#1 (07-09)',     '<td>6</td><td class="date">2026-07-09<br>（12日前）</td>' in main_h)
main_rows = len(re.findall(r'<td>\d+</td><td class="date">', main_h))
chk(f'66 main history rows (found {main_rows})', main_rows == 66)
# 4人集計タブが壊れていないこと
four_rows = len(re.findall(r'<td>\d+</td><td class="date">', four_h))
chk(f'4-player tab still 4 rows (found {four_rows})', four_rows == 4)
chk('4-player total unchanged',     '<div class="total-num" id="f-total">4</div>' in four_h)
chk('4-player row#1 intact',        '<td>1</td><td class="date">2026-07-14<br>（7日前）</td>' in four_h)
chk('no old header date',           '2026-07-09 集計' not in h)
chk('no 61 total',                  '<div class="total-num">61</div>' not in h)

print(f'\nResult: {ok} OK / {ng} NG')
