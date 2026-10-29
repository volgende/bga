# -*- coding: utf-8 -*-
import re
from datetime import date, datetime

path = r"bga_results.html"
with open(path, encoding='utf-8') as f:
    html = f.read()

today = date(2026, 10, 30)

# ════ 新規4戦（すべて本日10/30・3人戦）════
#  1 キャッスルコンボ(castlecombo,30分,既存) 1位sas83/2位Jin82/3位aohige73  W:sas
#  2 ザ・ラスト(thelast,10分,新)             1位aohige-17/2位Jin-25/3位sas-50 W:aohige
#  3 スカルキング(skullking,20分,既存)        1位Jin330/2位aohige200/3位sas10  W:Jin
#  4 西フランク王国の建築家(architectsofthewestkingdom,30分,新) 1位sas43/2位aohige39/3位Jin39 W:sas

# ── 1. ヘッダー ──
html = html.replace('2026-10-23 集計', '2026-10-30 集計')

# ── 2. 相対日付（today=2026-10-30） ──
def upd_date(m):
    d = datetime.strptime(m.group(1), '%Y-%m-%d').date()
    n = (today - d).days
    return f'<td class="date">{m.group(1)}<br>（{"本日" if n==0 else str(n)+"日前"}）</td>'
html = re.sub(r'<td class="date">(\d{4}-\d{2}-\d{2})<br>（[^）]+）</td>', upd_date, html)

# ── 3. メインカード 110→114 ──
# sasuken 39/40/31→41/40/33, aohige 43/43/24→44/45/25, Jin 31/37/42→32/39/43
html = html.replace('<span class="rank-count s">39</span>', '<span class="rank-count s">41</span>')
html = html.replace('<span class="rank-count a">43</span>', '<span class="rank-count a">44</span>')
html = html.replace('<span class="rank-count j">31</span>', '<span class="rank-count j">32</span>')
html = html.replace('<span class="rank-count c2">43</span>', '<span class="rank-count c2">45</span>')  # aohige c2
html = html.replace('<span class="rank-count c2">37</span>', '<span class="rank-count c2">39</span>')  # Jin c2
html = html.replace('<span class="rank-count c3">31</span>', '<span class="rank-count c3">33</span>')  # sas c3
html = html.replace('<span class="rank-count c3">24</span>', '<span class="rank-count c3">25</span>')  # aohige c3
html = html.replace('<span class="rank-count c3">42</span>', '<span class="rank-count c3">43</span>')  # Jin c3
html = html.replace('<div class="card-sub">110戦中</div>', '<div class="card-sub">114戦中</div>')
html = html.replace('<div class="total-num">110</div>', '<div class="total-num">114</div>')

# ── 4a. ゲーム別成績 既存増分 ──
# キャッスルコンボ 3→4戦, s0→1(25%), a3(100%)→3(75%)
html = html.replace(
    '        <td><a href="https://boardgamearena.com/gamepanel?game=castlecombo" target="_blank" rel="noopener">キャッスルコンボ</a><br><span style="font-weight:400;color:#999;font-size:.75rem">Castle Combo</span></td>\n'
    '        <td>3</td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num s">0</span><div class="bar-bg"></div></div></td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num a">3</span><div class="bar-bg"><div class="bar-fill bar-a" style="width:100%"></div></div></div></td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num j">0</span><div class="bar-bg"></div></div></td>',
    '        <td><a href="https://boardgamearena.com/gamepanel?game=castlecombo" target="_blank" rel="noopener">キャッスルコンボ</a><br><span style="font-weight:400;color:#999;font-size:.75rem">Castle Combo</span></td>\n'
    '        <td>4</td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num s">1</span><div class="bar-bg"><div class="bar-fill bar-s" style="width:25%"></div></div></div></td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num a">3</span><div class="bar-bg"><div class="bar-fill bar-a" style="width:75%"></div></div></div></td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num j">0</span><div class="bar-bg"></div></div></td>'
)
# スカルキング 4→5戦, a2(50%)→2(40%), j2(50%)→3(60%)
html = html.replace(
    '        <td><a href="https://boardgamearena.com/gamepanel?game=skullking" target="_blank" rel="noopener">スカルキング</a><br><span style="font-weight:400;color:#999;font-size:.75rem">Skull King</span></td>\n'
    '        <td>4</td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num s">0</span><div class="bar-bg"></div></div></td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num a">2</span><div class="bar-bg"><div class="bar-fill bar-a" style="width:50%"></div></div></div></td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num j">2</span><div class="bar-bg"><div class="bar-fill bar-j" style="width:50%"></div></div></div></td>',
    '        <td><a href="https://boardgamearena.com/gamepanel?game=skullking" target="_blank" rel="noopener">スカルキング</a><br><span style="font-weight:400;color:#999;font-size:.75rem">Skull King</span></td>\n'
    '        <td>5</td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num s">0</span><div class="bar-bg"></div></div></td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num a">2</span><div class="bar-bg"><div class="bar-fill bar-a" style="width:40%"></div></div></div></td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num j">3</span><div class="bar-bg"><div class="bar-fill bar-j" style="width:60%"></div></div></div></td>'
)

