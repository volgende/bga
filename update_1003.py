# -*- coding: utf-8 -*-
import re
from datetime import date, datetime

path = r"bga_results.html"
with open(path, encoding='utf-8') as f:
    html = f.read()

today = date(2026, 10, 3)

# ════════════════════════════════════════════════
# 新規11戦（すべて3人戦・通常集計、放棄2戦は除外）
#  1 タクタ(tacta,20分,既存)          10/03  1sas52/2aohige49/3Jin48    W:sas
#  2 カルヌタ(carnuta,10分,新)         10/03  1sas62/2Jin59/3aohige39    W:sas
#  3 マラケシュ(marrakech,20分,新)     10/03  1Jin49/2sas45/3aohige31    W:Jin
#  4 テラマーズ(terraformingmars,120,既)10/03 1Jin91/2aohige90/3sas77    W:Jin
#  5 ラウハ(rauha,20分,新)             09/18  1aohige125/2sas122/3Jin97  W:aohige
#  6 スペースベース(spacebase,10分,新)  09/08  1Jin44/2aohige29/3sas25    W:Jin
#  7 金庫(vaultdenofthieves,20分,新)    09/08  1sas18/2aohige15/3Jin14    W:sas
#  8 金庫(vaultdenofthieves,20分,新)    09/08  1sas21/2aohige19/3Jin18    W:sas
#  9 リフレクション(laserreflection,20,新)09/08 1sas67/2aohige39/3Jin-39  W:sas
# 10 デワン(dewan,20分,既)             09/08  1sas41/2aohige36/3Jin12    W:sas
# 11 ヘゲモニー(hegemony,100分,新)      09/08  1Jin1/1aohige1(タイ)/3sas0 W:Jin&aohige
# ════════════════════════════════════════════════

# ── 1. ヘッダー日付 ──
html = html.replace('2026-09-04 集計', '2026-10-03 集計')

# ── 2. 相対日付の更新（全タブ対象, today=2026-10-03） ──
def upd_date(m):
    d = datetime.strptime(m.group(1), '%Y-%m-%d').date()
    n = (today - d).days
    label = '本日' if n == 0 else f'{n}日前'
    return f'<td class="date">{m.group(1)}<br>（{label}）</td>'
html = re.sub(r'<td class="date">(\d{4}-\d{2}-\d{2})<br>（[^）]+）</td>', upd_date, html)

# ── 3. プレイヤーカード 88→99 ──
# sasuken 27/34/27 → 33/36/30
html = html.replace('<span class="rank-count s">27</span>', '<span class="rank-count s">33</span>')
html = html.replace('<span class="rank-count c2">34</span>', '<span class="rank-count c2">36</span>')  # sas c2
html = html.replace('<span class="rank-count c3">27</span>', '<span class="rank-count c3">30</span>')  # sas c3
# aohige 39/30/19 → 41/37/21
html = html.replace('<span class="rank-count a">39</span>', '<span class="rank-count a">41</span>')
html = html.replace('<span class="rank-count c2">30</span>', '<span class="rank-count c2">37</span>')  # aohige c2
html = html.replace('<span class="rank-count c3">19</span>', '<span class="rank-count c3">21</span>')  # aohige c3
# Jin 24/31/33 → 28/32/39
html = html.replace('<span class="rank-count j">24</span>', '<span class="rank-count j">28</span>')
html = html.replace('<span class="rank-count c2">31</span>', '<span class="rank-count c2">32</span>')  # Jin c2
html = html.replace('<span class="rank-count c3">33</span>', '<span class="rank-count c3">39</span>')  # Jin c3
# 総数 88→99
html = html.replace('<div class="card-sub">88戦中</div>', '<div class="card-sub">99戦中</div>')
html = html.replace('<div class="total-num">88</div>', '<div class="total-num">99</div>')

