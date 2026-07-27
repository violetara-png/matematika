# -*- coding: utf-8 -*-
"""Sukuria mokytojo-lapas.html iš skill šablono: pilni sprendimai + seifo kodai.
Sprendimus (sol) skaito tiesiai iš _data.js VARIANTS (gen_escape.py juos apskaičiuoja
iš fractions)."""
import re, io, json

with io.open("_data.js", encoding="utf-8") as f:
    js = f.read()

# ištraukiam kiekvieną variantą (blokas tarp [ ... ]) ir jame kiekvieną stotelę
variant_blocks = re.findall(r'\[\s*((?:\{[^}]*\},?\s*)+)\]', js, re.S)
variants = []
for blk in variant_blocks:
    items = re.findall(
        r'\{\s*title:"([^"]*)",\s*eq:"([^"]*)",\s*q:"((?:[^"\\]|\\.)*)",\s*ans:(\d),\s*sol:"((?:[^"\\]|\\.)*)"\s*\}',
        blk)
    if items:
        variants.append(items)

def unesc(s):
    return s.replace('\\"','"').replace('\\\\','\\')

# sudarom teacher VARIANTS JS
tv = []
for vi, items in enumerate(variants):
    code = "".join(a for (_,_,_,a,_) in items)
    rows = []
    for idx,(title,eq,q,ans,sol) in enumerate(items, 1):
        eq = unesc(eq); q = unesc(q); sol = unesc(sol)
        if eq.strip()=="":
            rows.append(f'   ["{idx}w",{json.dumps(q, ensure_ascii=False)},{json.dumps(sol, ensure_ascii=False)},{ans}],')
        else:
            rows.append(f'   [{idx},{json.dumps(eq, ensure_ascii=False)},{json.dumps(sol, ensure_ascii=False)},{ans}],')
    tv.append(f' {{ code:"{code}", rows:[\n' + "\n".join(rows) + "\n ]}")
teacher_js = "const VARIANTS = [\n" + ",\n".join(tv) + "\n];\n"

# patikra
for vi, items in enumerate(variants,1):
    code = "".join(a for (_,_,_,a,_) in items)
    assert len(code)==10, (vi, code)
print("Variantų:", len(variants), "kodai:", ["".join(a for (_,_,_,a,_) in v) for v in variants])

# --- įdedam į šabloną ---
TPL = r"c:\Users\Violeta\Desktop\Ai asistentas\.claude\skills\pabegimo-kambarys\references\mokytojo-lapas-template.html"
with io.open(TPL, encoding="utf-8") as f:
    html = f.read()

html = html.replace("Mokytojo lapas · Pabėgimo kambarys · Lygtys · 6 kl.",
                    "Mokytojo lapas · Pabėgimo kambarys · Dalijimas proporcingai · 6 kl.")
html = html.replace(
    'Tema: <b>Lygtys</b> · 6 klasė · Profesoriaus Lygtickio laboratorija · 10 spynų · 4 variantai',
    'Tema: <b>Dalijimas proporcingai</b> (6.2.3) · 6 klasė · Slaptasis seifas · 10 ratukų · 4 variantai')
html = html.replace("sprendžia 10 lygčių iš eilės. Kiekvienos lygties sprendinys <b>x</b> yra vienas galutinio seifo kodo",
                    "sprendžia 10 dalijimo galvosūkių iš eilės. Kiekvieno atsakymas (vienaženklė dalis) yra vienas galutinio seifo kodo")
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
