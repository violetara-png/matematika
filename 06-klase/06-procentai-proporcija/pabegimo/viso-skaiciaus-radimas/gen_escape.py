# -*- coding: utf-8 -*-
"""6.1.3 „Ieškome viso skaičiaus" pabėgimo kambario HINTS + VARIANTS generatorius.
Kiekviena stotelė — „rask visą skaičių" galvosūkis, kurio atsakymas VIENAŽENKLIS (0–9):
arba pats visas skaičius yra vienaženklis, arba prašoma konkretaus jo skaitmens
(dešimčių / šimtų / vienetų). Visus atsakymus tikrina fractions; kodai (10 skaitm.)
tarp variantų skiriasi. Išveda _data.js (HINTS + VARIANTS), kurį įterpiam į index.html."""
from fractions import Fraction as F
import json

def whole(pp, m):
    A = F(m) * 100 / F(pp)
    assert A.denominator == 1, (pp, m, A)
    return A.numerator

def tens(n):  return (n // 10) % 10
def hund(n):  return (n // 100) % 10
def units(n): return n % 10

# Stotelių tipai (fiksuota tvarka), skaičiai (m) skiriasi tarp variantų.
KINDS = ["p50","p10t","p25","p1h","p33","p5t","w50","p125t","p10t","w33"]
CFG = [
  [2, 3, 1, 7, 2, 1, 4, 3, 9, 6],
  [3, 5, 2, 4, 3, 2, 2, 4, 7, 8],
  [1, 8, 1, 6, 1, 3, 3, 5, 5, 4],
  [4, 2, 2, 9, 2, 4, 1, 2, 6, 7],
]

HINTS = [
  "Kryptis viso skaičiaus link: 1 % = dalis : procentai, o visas = 1 % · 100. Su 50 % pagalvok, kelinta viso skaičiaus dalis yra pusė.",
  "Pirma rask visą skaičių (dalį dalink iš 10 ir daugink iš 100), o paskui pažiūrėk, koks skaitmuo stovi dešimčių vietoje.",
  "25 % tai ketvirtadalis. Jei ketvirtadalis žinomas, kiek tokių dalių reikia visumai?",
  "1 % yra mažiausia dalis; visas skaičius už ją didesnis lygiai 100 kartų. Radęs jį, imk šimtų skaitmenį.",
  "33⅓ % tai ta pati trupmena 1/3. Jei trečdalis lygus duotam skaičiui, koks tada visas?",
  "5 % telpa visame skaičiuje 20 kartų (nes 100 : 5 = 20). Radęs visą skaičių, imk dešimčių skaitmenį.",
  "Nuolaida 50 % tai lygiai pusė kainos. Jei pusė žinoma, kiek yra visa kaina?",
  "12,5 % tai 1/8 dalis; aštuoni tokie gabalėliai sudaro visumą. Radęs ją, imk dešimčių skaitmenį.",
  "Vėl per 10 %: dalį dalink iš 10 ir daugink iš 100; tau reikia rezultato dešimčių skaitmens.",
  "Nuolaida 33⅓ % tai trečdalis kainos. Radęs visą kainą (dalį · 3), imk jos vienetų skaitmenį.",
]

def build_station(kind, m, idx):
    if kind == "p50":
        A = whole(50, m); ans = A
        return {"title": "Seifo ratukas Nr. 1", "eq": f"50 % skaičiaus = {m}",
                "q": f"Pirmasis seifo ratukas. 50 % kažkokio skaičiaus lygu {m}. Koks tas visas skaičius?",
                "ans": ans, "sol": f"{m} : 50 · 100 = {A}"}
    if kind == "p25":
        A = whole(25, m); ans = A
        return {"title": "Ketvirčio spyna", "eq": f"25 % skaičiaus = {m}",
                "q": f"25 % skaičiaus lygu {m}. Koks visas skaičius?",
                "ans": ans, "sol": f"{m} : 25 · 100 = {A}  (25 % = 1/4, tad {m} · 4)"}
    if kind == "p33":
        A = whole(F(100,3), m); ans = A
        return {"title": "Trupmenos kodas", "eq": f"33⅓ % skaičiaus = {m}",
                "q": f"33⅓ % (tai 1/3) skaičiaus lygu {m}. Koks visas skaičius?",
                "ans": ans, "sol": f"33⅓ % = 1/3, tad visas = {m} · 3 = {A}"}
    if kind == "p10t":
        A = whole(10, m); ans = tens(A)
        return {"title": "Dešimtukų grotelės", "eq": f"10 % skaičiaus = {m}",
                "q": f"10 % skaičiaus lygu {m}. Koks visas skaičius? Įrašyk jo dešimčių skaitmenį.",
                "ans": ans, "sol": f"{m} : 10 · 100 = {A}; dešimčių skaitmuo {ans}"}
    if kind == "p1h":
        A = whole(1, m); ans = hund(A)
        return {"title": "Šimtų užraktas", "eq": f"1 % skaičiaus = {m}",
                "q": f"1 % skaičiaus lygu {m}. Koks visas skaičius? Įrašyk jo šimtų skaitmenį.",
                "ans": ans, "sol": f"{m} · 100 = {A}; šimtų skaitmuo {ans}"}
    if kind == "p5t":
        A = whole(5, m); ans = tens(A)
        return {"title": "Penketuko skląstis", "eq": f"5 % skaičiaus = {m}",
                "q": f"5 % skaičiaus lygu {m}. Koks visas skaičius? Įrašyk jo dešimčių skaitmenį.",
                "ans": ans, "sol": f"{m} : 5 · 100 = {A}; dešimčių skaitmuo {ans}"}
    if kind == "p125t":
        A = whole(F(25,2), m); ans = tens(A)
        return {"title": "Aštuntadalio spyna", "eq": f"12,5 % skaičiaus = {m}",
                "q": f"12,5 % (tai 1/8) skaičiaus lygu {m}. Koks visas skaičius? Įrašyk jo dešimčių skaitmenį.",
                "ans": ans, "sol": f"12,5 % = 1/8, tad visas = {m} · 8 = {A}; dešimčių skaitmuo {ans}"}
    if kind == "w50":
        A = whole(50, m); ans = A
        return {"title": "Sargybos mįslė", "eq": "",
                "q": f"Sargybos mįslė: prekė atpigo 50 % ir tai sudarė {m} Eur. Kiek prekė kainavo be nuolaidos?",
                "ans": ans, "sol": f"50 % = pusė kainos, tad kaina = {m} · 2 = {A} Eur"}
    if kind == "w33":
        A = whole(F(100,3), m); ans = units(A)
        return {"title": "Pabėgimo mįslė", "eq": "",
                "q": f"Paskutinis ratukas! Prekė atpigo 33⅓ % ir tai sudarė {m} Eur. Kiek prekė kainavo be nuolaidos? Įrašyk atsakymo vienetų skaitmenį.",
                "ans": ans, "sol": f"33⅓ % = 1/3, tad kaina = {m} · 3 = {A} Eur; vienetų skaitmuo {ans}"}
    raise ValueError(kind)

variants = []
for ms in CFG:
    sts = [build_station(KINDS[i], ms[i], i) for i in range(10)]
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
print("OK: 4 variantai, visi atsakymai vienaženkliai (0–9), kodai unikalūs.")

# --- _data.js (HINTS + VARIANTS, JSON-suderinamas JS) ---
js  = "const HINTS = " + json.dumps(HINTS, ensure_ascii=False) + ";\n\n"
js += "const VARIANTS = " + json.dumps(variants, ensure_ascii=False, indent=1) + ";\n"
with open("_data.js", "w", encoding="utf-8") as f:
    f.write(js)
print("Įrašyta _data.js")