# ── 4a. ゲーム別成績: 既存タイトル増分 ──
# タクタ 3→4戦, s2(67%)→3(75%), j1(33%)→1(25%)
html = html.replace(
    '        <td><a href="https://boardgamearena.com/gamepanel?game=tacta" target="_blank" rel="noopener">タクタ</a><br><span style="font-weight:400;color:#999;font-size:.75rem">Tacta</span></td>\n'
    '        <td>3</td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num s">2</span><div class="bar-bg"><div class="bar-fill bar-s" style="width:67%"></div></div></div></td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num a">0</span><div class="bar-bg"></div></div></td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num j">1</span><div class="bar-bg"><div class="bar-fill bar-j" style="width:33%"></div></div></div></td>',
    '        <td><a href="https://boardgamearena.com/gamepanel?game=tacta" target="_blank" rel="noopener">タクタ</a><br><span style="font-weight:400;color:#999;font-size:.75rem">Tacta</span></td>\n'
    '        <td>4</td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num s">3</span><div class="bar-bg"><div class="bar-fill bar-s" style="width:75%"></div></div></div></td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num a">0</span><div class="bar-bg"></div></div></td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num j">1</span><div class="bar-bg"><div class="bar-fill bar-j" style="width:25%"></div></div></div></td>'
)
# テラマーズ 2→3戦, a2(100%)→2(67%), j0→1(33%)
html = html.replace(
    '        <td><a href="https://boardgamearena.com/gamepanel?game=terraformingmars" target="_blank" rel="noopener">テラフォーミング・マーズ</a><br><span style="font-weight:400;color:#999;font-size:.75rem">Terraforming Mars</span></td>\n'
    '        <td>2</td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num s">0</span><div class="bar-bg"></div></div></td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num a">2</span><div class="bar-bg"><div class="bar-fill bar-a" style="width:100%"></div></div></div></td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num j">0</span><div class="bar-bg"></div></div></td>',
    '        <td><a href="https://boardgamearena.com/gamepanel?game=terraformingmars" target="_blank" rel="noopener">テラフォーミング・マーズ</a><br><span style="font-weight:400;color:#999;font-size:.75rem">Terraforming Mars</span></td>\n'
    '        <td>3</td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num s">0</span><div class="bar-bg"></div></div></td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num a">2</span><div class="bar-bg"><div class="bar-fill bar-a" style="width:67%"></div></div></div></td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num j">1</span><div class="bar-bg"><div class="bar-fill bar-j" style="width:33%"></div></div></div></td>'
)
# デワン 1→2戦, s0→1(50%), j1(100%)→1(50%)
html = html.replace(
    '        <td><a href="https://boardgamearena.com/gamepanel?game=dewan" target="_blank" rel="noopener">デワン</a><br><span style="font-weight:400;color:#999;font-size:.75rem">Dewan</span></td>\n'
    '        <td>1</td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num s">0</span><div class="bar-bg"></div></div></td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num a">0</span><div class="bar-bg"></div></div></td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num j">1</span><div class="bar-bg"><div class="bar-fill bar-j" style="width:100%"></div></div></div></td>',
    '        <td><a href="https://boardgamearena.com/gamepanel?game=dewan" target="_blank" rel="noopener">デワン</a><br><span style="font-weight:400;color:#999;font-size:.75rem">Dewan</span></td>\n'
    '        <td>2</td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num s">1</span><div class="bar-bg"><div class="bar-fill bar-s" style="width:50%"></div></div></div></td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num a">0</span><div class="bar-bg"></div></div></td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num j">1</span><div class="bar-bg"><div class="bar-fill bar-j" style="width:50%"></div></div></div></td>'
)

