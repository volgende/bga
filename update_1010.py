# -*- coding: utf-8 -*-
import re
from datetime import date, datetime

path = r"bga_results.html"
with open(path, encoding='utf-8') as f:
    html = f.read()

today = date(2026, 10, 10)

# ════════════════════════════════════════════════
# 新規3戦（すべて本日 2026-10-10）
#  G1 フォレストシャッフル:スモーキーマウンテン(forestshufflesmokymountains,30分) 4人戦(nacchi含む)
#     1位nacchi165/2位aohige159/3位sasuken158/4位Jin127
#     → メイン: 3人相対順位 aohige1/sas2/Jin3 で集計(注記付き)。4人集計にも反映(nacchi非カード)
#  G2 フォレストシャッフル:スモーキーマウンテン(30分) 3人戦 1位sas71/2位aohige53/3位Jin50
#  G3 アルティメット・レールロード(ultimaterailroads,40分) 3人戦 1位aohige346/2位sas313/3位Jin232
# ════════════════════════════════════════════════

# ── 1. ヘッダー日付 ──
html = html.replace('2026-10-03 集計', '2026-10-10 集計')

# ── 2. 相対日付の更新（全タブ, today=2026-10-10） ──
def upd_date(m):
    d = datetime.strptime(m.group(1), '%Y-%m-%d').date()
    n = (today - d).days
    label = '本日' if n == 0 else f'{n}日前'
    return f'<td class="date">{m.group(1)}<br>（{label}）</td>'
html = re.sub(r'<td class="date">(\d{4}-\d{2}-\d{2})<br>（[^）]+）</td>', upd_date, html)

# ── 3. メインプレイヤーカード 99→102 ──
# G1(4人→3人投影): aohige1/sas2/Jin3  G2: sas1/aohige2/Jin3  G3: aohige1/sas2/Jin3
# sasuken 33/36/30 → 34/38/30  (1位+1:G2, 2位+2:G1,G3)
html = html.replace('<span class="rank-count s">33</span>', '<span class="rank-count s">34</span>')
html = html.replace('<span class="rank-count c2">36</span>', '<span class="rank-count c2">38</span>')  # sas c2
# aohige 41/37/21 → 43/38/21  (1位+2:G1,G3, 2位+1:G2)
html = html.replace('<span class="rank-count a">41</span>', '<span class="rank-count a">43</span>')
html = html.replace('<span class="rank-count c2">37</span>', '<span class="rank-count c2">38</span>')  # aohige c2
# Jin 28/32/39 → 28/32/42  (3位+3:G1,G2,G3)
html = html.replace('<span class="rank-count c3">39</span>', '<span class="rank-count c3">42</span>')  # Jin c3
# 総数 99→102
html = html.replace('<div class="card-sub">99戦中</div>', '<div class="card-sub">102戦中</div>')
html = html.replace('<div class="total-num">99</div>', '<div class="total-num">102</div>')

# ── 4. メイン ゲーム別成績: 新規2タイトル先頭追加 ──
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
        f'        {cell("s", s)}\n        {cell("a", a)}\n        {cell("j", j)}\n'
        '      </tr>\n'
    )
new_gs = (
    gs_row('forestshufflesmokymountains', 'フォレストシャッフル: スモーキーマウンテン', 'Forest Shuffle: Smoky Mountains', 2, 1, 1, 0) +
    gs_row('ultimaterailroads', 'アルティメット・レールロード', 'Ultimate Railroads', 1, 0, 1, 0)
)
_gs_anchor = '    <tbody>\n      <tr>\n        <td><a href="https://boardgamearena.com/gamepanel?game=carnuta"'
assert html.count(_gs_anchor) == 1, f"gs anchor count={html.count(_gs_anchor)}"
html = html.replace(_gs_anchor, '    <tbody>\n' + new_gs + '      <tr>\n        <td><a href="https://boardgamearena.com/gamepanel?game=carnuta"')

