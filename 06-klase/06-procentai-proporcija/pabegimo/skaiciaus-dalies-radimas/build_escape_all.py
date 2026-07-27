# -*- coding: utf-8 -*-
"""6.1.2 pabėgimo kambarys: stotelės (vienaženkliai atsakymai, dalies radimas),
index.html + mokytojo-lapas.html iš skill šablonų. Viskas patikrinta fractions."""
import re, io, json
from fractions import Fraction as F

TPL_DIR = r"c:\Users\Violeta\Desktop\Ai asistentas\.claude\skills\pabegimo-kambarys\references"

def part(p,a): return F(p,100)*a

HINTS=[
 "„p % iš skaičiaus“ reiškia dalį nuo viso skaičiaus. Pirma rask 1 % (skaičių padalink iš 100), tada padaugink iš p.",
 "Tas pats: procentus paversk dešimtainiu (padalink iš 100) ir padaugink iš viso skaičiaus.",
 "Trupmena nurodytą dalį rask taip: skaičių padalink iš vardiklio ir padaugink iš skaitiklio.",
 "10 % — tai dešimtoji dalis. Kaip greitai rasti dešimtąją skaičiaus dalį?",
 "Trupmena: padalink iš vardiklio, padaugink iš skaitiklio. Nesuklysk, kuris skaičius kur.",
 "50 % — tai pusė. Kiek bus pusė šio skaičiaus?",
 "1 % — tai šimtoji dalis. Bet pirma pavesk viską į tuos pačius vienetus.",
 "100 % — tai visas skaičius. Kiek procentų yra visas dydis?",
 "Užrašyk procentus dešimtainiu (:100) ir padaugink iš skaičiaus.",
 "Užrašyk žodžius veiksmu: „p % nuo A“ = A · (p : 100). Sudaryk ir suskaičiuok pats.",
]

# (p, a) arba ("frac", F, a). Visi atsakymai vienaženkliai.
CFG=[
 [ (10,40),(20,15),("f",F(1,2),18),(50,8),("f",F(1,4),20),(25,32),(1,700),(100,3),(5,80),("word",5) ],
 [ (10,70),(30,20),("f",F(1,2),8),(50,18),("f",F(1,4),16),(20,15),(1,500),(100,4),(5,60),("word",4) ],
 [ (20,20),(25,32),("f",F(1,3),27),(50,14),("f",F(2,5),20),(30,20),(1,900),(100,7),(40,15),("word",6) ],
 [ (10,90),(50,12),("f",F(1,4),24),(20,45),("f",F(3,5),15),(25,20),(1,600),(100,8),(5,80),("word",5) ],
]

TITLES=["Seifo ratukas Nr. 1","Seifo ratukas Nr. 2","Trupmenos spyna","Greitoji spyna",
        "Antra trupmenos spyna","Ratukas Nr. 6","Vienetų mįslė","Viso dydžio spyna",
        "Priešpaskutinė spyna","Pabėgimo mįslė"]

def station(cfg, idx):
    t=cfg
    if t[0]=="f":
        _,fr,a=t; ans=fr*a
        assert ans.denominator==1 and 0<=ans<=9, (fr,a,ans)
        return {"title":TITLES[idx],"eq":f"{fr.numerator}/{fr.denominator} iš {a} = ?",
                "q":f"Rask trupmena nurodytą dalį: {fr.numerator}/{fr.denominator} iš {a}. Įrašyk skaičių.","ans":int(ans),
                "sol":f"{a} : {fr.denominator} · {fr.numerator} = {int(ans)}"}
    if t[0]=="word":
        m=t[1]
        return {"title":TITLES[idx],"eq":f"10 % iš {m*10} = ?",
                "q":f"Paskutinis ratukas! Parduotuvėje prekė {m*10} Eur, nuolaida 10 %. Kiek eurų nuolaida? Tai paskutinis kodo skaitmuo.","ans":m,
                "sol":f"{m*10} · 0,1 = {m}"}
    p,a=t; ans=part(p,a)
    assert ans.denominator==1 and 0<=ans<=9, (p,a,ans)
    return {"title":TITLES[idx],"eq":f"{p} % iš {a} = ?",
            "q":f"Rask {p} % nuo {a}. Įrašyk skaičių.","ans":int(ans),
            "sol":f"{a} · 0,{'0' if p<10 else ''}{p} = {int(ans)}" if p not in (100,) else f"visas skaičius = {int(ans)}"}

