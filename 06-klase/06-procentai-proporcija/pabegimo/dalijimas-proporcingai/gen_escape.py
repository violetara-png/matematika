# -*- coding: utf-8 -*-
"""6.2.3 „Dalijimas proporcingai“ pabėgimo kambario VARIANTS + HINTS generatorius.
Kiekviena stotelė — dalijimo santykiu galvosūkis, kurio ieškoma dalis (viena dalelė,
mažesnė / didesnė / didžiausia dalis) yra VIENAŽENKLĖ (0–9). Visus atsakymus tikrina
fractions; seifo kodai (10 skaitm.) tarp variantų skiriasi.
Išveda _data.js — HINTS + VARIANTS (su sol lauku mokytojo lapui)."""
from fractions import Fraction as F
import json

def one(D, ratio):
    return F(D) / sum(ratio)

# Stotelių tipai pastovūs per indeksą (kad HINTS[i] atitiktų):
# 0 one2 · 1 min2 · 2 max2 · 3 one2 · 4 one3 · 5 max3 · 6 one2 · 7 one2 · 8 min2 · 9 word(min2)
TITLES = ["Seifo ratukas Nr. 1","Mažesnės dalies spyna","Didesnės dalies spyna",
          "Seifo ratukas Nr. 2","Trijų dalių užraktas","Didžiausios dalies spyna",
          "Seifo ratukas Nr. 3","Sargybos ratukas","Priešpaskutinė spyna","Pabėgimo mįslė"]

# Per variantą — 10 galvosūkių parametrai (kind, *params)
# kind: one2(D,a,b) min2(D,a,b) max2(D,a,b) one3(D,a,b,c) max3(D,a,b,c) word(D,a,b,story)
CFG = [
  [ ("one2",20,2,3), ("min2",15,2,3), ("max2",15,2,3), ("one2",21,3,4),
    ("one3",18,2,3,4), ("max3",18,2,3,4), ("one2",40,3,5), ("one2",28,3,4),
    ("min2",16,3,5), ("word",10,2,3,"Du agentai pasidalijo 10 slaptų raktų santykiu 2 : 3. Kiek gavo tas, kuriam teko mažiau?") ],
  [ ("one2",24,5,1), ("min2",12,1,3), ("max2",12,1,3), ("one2",35,3,4),
    ("one3",9,2,3,4), ("max3",9,2,3,4), ("one2",40,3,5), ("one2",28,3,4),
    ("min2",18,4,5), ("word",15,2,3,"Dvi seserys pasidalijo 15 saldainių santykiu 2 : 3. Kiek gavo ta, kuriai teko mažiau?") ],
  [ ("one2",18,2,4), ("min2",10,2,3), ("max2",10,2,3), ("one2",16,1,3),
    ("one3",12,1,2,3), ("max3",12,1,2,3), ("one2",45,4,5), ("one2",24,3,5),
    ("min2",14,2,5), ("word",20,1,3,"Du draugai pasidalijo 20 Eur santykiu 1 : 3. Kiek eurų gavo tas, kuriam teko mažiau?") ],
  [ ("one2",35,2,3), ("min2",12,1,2), ("max2",12,1,2), ("one2",27,4,5),
    ("one3",15,1,2,2), ("max3",15,1,2,2), ("one2",45,4,5), ("one2",16,3,1),
    ("min2",18,5,4), ("word",24,1,5,"Du sargybiniai pasidalijo 24 monetas santykiu 1 : 5. Kiek gavo tas, kuriam teko mažiau?") ],
]

HINTS = [
  "Kai dalijame santykiu, viena dalelė = dydis padalytas iš dalelių sumos (a + b). Sudėk santykio skaičius ir tuo padalink dydį.",
  "Pirma rask vieną dalelę (dydis : (a + b)). Mažesnę dalį atitinka mažesnysis santykio skaičius, tad vieną dalelę padaugink iš jo.",
  "Rask vieną dalelę, tada didesnę dalį atitinka didesnysis santykio skaičius. Padaugink vieną dalelę iš jo.",
  "Ta pati mintis: sudėk santykio skaičius (dalelių suma) ir tuo padalink dydį, gausi vieną dalelę.",
  "Trys dalys, tad dalelių suma dabar iš trijų skaičių. Sudėk visus tris ir tuo padalink dydį.",
  "Rask vieną dalelę (dydis : dalelių suma), o didžiausią dalį atitinka didžiausias santykio skaičius. Padaugink.",
  "Vėl viena dalelė: sudėk santykio skaičius ir dydį padalink iš tos sumos.",
  "Dalelių suma, tada dalyba. Nepamiršk: dalini iš santykio skaičių SUMOS, ne iš dalių skaičiaus.",
  "Rask vieną dalelę, tada mažesnę dalį gauni padauginęs vieną dalelę iš mažesniojo santykio skaičiaus.",
  "Užrašyk uždavinį kaip dalijimą santykiu: sudėk santykio skaičius, dydį padalink iš sumos, mažesnę dalį atitinka mažesnysis skaičius. Skaičiuok pats.",
]