# ── 5. メイン棒グラフ（スケール20のまま変更なし） ──
# 30分: s1→2(40px), a7→8(160px)  (G2:sas, G1:aohige)
html = html.replace(
    '            <!-- 30分: s=1(20px), a=7(140px), j=4(80px) -->\n'
    '            <div class="pt-group">\n'
    '              <div class="pt-bar bar-s" style="height:20px;background:var(--s)" title="sasuken2999: 1勝"><span class="pt-n">1</span></div>\n'
    '              <div class="pt-bar bar-a" style="height:140px;background:var(--a)" title="aohige nagoya: 7勝"><span class="pt-n">7</span></div>\n'
    '              <div class="pt-bar bar-j" style="height:80px;background:var(--j)" title="Jin2798: 4勝"><span class="pt-n">4</span></div>\n'
    '            </div>',
    '            <!-- 30分: s=2(40px), a=8(160px), j=4(80px) -->\n'
    '            <div class="pt-group">\n'
    '              <div class="pt-bar bar-s" style="height:40px;background:var(--s)" title="sasuken2999: 2勝"><span class="pt-n">2</span></div>\n'
    '              <div class="pt-bar bar-a" style="height:160px;background:var(--a)" title="aohige nagoya: 8勝"><span class="pt-n">8</span></div>\n'
    '              <div class="pt-bar bar-j" style="height:80px;background:var(--j)" title="Jin2798: 4勝"><span class="pt-n">4</span></div>\n'
    '            </div>'
)
# 40分: a3→4(80px)  (G3:aohige)
html = html.replace(
    '            <!-- 40分: s=4(80px), a=3(60px), j=3(60px) -->\n'
    '            <div class="pt-group">\n'
    '              <div class="pt-bar bar-s" style="height:80px;background:var(--s)" title="sasuken2999: 4勝"><span class="pt-n">4</span></div>\n'
    '              <div class="pt-bar bar-a" style="height:60px;background:var(--a)" title="aohige nagoya: 3勝"><span class="pt-n">3</span></div>\n'
    '              <div class="pt-bar bar-j" style="height:60px;background:var(--j)" title="Jin2798: 3勝"><span class="pt-n">3</span></div>\n'
    '            </div>',
    '            <!-- 40分: s=4(80px), a=4(80px), j=3(60px) -->\n'
    '            <div class="pt-group">\n'
    '              <div class="pt-bar bar-s" style="height:80px;background:var(--s)" title="sasuken2999: 4勝"><span class="pt-n">4</span></div>\n'
    '              <div class="pt-bar bar-a" style="height:80px;background:var(--a)" title="aohige nagoya: 4勝"><span class="pt-n">4</span></div>\n'
    '              <div class="pt-bar bar-j" style="height:60px;background:var(--j)" title="Jin2798: 3勝"><span class="pt-n">3</span></div>\n'
    '            </div>'
)

# ── 6. メイン X軸 ──
html = html.replace(
    '/ ツォルキン: マヤ神聖歴 / ポンドスケープ / コーヒーラッシュ">8タイトル ▴</span>',
    '/ ツォルキン: マヤ神聖歴 / ポンドスケープ / コーヒーラッシュ / フォレストシャッフル:スモーキーマウンテン">9タイトル ▴</span>'
)
html = html.replace(
    '/ ロレンツォ・イル・マニーフィコ / ワンダラスクリーチャーズ">7タイトル ▴</span>',
    '/ ロレンツォ・イル・マニーフィコ / ワンダラスクリーチャーズ / アルティメット・レールロード">8タイトル ▴</span>'
)

# ── 7. メイン履歴 シフト+挿入 ──
marker = '</div><!-- /tab-main -->'
idx = html.index(marker)
main_part, rest_part = html[:idx], html[idx:]
for i in range(99, 0, -1):
    main_part = main_part.replace(f'<td>{i}</td><td class="date">', f'<td>{i+3}</td><td class="date">')

def rrow(badge, cls, name, score):
    return f'          <div class="rrow"><span class="badge {badge}">{badge[-1]}位</span><span class="p-{cls}">{name}</span><span class="score">{score}pt</span></div>\n'

