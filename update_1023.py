# -*- coding: utf-8 -*-
import re
from datetime import date, datetime

path = r"bga_results.html"
with open(path, encoding='utf-8') as f:
    html = f.read()

today = date(2026, 10, 23)

# ════ 新規8戦（すべて本日10/23・3人戦、4人戦なし）════
#  1 トリオ(trio,10分)        1位Jin1/2位sas0/2位aohige0(タイ)        W:Jin
#  2 トリオ(trio,10分)        1位sas1/2位Jin0/2位aohige0(タイ)        W:sas
#  3 トリオ(trio,10分)        1位sas1/2位Jin0/2位aohige0(タイ)        W:sas
#  4 それはオレの牧場だ！(splits,10分) 1位sas15/2位Jin14/3位aohige14   W:sas
#  5 それはオレの牧場だ！(splits,10分) 1位Jin16/2位sas16/3位aohige10   W:Jin
#  6 Labyrinth(labyrinth,30分) 1位sas9/2位Jin7/2位aohige7(タイ)        W:sas
#  7 チャレンジャーズ！ビーチカップ(challengersbeachcup,20分) 1位Jin1/2位aohige0/3位sas-1 W:Jin
#  8 フォレストシャッフル:ダートムーア(forestshuffledartmoor,30分,既存) 1位sas226/2位Jin194/3位aohige125 W:sas

# ── 1. ヘッダー ──
html = html.replace('2026-10-10 集計', '2026-10-23 集計')

# ── 2. 相対日付（today=2026-10-23） ──
def upd_date(m):
    d = datetime.strptime(m.group(1), '%Y-%m-%d').date()
    n = (today - d).days
    return f'<td class="date">{m.group(1)}<br>（{"本日" if n==0 else str(n)+"日前"}）</td>'
html = re.sub(r'<td class="date">(\d{4}-\d{2}-\d{2})<br>（[^）]+）</td>', upd_date, html)

# ── 3. メインカード 102→110 ──
# sasuken 34/38/30→39/40/31, aohige 43/38/21→43/43/24, Jin 28/32/42→31/37/42
html = html.replace('<span class="rank-count s">34</span>', '<span class="rank-count s">39</span>')
html = html.replace('<span class="rank-count j">28</span>', '<span class="rank-count j">31</span>')
# c2=38 が sasuken/aohige で重複 → 出現順に置換（sasuken→40, aohige→43）
assert html.count('<span class="rank-count c2">38</span>') == 2, html.count('<span class="rank-count c2">38</span>')
html = html.replace('<span class="rank-count c2">38</span>', '<span class="rank-count c2">40</span>', 1)  # sasuken
html = html.replace('<span class="rank-count c2">38</span>', '<span class="rank-count c2">43</span>', 1)  # aohige
html = html.replace('<span class="rank-count c2">32</span>', '<span class="rank-count c2">37</span>')  # Jin c2
html = html.replace('<span class="rank-count c3">30</span>', '<span class="rank-count c3">31</span>')  # sas c3
html = html.replace('<span class="rank-count c3">21</span>', '<span class="rank-count c3">24</span>')  # aohige c3
html = html.replace('<div class="card-sub">102戦中</div>', '<div class="card-sub">110戦中</div>')
html = html.replace('<div class="total-num">102</div>', '<div class="total-num">110</div>')

# ── 4a. ゲーム別成績: ダートムーア 1→2戦(s0→1(50%), a1(100%)→1(50%)) ──
html = html.replace(
    '        <td><a href="https://boardgamearena.com/gamepanel?game=forestshuffledartmoor" target="_blank" rel="noopener">フォレストシャッフル:ダートムーア</a><br><span style="font-weight:400;color:#999;font-size:.75rem">Forest Shuffle: Dartmoor</span></td>\n'
    '        <td>1</td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num s">0</span><div class="bar-bg"></div></div></td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num a">1</span><div class="bar-bg"><div class="bar-fill bar-a" style="width:100%"></div></div></div></td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num j">0</span><div class="bar-bg"></div></div></td>',
    '        <td><a href="https://boardgamearena.com/gamepanel?game=forestshuffledartmoor" target="_blank" rel="noopener">フォレストシャッフル:ダートムーア</a><br><span style="font-weight:400;color:#999;font-size:.75rem">Forest Shuffle: Dartmoor</span></td>\n'
    '        <td>2</td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num s">1</span><div class="bar-bg"><div class="bar-fill bar-s" style="width:50%"></div></div></div></td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num a">1</span><div class="bar-bg"><div class="bar-fill bar-a" style="width:50%"></div></div></div></td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num j">0</span><div class="bar-bg"></div></div></td>'
)

