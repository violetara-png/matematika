# -*- coding: utf-8 -*-
"""6.2.1 pabėgimo kambario VARIANTS + HINTS generatorius.
Kiekviena stotelė — proporcijos galvosūkis, kurio nežinomas narys x yra VIENAŽENKLIS (0–9).
Visus x apskaičiuoja fractions (a·d = b·c); kodai (10 skaitm.) tarp variantų skiriasi.
Išveda JS bloką (_data.js), kurį įterpiam į index.html."""
from fractions import Fraction as F
import json

def solve(a, b, c, d):
    """Proporcija a:b = c:d, vienas narys None. Grąžina x. a·d = b·c."""
    if a is None: return F(b) * F(c) / F(d)
    if b is None: return F(a) * F(d) / F(c)
    if c is None: return F(a) * F(d) / F(b)
    if d is None: return F(b) * F(c) / F(a)
    raise ValueError

# Per-variant: 10 proporcijų (a,b,c,d) su vienu None. Tipai vienodi, skaičiai kiti.
CFG = [
  [ (None,2,6,4), (3,None,6,8), (None,5,4,10), (6,3,None,4), (2,None,4,10),
    (None,6,1,6), (4,2,None,3), (None,3,3,9), (None,4,3,6), (None,9,1,3) ],
  [ (None,3,4,6), (2,None,4,8), (None,4,3,6), (8,4,None,3), (3,None,6,10),
    (None,7,1,7), (6,3,None,4), (None,2,4,8), (None,5,6,10), (9,None,3,3) ],
  [ (None,4,6,8), (4,None,2,4), (None,6,2,4), (5,2,None,2), (2,None,3,9),
    (None,8,1,8), (6,3,None,2), (None,4,3,6), (None,6,5,10), (8,None,2,2) ],
  [ (None,6,2,4), (5,None,5,3), (None,3,8,12), (9,3,None,2), (4,None,3,6),
    (None,9,1,9), (8,4,None,3), (None,4,2,4), (None,7,4,4), (2,None,4,8) ],
]

TITLES = [
  "Seifo ratukas Nr. 1","Seifo ratukas Nr. 2","Atbulinė spyna","Trupmenos kodas",
  "Antra atbulinė spyna","Dalininko užraktas","Skaitmenų grotelės","Sargybos mįslė",
  "Priešpaskutinė spyna","Pabėgimo mįslė",
]

HINTS = [
  "Proporcija — dviejų santykių lygybė. Pagrindinė savybė: kraštinių narių sandauga lygi vidinių narių sandaugai (a·d = b·c).",
  "Kraštiniai — pirmas ir paskutinis narys; vidiniai — du viduryje. Sudaugink žinomus ir sudaryk lygybę su x.",
  "Užrašyk sandaugų lygybę: kraštinis · kraštinis = vidinis · vidinis. Vienoje pusėje bus x.",
  "Suskaičiuok žinomų narių sandaugą — tai skaičius, kuriam turi būti lygi kita sandauga su x.",
  "Kai gauni pavidalą „x · skaičius = skaičius“, x rasi padalinęs dešinę pusę iš skaičiaus prie x.",
  "Nesumaišyk narių: dauginam kraštinį su kraštiniu, o ne du vieno santykio narius.",
  "Patikrink save: įstatęs rastą x atgal, abi sandaugos (kraštinių ir vidinių) turi sutapti.",
  "Jei nežinomasis yra vidurinis narys, jis vis tiek randamas iš tos pačios lygybės a·d = b·c.",
  "Atsakymas — vienaženklis skaičius (0–9). Jei gavai daugiaženklį, patikrink dauginimą.",
  "Užrašyk lygybę tvarkingai ir suskaičiuok pats — kiekvienas ratukas duoda po vieną kodo skaitmenį.",
]

def disp(tpl):
    a, b, c, d = ["x" if t is None else str(t) for t in tpl]
    return f"{a} : {b} = {c} : {d}"

variants = []
for ci, cfg in enumerate(CFG, 1):
    sts = []
    for si, tpl in enumerate(cfg):
        x = solve(*tpl)
        assert x.denominator == 1 and 0 <= x <= 9, (ci, si, tpl, x)
        ans = int(x)
        eq = disp(tpl) + "  (x = ?)"
        q = (f"Rask nežinomą proporcijos narį x proporcijoje {disp(tpl)} "
             f"ir įrašyk jį kaip šio ratuko kodo skaitmenį.")
        sts.append({"title": TITLES[si], "eq": eq, "q": q, "ans": ans})
    variants.append(sts)

# --- patikra: visi ans 0..9, kodai skiriasi ---
codes = []
for i, v in enumerate(variants, 1):
    for j, s in enumerate(v):
        assert isinstance(s["ans"], int) and 0 <= s["ans"] <= 9, (i, j, s["ans"])
    code = "".join(str(s["ans"]) for s in v)
    codes.append(code)
    print(f"Variantas {i}: kodas {code}")
assert len(set(codes)) == 4, ("kodai kartojasi!", codes)
print("OK: 4 variantai, visi atsakymai vienaženkliai, kodai unikalūs.")

# --- JS blokas ---
def js_variant(v):
    rows = []
    for s in v:
        eq = s["eq"].replace('"', '\\"')
        q = s["q"].replace('"', '\\"')
        title = s["title"].replace('"', '\\"')
        rows.append(f'  {{ title:"{title}", eq:"{eq}", q:"{q}", ans:{s["ans"]} }},')
    return " [\n" + "\n".join(rows) + "\n ]"

js = "const HINTS = " + json.dumps(HINTS, ensure_ascii=False, indent=0).replace("\n", "") + ";\n\n"
js += "const VARIANTS = [\n" + ",\n".join(js_variant(v) for v in variants) + "\n];\n"
with open("_data.js", "w", encoding="utf-8") as f:
    f.write(js)
print("Įrašyta _data.js")
