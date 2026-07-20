path = r"bga_results.html"
with open(path, encoding='utf-8') as f:
    html = f.read()

# オルレアン ゲーム別成績: 1戦(a=1 100%) → 2戦(a=2 100%)
old = (
    '        <td><a href="https://boardgamearena.com/gamepanel?game=orleans" target="_blank" rel="noopener">オルレアン</a><br><span style="font-weight:400;color:#999;font-size:.75rem">Orléans</span></td>\n'
    '        <td>1</td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num s">0</span><div class="bar-bg"></div></div></td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num a">1</span><div class="bar-bg"><div class="bar-fill bar-a" style="width:100%"></div></div></div></td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num j">0</span><div class="bar-bg"></div></div></td>'
)
new = (
    '        <td><a href="https://boardgamearena.com/gamepanel?game=orleans" target="_blank" rel="noopener">オルレアン</a><br><span style="font-weight:400;color:#999;font-size:.75rem">Orléans</span></td>\n'
    '        <td>2</td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num s">0</span><div class="bar-bg"></div></div></td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num a">2</span><div class="bar-bg"><div class="bar-fill bar-a" style="width:100%"></div></div></div></td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num j">0</span><div class="bar-bg"></div></div></td>'
)

assert html.count(old) == 1, f"anchor not unique: {html.count(old)}"
html = html.replace(old, new)

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

chk('orleans plays=2',  new in h)
chk('orleans old gone', old not in h)

# ゲーム別成績テーブルの対戦数合計が66になること
import re
marker = '</div><!-- /tab-main -->'
main_h = h[:h.index(marker)]
gs_start = main_h.index('<table class="gs-table">')
gs_end   = main_h.index('</table>', gs_start)
gs = main_h[gs_start:gs_end]
plays = [int(m) for m in re.findall(r'</td>\n        <td>(\d+)</td>\n', gs)]
chk(f'gamestats total plays = 66 (found {sum(plays)} over {len(plays)} titles)', sum(plays) == 66)

# 1位の合計が66になること（同点1位があるため >= 66 を許容せず実数を表示）
wins_s = sum(int(m) for m in re.findall(r'win-num s">(\d+)<', gs))
wins_a = sum(int(m) for m in re.findall(r'win-num a">(\d+)<', gs))
wins_j = sum(int(m) for m in re.findall(r'win-num j">(\d+)<', gs))
print(f'   gamestats wins: s={wins_s}, a={wins_a}, j={wins_j}, sum={wins_s+wins_a+wins_j}')
chk('gamestats s wins = 21',  wins_s == 21)
chk('gamestats a wins = 31',  wins_a == 31)
chk('gamestats j wins = 14',  wins_j == 14)

print(f'\nResult: {ok} OK / {ng} NG')
