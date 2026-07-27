# -*- coding: utf-8 -*-
"""6.2.2 pabėgimo kambario VARIANTS + HINTS generatorius.
Kiekviena stotelė — procentų galvosūkis, sprendžiamas sudarant proporciją, kurio
atsakymas VIENAŽENKLIS (0–9). Tipai iš eilės: dalis, procentai, visas dydis...
Visus atsakymus tikrina fractions; kodai (10 skaitm.) tarp variantų skiriasi.
Išveda _data.js, kurį įterpiam į index.html."""
from fractions import Fraction as F
import json

# Stočių tipai pagal indeksą (vienodi visuose variantuose):
#   0 part, 1 pct, 2 whole, 3 part, 4 pct, 5 part, 6 whole, 7 pct, 8 part, 9 whole
# part  = ("part", p, N)  -> p % nuo N            ans = p*N/100
# pct   = ("pct",  a, N)  -> kiek % yra a nuo N   ans = a/N*100
# whole = ("whole",p, a)  -> p % nuo x = a        ans = a*100/p
CFG = [
  [("part",10,40),("pct",3,60),("whole",50,4),("part",25,20),("pct",4,50),
   ("part",20,30),("whole",25,2),("pct",3,50),("part",40,20),("whole",20,1)],
  [("part",50,8),("pct",2,40),("whole",50,3),("part",5,60),("pct",6,75),
   ("part",30,20),("whole",25,1),("pct",3,50),("part",10,70),("whole",75,6)],
  [("part",20,45),("pct",2,25),("whole",50,2),("part",25,8),("pct",7,100),
   ("part",10,40),("whole",75,6),("pct",4,50),("part",20,30),("whole",50,4)],
  [("part",25,20),("pct",6,200),("whole",20,1),("part",50,8),("pct",4,50),
   ("part",20,45),("whole",50,3),("pct",3,60),("part",10,70),("whole",25,2)],
]

TITLES = [
  "Seifo ratukas Nr. 1","Seifo ratukas Nr. 2","Atbulinė spyna","Ratukas Nr. 4",
  "Procentų spyna","Ratukas Nr. 6","Antra atbulinė spyna","Dalies užraktas",
  "Priešpaskutinis ratukas","Pabėgimo spyna",
]

HINTS = [
  "Sudaryk proporciją: 100 % atitinka visą dydį, p % atitinka x. Iš visas/x = 100/p rask x (visas · p : 100).",
  "Proporcija: visas dydis atitinka 100 %, dalis atitinka x %. Dalis · 100 : visas duoda procentus.",
  "Atbulai: 100 % atitinka visą dydį x, p % atitinka duotą dalį. Dalis · 100 : p duoda visą dydį.",
  "Vėl dalis: visas · p : 100. Pirma užrašyk schemą, kas atitinka 100 %.",
  "Kiek procentų? Dalis · 100 : visas dydis. Atsakymą užrašyk vienu skaitmeniu.",
  "Dalis: p % nuo viso dydžio. Padaugink visą dydį iš p ir padalink iš 100.",
  "Ieškai viso dydžio: duotą dalį daugink iš 100 ir dalink iš procentų.",
  "Kiek procentų sudaro dalis? Sudaryk proporciją ir rask x % (dalis · 100 : visas).",
  "Dar viena dalis: visas · p : 100. Kablelio nebus, atsakymas vienaženklis.",
  "Paskutinė spyna, ieškai viso dydžio: dalis · 100 : p. Įrašyk gautą skaitmenį.",
]

def build_station(spec, idx):
    kind = spec[0]
    if kind == "part":
        _, p, N = spec
        ans = F(p) * N / 100
        assert ans.denominator == 1, (spec, ans)
        eq = f"{p} % nuo {N} = ?"
        q = f"Kiek yra {p} % nuo {N}? Sudaryk proporciją (100 % atitinka {N}) ir įrašyk atsakymą."
        return {"title": TITLES[idx], "eq": eq, "q": q, "ans": int(ans)}
    if kind == "pct":
        _, a, N = spec
        ans = F(a) / N * 100
        assert ans.denominator == 1, (spec, ans)
        eq = f"{a} iš {N} = ? %"
        q = f"Kiek procentų sudaro {a} nuo {N}? Sudaryk proporciją ({N} atitinka 100 %) ir įrašyk skaičių."
        return {"title": TITLES[idx], "eq": eq, "q": q, "ans": int(ans)}
    if kind == "whole":
        _, p, a = spec
        ans = F(a) * 100 / p
        assert ans.denominator == 1, (spec, ans)
        eq = f"{p} % nuo ? = {a}"
        q = f"Atbulinė spyna: jei {p} % viso dydžio yra {a}, koks visas dydis? Sudaryk proporciją (100 % atitinka x)."
        return {"title": TITLES[idx], "eq": eq, "q": q, "ans": int(ans)}
    raise ValueError(kind)

variants = []
for cfg in CFG:
    sts = [build_station(spec, i) for i, spec in enumerate(cfg)]
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
