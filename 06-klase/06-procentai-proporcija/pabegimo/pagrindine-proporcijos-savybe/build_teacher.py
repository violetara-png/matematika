# -*- coding: utf-8 -*-
"""Sukuria mokytojo-lapas.html iš skill šablono: pilni sprendimai + seifo kodai,
recomputuoti iš tų pačių stotelių duomenų (_data.js VARIANTS). Tema: proporcijos."""
import re, io, json

# Perskaitom VARIANTS iš _data.js (JS -> pasiimam eq/q/ans)
with io.open("_data.js", encoding="utf-8") as f:
    js = f.read()
variant_blocks = re.findall(r'\[\s*((?:\{[^}]*\},?\s*)+)\]', js, re.S)
variants = []
for blk in variant_blocks:
    items = re.findall(r'\{\s*title:"([^"]*)",\s*eq:"([^"]*)",\s*q:"([^"]*)",\s*ans:(\d)\s*\}', blk)
    if items:
        variants.append(items)

def solution(eq, ans):
    """eq pavidalas: 'A : B = C : D  (x = ?)'. Grąžina žingsnius su pagrindine savybe."""
    core = eq.split("(")[0].strip()
    left, right = core.split("=")
    a, b = [t.strip() for t in left.split(":")]
    c, d = [t.strip() for t in right.split(":")]
    m = [a, b, c, d]
    xi = m.index("x")
    def prod(p, q):
        return int(p) * int(q)
    if xi == 0:   # x kraštinis
        return f"x · {d} = {b} · {c}  →  {d}x = {prod(b, c)}  →  x = {ans}"
    if xi == 3:   # x kraštinis
        return f"{a} · x = {b} · {c}  →  {a}x = {prod(b, c)}  →  x = {ans}"
    if xi == 1:   # x vidinis
        return f"{a} · {d} = x · {c}  →  {c}x = {prod(a, d)}  →  x = {ans}"
    if xi == 2:   # x vidinis
        return f"{a} · {d} = {b} · x  →  {b}x = {prod(a, d)}  →  x = {ans}"
    return f"= {ans}"

# sudarom teacher VARIANTS JS
tv = []
for vi, items in enumerate(variants):
    code = "".join(a for (_, _, _, a) in items)
    rows = []
    for idx, (title, eq, q, ans) in enumerate(items, 1):
        eq_show = eq.split("(")[0].strip()  # be „(x = ?)“
        sol = solution(eq, ans)
        rows.append(f'   [{idx},"{eq_show}",{json.dumps(sol, ensure_ascii=False)},{ans}],')
    tv.append(f' {{ code:"{code}", rows:[\n' + "\n".join(rows) + "\n ]}")
teacher_js = "const VARIANTS = [\n" + ",\n".join(tv) + "\n];\n"

# patikra: kodas = ans iš eilės, po 10 skaitmenų
for vi, items in enumerate(variants, 1):
    code = "".join(a for (_, _, _, a) in items)
    assert len(code) == 10, (vi, code)
print("Variantų:", len(variants), "kodai:", ["".join(a for (_, _, _, a) in v) for v in variants])

# --- įdedam į šabloną ---
TPL = r"c:\Users\Violeta\Desktop\Ai asistentas\.claude\skills\pabegimo-kambarys\references\mokytojo-lapas-template.html"
with io.open(TPL, encoding="utf-8") as f:
    html = f.read()

html = html.replace("Mokytojo lapas · Pabėgimo kambarys · Lygtys · 6 kl.",
                    "Mokytojo lapas · Pabėgimo kambarys · Pagrindinė proporcijos savybė · 6 kl.")
html = html.replace(
    'Tema: <b>Lygtys</b> · 6 klasė · Profesoriaus Lygtickio laboratorija · 10 spynų · 4 variantai',
    'Tema: <b>Pagrindinė proporcijos savybė</b> (6.2.1) · 6 klasė · Slaptasis seifas · 10 ratukų · 4 variantai')
html = html.replace("sprendžia 10 lygčių iš eilės. Kiekvienos lygties sprendinys <b>x</b> yra vienas galutinio seifo kodo",
                    "sprendžia 10 proporcijos galvosūkių iš eilės. Kiekvieno nežinomas narys <b>x</b> (vienaženklis) yra vienas galutinio seifo kodo")
html = html.replace("skaitmuo (iš eilės nuo 1 iki 10 spynos). Surinkęs visą kodą ir įvedęs jį į seifą, mokinys „pabėga\".",
                    "skaitmuo (iš eilės nuo 1 iki 10 ratuko). Surinkęs visą kodą ir įvedęs jį į seifą, mokinys „pabėga“.")
html = html.replace('priminkite mygtuką „💡 Patarimas" prie kiekvienos spynos.',
                    'priminkite mygtuką „💡 Patarimas“ prie kiekvieno ratuko.')

# pakeičiam VARIANTS bloką
pat = re.compile(r'const VARIANTS = \[.*?\];\n', re.S)
assert pat.search(html)
html = pat.sub(teacher_js, html, count=1)

with io.open("mokytojo-lapas.html", "w", encoding="utf-8") as f:
    f.write(html)
print("mokytojo-lapas.html sukurtas,", len(html), "simb.")
