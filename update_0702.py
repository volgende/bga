import re
from datetime import date, datetime

path = r"bga_results.html"
with open(path, encoding='utf-8') as f:
    html = f.read()

today = date(2026, 7, 2)

# ── 1. ヘッダー日付更新 ──
html = html.replace('2026-06-25 集計', '2026-07-02 集計')

# ── 2. 相対日付の更新 ──
def upd_date(m):
    d = datetime.strptime(m.group(1), '%Y-%m-%d').date()
    n = (today - d).days
    label = '本日' if n == 0 else f'{n}日前'
    return f'<td class="date">{m.group(1)}<br>（{label}）</td>'
html = re.sub(r'<td class="date">(\d{4}-\d{2}-\d{2})<br>（[^）]+）</td>', upd_date, html)

# ── 3. プレイヤーカード更新 ──
# sasuken: 1位 16→18 (シフティング2試合)
html = html.replace('<span class="rank-count s">16</span>', '<span class="rank-count s">18</span>')
# sasuken: 2位 25→26 (アグリコラ以外の2位 ※シフティング2はsasuken 2位)
html = html.replace('<span class="rank-count c2">25</span>', '<span class="rank-count c2">26</span>')
# aohige: 1位 26→27 (シフティング2)
html = html.replace('<span class="rank-count a">26</span>', '<span class="rank-count a">27</span>')
# aohige: 2位 16→17 (シフティング1)
html = html.replace('<span class="rank-count c2">16</span>', '<span class="rank-count c2">17</span>')
# aohige: 3位 14→15 (アグリコラ)
html = html.replace('<span class="rank-count c3">14</span>', '<span class="rank-count c3">15</span>')
# Jin: 2位 21→22 (アグリコラ)
html = html.replace('<span class="rank-count c2">21</span>', '<span class="rank-count c2">22</span>')
# Jin: 3位 21→23 (シフティング2試合)
html = html.replace('<span class="rank-count c3">21</span>', '<span class="rank-count c3">23</span>')
# 総対戦数 56→59
html = html.replace('<div class="card-sub">56戦中</div>', '<div class="card-sub">59戦中</div>')
html = html.replace('<div class="total-num">56</div>', '<div class="total-num">59</div>')

# ── 4. ゲーム別成績: 新ゲーム2タイトルを先頭に追加 ──
new_game_rows = (
    '      <tr>\n'
    '        <td><a href="https://boardgamearena.com/gamepanel?game=shiftingstones" target="_blank" rel="noopener">シフティング・ストーンズ</a><br>'
    '<span style="font-weight:400;color:#999;font-size:.75rem">Shifting Stones</span></td>\n'
    '        <td>2</td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num s">1</span><div class="bar-bg"><div class="bar-fill bar-s" style="width:50%"></div></div></div></td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num a">1</span><div class="bar-bg"><div class="bar-fill bar-a" style="width:50%"></div></div></div></td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num j">0</span><div class="bar-bg"></div></div></td>\n'
    '      </tr>\n'
    '      <tr>\n'
    '        <td><a href="https://boardgamearena.com/gamepanel?game=agricola" target="_blank" rel="noopener">アグリコラ</a><br>'
    '<span style="font-weight:400;color:#999;font-size:.75rem">Agricola</span></td>\n'
    '        <td>1</td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num s">1</span><div class="bar-bg"><div class="bar-fill bar-s" style="width:100%"></div></div></div></td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num a">0</span><div class="bar-bg"></div></div></td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num j">0</span><div class="bar-bg"></div></div></td>\n'
    '      </tr>\n'
)
html = html.replace(
    '    <tbody>\n'
    '      <tr>\n'
    '        <td><a href="https://boardgamearena.com/gamepanel?game=marcopolotwo"',
    '    <tbody>\n'
    + new_game_rows +
    '      <tr>\n'
    '        <td><a href="https://boardgamearena.com/gamepanel?game=marcopolotwo"'
)

