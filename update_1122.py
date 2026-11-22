# -*- coding: utf-8 -*-
import re
from datetime import date, datetime

path = r"bga_results.html"
with open(path, encoding='utf-8') as f:
    html = f.read()

today = date(2026, 11, 22)

# ════ 新規5戦（すべて2026-11-20・3人戦。sasuken×aohige2人戦のシティーズ#950921164は除外済み）════
#  1 タクタ(tacta,20分,既存)            1位aohige52/2位sas48/3位Jin41        W:aohige
#  2 ファンタジータイルズ(fantasytiles,30分,新) 1位Jin240/2位sas231/3位aohige198 W:Jin
#  3 ヒューゴ:オバケと鬼ごっこ(escapefromthehiddencastle,10分,新) 1位Jin-19/2位aohige-29/3位sas-46 W:Jin
#  4 軍扇:トシ・ランボの戦い(gunsen,30分,新) 1位aohige7/2位sas4/2位Jin4(タイ)     W:aohige
#  5 シティーズ(cities,20分,新)          1位aohige69/2位sas64/3位Jin60         W:aohige

# ── 1. ヘッダー ──
html = html.replace('2026-10-30 集計', '2026-11-22 集計')

# ── 2. 相対日付（today=2026-11-22） ──
def upd_date(m):
    d = datetime.strptime(m.group(1), '%Y-%m-%d').date()
    n = (today - d).days
    return f'<td class="date">{m.group(1)}<br>（{"本日" if n==0 else str(n)+"日前"}）</td>'
html = re.sub(r'<td class="date">(\d{4}-\d{2}-\d{2})<br>（[^）]+）</td>', upd_date, html)

# ── 3. メインカード 114→119 ──
# sasuken 41/40/33→41/44/34, aohige 44/45/25→47/46/26, Jin 32/39/43→34/40/45
html = html.replace('<span class="rank-count a">44</span>', '<span class="rank-count a">47</span>')  # aohige 1位
html = html.replace('<span class="rank-count j">32</span>', '<span class="rank-count j">34</span>')  # Jin 1位
# c2: sasuken 40→44 を Jin 39→40 より先に
html = html.replace('<span class="rank-count c2">40</span>', '<span class="rank-count c2">44</span>')  # sas c2
html = html.replace('<span class="rank-count c2">45</span>', '<span class="rank-count c2">46</span>')  # aohige c2
html = html.replace('<span class="rank-count c2">39</span>', '<span class="rank-count c2">40</span>')  # Jin c2
# c3
html = html.replace('<span class="rank-count c3">33</span>', '<span class="rank-count c3">34</span>')  # sas c3
html = html.replace('<span class="rank-count c3">25</span>', '<span class="rank-count c3">26</span>')  # aohige c3
html = html.replace('<span class="rank-count c3">43</span>', '<span class="rank-count c3">45</span>')  # Jin c3
html = html.replace('<div class="card-sub">114戦中</div>', '<div class="card-sub">119戦中</div>')
html = html.replace('<div class="total-num">114</div>', '<div class="total-num">119</div>')

# ── 4a. ゲーム別成績: タクタ 4→5戦, s3(75%)→3(60%), a0→1(20%), j1(25%)→1(20%) ──
html = html.replace(
    '        <td><span class="gtag">【アブストラクト（完全情報）】</span><a href="https://boardgamearena.com/gamepanel?game=tacta" target="_blank" rel="noopener">タクタ</a><br><span style="font-weight:400;color:#999;font-size:.75rem">Tacta</span></td>\n'
    '        <td>4</td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num s">3</span><div class="bar-bg"><div class="bar-fill bar-s" style="width:75%"></div></div></div></td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num a">0</span><div class="bar-bg"></div></div></td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num j">1</span><div class="bar-bg"><div class="bar-fill bar-j" style="width:25%"></div></div></div></td>',
    '        <td><span class="gtag">【アブストラクト（完全情報）】</span><a href="https://boardgamearena.com/gamepanel?game=tacta" target="_blank" rel="noopener">タクタ</a><br><span style="font-weight:400;color:#999;font-size:.75rem">Tacta</span></td>\n'
    '        <td>5</td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num s">3</span><div class="bar-bg"><div class="bar-fill bar-s" style="width:60%"></div></div></div></td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num a">1</span><div class="bar-bg"><div class="bar-fill bar-a" style="width:20%"></div></div></div></td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num j">1</span><div class="bar-bg"><div class="bar-fill bar-j" style="width:20%"></div></div></div></td>'
)

