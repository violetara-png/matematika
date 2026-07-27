# -*- coding: utf-8 -*-
"""Sukuria mokytojo-lapas.html iš skill šablono: pilni sprendimai + seifo kodai,
paimti iš tų pačių stotelių duomenų (_data.js VARIANTS su „sol" lauku)."""
import re, io, json

# --- Perskaitom VARIANTS iš _data.js (JSON-suderinamas JS) ---
with io.open("_data.js", encoding="utf-8") as f:
    js = f.read()
marker = "const VARIANTS ="
varpart = js[js.index(marker) + len(marker):].strip()
if varpart.endswith(";"):
    varpart = varpart[:-1]
variants = json.loads(varpart)   # sąrašas 4 variantų, kiekvienas — 10 stotelių dict'ų

# --- sudarom teacher VARIANTS struktūrą ---
teacher = []
for v in variants:
    code = "".join(str(s["ans"]) for s in v)
    assert len(code) == 10, code
    rows = []
    for idx, s in enumerate(v, 1):
        if s["eq"].strip() == "":
            rows.append([f"{idx}w", s["q"], s["sol"], s["ans"]])
        else:
            rows.append([idx, s["eq"], s["sol"], s["ans"]])
    teacher.append({"code": code, "rows": rows})

teacher_js = "const VARIANTS = " + json.dumps(teacher, ensure_ascii=False, indent=1) + ";\n"
print("Variantų:", len(teacher), "kodai:", [t["code"] for t in teacher])

# --- įdedam į šabloną ---
TPL = r"c:\Users\Violeta\Desktop\Ai asistentas\.claude\skills\pabegimo-kambarys\references\mokytojo-lapas-template.html"
with io.open(TPL, encoding="utf-8") as f:
    html = f.read()

html = html.replace("Mokytojo lapas · Pabėgimo kambarys · Lygtys · 6 kl.",
                    "Mokytojo lapas · Pabėgimo kambarys · Ieškome viso skaičiaus · 6 kl.")
html = html.replace(
    'Tema: <b>Lygtys</b> · 6 klasė · Profesoriaus Lygtickio laboratorija · 10 spynų · 4 variantai',
    'Tema: <b>Ieškome viso skaičiaus</b> (6.1.3) · 6 klasė · Slaptasis seifas · 10 ratukų · 4 variantai')
html = html.replace("sprendžia 10 lygčių iš eilės. Kiekvienos lygties sprendinys <b>x</b> yra vienas galutinio seifo kodo",
                    "sprendžia 10 „rask visą skaičių“ galvosūkių iš eilės. Kiekvieno atsakymas (vienaženklis) yra vienas galutinio seifo kodo")
html = html.replace("skaitmuo (iš eilės nuo 1 iki 10 spynos). Surinkęs visą kodą ir įvedęs jį į seifą, mokinys „pabėga\".",
                    "skaitmuo (iš eilės nuo 1 iki 10 ratuko). Surinkęs visą kodą ir įvedęs jį į seifą, mokinys „pabėga“.")
html = html.replace('priminkite mygtuką „💡 Patarimas" prie kiekvienos spynos.',
                    'priminkite mygtuką „💡 Patarimas“ prie kiekvieno ratuko.')

# pakeičiam VARIANTS bloką
pat = re.compile(r'const VARIANTS = \[.*?\];\n', re.S)
assert pat.search(html), "nerastas VARIANTS blokas šablone"
html = pat.sub(teacher_js, html, count=1)

with io.open("mokytojo-lapas.html", "w", encoding="utf-8") as f:
    f.write(html)
print("mokytojo-lapas.html sukurtas,", len(html), "simb.")