# G1 メイン行(4人戦注記付き, 3人投影)
g1_main = (
    '\n      <tr>\n'
    '        <td>1</td><td class="date">2026-10-10<br>（本日）</td>\n'
    '        <td class="game-name"><a href="https://boardgamearena.com/gamepanel?game=forestshufflesmokymountains" target="_blank" rel="noopener">フォレストシャッフル: スモーキーマウンテン</a><br>'
    '<span style="font-weight:400;color:#999;font-size:.78rem">Forest Shuffle: Smoky Mountains</span><br>'
    '<span style="color:#e8590c;font-size:.7rem">※4人戦（nacchi8787が1位）／3人相対順位で集計</span></td>\n'
    '        <td class="pt-time">30</td>\n'
    '        <td><div class="rank">\n'
    + rrow('b1','a','aohige nagoya','159') + rrow('b2','s','sasuken2999','158') + rrow('b3','j','Jin2798','127') +
    '        </div></td>\n      </tr>\n'
)
# G2 メイン行(3人戦)
g2_main = (
    '\n      <tr>\n'
    '        <td>2</td><td class="date">2026-10-10<br>（本日）</td>\n'
    '        <td class="game-name"><a href="https://boardgamearena.com/gamepanel?game=forestshufflesmokymountains" target="_blank" rel="noopener">フォレストシャッフル: スモーキーマウンテン</a><br>'
    '<span style="font-weight:400;color:#999;font-size:.78rem">Forest Shuffle: Smoky Mountains</span></td>\n'
    '        <td class="pt-time">30</td>\n'
    '        <td><div class="rank">\n'
    + rrow('b1','s','sasuken2999','71') + rrow('b2','a','aohige nagoya','53') + rrow('b3','j','Jin2798','50') +
    '        </div></td>\n      </tr>\n'
)
# G3 メイン行(3人戦)
g3_main = (
    '\n      <tr>\n'
    '        <td>3</td><td class="date">2026-10-10<br>（本日）</td>\n'
    '        <td class="game-name"><a href="https://boardgamearena.com/gamepanel?game=ultimaterailroads" target="_blank" rel="noopener">アルティメット・レールロード</a><br>'
    '<span style="font-weight:400;color:#999;font-size:.78rem">Ultimate Railroads</span></td>\n'
    '        <td class="pt-time">40</td>\n'
    '        <td><div class="rank">\n'
    + rrow('b1','a','aohige nagoya','346') + rrow('b2','s','sasuken2999','313') + rrow('b3','j','Jin2798','232') +
    '        </div></td>\n      </tr>\n'
)
main_part = main_part.replace(
    '    <tbody>\n\n      <tr>\n        <td>4</td><td class="date">2026-10-03<br>（7日前）</td>',
    '    <tbody>\n' + g1_main + g2_main + g3_main + '      <tr>\n        <td>4</td><td class="date">2026-10-03<br>（7日前）</td>'
)
html = main_part + rest_part

# ── 8. 4人集計タブ ──
# 8a. カード（3人のみ更新, nacchi非カード, ponytailthes不変）
html = html.replace('<span class="rank-count c3" id="f-s3">1</span>', '<span class="rank-count c3" id="f-s3">2</span>')  # sas 3位 1→2
html = html.replace('<span class="rank-count c2" id="f-a2">2</span>', '<span class="rank-count c2" id="f-a2">3</span>')  # aohige 2位 2→3
html = html.replace('<span class="rank-count c4" id="f-j4">1</span>', '<span class="rank-count c4" id="f-j4">2</span>')  # Jin 4位 1→2
html = html.replace('<div class="card-sub" id="f-sub-s">4戦中</div>', '<div class="card-sub" id="f-sub-s">5戦中</div>')
html = html.replace('<div class="card-sub" id="f-sub-a">4戦中</div>', '<div class="card-sub" id="f-sub-a">5戦中</div>')
html = html.replace('<div class="card-sub" id="f-sub-j">4戦中</div>', '<div class="card-sub" id="f-sub-j">5戦中</div>')
html = html.replace('<div class="total-num" id="f-total">4</div>', '<div class="total-num" id="f-total">5</div>')
html = html.replace(
    '<div class="total-sub" style="margin-top:4px">sasuken / aohige / ponytailthes / Jin</div>',
    '<div class="total-sub" style="margin-top:4px">sasuken / aohige / Jin ＋ 4人目（ponytailthes・nacchi8787）</div>'
)