# ── 4b. ゲーム別成績: 新規4タイトル先頭追加（【ジャンル】付き） ──
def gs_row(genre, slug, jp, en, plays, s, a, j):
    def cell(cls, w):
        if w == 0:
            return f'<td><div class="win-bar-wrap"><span class="win-num {cls}">0</span><div class="bar-bg"></div></div></td>'
        pct = round(w / plays * 100)
        return (f'<td><div class="win-bar-wrap"><span class="win-num {cls}">{w}</span>'
                f'<div class="bar-bg"><div class="bar-fill bar-{cls}" style="width:{pct}%"></div></div></div></td>')
    return ('      <tr>\n'
            f'        <td><span class="gtag">【{genre}】</span><a href="https://boardgamearena.com/gamepanel?game={slug}" target="_blank" rel="noopener">{jp}</a><br>'
            f'<span style="font-weight:400;color:#999;font-size:.75rem">{en}</span></td>\n'
            f'        <td>{plays}</td>\n'
            f'        {cell("s", s)}\n        {cell("a", a)}\n        {cell("j", j)}\n      </tr>\n')
new_gs = (
    gs_row('カード／タイルドラフト','fantasytiles','ファンタジータイルズ','Fantasy Tiles',1,0,0,1) +
    gs_row('ブラフ・ダイス','escapefromthehiddencastle','ヒューゴ: オバケと鬼ごっこ','HUGO',1,0,0,1) +
    gs_row('エリアマジョリティ・陣取り','gunsen','軍扇: トシ・ランボの戦い','Gunsen: The Battle for Toshi Ranbo',1,0,1,0) +
    gs_row('カード／タイルドラフト','cities','シティーズ','Cities',1,0,1,0)
)
_anchor = '    <tbody>\n      <tr>\n        <td><span class="gtag">【スピード・アクション・パズル】</span><a href="https://boardgamearena.com/gamepanel?game=thelast"'
assert html.count(_anchor) == 1, f"gs anchor={html.count(_anchor)}"
html = html.replace(_anchor, '    <tbody>\n' + new_gs + '      <tr>\n        <td><span class="gtag">【スピード・アクション・パズル】</span><a href="https://boardgamearena.com/gamepanel?game=thelast"')

# ── 5. 棒グラフ（スケール20維持） ──
# 10分 j5→6(120)
html = html.replace(
    '            <!-- 10分: s=7(140px), a=3(60px), j=5(100px) -->\n'
    '            <div class="pt-group">\n'
    '              <div class="pt-bar bar-s" style="height:140px;background:var(--s)" title="sasuken2999: 7勝"><span class="pt-n">7</span></div>\n'
    '              <div class="pt-bar bar-a" style="height:60px;background:var(--a)" title="aohige nagoya: 3勝"><span class="pt-n">3</span></div>\n'
    '              <div class="pt-bar bar-j" style="height:100px;background:var(--j)" title="Jin2798: 5勝"><span class="pt-n">5</span></div>\n'
    '            </div>',
    '            <!-- 10分: s=7(140px), a=3(60px), j=6(120px) -->\n'
    '            <div class="pt-group">\n'
    '              <div class="pt-bar bar-s" style="height:140px;background:var(--s)" title="sasuken2999: 7勝"><span class="pt-n">7</span></div>\n'
    '              <div class="pt-bar bar-a" style="height:60px;background:var(--a)" title="aohige nagoya: 3勝"><span class="pt-n">3</span></div>\n'
    '              <div class="pt-bar bar-j" style="height:120px;background:var(--j)" title="Jin2798: 6勝"><span class="pt-n">6</span></div>\n'
    '            </div>'
)
# 20分 a11→13(260)
html = html.replace(
    '              <div class="pt-bar bar-a" style="height:220px;background:var(--a)" title="aohige nagoya: 11勝"><span class="pt-n">11</span></div>',
    '              <div class="pt-bar bar-a" style="height:260px;background:var(--a)" title="aohige nagoya: 13勝"><span class="pt-n">13</span></div>'
)
html = html.replace('<!-- 20分: s=19(380px), a=11(220px), j=15(300px) -->', '<!-- 20分: s=19(380px), a=13(260px), j=15(300px) -->')
# 30分 a8→9(180), j4→5(100)
html = html.replace(
    '            <!-- 30分: s=6(120px), a=8(160px), j=4(80px) -->\n'
    '            <div class="pt-group">\n'
    '              <div class="pt-bar bar-s" style="height:120px;background:var(--s)" title="sasuken2999: 6勝"><span class="pt-n">6</span></div>\n'
    '              <div class="pt-bar bar-a" style="height:160px;background:var(--a)" title="aohige nagoya: 8勝"><span class="pt-n">8</span></div>\n'
    '              <div class="pt-bar bar-j" style="height:80px;background:var(--j)" title="Jin2798: 4勝"><span class="pt-n">4</span></div>\n'
    '            </div>',
    '            <!-- 30分: s=6(120px), a=9(180px), j=5(100px) -->\n'
    '            <div class="pt-group">\n'
    '              <div class="pt-bar bar-s" style="height:120px;background:var(--s)" title="sasuken2999: 6勝"><span class="pt-n">6</span></div>\n'
    '              <div class="pt-bar bar-a" style="height:180px;background:var(--a)" title="aohige nagoya: 9勝"><span class="pt-n">9</span></div>\n'
    '              <div class="pt-bar bar-j" style="height:100px;background:var(--j)" title="Jin2798: 5勝"><span class="pt-n">5</span></div>\n'
    '            </div>'
)