variants=[[station(c,i) for i,c in enumerate(v)] for v in CFG]
codes=["".join(str(s["ans"]) for s in v) for v in variants]
assert len(set(codes))==4, codes
for v in variants:
    for s in v: assert 0<=s["ans"]<=9
print("Kodai:",codes)

# ---- index.html ----
html=io.open(fr"{TPL_DIR}\pabegimo-kambarys-template.html",encoding="utf-8").read()
html=html.replace("<title>Pabėgimas · Lygtys su skliaustais · 6 klasė</title>",
                  "<title>Pabėgimas · Ieškome skaičiaus dalies · 6 klasė</title>")
html=html.replace("Pabėgimo planas · Kamera Nr. 6","Slaptoji operacija · Seifas Nr. 100")
html=html.replace('Matematikos <span class="amber">kalėjimas</span>','Slaptasis <span class="amber">seifas</span>')
html=html.replace('Pabėgimo kambarys · Lygtys su skliaustais · 6 klasė','Pabėgimo kambarys · Ieškome skaičiaus dalies · 6 klasė')
old_story=re.search(r'<div class="story">.*?</div>',html,re.S).group(0)
html=html.replace(old_story,'''<div class="story">
      <p><span class="drop">Agente,</span> tave užrakino slaptoje saugykloje. Kelias laukan, atidaryti dešimties ratukų seifą. Ant sienos, buvusio agento žinutė:</p>
      <p style="margin:12px 0 0"><i>„Kiekvienas ratukas atsirakina radus skaičiaus dalį (procentą arba trupmeną). Kiekvieno atsakymas, vienas skaitmuo, ir tai vienas seifo kodo skaitmuo. Surink visą kodą ir dink.“</i></p>
      <p style="margin:12px 0 0">Spręsk iš eilės. Laikas bėga.</p>
    </div>''')
html=html.replace("<b>🔒 10 grandinių.</b> Atrakinamos iš eilės, sprendžiant skliaustų lygtis.",
                  "<b>🔒 10 ratukų.</b> Atrakinami iš eilės ieškant skaičiaus dalies.")
html=html.replace("<b>🔢 Kiekviena grandinė</b> duoda po vieną pagrindinių vartų kodo skaitmenį.",
                  "<b>🔢 Kiekvienas ratukas</b> duoda po vieną seifo kodo skaitmenį (0–9).")
html=html.replace("<b>⏱ 30 minučių.</b> Kuo greičiau, tuo aukštesnis bėglio rangas.",
                  "<b>⏱ 30 minučių.</b> Kuo greičiau, tuo aukštesnis agento rangas.")
html=html.replace("<h2>🚪 Pagrindiniai vartai</h2>","<h2>🔓 Pagrindinis seifas</h2>")
html=html.replace('<div class="sub">Surinkti skaitmenys (iš eilės nuo 1 iki 10 grandinės):</div>',
                  '<div class="sub">Surinkti skaitmenys (iš eilės nuo 1 iki 10 ratuko):</div>')