def build_station(idx, spec):
    kind = spec[0]
    title = TITLES[idx]
    if kind == "one2":
        D,a,b = spec[1],spec[2],spec[3]; s=a+b; op=one(D,(a,b))
        assert op.denominator==1, (D,a,b,op)
        ans=int(op)
        eq=f"{D} : ({a} + {b}) = ?"
        q="Rask, kiek tenka vienai dalelei."
        sol=f"{D} : ({a}+{b}) = {D} : {s} = {ans}"
    elif kind in ("min2","max2"):
        D,a,b = spec[1],spec[2],spec[3]; s=a+b; op=one(D,(a,b))
        p=sorted([op*a, op*b])
        val = p[0] if kind=="min2" else p[1]
        assert val.denominator==1, (D,a,b,val)
        ans=int(val)
        r = min(a,b) if kind=="min2" else max(a,b)
        eq=f"{D} santykiu {a} : {b}"
        q=f"{D} padalyk santykiu {a} : {b}. Kokia {'mažesnė' if kind=='min2' else 'didesnė'} dalis?"
        sol=f"viena dalelė {D}:{s}={int(op)}; {'mažesnė' if kind=='min2' else 'didesnė'} dalis {int(op)}·{r} = {ans}"
    elif kind == "one3":
        D,a,b,c = spec[1],spec[2],spec[3],spec[4]; s=a+b+c; op=one(D,(a,b,c))
        assert op.denominator==1
        ans=int(op)
        eq=f"{D} : ({a} + {b} + {c}) = ?"
        q="Rask, kiek tenka vienai dalelei (trys dalys)."
        sol=f"{D} : ({a}+{b}+{c}) = {D} : {s} = {ans}"
    elif kind == "max3":
        D,a,b,c = spec[1],spec[2],spec[3],spec[4]; s=a+b+c; op=one(D,(a,b,c))
        mr=max(a,b,c); val=op*mr
        assert val.denominator==1
        ans=int(val)
        eq=f"{D} santykiu {a} : {b} : {c}"
        q=f"{D} padalyk santykiu {a} : {b} : {c}. Kokia didžiausia dalis?"
        sol=f"viena dalelė {D}:{s}={int(op)}; didžiausia dalis {int(op)}·{mr} = {ans}"
    elif kind == "word":
        D,a,b,story = spec[1],spec[2],spec[3],spec[4]; s=a+b; op=one(D,(a,b))
        p=sorted([op*a, op*b]); val=p[0]
        assert val.denominator==1
        ans=int(val)
        eq=""
        q=story
        sol=f"dalelių {a}+{b}={s}; {D}:{s}={int(op)}; mažesnė dalis {int(op)}·{min(a,b)} = {ans}"
    else:
        raise ValueError(kind)
    return {"title":title, "eq":eq, "q":q, "ans":ans, "sol":sol}

variants = []
for cfg in CFG:
    sts = [build_station(i, spec) for i, spec in enumerate(cfg)]
    variants.append(sts)

# --- patikra: visi ans 0..9, kodai skiriasi ---
codes = []
for i,v in enumerate(variants,1):
    for j,s in enumerate(v):
        assert isinstance(s["ans"],int) and 0<=s["ans"]<=9, (i,j,s["ans"])
    code = "".join(str(s["ans"]) for s in v)
    codes.append(code)
    print(f"Variantas {i}: kodas {code}")
assert len(set(codes))==4, ("kodai kartojasi!", codes)
print("OK: 4 variantai, visi atsakymai vienaženkliai, kodai unikalūs.")

# --- JS blokas ---
def esc(s):
    return s.replace('\\','\\\\').replace('"','\\"')

def js_variant(v):
    rows = []
    for s in v:
        rows.append(f'  {{ title:"{esc(s["title"])}", eq:"{esc(s["eq"])}", q:"{esc(s["q"])}", ans:{s["ans"]}, sol:"{esc(s["sol"])}" }},')
    return " [\n" + "\n".join(rows) + "\n ]"

js = "const HINTS = " + json.dumps(HINTS, ensure_ascii=False, indent=0).replace("\n","") + ";\n\n"
js += "const VARIANTS = [\n" + ",\n".join(js_variant(v) for v in variants) + "\n];\n"
with open("_data.js","w",encoding="utf-8") as f:
    f.write(js)
print("Įrašyta _data.js")
