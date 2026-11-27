# -*- coding: utf-8 -*-
import re
from datetime import date, datetime

path = r"bga_results.html"
with open(path, encoding='utf-8') as f:
    html = f.read()

today = date(2026, 11, 27)

# ════ 新規3戦（すべて本日2026-11-27・3人戦）════
#  1 シフティング・ストーンズ(shiftingstones,20分,既存) 1位aohige19/2位sas17/3位Jin16  W:aohige
#  2 ハーモニーズ(harmonies,20分,新)                    1位Jin93/2位aohige82/3位sas78    W:Jin
#  3 ファンタジータイルズ(fantasytiles,30分,既存)        1位Jin190/2位sas175/3位aohige160 W:Jin

# ── 1. ヘッダー ──
html = html.replace('2026-11-22 集計', '2026-11-27 集計')

# ── 2. 相対日付（today=2026-11-27） ──
def upd_date(m):
    d = datetime.strptime(m.group(1), '%Y-%m-%d').date()
    n = (today - d).days
    return f'<td class="date">{m.group(1)}<br>（{"本日" if n==0 else str(n)+"日前"}）</td>'
html = re.sub(r'<td class="date">(\d{4}-\d{2}-\d{2})<br>（[^）]+）</td>', upd_date, html)

# ── 3. メインカード 119→122 ──
# sasuken 41/44/34→41/46/35, aohige 47/46/26→48/47/27, Jin 34/40/45→36/40/46
html = html.replace('<span class="rank-count a">47</span>', '<span class="rank-count a">48</span>')  # aohige 1位
html = html.replace('<span class="rank-count j">34</span>', '<span class="rank-count j">36</span>')  # Jin 1位
# c2: aohige 46→47 を sasuken 44→46 より先に（46の衝突回避）
html = html.replace('<span class="rank-count c2">46</span>', '<span class="rank-count c2">47</span>')  # aohige c2
html = html.replace('<span class="rank-count c2">44</span>', '<span class="rank-count c2">46</span>')  # sas c2
# c3
html = html.replace('<span class="rank-count c3">34</span>', '<span class="rank-count c3">35</span>')  # sas c3
html = html.replace('<span class="rank-count c3">26</span>', '<span class="rank-count c3">27</span>')  # aohige c3
html = html.replace('<span class="rank-count c3">45</span>', '<span class="rank-count c3">46</span>')  # Jin c3
html = html.replace('<div class="card-sub">119戦中</div>', '<div class="card-sub">122戦中</div>')
html = html.replace('<div class="total-num">119</div>', '<div class="total-num">122</div>')

# ── 4a. ゲーム別成績 既存増分 ──
# シフティング・ストーンズ 2→3戦, s1(50%)→1(33%), a1(50%)→2(67%)
html = html.replace(
    '        <td><span class="gtag">【アブストラクト（完全情報）】</span><a href="https://boardgamearena.com/gamepanel?game=shiftingstones" target="_blank" rel="noopener">シフティング・ストーンズ</a><br><span style="font-weight:400;color:#999;font-size:.75rem">Shifting Stones</span></td>\n'
    '        <td>2</td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num s">1</span><div class="bar-bg"><div class="bar-fill bar-s" style="width:50%"></div></div></div></td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num a">1</span><div class="bar-bg"><div class="bar-fill bar-a" style="width:50%"></div></div></div></td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num j">0</span><div class="bar-bg"></div></div></td>',
    '        <td><span class="gtag">【アブストラクト（完全情報）】</span><a href="https://boardgamearena.com/gamepanel?game=shiftingstones" target="_blank" rel="noopener">シフティング・ストーンズ</a><br><span style="font-weight:400;color:#999;font-size:.75rem">Shifting Stones</span></td>\n'
    '        <td>3</td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num s">1</span><div class="bar-bg"><div class="bar-fill bar-s" style="width:33%"></div></div></div></td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num a">2</span><div class="bar-bg"><div class="bar-fill bar-a" style="width:67%"></div></div></div></td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num j">0</span><div class="bar-bg"></div></div></td>'
)
# ファンタジータイルズ 1→2戦, j1(100%)→2(100%)
html = html.replace(
    '        <td><span class="gtag">【カード／タイルドラフト】</span><a href="https://boardgamearena.com/gamepanel?game=fantasytiles" target="_blank" rel="noopener">ファンタジータイルズ</a><br><span style="font-weight:400;color:#999;font-size:.75rem">Fantasy Tiles</span></td>\n'
    '        <td>1</td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num s">0</span><div class="bar-bg"></div></div></td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num a">0</span><div class="bar-bg"></div></div></td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num j">1</span><div class="bar-bg"><div class="bar-fill bar-j" style="width:100%"></div></div></div></td>',
    '        <td><span class="gtag">【カード／タイルドラフト】</span><a href="https://boardgamearena.com/gamepanel?game=fantasytiles" target="_blank" rel="noopener">ファンタジータイルズ</a><br><span style="font-weight:400;color:#999;font-size:.75rem">Fantasy Tiles</span></td>\n'
    '        <td>2</td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num s">0</span><div class="bar-bg"></div></div></td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num a">0</span><div class="bar-bg"></div></div></td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num j">2</span><div class="bar-bg"><div class="bar-fill bar-j" style="width:100%"></div></div></div></td>'
)