# ── 6. X軸 ──
html = html.replace('それはオレの牧場だ！ / ザ・ラスト">9タイトル ▴</span>',
                    'それはオレの牧場だ！ / ザ・ラスト / ヒューゴ">10タイトル ▴</span>')
html = html.replace('/ チャレンジャーズ！ビーチカップ">26タイトル ▴</span>',
                    '/ チャレンジャーズ！ビーチカップ / シティーズ">27タイトル ▴</span>')
html = html.replace('/ Labyrinth / 西フランク王国の建築家">11タイトル ▴</span>',
                    '/ Labyrinth / 西フランク王国の建築家 / ファンタジータイルズ / 軍扇">13タイトル ▴</span>')

# ── 7. メイン履歴 シフト+挿入 ──
marker = '</div><!-- /tab-main -->'
idx = html.index(marker)
main_part, rest_part = html[:idx], html[idx:]
for i in range(114, 0, -1):
    main_part = main_part.replace(f'<td>{i}</td><td class="date">', f'<td>{i+5}</td><td class="date">')

def rrow(badge, cls, name, score):
    return f'          <div class="rrow"><span class="badge {badge}">{badge[-1]}位</span><span class="p-{cls}">{name}</span><span class="score">{score}pt</span></div>\n'
def hist(num, slug, jp, en, minutes, ranks):
    return ('\n      <tr>\n'
            f'        <td>{num}</td><td class="date">2026-11-20<br>（2日前）</td>\n'
            f'        <td class="game-name"><a href="https://boardgamearena.com/gamepanel?game={slug}" target="_blank" rel="noopener">{jp}</a><br>'
            f'<span style="font-weight:400;color:#999;font-size:.78rem">{en}</span></td>\n'
            f'        <td class="pt-time">{minutes}</td>\n'
            '        <td><div class="rank">\n' + ''.join(rrow(*r) for r in ranks) +
            '        </div></td>\n      </tr>\n')
new_rows = (
    hist(1,'tacta','タクタ','Tacta',20,[('b1','a','aohige nagoya','52'),('b2','s','sasuken2999','48'),('b3','j','Jin2798','41')]) +
    hist(2,'fantasytiles','ファンタジータイルズ','Fantasy Tiles',30,[('b1','j','Jin2798','240'),('b2','s','sasuken2999','231'),('b3','a','aohige nagoya','198')]) +
    hist(3,'escapefromthehiddencastle','ヒューゴ: オバケと鬼ごっこ','HUGO',10,[('b1','j','Jin2798','-19'),('b2','a','aohige nagoya','-29'),('b3','s','sasuken2999','-46')]) +
    hist(4,'gunsen','軍扇: トシ・ランボの戦い','Gunsen: The Battle for Toshi Ranbo',30,[('b1','a','aohige nagoya','7'),('b2','s','sasuken2999','4'),('b2','j','Jin2798','4')]) +
    hist(5,'cities','シティーズ','Cities',20,[('b1','a','aohige nagoya','69'),('b2','s','sasuken2999','64'),('b3','j','Jin2798','60')])
)
_hanchor = '    <tbody>\n\n      <tr>\n        <td>6</td><td class="date">2026-10-30<br>（23日前）</td>'
assert main_part.count(_hanchor) == 1, f"hist anchor={main_part.count(_hanchor)}"
main_part = main_part.replace(_hanchor, '    <tbody>\n' + new_rows + '      <tr>\n        <td>6</td><td class="date">2026-10-30<br>（23日前）</td>')
html = main_part + rest_part

with open(path, 'w', encoding='utf-8') as f:
    f.write(html)