# ── 4b. ゲーム別成績: 新規4タイトル先頭追加 ──
def gs_row(slug, jp, en, plays, s, a, j):
    def cell(cls, w):
        if w == 0:
            return f'<td><div class="win-bar-wrap"><span class="win-num {cls}">0</span><div class="bar-bg"></div></div></td>'
        pct = round(w / plays * 100)
        return (f'<td><div class="win-bar-wrap"><span class="win-num {cls}">{w}</span>'
                f'<div class="bar-bg"><div class="bar-fill bar-{cls}" style="width:{pct}%"></div></div></div></td>')
    return ('      <tr>\n'
            f'        <td><a href="https://boardgamearena.com/gamepanel?game={slug}" target="_blank" rel="noopener">{jp}</a><br>'
            f'<span style="font-weight:400;color:#999;font-size:.75rem">{en}</span></td>\n'
            f'        <td>{plays}</td>\n'
            f'        {cell("s", s)}\n        {cell("a", a)}\n        {cell("j", j)}\n      </tr>\n')
new_gs = (
    gs_row('trio', 'トリオ', 'Trio', 3, 2, 0, 1) +
    gs_row('splits', 'それはオレの牧場だ！', 'Battle Sheep', 2, 1, 0, 1) +
    gs_row('labyrinth', 'Labyrinth', 'Labyrinth', 1, 1, 0, 0) +
    gs_row('challengersbeachcup', 'チャレンジャーズ！ビーチカップ', 'Challengers! beachcup', 1, 0, 0, 1)
)
_anchor = '    <tbody>\n      <tr>\n        <td><a href="https://boardgamearena.com/gamepanel?game=forestshufflesmokymountains"'
assert html.count(_anchor) == 1, f"gs anchor={html.count(_anchor)}"
html = html.replace(_anchor, '    <tbody>\n' + new_gs + '      <tr>\n        <td><a href="https://boardgamearena.com/gamepanel?game=forestshufflesmokymountains"')

# ── 5. 棒グラフ（スケール20維持） ──
# 10分 s4→7(140), j3→5(100)
html = html.replace(
    '            <!-- 10分: s=4(80px), a=2(40px), j=3(60px) -->\n'
    '            <div class="pt-group">\n'
    '              <div class="pt-bar bar-s" style="height:80px;background:var(--s)" title="sasuken2999: 4勝"><span class="pt-n">4</span></div>\n'
    '              <div class="pt-bar bar-a" style="height:40px;background:var(--a)" title="aohige nagoya: 2勝"><span class="pt-n">2</span></div>\n'
    '              <div class="pt-bar bar-j" style="height:60px;background:var(--j)" title="Jin2798: 3勝"><span class="pt-n">3</span></div>\n'
    '            </div>',
    '            <!-- 10分: s=7(140px), a=2(40px), j=5(100px) -->\n'
    '            <div class="pt-group">\n'
    '              <div class="pt-bar bar-s" style="height:140px;background:var(--s)" title="sasuken2999: 7勝"><span class="pt-n">7</span></div>\n'
    '              <div class="pt-bar bar-a" style="height:40px;background:var(--a)" title="aohige nagoya: 2勝"><span class="pt-n">2</span></div>\n'
    '              <div class="pt-bar bar-j" style="height:100px;background:var(--j)" title="Jin2798: 5勝"><span class="pt-n">5</span></div>\n'
    '            </div>'
)
# 20分 j13→14(280)
html = html.replace(
    '              <div class="pt-bar bar-j" style="height:260px;background:var(--j)" title="Jin2798: 13勝"><span class="pt-n">13</span></div>',
    '              <div class="pt-bar bar-j" style="height:280px;background:var(--j)" title="Jin2798: 14勝"><span class="pt-n">14</span></div>'
)
html = html.replace('<!-- 20分: s=19(380px), a=11(220px), j=13(260px) -->',
                    '<!-- 20分: s=19(380px), a=11(220px), j=14(280px) -->')
# 30分 s2→4(80)
html = html.replace(
    '            <!-- 30分: s=2(40px), a=8(160px), j=4(80px) -->\n'
    '            <div class="pt-group">\n'
    '              <div class="pt-bar bar-s" style="height:40px;background:var(--s)" title="sasuken2999: 2勝"><span class="pt-n">2</span></div>\n'
    '              <div class="pt-bar bar-a" style="height:160px;background:var(--a)" title="aohige nagoya: 8勝"><span class="pt-n">8</span></div>\n'
    '              <div class="pt-bar bar-j" style="height:80px;background:var(--j)" title="Jin2798: 4勝"><span class="pt-n">4</span></div>\n'
    '            </div>',
    '            <!-- 30分: s=4(80px), a=8(160px), j=4(80px) -->\n'
    '            <div class="pt-group">\n'
    '              <div class="pt-bar bar-s" style="height:80px;background:var(--s)" title="sasuken2999: 4勝"><span class="pt-n">4</span></div>\n'
    '              <div class="pt-bar bar-a" style="height:160px;background:var(--a)" title="aohige nagoya: 8勝"><span class="pt-n">8</span></div>\n'
    '              <div class="pt-bar bar-j" style="height:80px;background:var(--j)" title="Jin2798: 4勝"><span class="pt-n">4</span></div>\n'
    '            </div>'
)