# ── 4b. ゲーム別成績: 新規7タイトルを先頭に追加 ──
def gs_row(slug, jp, en, plays, s, a, j):
    def cell(cls, w):
        if w == 0:
            return f'<td><div class="win-bar-wrap"><span class="win-num {cls}">0</span><div class="bar-bg"></div></div></td>'
        pct = round(w / plays * 100)
        return (f'<td><div class="win-bar-wrap"><span class="win-num {cls}">{w}</span>'
                f'<div class="bar-bg"><div class="bar-fill bar-{cls}" style="width:{pct}%"></div></div></div></td>')
    return (
        '      <tr>\n'
        f'        <td><a href="https://boardgamearena.com/gamepanel?game={slug}" target="_blank" rel="noopener">{jp}</a><br>'
        f'<span style="font-weight:400;color:#999;font-size:.75rem">{en}</span></td>\n'
        f'        <td>{plays}</td>\n'
        f'        {cell("s", s)}\n'
        f'        {cell("a", a)}\n'
        f'        {cell("j", j)}\n'
        '      </tr>\n'
    )
new_gs = (
    gs_row('carnuta', 'カルヌタ', 'Carnuta', 1, 1, 0, 0) +
    gs_row('marrakech', 'マラケシュ', 'Marrakech', 1, 0, 0, 1) +
    gs_row('rauha', 'ラウハ', 'Rauha', 1, 0, 1, 0) +
    gs_row('spacebase', 'スペースベース', 'Space Base', 1, 0, 0, 1) +
    gs_row('vaultdenofthieves', '金庫: 泥棒の巣窟', 'Vault A Den of Thieves', 2, 2, 0, 0) +
    gs_row('laserreflection', 'リフレクション', 'Reflection', 1, 1, 0, 0) +
    gs_row('hegemony', 'ヘゲモニー', 'Hegemony', 1, 0, 1, 1)
)
html = html.replace(
    '    <tbody>\n'
    '      <tr>\n'
    '        <td><a href="https://boardgamearena.com/gamepanel?game=digitcode"',
    '    <tbody>\n'
    + new_gs +
    '      <tr>\n'
    '        <td><a href="https://boardgamearena.com/gamepanel?game=digitcode"'
)

# ── 5. グラフ スケール 14→20 拡張（20px/勝維持） ──
# 5a. CSS
html = html.replace('padding-top: 0; height: 260px; padding-bottom: 0; box-sizing: border-box;',
                    'padding-top: 0; height: 380px; padding-bottom: 0; box-sizing: border-box;')
html = html.replace('height: 300px; position: relative; border-left: 2px solid #ccc;',
                    'height: 420px; position: relative; border-left: 2px solid #ccc;')
html = html.replace('/* gridlines at 2,4,6,8,10,12,14 wins (each 2 wins = 40px) */',
                    '/* gridlines at 2,4,6,8,10,12,14,16,18,20 wins (each 2 wins = 40px) */')
html = html.replace('    display: flex; height: 280px; align-items: flex-end;',
                    '    display: flex; height: 400px; align-items: flex-end;')
html = html.replace('  .pt-group { flex: 1; display: flex; align-items: flex-end; justify-content: center; gap: 4px; height: 280px; }',
                    '  .pt-group { flex: 1; display: flex; align-items: flex-end; justify-content: center; gap: 4px; height: 400px; }')

# 5b. Y軸ラベル 7→10
html = html.replace(
    '      <!-- Y軸ラベル: 上から 14,12,10,8,6,4,2（280px ÷ 7段階 = 40px/段） -->\n'
    '      <div class="pt-yaxis">\n'
    '        <span class="pt-yl">14</span>\n'
    '        <span class="pt-yl">12</span>\n'
    '        <span class="pt-yl">10</span>\n'
    '        <span class="pt-yl">8</span>\n'
    '        <span class="pt-yl">6</span>\n'
    '        <span class="pt-yl">4</span>\n'
    '        <span class="pt-yl">2</span>\n'
    '      </div>',
    '      <!-- Y軸ラベル: 上から 20,18,16,14,12,10,8,6,4,2（400px ÷ 10段階 = 40px/段） -->\n'
    '      <div class="pt-yaxis">\n'
    '        <span class="pt-yl">20</span>\n'
    '        <span class="pt-yl">18</span>\n'
    '        <span class="pt-yl">16</span>\n'
    '        <span class="pt-yl">14</span>\n'
    '        <span class="pt-yl">12</span>\n'
    '        <span class="pt-yl">10</span>\n'
    '        <span class="pt-yl">8</span>\n'
    '        <span class="pt-yl">6</span>\n'
    '        <span class="pt-yl">4</span>\n'
    '        <span class="pt-yl">2</span>\n'
    '      </div>'
)