# ── 4b. ゲーム別成績 新規2タイトル先頭追加 ──
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
    gs_row('thelast', 'ザ・ラスト', 'The Last', 1, 0, 1, 0) +
    gs_row('architectsofthewestkingdom', '西フランク王国の建築家', 'Architects of the West Kingdom', 1, 1, 0, 0)
)
_anchor = '    <tbody>\n      <tr>\n        <td><a href="https://boardgamearena.com/gamepanel?game=trio"'
assert html.count(_anchor) == 1, f"gs anchor={html.count(_anchor)}"
html = html.replace(_anchor, '    <tbody>\n' + new_gs + '      <tr>\n        <td><a href="https://boardgamearena.com/gamepanel?game=trio"')

# ── 5. 棒グラフ（スケール20維持） ──
# 10分 a2→3(60)
html = html.replace(
    '              <div class="pt-bar bar-a" style="height:40px;background:var(--a)" title="aohige nagoya: 2勝"><span class="pt-n">2</span></div>\n'
    '              <div class="pt-bar bar-j" style="height:100px;background:var(--j)" title="Jin2798: 5勝"><span class="pt-n">5</span></div>',
    '              <div class="pt-bar bar-a" style="height:60px;background:var(--a)" title="aohige nagoya: 3勝"><span class="pt-n">3</span></div>\n'
    '              <div class="pt-bar bar-j" style="height:100px;background:var(--j)" title="Jin2798: 5勝"><span class="pt-n">5</span></div>'
)
html = html.replace('<!-- 10分: s=7(140px), a=2(40px), j=5(100px) -->', '<!-- 10分: s=7(140px), a=3(60px), j=5(100px) -->')
# 20分 j14→15(300)
html = html.replace(
    '              <div class="pt-bar bar-j" style="height:280px;background:var(--j)" title="Jin2798: 14勝"><span class="pt-n">14</span></div>',
    '              <div class="pt-bar bar-j" style="height:300px;background:var(--j)" title="Jin2798: 15勝"><span class="pt-n">15</span></div>'
)
html = html.replace('<!-- 20分: s=19(380px), a=11(220px), j=14(280px) -->', '<!-- 20分: s=19(380px), a=11(220px), j=15(300px) -->')
# 30分 s4→6(120)
html = html.replace(
    '            <!-- 30分: s=4(80px), a=8(160px), j=4(80px) -->\n'
    '            <div class="pt-group">\n'
    '              <div class="pt-bar bar-s" style="height:80px;background:var(--s)" title="sasuken2999: 4勝"><span class="pt-n">4</span></div>',
    '            <!-- 30分: s=6(120px), a=8(160px), j=4(80px) -->\n'
    '            <div class="pt-group">\n'
    '              <div class="pt-bar bar-s" style="height:120px;background:var(--s)" title="sasuken2999: 6勝"><span class="pt-n">6</span></div>'
)

# ── 6. X軸 ──
html = html.replace(
    '/ スペースベース / トリオ / それはオレの牧場だ！">8タイトル ▴</span>',
    '/ スペースベース / トリオ / それはオレの牧場だ！ / ザ・ラスト">9タイトル ▴</span>'
)
html = html.replace(
    '/ フォレストシャッフル:スモーキーマウンテン / Labyrinth">10タイトル ▴</span>',
    '/ フォレストシャッフル:スモーキーマウンテン / Labyrinth / 西フランク王国の建築家">11タイトル ▴</span>'
)

# ── 7. メイン履歴 シフト+挿入 ──
marker = '</div><!-- /tab-main -->'
idx = html.index(marker)
main_part, rest_part = html[:idx], html[idx:]
for i in range(110, 0, -1):
    main_part = main_part.replace(f'<td>{i}</td><td class="date">', f'<td>{i+4}</td><td class="date">')

def rrow(badge, cls, name, score):
    return f'          <div class="rrow"><span class="badge {badge}">{badge[-1]}位</span><span class="p-{cls}">{name}</span><span class="score">{score}pt</span></div>\n'
def hist(num, slug, jp, en, minutes, ranks):
    return ('\n      <tr>\n'
            f'        <td>{num}</td><td class="date">2026-10-30<br>（本日）</td>\n'
            f'        <td class="game-name"><a href="https://boardgamearena.com/gamepanel?game={slug}" target="_blank" rel="noopener">{jp}</a><br>'
            f'<span style="font-weight:400;color:#999;font-size:.78rem">{en}</span></td>\n'
            f'        <td class="pt-time">{minutes}</td>\n'
            '        <td><div class="rank">\n' + ''.join(rrow(*r) for r in ranks) +
            '        </div></td>\n      </tr>\n')