print("Done!")

# ════ 検証 ════
import sys; sys.stdout.reconfigure(encoding='utf-8')
with open(path, encoding='utf-8') as f:
    h = f.read()
main_h = h[:h.index(marker)]
ok = ng = 0
def chk(n, c):
    global ok, ng
    print(('OK ' if c else 'NG ')+n); ok += bool(c); ng += (not c)
chk('header 11-22', '2026-11-22 集計' in h)
chk('no old header', '2026-10-30 集計' not in h)
chk('total 119', '<div class="total-num">119</div>' in h)
chk('card-sub 119 x3', h.count('<div class="card-sub">119戦中</div>') == 3)
chk('sas s=41', '<span class="rank-count s">41</span>' in h)
chk('aohige a=47', '<span class="rank-count a">47</span>' in h)
chk('Jin j=34', '<span class="rank-count j">34</span>' in h)
chk('sas c2=44', '<span class="rank-count c2">44</span>' in h)
chk('aohige c2=46', '<span class="rank-count c2">46</span>' in h)
chk('Jin c2=40', '<span class="rank-count c2">40</span>' in h)
chk('sas c3=34', '<span class="rank-count c3">34</span>' in h)
chk('aohige c3=26', '<span class="rank-count c3">26</span>' in h)
chk('Jin c3=45', '<span class="rank-count c3">45</span>' in h)
chk('sum sas 41+44+34=119', 41+44+34 == 119)
chk('sum aohige 47+46+26=119', 47+46+26 == 119)
chk('sum Jin 34+40+45=119', 34+40+45 == 119)
for g,jp in [('fantasytiles','ファンタジータイルズ'),('escapefromthehiddencastle','ヒューゴ: オバケと鬼ごっこ'),('gunsen','軍扇: トシ・ランボの戦い'),('cities','シティーズ')]:
    chk(f'gs {g}', f'game={g}" target="_blank" rel="noopener">{jp}' in h)
chk('tacta plays5', 'game=tacta" target="_blank" rel="noopener">タクタ</a><br><span style="font-weight:400;color:#999;font-size:.75rem">Tacta</span></td>\n        <td>5</td>' in h)
chk('gs new rows have gtag', h.count('【カード／タイルドラフト】<a href="https://boardgamearena.com/gamepanel?game=fantasytiles') == 1)
_gsm = main_h[main_h.index('id="ms-games"'):]; _gsm = _gsm[:_gsm.index('</table>')]
_plays = sum(int(x) for x in re.findall(r'</td>\n        <td>(\d+)</td>\n        <td><div class="win-bar-wrap"', _gsm))
chk(f'gs plays sum=119 (found {_plays})', _plays == 119)
chk('10min j=6', '<!-- 10分: s=7(140px), a=3(60px), j=6(120px) -->' in h)
chk('20min a=13', '<!-- 20分: s=19(380px), a=13(260px), j=15(300px) -->' in h)
chk('30min a=9 j=5', '<!-- 30分: s=6(120px), a=9(180px), j=5(100px) -->' in h)
chk('no bar over 400', 'height:420px;background' not in h and 'height:400px;background' not in h)
chk('scale 20', h.count('<span class="pt-yl">') == 10)
def bs(cls): return sum(int(x) for x in re.findall(r'pt-bar '+cls+r'[^>]*title="[^"]*: (\d+)勝"', main_h))
chk('bar sum sas=41', bs('bar-s') == 41)
chk('bar sum aohige=47', bs('bar-a') == 47)
chk('bar sum Jin=34', bs('bar-j') == 34)
chk('x10 10titles', 'ザ・ラスト / ヒューゴ">10タイトル' in h)
chk('x20 27titles', 'シティーズ">27タイトル' in h)
chk('x30 13titles', 'ファンタジータイルズ / 軍扇">13タイトル' in h)
chk('row1 tacta 2days', '<td>1</td><td class="date">2026-11-20<br>（2日前）</td>' in main_h)
chk('row5 cities 2days', '<td>5</td><td class="date">2026-11-20<br>（2日前）</td>' in main_h)
chk('row6 former1 10-30', '<td>6</td><td class="date">2026-10-30<br>（23日前）</td>' in main_h)
chk('gunsen tie 2xb2', main_h.count('<span class="badge b2">2位</span><span class="p-j">Jin2798</span><span class="score">4pt</span>') == 1)
mr = len(re.findall(r'<td>\d+</td><td class="date">', main_h))
chk(f'main 119 rows (found {mr})', mr == 119)
print(f'\nResult: {ok} OK / {ng} NG')