# 5c. グリッドライン 7→10 (top = 20 + (20-n)*20)
html = html.replace(
    '          <!-- グリッドライン (padding-top:20px 分を加算: top = 20 + (14-n)*20) -->\n'
    '          <div class="pt-gl" style="top:20px"  title="14勝ライン"></div><!-- 14wins -->\n'
    '          <div class="pt-gl" style="top:60px"  title="12勝ライン"></div><!-- 12wins -->\n'
    '          <div class="pt-gl" style="top:100px" title="10勝ライン"></div><!-- 10wins -->\n'
    '          <div class="pt-gl" style="top:140px" title="8勝ライン"></div><!-- 8wins -->\n'
    '          <div class="pt-gl" style="top:180px" title="6勝ライン"></div><!-- 6wins -->\n'
    '          <div class="pt-gl" style="top:220px" title="4勝ライン"></div><!-- 4wins -->\n'
    '          <div class="pt-gl" style="top:260px" title="2勝ライン"></div><!-- 2wins -->',
    '          <!-- グリッドライン (padding-top:20px 分を加算: top = 20 + (20-n)*20) -->\n'
    '          <div class="pt-gl" style="top:20px"  title="20勝ライン"></div><!-- 20wins -->\n'
    '          <div class="pt-gl" style="top:60px"  title="18勝ライン"></div><!-- 18wins -->\n'
    '          <div class="pt-gl" style="top:100px" title="16勝ライン"></div><!-- 16wins -->\n'
    '          <div class="pt-gl" style="top:140px" title="14勝ライン"></div><!-- 14wins -->\n'
    '          <div class="pt-gl" style="top:180px" title="12勝ライン"></div><!-- 12wins -->\n'
    '          <div class="pt-gl" style="top:220px" title="10勝ライン"></div><!-- 10wins -->\n'
    '          <div class="pt-gl" style="top:260px" title="8勝ライン"></div><!-- 8wins -->\n'
    '          <div class="pt-gl" style="top:300px" title="6勝ライン"></div><!-- 6wins -->\n'
    '          <div class="pt-gl" style="top:340px" title="4勝ライン"></div><!-- 4wins -->\n'
    '          <div class="pt-gl" style="top:380px" title="2勝ライン"></div><!-- 2wins -->'
)

