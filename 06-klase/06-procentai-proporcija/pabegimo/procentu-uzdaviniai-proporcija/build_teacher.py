# -*- coding: utf-8 -*-
"""Sukuria mokytojo-lapas.html iš skill šablono: pilni sprendimai (proporcija) +
seifo kodai, recomputuoti iš tų pačių stotelių duomenų (_data.js VARIANTS)."""
import re, io, json

with io.open("_data.js", encoding="utf-8") as f:
    js = f.read()
variant_blocks = re.findall(r'\[\s*((?:\{[^}]*\},?\s*)+)\]', js, re.S)
variants = []
for blk in variant_blocks:
    items = re.findall(r'\{\s*title:"([^"]*)",\s*eq:"([^"]*)",\s*q:"([^"]*)",\s*ans:(\d)\s*\}', blk)
    if items:
        variants.append(items)

def solution(eq, ans):
    eq = eq.strip()
    # pct: "A iš N = ? %"
    m = re.match(r'(\d+) iš (\d+) = \? %', eq)
    if m:
        a, N = int(m.group(1)), int(m.group(2))
        return f"{N} atitinka 100 %, {a} atitinka x %  →  {a} · 100 : {N} = {ans} %"
    # whole: "P % nuo ? = A"
    m = re.match(r'(\d+) % nuo \? = (\d+)', eq)
    if m:
        p, a = int(m.group(1)), int(m.group(2))
        return f"100 % atitinka x, {p} % atitinka {a}  →  {a} · 100 : {p} = {ans}"
    # part: "P % nuo N = ?"
    m = re.match(r'(\d+) % nuo (\d+) = \?', eq)
    if m:
        p, N = int(m.group(1)), int(m.group(2))
        return f"100 % atitinka {N}, {p} % atitinka x  →  {N} · {p} : 100 = {ans}"
    return f"= {ans}"

tv = []
for vi, items in enumerate(variants):
    code = "".join(a for (_, _, _, a) in items)
    rows = []
    for idx, (title, eq, q, ans) in enumerate(items, 1):
        sol = solution(eq, ans)
        rows.append(f'   [{idx},"{eq}",{json.dumps(sol, ensure_ascii=False)},{ans}],')
    tv.append(f' {{ code:"{code}", rows:[\n' + "\n".join(rows) + "\n ]}")
teacher_js = "const VARIANTS = [\n" + ",\n".join(tv) + "\n];\n"

for vi, items in enumerate(variants, 1):
    code = "".join(a for (_, _, _, a) in items)
    assert len(code) == 10, (vi, code)
print("Variantų:", len(variants), "kodai:", ["".join(a for (_, _, _, a) in v) for v in variants])

TPL = r"c:\Users\Violeta\Desktop\Ai asistentas\.claude\skills\pabegimo-kambarys\references\mokytojo-lapas-template.html"
with io.open(TPL, encoding="utf-8") as f:
    html = f.read()

html = html.replace("Mokytojo lapas · Pabėgimo kambarys · Lygtys · 6 kl.",
                    "Mokytojo lapas · Pabėgimo kambarys · Procentai per proporciją · 6 kl.")
html = html.replace(
    'Tema: <b>Lygtys</b> · 6 klasė · Profesoriaus Lygtickio laboratorija · 10 spynų · 4 variantai',
    'Tema: <b>Procentų uždaviniai sudarant proporciją</b> (6.2.2) · 6 klasė · Slaptasis seifas · 10 ratukų · 4 variantai')
html = html.replace("sprendžia 10 lygčių iš eilės. Kiekvienos lygties sprendinys <b>x</b> yra vienas galutinio seifo kodo",
                    "sprendžia 10 procentų uždavinių iš eilės (sudarydami proporciją). Kiekvieno atsakymas (vienaženklis) yra vienas galutinio seifo kodo")
html = html.replace("skaitmuo (iš eilės nuo 1 iki 10 spynos). Surinkęs visą kodą ir įvedęs jį į seifą, mokinys „pabėga\".",
                    "skaitmuo (iš eilės nuo 1 iki 10 ratuko). Surinkęs visą kodą ir įvedęs jį į seifą, mokinys „pabėga“.")
html = html.replace('priminkite mygtuką „💡 Patarimas" prie kiekvienos spynos.',
                    'priminkite mygtuką „💡 Patarimas“ prie kiekvieno ratuko.')

pat = re.compile(r'const VARIANTS = \[.*?\];\n', re.S)
assert pat.search(html)
html = pat.sub(teacher_js, html, count=1)

with io.open("mokytojo-lapas.html", "w", encoding="utf-8") as f:
    f.write(html)
print("mokytojo-lapas.html sukurtas,", len(html), "simb.")