# ── 5. 棒グラフ更新 ──
# 20分: s=9→10(200px), a=4→5(100px) (シフティング2試合)
html = html.replace(
    '            <!-- 20分: s=9(180px), a=4(80px), j=8(160px) -->\n'
    '            <div class="pt-group">\n'
    '              <div class="pt-bar bar-s" style="height:180px;background:var(--s)" title="sasuken2999: 9勝"><span class="pt-n">9</span></div>\n'
    '              <div class="pt-bar bar-a" style="height:80px;background:var(--a)" title="aohige nagoya: 4勝"><span class="pt-n">4</span></div>\n'
    '              <div class="pt-bar bar-j" style="height:160px;background:var(--j)" title="Jin2798: 8勝"><span class="pt-n">8</span></div>\n'
    '            </div>',
    '            <!-- 20分: s=10(200px), a=5(100px), j=8(160px) -->\n'
    '            <div class="pt-group">\n'
    '              <div class="pt-bar bar-s" style="height:200px;background:var(--s)" title="sasuken2999: 10勝"><span class="pt-n">10</span></div>\n'
    '              <div class="pt-bar bar-a" style="height:100px;background:var(--a)" title="aohige nagoya: 5勝"><span class="pt-n">5</span></div>\n'
    '              <div class="pt-bar bar-j" style="height:160px;background:var(--j)" title="Jin2798: 8勝"><span class="pt-n">8</span></div>\n'
    '            </div>'
)

# 50分: s=2→3(60px) (アグリコラでsasuken 1位)
html = html.replace(
    '            <!-- 50分: s=2(40px), a=2(40px) -->\n'
    '            <div class="pt-group">\n'
    '              <div class="pt-bar bar-s" style="height:40px;background:var(--s)" title="sasuken2999: 2勝"><span class="pt-n">2</span></div>\n'
    '              <div class="pt-bar bar-a" style="height:40px;background:var(--a)" title="aohige nagoya: 2勝"><span class="pt-n">2</span></div>\n'
    '            </div>',
    '            <!-- 50分: s=3(60px), a=2(40px) -->\n'
    '            <div class="pt-group">\n'
    '              <div class="pt-bar bar-s" style="height:60px;background:var(--s)" title="sasuken2999: 3勝"><span class="pt-n">3</span></div>\n'
    '              <div class="pt-bar bar-a" style="height:40px;background:var(--a)" title="aohige nagoya: 2勝"><span class="pt-n">2</span></div>\n'
    '            </div>'
)

# ── 6. X軸ラベル更新 ──
# 20分: 14→15タイトル (シフティング・ストーンズ追加)
html = html.replace(
    '<span class="pt-xg" title="タクタ / シャーロック13 / レフュージ / スシゴー! / アップ・オア・ダウン? / フリップ7 / スカルキング / マウンテンゴーツ / オリフラム / ドラフトサウルス / キャプテン・フリップ / イプソ / こねこばくはつ / 宵と暁の呪文書">14タイトル ▴</span>',
    '<span class="pt-xg" title="タクタ / シャーロック13 / レフュージ / スシゴー! / アップ・オア・ダウン? / フリップ7 / スカルキング / マウンテンゴーツ / オリフラム / ドラフトサウルス / キャプテン・フリップ / イプソ / こねこばくはつ / 宵と暁の呪文書 / シフティング・ストーンズ">15タイトル ▴</span>'
)
# 50分: 2→3タイトル (アグリコラ追加)
html = html.replace(
    '<span class="pt-xg" title="チャレンジャーズ! / ダーウィンズ・ジャーニー">2タイトル ▴</span>',
    '<span class="pt-xg" title="チャレンジャーズ! / ダーウィンズ・ジャーニー / アグリコラ">3タイトル ▴</span>'
)

# ── 7. 履歴行番号シフト 56→59, ..., 1→4 ──
for i in range(56, 0, -1):
    html = html.replace(
        f'<td>{i}</td><td class="date">',
        f'<td>{i+3}</td><td class="date">'
    )