# 5d. バー更新
# 10分: s3→4(80), j2→3(60)
html = html.replace(
    '            <!-- 10分: s=3(60px), a=2(40px), j=2(40px) -->\n'
    '            <div class="pt-group">\n'
    '              <div class="pt-bar bar-s" style="height:60px;background:var(--s)" title="sasuken2999: 3勝"><span class="pt-n">3</span></div>\n'
    '              <div class="pt-bar bar-a" style="height:40px;background:var(--a)" title="aohige nagoya: 2勝"><span class="pt-n">2</span></div>\n'
    '              <div class="pt-bar bar-j" style="height:40px;background:var(--j)" title="Jin2798: 2勝"><span class="pt-n">2</span></div>\n'
    '            </div>',
    '            <!-- 10分: s=4(80px), a=2(40px), j=3(60px) -->\n'
    '            <div class="pt-group">\n'
    '              <div class="pt-bar bar-s" style="height:80px;background:var(--s)" title="sasuken2999: 4勝"><span class="pt-n">4</span></div>\n'
    '              <div class="pt-bar bar-a" style="height:40px;background:var(--a)" title="aohige nagoya: 2勝"><span class="pt-n">2</span></div>\n'
    '              <div class="pt-bar bar-j" style="height:60px;background:var(--j)" title="Jin2798: 3勝"><span class="pt-n">3</span></div>\n'
    '            </div>'
)
# 20分: s14→19(380), a10→11(220), j12→13(260)
html = html.replace(
    '            <!-- 20分: s=14(280px), a=10(200px), j=12(240px) -->\n'
    '            <div class="pt-group">\n'
    '              <div class="pt-bar bar-s" style="height:280px;background:var(--s)" title="sasuken2999: 14勝"><span class="pt-n">14</span></div>\n'
    '              <div class="pt-bar bar-a" style="height:200px;background:var(--a)" title="aohige nagoya: 10勝"><span class="pt-n">10</span></div>\n'
    '              <div class="pt-bar bar-j" style="height:240px;background:var(--j)" title="Jin2798: 12勝"><span class="pt-n">12</span></div>\n'
    '            </div>',
    '            <!-- 20分: s=19(380px), a=11(220px), j=13(260px) -->\n'
    '            <div class="pt-group">\n'
    '              <div class="pt-bar bar-s" style="height:380px;background:var(--s)" title="sasuken2999: 19勝"><span class="pt-n">19</span></div>\n'
    '              <div class="pt-bar bar-a" style="height:220px;background:var(--a)" title="aohige nagoya: 11勝"><span class="pt-n">11</span></div>\n'
    '              <div class="pt-bar bar-j" style="height:260px;background:var(--j)" title="Jin2798: 13勝"><span class="pt-n">13</span></div>\n'
    '            </div>'
)
# 100分: j1→2(40), aohige新規1(20)
html = html.replace(
    '            <!-- 100分: j=1(20px) -->\n'
    '            <div class="pt-group">\n'
    '              <div class="pt-bar bar-j" style="height:20px;background:var(--j)" title="Jin2798: 1勝"><span class="pt-n">1</span></div>\n'
    '            </div>',
    '            <!-- 100分: a=1(20px), j=2(40px) -->\n'
    '            <div class="pt-group">\n'
    '              <div class="pt-bar bar-a" style="height:20px;background:var(--a)" title="aohige nagoya: 1勝"><span class="pt-n">1</span></div>\n'
    '              <div class="pt-bar bar-j" style="height:40px;background:var(--j)" title="Jin2798: 2勝"><span class="pt-n">2</span></div>\n'
    '            </div>'
)
# 120分: aohige2(40)維持, Jin新規1(20)
html = html.replace(
    '            <!-- 120分: a=2(40px) -->\n'
    '            <div class="pt-group">\n'
    '              <div class="pt-bar bar-a" style="height:40px;background:var(--a)" title="aohige nagoya: 2勝"><span class="pt-n">2</span></div>\n'
    '            </div>',
    '            <!-- 120分: a=2(40px), j=1(20px) -->\n'
    '            <div class="pt-group">\n'
    '              <div class="pt-bar bar-a" style="height:40px;background:var(--a)" title="aohige nagoya: 2勝"><span class="pt-n">2</span></div>\n'
    '              <div class="pt-bar bar-j" style="height:20px;background:var(--j)" title="Jin2798: 1勝"><span class="pt-n">1</span></div>\n'
    '            </div>'
)