# ── 6. X軸 ──
html = html.replace(
    '/ ディギング・フォー・ダイノス / カルヌタ / スペースベース">6タイトル ▴</span>',
    '/ ディギング・フォー・ダイノス / カルヌタ / スペースベース / トリオ / それはオレの牧場だ！">8タイトル ▴</span>'
)
html = html.replace(
    '/ 金庫: 泥棒の巣窟 / リフレクション">25タイトル ▴</span>',
    '/ 金庫: 泥棒の巣窟 / リフレクション / チャレンジャーズ！ビーチカップ">26タイトル ▴</span>'
)
html = html.replace(
    '/ コーヒーラッシュ / フォレストシャッフル:スモーキーマウンテン">9タイトル ▴</span>',
    '/ コーヒーラッシュ / フォレストシャッフル:スモーキーマウンテン / Labyrinth">10タイトル ▴</span>'
)

# ── 7. メイン履歴 シフト+挿入 ──
marker = '</div><!-- /tab-main -->'
idx = html.index(marker)
main_part, rest_part = html[:idx], html[idx:]
for i in range(102, 0, -1):
    main_part = main_part.replace(f'<td>{i}</td><td class="date">', f'<td>{i+8}</td><td class="date">')

def rrow(badge, cls, name, score):
    return f'          <div class="rrow"><span class="badge {badge}">{badge[-1]}位</span><span class="p-{cls}">{name}</span><span class="score">{score}pt</span></div>\n'
def hist(num, slug, jp, en, minutes, ranks):
    return ('\n      <tr>\n'
            f'        <td>{num}</td><td class="date">2026-10-23<br>（本日）</td>\n'
            f'        <td class="game-name"><a href="https://boardgamearena.com/gamepanel?game={slug}" target="_blank" rel="noopener">{jp}</a><br>'
            f'<span style="font-weight:400;color:#999;font-size:.78rem">{en}</span></td>\n'
            f'        <td class="pt-time">{minutes}</td>\n'
            '        <td><div class="rank">\n' + ''.join(rrow(*r) for r in ranks) +
            '        </div></td>\n      </tr>\n')
new_rows = (
    hist(1,'trio','トリオ','Trio',10,[('b1','j','Jin2798','1'),('b2','s','sasuken2999','0'),('b2','a','aohige nagoya','0')]) +
    hist(2,'trio','トリオ','Trio',10,[('b1','s','sasuken2999','1'),('b2','j','Jin2798','0'),('b2','a','aohige nagoya','0')]) +
    hist(3,'trio','トリオ','Trio',10,[('b1','s','sasuken2999','1'),('b2','j','Jin2798','0'),('b2','a','aohige nagoya','0')]) +
    hist(4,'splits','それはオレの牧場だ！','Battle Sheep',10,[('b1','s','sasuken2999','15'),('b2','j','Jin2798','14'),('b3','a','aohige nagoya','14')]) +
    hist(5,'splits','それはオレの牧場だ！','Battle Sheep',10,[('b1','j','Jin2798','16'),('b2','s','sasuken2999','16'),('b3','a','aohige nagoya','10')]) +
    hist(6,'labyrinth','Labyrinth','Labyrinth',30,[('b1','s','sasuken2999','9'),('b2','j','Jin2798','7'),('b2','a','aohige nagoya','7')]) +
    hist(7,'challengersbeachcup','チャレンジャーズ！ビーチカップ','Challengers! beachcup',20,[('b1','j','Jin2798','1'),('b2','a','aohige nagoya','0'),('b3','s','sasuken2999','-1')]) +
    hist(8,'forestshuffledartmoor','フォレストシャッフル:ダートムーア','Forest Shuffle: Dartmoor',30,[('b1','s','sasuken2999','226'),('b2','j','Jin2798','194'),('b3','a','aohige nagoya','125')])
)
_hanchor = '    <tbody>\n\n      <tr>\n        <td>9</td><td class="date">2026-10-10<br>（13日前）</td>'
assert main_part.count(_hanchor) == 1, f"hist anchor={main_part.count(_hanchor)}"
main_part = main_part.replace(_hanchor, '    <tbody>\n' + new_rows + '      <tr>\n        <td>9</td><td class="date">2026-10-10<br>（13日前）</td>')
html = main_part + rest_part