# ── 8. 新規履歴行3行を先頭に挿入 ──
new_rows = (
    '\n'
    '      <tr>\n'
    '        <td>1</td><td class="date">2026-06-30<br>（2日前）</td>\n'
    '        <td class="game-name"><a href="https://boardgamearena.com/gamepanel?game=shiftingstones" target="_blank" rel="noopener">シフティング・ストーンズ</a><br>'
    '<span style="font-weight:400;color:#999;font-size:.78rem">Shifting Stones</span></td>\n'
    '        <td class="pt-time">20</td>\n'
    '        <td><div class="rank">\n'
    '          <div class="rrow"><span class="badge b1">1位</span><span class="p-s">sasuken2999</span><span class="score">19pt</span></div>\n'
    '          <div class="rrow"><span class="badge b2">2位</span><span class="p-a">aohige nagoya</span><span class="score">16pt</span></div>\n'
    '          <div class="rrow"><span class="badge b3">3位</span><span class="p-j">Jin2798</span><span class="score">15pt</span></div>\n'
    '        </div></td>\n'
    '      </tr>\n'
    '\n'
    '      <tr>\n'
    '        <td>2</td><td class="date">2026-06-30<br>（2日前）</td>\n'
    '        <td class="game-name"><a href="https://boardgamearena.com/gamepanel?game=shiftingstones" target="_blank" rel="noopener">シフティング・ストーンズ</a><br>'
    '<span style="font-weight:400;color:#999;font-size:.78rem">Shifting Stones</span></td>\n'
    '        <td class="pt-time">20</td>\n'
    '        <td><div class="rank">\n'
    '          <div class="rrow"><span class="badge b1">1位</span><span class="p-a">aohige nagoya</span><span class="score">16pt</span></div>\n'
    '          <div class="rrow"><span class="badge b2">2位</span><span class="p-s">sasuken2999</span><span class="score">12pt</span></div>\n'
    '          <div class="rrow"><span class="badge b3">3位</span><span class="p-j">Jin2798</span><span class="score">10pt</span></div>\n'
    '        </div></td>\n'
    '      </tr>\n'
    '\n'
    '      <tr>\n'
    '        <td>3</td><td class="date">2026-06-30<br>（2日前）</td>\n'
    '        <td class="game-name"><a href="https://boardgamearena.com/gamepanel?game=agricola" target="_blank" rel="noopener">アグリコラ</a><br>'
    '<span style="font-weight:400;color:#999;font-size:.78rem">Agricola</span></td>\n'
    '        <td class="pt-time">50</td>\n'
    '        <td><div class="rank">\n'
    '          <div class="rrow"><span class="badge b1">1位</span><span class="p-s">sasuken2999</span><span class="score">34pt</span></div>\n'
    '          <div class="rrow"><span class="badge b2">2位</span><span class="p-j">Jin2798</span><span class="score">27pt</span></div>\n'
    '          <div class="rrow"><span class="badge b3">3位</span><span class="p-a">aohige nagoya</span><span class="score">26pt</span></div>\n'
    '        </div></td>\n'
    '      </tr>\n'
    '\n'
)
html = html.replace(
    '    <tbody>\n\n      <tr>\n        <td>4</td><td class="date">2026-06-25<br>（7日前）</td>',
    '    <tbody>\n' + new_rows + '      <tr>\n        <td>4</td><td class="date">2026-06-25<br>（7日前）</td>'
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

chk('header 2026-07-02',           '2026-07-02 集計' in h)
chk('total-num 59',                 '<div class="total-num">59</div>' in h)
chk('card-sub 59 x3',              h.count('<div class="card-sub">59戦中</div>') == 3)
chk('sasuken s=18',                '<span class="rank-count s">18</span>' in h)
chk('sasuken c2=26',               '<span class="rank-count c2">26</span>' in h)
chk('sasuken c3=15',               '<span class="rank-count c3">15</span>' in h)
chk('aohige a=27',                 '<span class="rank-count a">27</span>' in h)
chk('aohige c2=17',                '<span class="rank-count c2">17</span>' in h)
chk('aohige c3=15',                '<span class="rank-count c3">15</span>' in h)
chk('Jin j=14',                    '<span class="rank-count j">14</span>' in h)
chk('Jin c2=22',                   '<span class="rank-count c2">22</span>' in h)
chk('Jin c3=23',                   '<span class="rank-count c3">23</span>' in h)
chk('shiftingstones in gamestats', 'game=shiftingstones' in h)
chk('agricola in gamestats',       'game=agricola' in h)
chk('20min s=10 200px',            '<!-- 20分: s=10(200px), a=5(100px), j=8(160px) -->' in h)
chk('50min s=3 60px',              '<!-- 50分: s=3(60px), a=2(40px) -->' in h)
chk('20min 15titles',              '15タイトル' in h and 'シフティング・ストーンズ' in h)
chk('50min 3titles',               '3タイトル' in h and 'アグリコラ' in h)
chk('row#1 shifting 06-30',        '<td>1</td><td class="date">2026-06-30<br>（2日前）</td>' in h)
chk('row#2 shifting 06-30',        '<td>2</td><td class="date">2026-06-30<br>（2日前）</td>' in h)
chk('row#3 agricola 06-30',        '<td>3</td><td class="date">2026-06-30<br>（2日前）</td>' in h)
chk('row#4 = former#1 (06-25)',    '<td>4</td><td class="date">2026-06-25<br>（7日前）</td>' in h)
row_count = len(__import__('re').findall(r'<td>\d+</td><td class="date">', h))
chk(f'59 history rows (found {row_count})', row_count == 59)
chk('no old header date',          '2026-06-25 集計' not in h)
chk('no 56 total',                 '<div class="total-num">56</div>' not in h)

print(f'\nResult: {ok} OK / {ng} NG')