# ── 6. X軸ラベル ──
# 10分 4→6
html = html.replace(
    '<span class="pt-xg" title="YRO / レース・フォー・ザ・ギャラクシー / ディジットコード / ディギング・フォー・ダイノス">4タイトル ▴</span>',
    '<span class="pt-xg" title="YRO / レース・フォー・ザ・ギャラクシー / ディジットコード / ディギング・フォー・ダイノス / カルヌタ / スペースベース">6タイトル ▴</span>'
)
# 20分 21→25
html = html.replace(
    '/ ベジタブルストック / 郵便馬車 / クィブルス / デワン">21タイトル ▴</span>',
    '/ ベジタブルストック / 郵便馬車 / クィブルス / デワン / マラケシュ / ラウハ / 金庫: 泥棒の巣窟 / リフレクション">25タイトル ▴</span>'
)
# 100分 1→2
html = html.replace(
    '<span class="pt-xg" title="テラミスティカ：革新の時代">1タイトル ▴</span>',
    '<span class="pt-xg" title="テラミスティカ：革新の時代 / ヘゲモニー">2タイトル ▴</span>'
)

# ── 7-8. メイン履歴 シフト＋挿入 ──
marker = '</div><!-- /tab-main -->'
idx = html.index(marker)
main_part, rest_part = html[:idx], html[idx:]

# 7. 行番号シフト 88→99, ..., 1→12
for i in range(88, 0, -1):
    main_part = main_part.replace(
        f'<td>{i}</td><td class="date">',
        f'<td>{i+11}</td><td class="date">'
    )

# 8. 新規履歴行11行を先頭に挿入
def rrow(badge, cls, name, score):
    return f'          <div class="rrow"><span class="badge {badge}">{badge[-1]}位</span><span class="p-{cls}">{name}</span><span class="score">{score}pt</span></div>\n'

def hist_row(num, dstr, dlabel, slug, jp, en, minutes, ranks):
    # ranks: list of (badge, cls, name, score)
    rows = ''.join(rrow(*r) for r in ranks)
    return (
        '\n'
        '      <tr>\n'
        f'        <td>{num}</td><td class="date">{dstr}<br>（{dlabel}）</td>\n'
        f'        <td class="game-name"><a href="https://boardgamearena.com/gamepanel?game={slug}" target="_blank" rel="noopener">{jp}</a><br>'
        f'<span style="font-weight:400;color:#999;font-size:.78rem">{en}</span></td>\n'
        f'        <td class="pt-time">{minutes}</td>\n'
        '        <td><div class="rank">\n'
        f'{rows}'
        '        </div></td>\n'
        '      </tr>\n'
    )

S=('p? ','s','sasuken2999'); # placeholder, use explicit below
new_rows = (
    hist_row(1, '2026-10-03','本日','tacta','タクタ','Tacta',20,
             [('b1','s','sasuken2999','52'),('b2','a','aohige nagoya','49'),('b3','j','Jin2798','48')]) +
    hist_row(2, '2026-10-03','本日','carnuta','カルヌタ','Carnuta',10,
             [('b1','s','sasuken2999','62'),('b2','j','Jin2798','59'),('b3','a','aohige nagoya','39')]) +
    hist_row(3, '2026-10-03','本日','marrakech','マラケシュ','Marrakech',20,
             [('b1','j','Jin2798','49'),('b2','s','sasuken2999','45'),('b3','a','aohige nagoya','31')]) +
    hist_row(4, '2026-10-03','本日','terraformingmars','テラフォーミング・マーズ','Terraforming Mars',120,
             [('b1','j','Jin2798','91'),('b2','a','aohige nagoya','90'),('b3','s','sasuken2999','77')]) +
    hist_row(5, '2026-09-18','15日前','rauha','ラウハ','Rauha',20,
             [('b1','a','aohige nagoya','125'),('b2','s','sasuken2999','122'),('b3','j','Jin2798','97')]) +
    hist_row(6, '2026-09-08','25日前','spacebase','スペースベース','Space Base',10,
             [('b1','j','Jin2798','44'),('b2','a','aohige nagoya','29'),('b3','s','sasuken2999','25')]) +
    hist_row(7, '2026-09-08','25日前','vaultdenofthieves','金庫: 泥棒の巣窟','Vault A Den of Thieves',20,
             [('b1','s','sasuken2999','18'),('b2','a','aohige nagoya','15'),('b3','j','Jin2798','14')]) +
    hist_row(8, '2026-09-08','25日前','vaultdenofthieves','金庫: 泥棒の巣窟','Vault A Den of Thieves',20,
             [('b1','s','sasuken2999','21'),('b2','a','aohige nagoya','19'),('b3','j','Jin2798','18')]) +
    hist_row(9, '2026-09-08','25日前','laserreflection','リフレクション','Reflection',20,
             [('b1','s','sasuken2999','67'),('b2','a','aohige nagoya','39'),('b3','j','Jin2798','-39')]) +
    hist_row(10, '2026-09-08','25日前','dewan','デワン','Dewan',20,
             [('b1','s','sasuken2999','41'),('b2','a','aohige nagoya','36'),('b3','j','Jin2798','12')]) +
    hist_row(11, '2026-09-08','25日前','hegemony','ヘゲモニー','Hegemony',100,
             [('b1','j','Jin2798','1'),('b1','a','aohige nagoya','1'),('b3','s','sasuken2999','0')])
)

