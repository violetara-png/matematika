# -*- coding: utf-8 -*-
"""Sukonstruoja index.html iš skill šablono: pritaiko 'slaptojo seifo' siužetą
6.2.1 temai (Pagrindinė proporcijos savybė) ir įterpia sugeneruotus HINTS + VARIANTS iš _data.js."""
import re, io

TPL = r"c:\Users\Violeta\Desktop\Ai asistentas\.claude\skills\pabegimo-kambarys\references\pabegimo-kambarys-template.html"
with io.open(TPL, encoding="utf-8") as f:
    html = f.read()
with io.open("_data.js", encoding="utf-8") as f:
    data = f.read()

# brūkšnių tvarkymas duomenyse (VLKK: ne kaip skyryba)
data = data.replace(" — ", ", ")

# 1. <title>
html = html.replace(
    "<title>Pabėgimas · Lygtys su skliaustais · 6 klasė</title>",
    "<title>Pabėgimas · Pagrindinė proporcijos savybė · 6 klasė</title>")

# 2. badge
html = html.replace("Pabėgimo planas · Kamera Nr. 6", "Slaptoji operacija · Seifas Nr. 621")

# 3. h1
html = html.replace(
    'Matematikos <span class="amber">kalėjimas</span>',
    'Slaptasis <span class="amber">seifas</span>')

# 4. sub
html = html.replace(
    'Pabėgimo kambarys · Lygtys su skliaustais · 6 klasė',
    'Pabėgimo kambarys · Pagrindinė proporcijos savybė · 6 klasė')

# 5. story
old_story = re.search(r'<div class="story">.*?</div>', html, re.S).group(0)
new_story = '''<div class="story">
      <p><span class="drop">Agente,</span> tave užrakino slaptoje saugykloje. Vienintelis kelias laukan, atidaryti
      dešimties ratukų seifą. Ant sienos randi buvusio agento žinutę:</p>
      <p style="margin:12px 0 0"><i>„Kiekvienas seifo ratukas atsirakina radus nežinomą proporcijos narį. Taikyk
      pagrindinę proporcijos savybę: kraštinių sandauga lygi vidinių sandaugai (a·d = b·c). Kiekvienas ratukas duoda
      po vieną seifo kodo skaitmenį (0–9). Surink visą kodą, atidaryk seifą ir dink.“</i></p>
      <p style="margin:12px 0 0">Spręsk iš eilės. Kiekvienas atsakymas, vienas skaitmuo. Laikas bėga.</p>
    </div>'''
html = html.replace(old_story, new_story)

# 6. rules
html = html.replace("<b>🔒 10 grandinių.</b> Atrakinamos iš eilės, sprendžiant skliaustų lygtis.",
                    "<b>🔒 10 ratukų.</b> Atrakinami iš eilės randant nežinomą proporcijos narį (a·d = b·c).")
html = html.replace("<b>🔢 Kiekviena grandinė</b> duoda po vieną pagrindinių vartų kodo skaitmenį.",
                    "<b>🔢 Kiekvienas ratukas</b> duoda po vieną seifo kodo skaitmenį (0–9).")
html = html.replace("<b>⏱ 30 minučių.</b> Kuo greičiau, tuo aukštesnis bėglio rangas.",
                    "<b>⏱ 30 minučių.</b> Kuo greičiau, tuo aukštesnis agento rangas.")

# 7. vault antraštė
html = html.replace("<h2>🚪 Pagrindiniai vartai</h2>", "<h2>🔓 Pagrindinis seifas</h2>")
html = html.replace('<div class="sub">Surinkti skaitmenys (iš eilės nuo 1 iki 10 grandinės):</div>',
                    '<div class="sub">Surinkti skaitmenys (iš eilės nuo 1 iki 10 ratuko):</div>')
html = html.replace("🗝 Atrakinti vartus", "🗝 Atidaryti seifą")

# 8. win ekranas
html = html.replace("<h2>Pabėgai iš kalėjimo!</h2>", "<h2>Seifas atsidarė, pabėgai!</h2>")
old_wintext = re.search(r'<p style="color:var\(--muted\);max-width:520px;margin:0 auto">.*?</p>', html, re.S).group(0)
html = html.replace(old_wintext,
    '<p style="color:var(--muted);max-width:520px;margin:0 auto">Seifo durys atsivėrė, tu laisvas. '
    'Nežinomą proporcijos narį randi akimirksniu, geriau nei bet kuris saugyklos sargas.</p>')

# rangai
html = html.replace('rank="🥇 Legendinis bėglys (be patarimų ir klaidų!)"',
                    'rank="🥇 Legendinis agentas (be patarimų ir klaidų!)"')
html = html.replace('rank="🥈 Patyręs bėglys"', 'rank="🥈 Patyręs agentas"')
html = html.replace('rank="🥉 Vos spėjai — bet pabėgai!"', 'rank="🥉 Vos spėjai, bet pabėgai!"')

# 9. įterpiam duomenis: pakeičiam HINTS ... VARIANTS ]; bloką
pat = re.compile(r'/\* Patarimai TIK.*?\];\s*\n(?=let STATIONS)', re.S)
assert pat.search(html), "nerastas HINTS/VARIANTS blokas"
html = pat.sub(data + "\n", html, count=1)

with io.open("index.html", "w", encoding="utf-8") as f:
    f.write(html)
print("index.html sukurtas,", len(html), "simb.")