# ── 4b. ゲーム別成績 新規ハーモニーズを先頭に追加（fantasytilesの前） ──
harmonies_row = (
    '      <tr>\n'
    '        <td><span class="gtag">【カード／タイルドラフト】</span><a href="https://boardgamearena.com/gamepanel?game=harmonies" target="_blank" rel="noopener">ハーモニーズ</a><br>'
    '<span style="font-weight:400;color:#999;font-size:.75rem">Harmonies</span></td>\n'
    '        <td>1</td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num s">0</span><div class="bar-bg"></div></div></td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num a">0</span><div class="bar-bg"></div></div></td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num j">1</span><div class="bar-bg"><div class="bar-fill bar-j" style="width:100%"></div></div></div></td>\n'
    '      </tr>\n'
)
_anchor = '    <tbody>\n      <tr>\n        <td><span class="gtag">【カード／タイルドラフト】</span><a href="https://boardgamearena.com/gamepanel?game=fantasytiles"'
assert html.count(_anchor) == 1, f"gs anchor={html.count(_anchor)}"
html = html.replace(_anchor, '    <tbody>\n' + harmonies_row + '      <tr>\n        <td><span class="gtag">【カード／タイルドラフト】</span><a href="https://boardgamearena.com/gamepanel?game=fantasytiles"')

# ── 5. 棒グラフ（スケール20維持） ──
# 20分 a13→14(280), j15→16(320)
html = html.replace(
    '            <!-- 20分: s=19(380px), a=13(260px), j=15(300px) -->\n'
    '            <div class="pt-group">\n'
    '              <div class="pt-bar bar-s" style="height:380px;background:var(--s)" title="sasuken2999: 19勝"><span class="pt-n">19</span></div>\n'
    '              <div class="pt-bar bar-a" style="height:260px;background:var(--a)" title="aohige nagoya: 13勝"><span class="pt-n">13</span></div>\n'
    '              <div class="pt-bar bar-j" style="height:300px;background:var(--j)" title="Jin2798: 15勝"><span class="pt-n">15</span></div>\n'
    '            </div>',
    '            <!-- 20分: s=19(380px), a=14(280px), j=16(320px) -->\n'
    '            <div class="pt-group">\n'
    '              <div class="pt-bar bar-s" style="height:380px;background:var(--s)" title="sasuken2999: 19勝"><span class="pt-n">19</span></div>\n'
    '              <div class="pt-bar bar-a" style="height:280px;background:var(--a)" title="aohige nagoya: 14勝"><span class="pt-n">14</span></div>\n'
    '              <div class="pt-bar bar-j" style="height:320px;background:var(--j)" title="Jin2798: 16勝"><span class="pt-n">16</span></div>\n'
    '            </div>'
)
# 30分 j5→6(120)
html = html.replace(
    '              <div class="pt-bar bar-j" style="height:100px;background:var(--j)" title="Jin2798: 5勝"><span class="pt-n">5</span></div>\n'
    '            </div>',
    '              <div class="pt-bar bar-j" style="height:120px;background:var(--j)" title="Jin2798: 6勝"><span class="pt-n">6</span></div>\n'
    '            </div>', 1
)
html = html.replace('<!-- 30分: s=6(120px), a=9(180px), j=5(100px) -->', '<!-- 30分: s=6(120px), a=9(180px), j=6(120px) -->')

# ── 6. X軸 20分 27→28 ──
html = html.replace('/ チャレンジャーズ！ビーチカップ / シティーズ">27タイトル ▴</span>',
                    '/ チャレンジャーズ！ビーチカップ / シティーズ / ハーモニーズ">28タイトル ▴</span>')

# ── 7. メイン履歴 シフト+挿入 ──
marker = '</div><!-- /tab-main -->'
idx = html.index(marker)
main_part, rest_part = html[:idx], html[idx:]
for i in range(119, 0, -1):
    main_part = main_part.replace(f'<td>{i}</td><td class="date">', f'<td>{i+3}</td><td class="date">')

def rrow(badge, cls, name, score):
    return f'          <div class="rrow"><span class="badge {badge}">{badge[-1]}位</span><span class="p-{cls}">{name}</span><span class="score">{score}pt</span></div>\n'
def hist(num, slug, jp, en, minutes, ranks):
    return ('\n      <tr>\n'
            f'        <td>{num}</td><td class="date">2026-11-27<br>（本日）</td>\n'
            f'        <td class="game-name"><a href="https://boardgamearena.com/gamepanel?game={slug}" target="_blank" rel="noopener">{jp}</a><br>'
            f'<span style="font-weight:400;color:#999;font-size:.78rem">{en}</span></td>\n'
            f'        <td class="pt-time">{minutes}</td>\n'
            '        <td><div class="rank">\n' + ''.join(rrow(*r) for r in ranks) +
            '        </div></td>\n      </tr>\n')