with open(path, 'w', encoding='utf-8') as f:
    f.write(html)
print("Done!")

# ════ 検証 ════
with open(path, encoding='utf-8') as f:
    h = f.read()
main_h = h[:h.index(marker)]
ok = ng = 0
def chk(n, c):
    global ok, ng
    print(('OK ' if c else 'NG ')+n); ok += bool(c); ng += (not c)
chk('header 10-23', '2026-10-23 集計' in h)
chk('no old 10-10 header', '2026-10-10 集計' not in h)
chk('total 110', '<div class="total-num">110</div>' in h)
chk('card-sub 110 x3', h.count('<div class="card-sub">110戦中</div>') == 3)
chk('sas s=39', '<span class="rank-count s">39</span>' in h)
chk('aohige a=43', '<span class="rank-count a">43</span>' in h)
chk('Jin j=31', '<span class="rank-count j">31</span>' in h)
chk('sas c2=40', '<span class="rank-count c2">40</span>' in h)
chk('aohige c2=43', '<span class="rank-count c2">43</span>' in h)
chk('Jin c2=37', '<span class="rank-count c2">37</span>' in h)
chk('no c2=38 left', '<span class="rank-count c2">38</span>' not in h)
chk('sas c3=31', '<span class="rank-count c3">31</span>' in h)
chk('aohige c3=24', '<span class="rank-count c3">24</span>' in h)
chk('sum sas 39+40+31=110', 39+40+31 == 110)
chk('sum aohige 43+43+24=110', 43+43+24 == 110)
chk('sum Jin 31+37+42=110', 31+37+42 == 110)
for slug,jp in [('trio','トリオ'),('splits','それはオレの牧場だ！'),('labyrinth','Labyrinth'),('challengersbeachcup','チャレンジャーズ！ビーチカップ')]:
    chk(f'gs {slug}', f'game={slug}" target="_blank" rel="noopener">{jp}' in h)
chk('dartmoor plays2', 'game=forestshuffledartmoor" target="_blank" rel="noopener">フォレストシャッフル:ダートムーア</a><br><span style="font-weight:400;color:#999;font-size:.75rem">Forest Shuffle: Dartmoor</span></td>\n        <td>2</td>' in h)
_gsm = main_h[main_h.index('gs-table'):]; _gsm = _gsm[:_gsm.index('</table>')]
_plays = sum(int(x) for x in re.findall(r'</td>\n        <td>(\d+)</td>\n        <td><div class="win-bar-wrap"', _gsm))
chk(f'gs plays sum=110 (found {_plays})', _plays == 110)
chk('10min s=7', '<!-- 10分: s=7(140px), a=2(40px), j=5(100px) -->' in h)
chk('20min j=14', '<!-- 20分: s=19(380px), a=11(220px), j=14(280px) -->' in h)
chk('30min s=4', '<!-- 30分: s=4(80px), a=8(160px), j=4(80px) -->' in h)
chk('no bar over 400', 'height:420px;background' not in h and 'height:400px;background' not in h)
chk('scale 20 (10 ylabels)', h.count('<span class="pt-yl">') == 10)
def bs(cls): return sum(int(x) for x in re.findall(r'pt-bar '+cls+r'[^>]*title="[^"]*: (\d+)勝"', main_h))
chk('bar sum sas=39', bs('bar-s') == 39)
chk('bar sum aohige=43', bs('bar-a') == 43)
chk('bar sum Jin=31', bs('bar-j') == 31)
chk('x10 8titles', 'それはオレの牧場だ！">8タイトル' in h)
chk('x20 26titles', 'チャレンジャーズ！ビーチカップ">26タイトル' in h)
chk('x30 10titles', 'Labyrinth">10タイトル' in h)
chk('row1 trio today', '<td>1</td><td class="date">2026-10-23<br>（本日）</td>' in main_h)
chk('row8 dartmoor today', '<td>8</td><td class="date">2026-10-23<br>（本日）</td>' in main_h)
chk('row9 former1 10-10', '<td>9</td><td class="date">2026-10-10<br>（13日前）</td>' in main_h)
chk('trio tie 2xb2', main_h.count('<span class="badge b2">2位</span><span class="p-a">aohige nagoya</span><span class="score">0pt</span>') == 3)
mr = len(re.findall(r'<td>\d+</td><td class="date">', main_h))
chk(f'main 110 rows (found {mr})', mr == 110)
print(f'\nResult: {ok} OK / {ng} NG')