# 8b. 4人 ゲーム別成績: フォレスト行追加(勝者nacchiは列外→全員0)
f_gs = (
    '      <tr>\n'
    '        <td><a href="https://boardgamearena.com/gamepanel?game=forestshufflesmokymountains" target="_blank" rel="noopener">フォレストシャッフル: スモーキーマウンテン</a><br>'
    '<span style="font-weight:400;color:#999;font-size:.75rem">Forest Shuffle: Smoky Mountains</span></td>\n'
    '        <td>1</td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num s">0</span><div class="bar-bg"></div></div></td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num a">0</span><div class="bar-bg"></div></div></td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num p">0</span><div class="bar-bg"></div></div></td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num j">0</span><div class="bar-bg"></div></div></td>\n'
    '      </tr>\n'
)
html = html.replace('<tbody id="f-gamestats-body">\n', '<tbody id="f-gamestats-body">\n' + f_gs)

# 8c. 4人 履歴: シフト+G1挿入（f-history-body内のみ）
fh_s = html.index('<tbody id="f-history-body">')
fh_e = html.index('</tbody>', fh_s)
fh = html[fh_s:fh_e]
for i in [4, 3, 2, 1]:
    fh = fh.replace(f'<td>{i}</td><td class="date">', f'<td>{i+1}</td><td class="date">')
g1_four = (
    '\n      <tr>\n'
    '        <td>1</td><td class="date">2026-10-10<br>（本日）</td>\n'
    '        <td class="game-name"><a href="https://boardgamearena.com/gamepanel?game=forestshufflesmokymountains" target="_blank" rel="noopener">フォレストシャッフル: スモーキーマウンテン</a><br>'
    '<span style="font-weight:400;color:#999;font-size:.78rem">Forest Shuffle: Smoky Mountains</span></td>\n'
    '        <td class="pt-time">30</td>\n'
    '        <td><div class="rank">\n'
    '          <div class="rrow"><span class="badge b1">1位</span><span class="p-n" style="color:#9aa0a6;font-weight:700">nacchi8787</span><span class="score">165pt</span></div>\n'
    '          <div class="rrow"><span class="badge b2">2位</span><span class="p-a">aohige nagoya</span><span class="score">159pt</span></div>\n'
    '          <div class="rrow"><span class="badge b3">3位</span><span class="p-s">sasuken2999</span><span class="score">158pt</span></div>\n'
    '          <div class="rrow"><span class="badge b4">4位</span><span class="p-j">Jin2798</span><span class="score">127pt</span></div>\n'
    '        </div></td>\n      </tr>\n'
)
fh = fh.replace('<tbody id="f-history-body">\n', '<tbody id="f-history-body">\n' + g1_four)
html = html[:fh_s] + fh + html[fh_e:]

with open(path, 'w', encoding='utf-8') as f:
    f.write(html)
print("Done!")

# ════════ 検証 ════════
with open(path, encoding='utf-8') as f:
    h = f.read()
main_h = h[:h.index(marker)]
four_h = h[h.index('<div id="tab-four"'):]
ok = ng = 0
def chk(n, c):
    global ok, ng
    print(('OK ' if c else 'NG ')+n);
    if c: ok += 1
    else: ng += 1

