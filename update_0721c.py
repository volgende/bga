# 既存の集計漏れ修正: テラフォーミング・マーズ ゲーム別成績 aohige 1勝 → 2勝
# （履歴では 2026-04-21 / 2026-04-08 の2戦ともaohigeが1位。棒グラフ120分 a=2 は既に正しい）
path = r"bga_results.html"
with open(path, encoding='utf-8') as f:
    html = f.read()

old = (
    '        <td><a href="https://boardgamearena.com/gamepanel?game=terraformingmars" target="_blank" rel="noopener">テラフォーミング・マーズ</a><br><span style="font-weight:400;color:#999;font-size:.75rem">Terraforming Mars</span></td>\n'
    '        <td>2</td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num s">0</span><div class="bar-bg"></div></div></td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num a">1</span><div class="bar-bg"><div class="bar-fill bar-a" style="width:100%"></div></div></div></td>\n'
    '        <td><div class="win-bar-wrap"><span class="win-num j">0</span><div class="bar-bg"></div></div></td>'
)
new = old.replace('<span class="win-num a">1</span>', '<span class="win-num a">2</span>')

assert html.count(old) == 1, f"anchor not unique: {html.count(old)}"
html = html.replace(old, new)

with open(path, 'w', encoding='utf-8') as f:
    f.write(html)

print("Done!")
