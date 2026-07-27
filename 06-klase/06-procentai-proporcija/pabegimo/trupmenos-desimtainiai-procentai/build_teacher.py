# -*- coding: utf-8 -*-
"""Sukuria mokytojo-lapas.html iš skill šablono: pilni sprendimai + seifo kodai,
recomputuoti iš tų pačių stotelių duomenų (_data.js VARIANTS)."""
import re, io, json

# Perskaitom VARIANTS iš _data.js (JS -> pasiimam eq/q/ans)
with io.open("_data.js", encoding="utf-8") as f:
    js = f.read()
# ištraukiam kiekvieno objekto eq ir ans
variant_blocks = re.findall(r'\[\s*((?:\{[^}]*\},?\s*)+)\]', js, re.S)
# pirmas match yra HINTS masyvas? HINTS neturi { }, tad regex ima tik VARIANTS objektų blokus
variants = []
for blk in variant_blocks:
    items = re.findall(r'\{\s*title:"([^"]*)",\s*eq:"([^"]*)",\s*q:"([^"]*)",\s*ans:(\d)\s*\}', blk)
    if items:
        variants.append(items)

def solution(eq, ans):
    eq = eq.strip()
    m = re.match(r'0,0(\d) = \? %', eq)
    if m:
        return f"0,0{m.group(1)} · 100 = {ans} %"
    m = re.match(r'(\d)0 % = 0,\?', eq)
    if m:
        return f"{m.group(1)}0 % : 100 = 0,{m.group(1)}"
    m = re.match(r'(\d+)/(\d+) = \?0 %', eq)
    if m:
        n, d = int(m.group(1)), int(m.group(2))
        pv = n*100//d
        return f"{n}/{d} · 100 = {pv} %  →  dešimčių skaitmuo {ans}"
    if eq.startswith("1/100"):
        return "1/100 · 100 = 1 %  (viena šimtoji = 1 %)"
    return f"= {ans}"

# sudarom teacher VARIANTS JS
tv = []
for vi, items in enumerate(variants):
    code = "".join(a for (_,_,_,a) in items)
    rows = []
    for idx,(title,eq,q,ans) in enumerate(items, 1):
        if eq.strip()=="":
            rows.append(f'   ["{idx}w",{json.dumps(q, ensure_ascii=False)},{json.dumps("= "+ans, ensure_ascii=False)},{ans}],')
        else:
            sol = solution(eq, ans)
            rows.append(f'   [{idx},"{eq}",{json.dumps(sol, ensure_ascii=False)},{ans}],')
    tv.append(f' {{ code:"{code}", rows:[\n' + "\n".join(rows) + "\n ]}")
teacher_js = "const VARIANTS = [\n" + ",\n".join(tv) + "\n];\n"

# patikra: kodas = ans iš eilės
for vi, items in enumerate(variants,1):
    code = "".join(a for (_,_,_,a) in items)
    assert len(code)==10, (vi, code)
print("Variantų:", len(variants), "kodai:", [ "".join(a for (_,_,_,a) in v) for v in variants])

# --- įdedam į šabloną ---
TPL = r"c:\Users\Violeta\Desktop\Ai asistentas\.claude\skills\pabegimo-kambarys\references\mokytojo-lapas-template.html"
with io.open(TPL, encoding="utf-8") as f:
    html = f.read()

html = html.replace("Mokytojo lapas · Pabėgimo kambarys · Lygtys · 6 kl.",
                    "Mokytojo lapas · Pabėgimo kambarys · Trupmenos, dešimtainiai, procentai · 6 kl.")
html = html.replace(
    'Tema: <b>Lygtys</b> · 6 klasė · Profesoriaus Lygtickio laboratorija · 10 spynų · 4 variantai',
    'Tema: <b>Trupmenos, dešimtainiai skaičiai, procentai</b> (6.1.1) · 6 klasė · Slaptasis seifas · 10 ratukų · 4 variantai')
html = html.replace("sprendžia 10 lygčių iš eilės. Kiekvienos lygties sprendinys <b>x</b> yra vienas galutinio seifo kodo",
                    "sprendžia 10 konvertavimo galvosūkių iš eilės. Kiekvieno atsakymas (vienaženklis) yra vienas galutinio seifo kodo")
html = html.replace("skaitmuo (iš eilės nuo 1 iki 10 spynos). Surinkęs visą kodą ir įvedęs jį į seifą, mokinys „pabėga\".",
                    "skaitmuo (iš eilės nuo 1 iki 10 ratuko). Surinkęs visą kodą ir įvedęs jį į seifą, mokinys „pabėga“.")
html = html.replace('priminkite mygtuką „💡 Patarimas" prie kiekvienos spynos.',
                    'priminkite mygtuką „💡 Patarimas“ prie kiekvieno ratuko.')

# pakeičiam VARIANTS bloką
pat = re.compile(r'const VARIANTS = \[.*?\];\n', re.S)
assert pat.search(html)
html = pat.sub(teacher_js, html, count=1)

with io.open("mokytojo-lapas.html","w",encoding="utf-8") as f:
    f.write(html)
print("mokytojo-lapas.html sukurtas,", len(html), "simb.")