new_rows = (
    hist(1,'castlecombo','キャッスルコンボ','Castle Combo',30,[('b1','s','sasuken2999','83'),('b2','j','Jin2798','82'),('b3','a','aohige nagoya','73')]) +
    hist(2,'thelast','ザ・ラスト','The Last',10,[('b1','a','aohige nagoya','-17'),('b2','j','Jin2798','-25'),('b3','s','sasuken2999','-50')]) +
    hist(3,'skullking','スカルキング','Skull King',20,[('b1','j','Jin2798','330'),('b2','a','aohige nagoya','200'),('b3','s','sasuken2999','10')]) +
    hist(4,'architectsofthewestkingdom','西フランク王国の建築家','Architects of the West Kingdom',30,[('b1','s','sasuken2999','43'),('b2','a','aohige nagoya','39'),('b3','j','Jin2798','39')])
)
_hanchor = '    <tbody>\n\n      <tr>\n        <td>5</td><td class="date">2026-10-23<br>（7日前）</td>'
assert main_part.count(_hanchor) == 1, f"hist anchor={main_part.count(_hanchor)}"
main_part = main_part.replace(_hanchor, '    <tbody>\n' + new_rows + '      <tr>\n        <td>5</td><td class="date">2026-10-23<br>（7日前）</td>')
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
chk('header 10-30', '2026-10-30 集計' in h)
chk('no old header', '2026-10-23 集計' not in h)
chk('total 114', '<div class="total-num">114</div>' in h)
chk('card-sub 114 x3', h.count('<div class="card-sub">114戦中</div>') == 3)
chk('sas s=41', '<span class="rank-count s">41</span>' in h)
chk('aohige a=44', '<span class="rank-count a">44</span>' in h)
chk('Jin j=32', '<span class="rank-count j">32</span>' in h)
chk('aohige c2=45', '<span class="rank-count c2">45</span>' in h)
chk('Jin c2=39', '<span class="rank-count c2">39</span>' in h)
chk('sas c3=33', '<span class="rank-count c3">33</span>' in h)
chk('aohige c3=25', '<span class="rank-count c3">25</span>' in h)
chk('Jin c3=43', '<span class="rank-count c3">43</span>' in h)
chk('sum sas 41+40+33=114', 41+40+33 == 114)
chk('sum aohige 44+45+25=114', 44+45+25 == 114)
chk('sum Jin 32+39+43=114', 32+39+43 == 114)
chk('gs thelast', 'game=thelast" target="_blank" rel="noopener">ザ・ラスト' in h)
chk('gs architects', 'game=architectsofthewestkingdom" target="_blank" rel="noopener">西フランク王国の建築家' in h)
chk('castle plays4', 'game=castlecombo" target="_blank" rel="noopener">キャッスルコンボ</a><br><span style="font-weight:400;color:#999;font-size:.75rem">Castle Combo</span></td>\n        <td>4</td>' in h)
chk('skull plays5', 'game=skullking" target="_blank" rel="noopener">スカルキング</a><br><span style="font-weight:400;color:#999;font-size:.75rem">Skull King</span></td>\n        <td>5</td>' in h)
_gsm = main_h[main_h.index('gs-table'):]; _gsm = _gsm[:_gsm.index('</table>')]
_plays = sum(int(x) for x in re.findall(r'</td>\n        <td>(\d+)</td>\n        <td><div class="win-bar-wrap"', _gsm))
chk(f'gs plays sum=114 (found {_plays})', _plays == 114)
chk('10min a=3', '<!-- 10分: s=7(140px), a=3(60px), j=5(100px) -->' in h)
chk('20min j=15', '<!-- 20分: s=19(380px), a=11(220px), j=15(300px) -->' in h)
chk('30min s=6', '<!-- 30分: s=6(120px), a=8(160px), j=4(80px) -->' in h)
chk('no bar over 400', 'height:420px;background' not in h and 'height:400px;background' not in h)
chk('scale 20', h.count('<span class="pt-yl">') == 10)
def bs(cls): return sum(int(x) for x in re.findall(r'pt-bar '+cls+r'[^>]*title="[^"]*: (\d+)勝"', main_h))
chk('bar sum sas=41', bs('bar-s') == 41)
chk('bar sum aohige=44', bs('bar-a') == 44)
chk('bar sum Jin=32', bs('bar-j') == 32)
chk('x10 9titles', 'それはオレの牧場だ！ / ザ・ラスト">9タイトル' in h)
chk('x30 11titles', '西フランク王国の建築家">11タイトル' in h)
chk('row1 castle today', '<td>1</td><td class="date">2026-10-30<br>（本日）</td>' in main_h)
chk('row4 architects today', '<td>4</td><td class="date">2026-10-30<br>（本日）</td>' in main_h)
chk('row5 former1 10-23', '<td>5</td><td class="date">2026-10-23<br>（7日前）</td>' in main_h)
mr = len(re.findall(r'<td>\d+</td><td class="date">', main_h))
chk(f'main 114 rows (found {mr})', mr == 114)
print(f'\nResult: {ok} OK / {ng} NG')