html=html.replace("🗝 Atrakinti vartus","🗝 Atidaryti seifą")
html=html.replace("<h2>Pabėgai iš kalėjimo!</h2>","<h2>Seifas atsidarė, pabėgai!</h2>")
old_wt=re.search(r'<p style="color:var\(--muted\);max-width:520px;margin:0 auto">.*?</p>',html,re.S).group(0)
html=html.replace(old_wt,'<p style="color:var(--muted);max-width:520px;margin:0 auto">Seifas atsivėrė. Skaičiaus dalį randi akimirksniu, geriau nei bet kuris saugyklos sargas.</p>')
html=html.replace('rank="🥇 Legendinis bėglys (be patarimų ir klaidų!)"','rank="🥇 Legendinis agentas (be patarimų ir klaidų!)"')
html=html.replace('rank="🥈 Patyręs bėglys"','rank="🥈 Patyręs agentas"')
html=html.replace('rank="🥉 Vos spėjai — bet pabėgai!"','rank="🥉 Vos spėjai, bet pabėgai!"')
html=html.replace("skliaustus tu atskliaudi geriau nei bet kuris sargybinis.","")

def js_variant(v):
    rows=[]
    for s in v:
        eq=s["eq"].replace('"','\\"'); q=s["q"].replace('"','\\"'); title=s["title"].replace('"','\\"')
        rows.append(f'  {{ title:"{title}", eq:"{eq}", q:"{q}", ans:{s["ans"]} }},')
    return " [\n"+"\n".join(rows)+"\n ]"
data="const HINTS = "+json.dumps(HINTS,ensure_ascii=False).replace(" — ",", ")+";\n\n"
data+="const VARIANTS = [\n"+",\n".join(js_variant(v) for v in variants)+"\n];\n"
pat=re.compile(r'/\* Patarimai TIK.*?\];\s*\n(?=let STATIONS)',re.S)
html=pat.sub(data+"\n",html,count=1)
io.open("index.html","w",encoding="utf-8").write(html)
print("index.html OK")

# ---- mokytojo-lapas.html ----
th=io.open(fr"{TPL_DIR}\mokytojo-lapas-template.html",encoding="utf-8").read()
th=th.replace("Mokytojo lapas · Pabėgimo kambarys · Lygtys · 6 kl.","Mokytojo lapas · Pabėgimo kambarys · Ieškome skaičiaus dalies · 6 kl.")
th=th.replace('Tema: <b>Lygtys</b> · 6 klasė · Profesoriaus Lygtickio laboratorija · 10 spynų · 4 variantai',
              'Tema: <b>Ieškome skaičiaus dalies</b> (6.1.2) · 6 klasė · Slaptasis seifas · 10 ratukų · 4 variantai')
th=th.replace("sprendžia 10 lygčių iš eilės. Kiekvienos lygties sprendinys <b>x</b> yra vienas galutinio seifo kodo",
              "sprendžia 10 dalies radimo galvosūkių iš eilės. Kiekvieno atsakymas (vienaženklis) yra vienas galutinio seifo kodo")
th=th.replace('skaitmuo (iš eilės nuo 1 iki 10 spynos). Surinkęs visą kodą ir įvedęs jį į seifą, mokinys „pabėga".',
              'skaitmuo (iš eilės nuo 1 iki 10 ratuko). Surinkęs visą kodą ir įvedęs jį į seifą, mokinys „pabėga“.')
th=th.replace('priminkite mygtuką „💡 Patarimas" prie kiekvienos spynos.','priminkite mygtuką „💡 Patarimas“ prie kiekvieno ratuko.')
tv=[]
for v in variants:
    code="".join(str(s["ans"]) for s in v)
    rows=[]
    for idx,s in enumerate(v,1):
        if idx==10:
            rows.append(f'   ["{idx}w",{json.dumps(s["q"],ensure_ascii=False)},{json.dumps(s["sol"],ensure_ascii=False)},{s["ans"]}],')
        else:
            rows.append(f'   [{idx},"{s["eq"]}",{json.dumps(s["sol"],ensure_ascii=False)},{s["ans"]}],')
    tv.append(f' {{ code:"{code}", rows:[\n'+"\n".join(rows)+"\n ]}")
teacher_js="const VARIANTS = [\n"+",\n".join(tv)+"\n];\n"
th=re.sub(r'const VARIANTS = \[.*?\];\n',teacher_js,th,count=1,flags=re.S)
io.open("mokytojo-lapas.html","w",encoding="utf-8").write(th)
print("mokytojo-lapas.html OK")