main_part = main_part.replace(
    '    <tbody>\n\n      <tr>\n        <td>12</td><td class="date">2026-09-04<br>（29日前）</td>',
    '    <tbody>\n' + new_rows + '      <tr>\n        <td>12</td><td class="date">2026-09-04<br>（29日前）</td>'
)

html = main_part + rest_part

with open(path, 'w', encoding='utf-8') as f:
    f.write(html)
print("Done!")

# ════════ 検証 ════════
with open(path, encoding='utf-8') as f:
    h = f.read()
main_h = h[:h.index(marker)]
rest_h = h[h.index(marker):]
ok = ng = 0
def chk(name, cond):
    global ok, ng
    if cond: ok += 1; print(f'OK {name}')
    else:    ng += 1; print(f'NG {name}')

chk('header 2026-10-03', '2026-10-03 集計' in h)
chk('no old header 09-04', '2026-09-04 集計' not in h)
chk('total-num 99', '<div class="total-num">99</div>' in h)
chk('card-sub 99 x3', h.count('<div class="card-sub">99戦中</div>') == 3)
chk('sas s=33', '<span class="rank-count s">33</span>' in h)
chk('sas c2=36', '<span class="rank-count c2">36</span>' in h)
chk('sas c3=30', '<span class="rank-count c3">30</span>' in h)
chk('aohige a=41', '<span class="rank-count a">41</span>' in h)
chk('aohige c2=37', '<span class="rank-count c2">37</span>' in h)
chk('aohige c3=21', '<span class="rank-count c3">21</span>' in h)
chk('Jin j=28', '<span class="rank-count j">28</span>' in h)
chk('Jin c2=32', '<span class="rank-count c2">32</span>' in h)
chk('Jin c3=39', '<span class="rank-count c3">39</span>' in h)
chk('sum sas 33+36+30=99', 33+36+30==99)
chk('sum aohige 41+37+21=99', 41+37+21==99)
chk('sum Jin 28+32+39=99', 28+32+39==99)
chk('no stale s=27 card', '<span class="rank-count s">27</span>' not in h)
# 新規タイトル game-stats
for slug,jp in [('carnuta','カルヌタ'),('marrakech','マラケシュ'),('rauha','ラウハ'),('spacebase','スペースベース'),('vaultdenofthieves','金庫: 泥棒の巣窟'),('laserreflection','リフレクション'),('hegemony','ヘゲモニー')]:
    chk(f'gs {slug}', f'game={slug}" target="_blank" rel="noopener">{jp}' in h)