new_rows = (
    hist(1,'shiftingstones','シフティング・ストーンズ','Shifting Stones',20,[('b1','a','aohige nagoya','19'),('b2','s','sasuken2999','17'),('b3','j','Jin2798','16')]) +
    hist(2,'harmonies','ハーモニーズ','Harmonies',20,[('b1','j','Jin2798','93'),('b2','a','aohige nagoya','82'),('b3','s','sasuken2999','78')]) +
    hist(3,'fantasytiles','ファンタジータイルズ','Fantasy Tiles',30,[('b1','j','Jin2798','190'),('b2','s','sasuken2999','175'),('b3','a','aohige nagoya','160')])
)
_hanchor = '    <tbody>\n\n      <tr>\n        <td>4</td><td class="date">2026-11-20<br>（7日前）</td>'
assert main_part.count(_hanchor) == 1, f"hist anchor={main_part.count(_hanchor)}"
main_part = main_part.replace(_hanchor, '    <tbody>\n' + new_rows + '      <tr>\n        <td>4</td><td class="date">2026-11-20<br>（7日前）</td>')
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
chk('header 11-27', '2026-11-27 集計' in h)
chk('no old header', '2026-11-22 集計' not in h)
chk('total 122', '<div class="total-num">122</div>' in h)
chk('card-sub 122 x3', h.count('<div class="card-sub">122戦中</div>') == 3)
chk('aohige a=48', '<span class="rank-count a">48</span>' in h)
chk('Jin j=36', '<span class="rank-count j">36</span>' in h)
chk('sas c2=46', '<span class="rank-count c2">46</span>' in h)
chk('aohige c2=47', '<span class="rank-count c2">47</span>' in h)
chk('Jin c2=40 kept', '<span class="rank-count c2">40</span>' in h)
chk('sas c3=35', '<span class="rank-count c3">35</span>' in h)
chk('aohige c3=27', '<span class="rank-count c3">27</span>' in h)
chk('Jin c3=46', '<span class="rank-count c3">46</span>' in h)
chk('sum sas 41+46+35=122', 41+46+35 == 122)
chk('sum aohige 48+47+27=122', 48+47+27 == 122)
chk('sum Jin 36+40+46=122', 36+40+46 == 122)
chk('gs harmonies', 'game=harmonies" target="_blank" rel="noopener">ハーモニーズ' in h)
chk('shifting plays3', 'game=shiftingstones" target="_blank" rel="noopener">シフティング・ストーンズ</a><br><span style="font-weight:400;color:#999;font-size:.75rem">Shifting Stones</span></td>\n        <td>3</td>' in h)
chk('fantasy plays2', 'game=fantasytiles" target="_blank" rel="noopener">ファンタジータイルズ</a><br><span style="font-weight:400;color:#999;font-size:.75rem">Fantasy Tiles</span></td>\n        <td>2</td>' in h)
chk('harmonies gtag', '【カード／タイルドラフト】</span><a href="https://boardgamearena.com/gamepanel?game=harmonies' in h)
_gsm = main_h[main_h.index('id="ms-games"'):]; _gsm = _gsm[:_gsm.index('</table>')]
_plays = sum(int(x) for x in re.findall(r'</td>\n        <td>(\d+)</td>\n        <td><div class="win-bar-wrap"', _gsm))
chk(f'gs plays sum=122 (found {_plays})', _plays == 122)
chk('20min a=14 j=16', '<!-- 20分: s=19(380px), a=14(280px), j=16(320px) -->' in h)
chk('30min j=6', '<!-- 30分: s=6(120px), a=9(180px), j=6(120px) -->' in h)
chk('no bar over 400', 'height:420px;background' not in h and 'height:400px;background' not in h)
chk('scale 20', h.count('<span class="pt-yl">') == 10)
def bs(cls): return sum(int(x) for x in re.findall(r'pt-bar '+cls+r'[^>]*title="[^"]*: (\d+)勝"', main_h))
chk('bar sum sas=41', bs('bar-s') == 41)
chk('bar sum aohige=48', bs('bar-a') == 48)
chk('bar sum Jin=36', bs('bar-j') == 36)
chk('x20 28titles', 'シティーズ / ハーモニーズ">28タイトル' in h)
chk('row1 shifting today', '<td>1</td><td class="date">2026-11-27<br>（本日）</td>' in main_h)
chk('row3 fantasy today', '<td>3</td><td class="date">2026-11-27<br>（本日）</td>' in main_h)
chk('row4 former1 11-20', '<td>4</td><td class="date">2026-11-20<br>（7日前）</td>' in main_h)
mr = len(re.findall(r'<td>\d+</td><td class="date">', main_h))
chk(f'main 122 rows (found {mr})', mr == 122)
print(f'\nResult: {ok} OK / {ng} NG')
