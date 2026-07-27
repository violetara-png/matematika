# -*- coding: utf-8 -*-
"""6.1.1 pabėgimo kambario VARIANTS + HINTS generatorius.
Kiekviena stotelė — konvertavimo galvosūkis, kurio atsakymas VIENAŽENKLIS (0–9).
Visus atsakymus tikrina fractions; kodai (10 skaitm.) tarp variantų skiriasi.
Išveda JS bloką, kurį įterpiam į index.html."""
from fractions import Fraction as F
import json

def tens_of_percent(fr):
    """Trupmenos procentų dešimčių skaitmuo (fr turi duoti sveiką dešimtį proc.)."""
    v = fr * 100
    assert v.denominator == 1 and v % 10 == 0, v
    return int(v // 10)

# Per-variant parametrai. Tipai vienodi, skaičiai kiti.
# S1,S2,S7 = 0,0a -> a %   (a)
# S3,S5    = a0 % -> 0,a    (a)   dešimtainio dešimtųjų skaitmuo
# S4,S6,S9 = trupmena -> procentų dešimčių skaitmuo
# S8       = 1/100 -> 1 % (sąvoka)  arba palyginimo skaitmuo
# S10      = žodinė mįslė
CFG = [
  # a1 a2 a7 |  b3 b5  | f4     f6     f9      | s8 | mysle_ans
  {"a1":3,"a2":7,"a7":9,"b3":4,"b5":6,"f4":F(1,2),"f6":F(4,5),"f9":F(9,10),"mysle":5},
  {"a1":2,"a2":8,"a7":6,"b3":5,"b5":3,"f4":F(3,5),"f6":F(7,10),"f9":F(1,2),"mysle":4},
  {"a1":4,"a2":9,"a7":5,"b3":7,"b5":2,"f4":F(2,5),"f6":F(3,5),"f9":F(4,5),"mysle":7},
  {"a1":6,"a2":3,"a7":8,"b3":4,"b5":9,"f4":F(1,2),"f6":F(9,10),"f9":F(7,10),"mysle":5},
]

HINTS = [
  "Į procentus einama dauginant iš 100. Kai skaičius mažas (0,0…), dauginant iš 100 kablelis pašoka per du skaitmenis į dešinę.",
  "Ta pati mintis: 0,0□ padaugink iš 100. Kur atsidurs skaitmuo po dviejų nulių?",
  "Procentai virsta dešimtainiu daliant iš 100. □0 % : 100 — kur nukeliaus kablelis?",
  "Trupmeną pavesk į procentus (dauginu iš 100). Gausi sveiką dešimtį procentų — tavęs prašo tik dešimčių skaitmens.",
  "Vėl: iš procentų į dešimtainį — dalink iš 100. Įsivaizduok kablelį, slenkantį per du skaitmenis kairėn.",
  "Pavesk trupmeną į procentus. Prisimink dažnas formas: 3/5, 7/10 ir panašios duoda apvalias dešimtis procentų.",
  "0,0□ · 100. Skaitmuo, buvęs šimtųjų vietoje, atsistos vienetų vietoje.",
  "Prisimink patį apibrėžimą: 1 % — tai viena šimtoji dydžio. Tad kiek procentų sudaro 1/100 dalis?",
  "Trupmeną · 100. Atsakymas — sveika dešimtis procentų; parašyk tik dešimčių skaitmenį.",
  "Užrašyk žodžius kaip veiksmą: „dalis · 100 = procentai“. Susidaryk lygtį ir suskaičiuok pats — atsakymas vienaženklis.",
]

def build_variant(c):
    a1,a2,a7 = c["a1"],c["a2"],c["a7"]
    b3,b5 = c["b3"],c["b5"]
    f4,f6,f9 = c["f4"],c["f6"],c["f9"]
    sts = []
    # S1
    sts.append({"title":"Seifo ratukas Nr. 1","eq":f"0,0{a1} = ? %","q":"Pirmasis seifo ratukas. Kiek procentų sudaro šis dešimtainis skaičius? Įrašyk skaitmenį.","ans":a1})
    # S2
    sts.append({"title":"Seifo ratukas Nr. 2","eq":f"0,0{a2} = ? %","q":"Antras ratukas. Pavesk dešimtainį į procentus.","ans":a2})
    # S3: b3*10 % -> 0,b3
    sts.append({"title":"Atbulinė spyna","eq":f"{b3}0 % = 0,?","q":"Ši spyna dirba atbulai: procentus pavesk į dešimtainį skaičių. Koks skaitmuo po kablelio?","ans":b3})
    # S4: fraction f4 -> tens digit of %
    sts.append({"title":"Trupmenos kodas","eq":f"{f4.numerator}/{f4.denominator} = ?0 %","q":"Pavesk trupmeną į procentus. Įrašyk gautų procentų dešimčių skaitmenį.","ans":tens_of_percent(f4)})
    # S5: b5*10 % -> 0,b5
    sts.append({"title":"Antra atbulinė spyna","eq":f"{b5}0 % = 0,?","q":"Vėl atbulai: procentus — į dešimtainį skaičių. Skaitmuo po kablelio?","ans":b5})
    # S6: fraction f6 -> tens digit
    sts.append({"title":"Dalininko užraktas","eq":f"{f6.numerator}/{f6.denominator} = ?0 %","q":"Trupmena į procentus. Įrašyk dešimčių skaitmenį.","ans":tens_of_percent(f6)})
    # S7: 0,0a7 -> a7
    sts.append({"title":"Skaitmenų grotelės","eq":f"0,0{a7} = ? %","q":"Dar vienas mažas dešimtainis. Kiek procentų? Įrašyk skaitmenį.","ans":a7})
    # S8: concept 1/100 -> 1 %
    sts.append({"title":"Sargybos mįslė","eq":"1/100 = ? %","q":"Sargybos klausimas: kiek procentų sudaro viena šimtoji (1/100) dydžio dalis?","ans":1})
    # S9: fraction f9 -> tens digit
    sts.append({"title":"Priešpaskutinė spyna","eq":f"{f9.numerator}/{f9.denominator} = ?0 %","q":"Trupmeną pavesk į procentus ir įrašyk dešimčių skaitmenį.","ans":tens_of_percent(f9)})
    # S10: mįslė (word) -> single digit
    m = c["mysle"]
    total = m*20
    sts.append({"title":"Pabėgimo mįslė","eq":"","q":f"Paskutinis ratukas! Parduotuvėje prekė kainavo {total} Eur, o nuolaida sudarė {m*100//total*0}… ne, paprasčiau: nuolaida sudarė 5 % ir tai lygu {m} Eur? Įrašyk, kiek DEŠIMTAINIŲ dalių (0,?) sudaro 50 % — tai ir yra kodas.","ans":m})
    return sts

# S10 mįslė perrašom aiškiau (5 kaip 0,5 = 50%), individualiai
def mysle_text(c):
    m = c["mysle"]
    # visų myslė: kiek yra 0,? kai procentai duoti
    return {"title":"Pabėgimo mįslė","eq":f"{m}0 % = 0,?","q":f"Paskutinis ratukas! Užrašyk {m}0 % dešimtainiu skaičiumi ir įrašyk skaitmenį po kablelio — tai paskutinis kodo skaitmuo.","ans":m}

variants = []
for c in CFG:
    sts = build_variant(c)
    sts[9] = mysle_text(c)  # aiškesnė mįslė
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
def js_variant(v):
    rows = []
    for s in v:
        eq = s["eq"].replace('"','\\"')
        q = s["q"].replace('"','\\"')
        title = s["title"].replace('"','\\"')
        rows.append(f'  {{ title:"{title}", eq:"{eq}", q:"{q}", ans:{s["ans"]} }},')
    return " [\n" + "\n".join(rows) + "\n ]"

js = "const HINTS = " + json.dumps(HINTS, ensure_ascii=False, indent=0).replace("\n","") + ";\n\n"
js += "const VARIANTS = [\n" + ",\n".join(js_variant(v) for v in variants) + "\n];\n"
with open("_data.js","w",encoding="utf-8") as f:
    f.write(js)
print("Įrašyta _data.js")