# 既存増分
chk('gs tacta plays4', 'game=tacta" target="_blank" rel="noopener">タクタ</a><br><span style="font-weight:400;color:#999;font-size:.75rem">Tacta</span></td>\n        <td>4</td>' in h)
chk('gs terra plays3', 'game=terraformingmars" target="_blank" rel="noopener">テラフォーミング・マーズ</a><br><span style="font-weight:400;color:#999;font-size:.75rem">Terraforming Mars</span></td>\n        <td>3</td>' in h)
chk('gs dewan plays2', 'game=dewan" target="_blank" rel="noopener">デワン</a><br><span style="font-weight:400;color:#999;font-size:.75rem">Dewan</span></td>\n        <td>2</td>' in h)
chk('vault plays=2 in gs', 'Vault A Den of Thieves</span></td>\n        <td>2</td>' in h)
# スケール
chk('yaxis 20 added', '<span class="pt-yl">20</span>' in h)
chk('yaxis 10 labels', h.count('<span class="pt-yl">') == 10)
chk('barzone 420px', 'height: 420px; position: relative;' in h)
chk('pt-groups 400px', 'display: flex; height: 400px; align-items: flex-end;' in h)
chk('pt-group 400px', 'gap: 4px; height: 400px; }' in h)
chk('yaxis height 380px', 'padding-top: 0; height: 380px;' in h)
chk('gl 20 at top20', 'style="top:20px"  title="20勝ライン"' in h)
chk('gl 2 at 380', 'style="top:380px" title="2勝ライン"' in h)
chk('gl count 10', h.count('class="pt-gl"') == 10)
# バー
chk('20min s=19 380', '<!-- 20分: s=19(380px), a=11(220px), j=13(260px) -->' in h)
chk('10min s=4', '<!-- 10分: s=4(80px), a=2(40px), j=3(60px) -->' in h)
chk('100min a1 j2', '<!-- 100分: a=1(20px), j=2(40px) -->' in h)
chk('120min a2 j1', '<!-- 120分: a=2(40px), j=1(20px) -->' in h)
chk('no bar over 400px', 'height:420px;background' not in h and 'height:400px;background' not in h)
# バー勝利数合計 = 1位数
def bar_sum(cls):
    return sum(int(x) for x in re.findall(r'pt-bar '+cls+r'[^>]*title="[^"]*: (\d+)勝"', h))
chk('bar sum sas=33', bar_sum('bar-s')==33)
chk('bar sum aohige=41', bar_sum('bar-a')==41)
chk('bar sum Jin=28', bar_sum('bar-j')==28)
# X軸
chk('x10 6titles', 'スペースベース">6タイトル' in h)
chk('x20 25titles', 'リフレクション">25タイトル' in h)
chk('x100 2titles', 'ヘゲモニー">2タイトル' in h)
# 履歴
chk('row1 tacta today', '<td>1</td><td class="date">2026-10-03<br>（本日）</td>' in main_h)
chk('row5 rauha 15d', '<td>5</td><td class="date">2026-09-18<br>（15日前）</td>' in main_h)
chk('row11 hegemony 25d', '<td>11</td><td class="date">2026-09-08<br>（25日前）</td>' in main_h)
chk('row12 former1 09-04', '<td>12</td><td class="date">2026-09-04<br>（29日前）</td>' in main_h)
chk('hegemony tie two b1', main_h.count('<span class="badge b1">1位</span><span class="p-j">Jin2798</span><span class="score">1pt</span>')==1 and main_h.count('<span class="badge b1">1位</span><span class="p-a">aohige nagoya</span><span class="score">1pt</span>')==1)
mr = len(re.findall(r'<td>\d+</td><td class="date">', main_h))
chk(f'99 main rows (found {mr})', mr == 99)
fr = len(re.findall(r'<td>\d+</td><td class="date">', rest_h[rest_h.index('/tab-shinken'):]))
chk(f'post-shinken rows=4 (found {fr})', fr == 4)
chk('shinken 2 rows', h.count('class="shinken-num"') == 2)
print(f'\nResult: {ok} OK / {ng} NG')