chk('header 10-10', '2026-10-10 集計' in h)
chk('no old header 10-03', '2026-10-03 集計' not in h)
chk('total 102', '<div class="total-num">102</div>' in h)
chk('card-sub 102 x3', h.count('<div class="card-sub">102戦中</div>') == 3)
chk('sas s=34', '<span class="rank-count s">34</span>' in h)
chk('aohige a=43', '<span class="rank-count a">43</span>' in h)
chk('Jin j=28 (unchanged)', '<span class="rank-count j">28</span>' in h)
chk('sas c2=38 & aohige c2=38 (x2)', h.count('<span class="rank-count c2">38</span>') == 2)
chk('Jin c3=42', '<span class="rank-count c3">42</span>' in h)
chk('sum sas 34+38+30=102', 34+38+30 == 102)
chk('sum aohige 43+38+21=102', 43+38+21 == 102)
chk('sum Jin 28+32+42=102', 28+32+42 == 102)
chk('gs forest smoky', 'game=forestshufflesmokymountains" target="_blank" rel="noopener">フォレストシャッフル: スモーキーマウンテン' in h)
chk('gs railroad', 'game=ultimaterailroads" target="_blank" rel="noopener">アルティメット・レールロード' in h)
_gsm = main_h[main_h.index('gs-table'):]; _gsm = _gsm[:_gsm.index('</table>')]
_plays = sum(int(x) for x in re.findall(r'</td>\n        <td>(\d+)</td>\n        <td><div class="win-bar-wrap"', _gsm))
chk(f'main gs plays sum=102 (found {_plays})', _plays == 102)
chk('30min a=8', '<!-- 30分: s=2(40px), a=8(160px), j=4(80px) -->' in h)
chk('40min a=4', '<!-- 40分: s=4(80px), a=4(80px), j=3(60px) -->' in h)
chk('no bar over 400', 'height:420px;background' not in h and 'height:400px;background' not in h)
chk('scale still 20 (10 ylabels)', h.count('<span class="pt-yl">') == 10)
def bar_sum(cls):
    return sum(int(x) for x in re.findall(r'pt-bar '+cls+r'[^>]*title="[^"]*: (\d+)勝"', main_h))
chk('bar sum sas=34', bar_sum('bar-s') == 34)
chk('bar sum aohige=43', bar_sum('bar-a') == 43)
chk('bar sum Jin=28', bar_sum('bar-j') == 28)
chk('x30 9titles', 'スモーキーマウンテン">9タイトル' in h)
chk('x40 8titles', 'アルティメット・レールロード">8タイトル' in h)
chk('row1 forest 4p note', '※4人戦（nacchi8787が1位）' in main_h)
chk('row1 today', '<td>1</td><td class="date">2026-10-10<br>（本日）</td>' in main_h)
chk('row3 railroad today', '<td>3</td><td class="date">2026-10-10<br>（本日）</td>' in main_h)
chk('row4 former1 10-03', '<td>4</td><td class="date">2026-10-03<br>（7日前）</td>' in main_h)
mr = len(re.findall(r'<td>\d+</td><td class="date">', main_h))
chk(f'main 102 rows (found {mr})', mr == 102)
# 4人集計
chk('f-s3=2', '<span class="rank-count c3" id="f-s3">2</span>' in h)
chk('f-a2=3', '<span class="rank-count c2" id="f-a2">3</span>' in h)
chk('f-j4=2', '<span class="rank-count c4" id="f-j4">2</span>' in h)
chk('f-total=5', '<div class="total-num" id="f-total">5</div>' in h)
chk('f-sub-s=5', '<div class="card-sub" id="f-sub-s">5戦中</div>' in h)
chk('f-sub-p unchanged=4', '<div class="card-sub" id="f-sub-p">4戦中</div>' in h)
chk('f subtitle nacchi', 'ponytailthes・nacchi8787' in h)
chk('f-gs forest row', four_h.count('game=forestshufflesmokymountains') >= 1)
chk('f-hist nacchi row', 'nacchi8787</span><span class="score">165pt</span>' in four_h)
fh2 = h[h.index('<tbody id="f-history-body">'):h.index('</tbody>', h.index('<tbody id="f-history-body">'))]
fhr = len(re.findall(r'<td>\d+</td><td class="date">', fh2))
chk(f'4p history 5 rows (found {fhr})', fhr == 5)
chk('4p row5 old (07-14)', '<td>5</td><td class="date">2026-07-14' in fh2)
print(f'\nResult: {ok} OK / {ng} NG')
