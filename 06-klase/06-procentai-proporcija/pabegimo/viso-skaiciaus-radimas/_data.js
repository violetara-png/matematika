const HINTS = ["Kryptis viso skaičiaus link: 1 % = dalis : procentai, o visas = 1 % · 100. Su 50 % pagalvok, kelinta viso skaičiaus dalis yra pusė.", "Pirma rask visą skaičių (dalį dalink iš 10 ir daugink iš 100), o paskui pažiūrėk, koks skaitmuo stovi dešimčių vietoje.", "25 % tai ketvirtadalis. Jei ketvirtadalis žinomas, kiek tokių dalių reikia visumai?", "1 % yra mažiausia dalis; visas skaičius už ją didesnis lygiai 100 kartų. Radęs jį, imk šimtų skaitmenį.", "33⅓ % tai ta pati trupmena 1/3. Jei trečdalis lygus duotam skaičiui, koks tada visas?", "5 % telpa visame skaičiuje 20 kartų (nes 100 : 5 = 20). Radęs visą skaičių, imk dešimčių skaitmenį.", "Nuolaida 50 % tai lygiai pusė kainos. Jei pusė žinoma, kiek yra visa kaina?", "12,5 % tai 1/8 dalis; aštuoni tokie gabalėliai sudaro visumą. Radęs ją, imk dešimčių skaitmenį.", "Vėl per 10 %: dalį dalink iš 10 ir daugink iš 100; tau reikia rezultato dešimčių skaitmens.", "Nuolaida 33⅓ % tai trečdalis kainos. Radęs visą kainą (dalį · 3), imk jos vienetų skaitmenį."];

const VARIANTS = [
 [
  {
   "title": "Seifo ratukas Nr. 1",
   "eq": "50 % skaičiaus = 2",
   "q": "Pirmasis seifo ratukas. 50 % kažkokio skaičiaus lygu 2. Koks tas visas skaičius?",
   "ans": 4,
   "sol": "2 : 50 · 100 = 4"
  },
  {
   "title": "Dešimtukų grotelės",
   "eq": "10 % skaičiaus = 3",
   "q": "10 % skaičiaus lygu 3. Koks visas skaičius? Įrašyk jo dešimčių skaitmenį.",
   "ans": 3,
   "sol": "3 : 10 · 100 = 30; dešimčių skaitmuo 3"
  },
  {
   "title": "Ketvirčio spyna",
   "eq": "25 % skaičiaus = 1",
   "q": "25 % skaičiaus lygu 1. Koks visas skaičius?",
   "ans": 4,
   "sol": "1 : 25 · 100 = 4  (25 % = 1/4, tad 1 · 4)"
  },
  {
   "title": "Šimtų užraktas",
   "eq": "1 % skaičiaus = 7",
   "q": "1 % skaičiaus lygu 7. Koks visas skaičius? Įrašyk jo šimtų skaitmenį.",
   "ans": 7,
   "sol": "7 · 100 = 700; šimtų skaitmuo 7"
  },
  {
   "title": "Trupmenos kodas",
   "eq": "33⅓ % skaičiaus = 2",
   "q": "33⅓ % (tai 1/3) skaičiaus lygu 2. Koks visas skaičius?",
   "ans": 6,
   "sol": "33⅓ % = 1/3, tad visas = 2 · 3 = 6"
  },
  {
   "title": "Penketuko skląstis",
   "eq": "5 % skaičiaus = 1",
   "q": "5 % skaičiaus lygu 1. Koks visas skaičius? Įrašyk jo dešimčių skaitmenį.",
   "ans": 2,
   "sol": "1 : 5 · 100 = 20; dešimčių skaitmuo 2"
  },
  {
   "title": "Sargybos mįslė",
   "eq": "",
   "q": "Sargybos mįslė: prekė atpigo 50 % ir tai sudarė 4 Eur. Kiek prekė kainavo be nuolaidos?",
   "ans": 8,
   "sol": "50 % = pusė kainos, tad kaina = 4 · 2 = 8 Eur"
  },
  {
   "title": "Aštuntadalio spyna",
   "eq": "12,5 % skaičiaus = 3",
   "q": "12,5 % (tai 1/8) skaičiaus lygu 3. Koks visas skaičius? Įrašyk jo dešimčių skaitmenį.",
   "ans": 2,
   "sol": "12,5 % = 1/8, tad visas = 3 · 8 = 24; dešimčių skaitmuo 2"
  },
  {
   "title": "Dešimtukų grotelės",
   "eq": "10 % skaičiaus = 9",
   "q": "10 % skaičiaus lygu 9. Koks visas skaičius? Įrašyk jo dešimčių skaitmenį.",
   "ans": 9,
   "sol": "9 : 10 · 100 = 90; dešimčių skaitmuo 9"
  },
  {
   "title": "Pabėgimo mįslė",
   "eq": "",
   "q": "Paskutinis ratukas! Prekė atpigo 33⅓ % ir tai sudarė 6 Eur. Kiek prekė kainavo be nuolaidos? Įrašyk atsakymo vienetų skaitmenį.",
   "ans": 8,
   "sol": "33⅓ % = 1/3, tad kaina = 6 · 3 = 18 Eur; vienetų skaitmuo 8"
  }
 ],
 [
  {
   "title": "Seifo ratukas Nr. 1",
   "eq": "50 % skaičiaus = 3",
   "q": "Pirmasis seifo ratukas. 50 % kažkokio skaičiaus lygu 3. Koks tas visas skaičius?",
   "ans": 6,
   "sol": "3 : 50 · 100 = 6"
  },
  {
   "title": "Dešimtukų grotelės",
   "eq": "10 % skaičiaus = 5",
   "q": "10 % skaičiaus lygu 5. Koks visas skaičius? Įrašyk jo dešimčių skaitmenį.",
   "ans": 5,
   "sol": "5 : 10 · 100 = 50; dešimčių skaitmuo 5"
  },
  {
   "title": "Ketvirčio spyna",
   "eq": "25 % skaičiaus = 2",
   "q": "25 % skaičiaus lygu 2. Koks visas skaičius?",
   "ans": 8,
   "sol": "2 : 25 · 100 = 8  (25 % = 1/4, tad 2 · 4)"
  },
  {
   "title": "Šimtų užraktas",
   "eq": "1 % skaičiaus = 4",
   "q": "1 % skaičiaus lygu 4. Koks visas skaičius? Įrašyk jo šimtų skaitmenį.",
   "ans": 4,
   "sol": "4 · 100 = 400; šimtų skaitmuo 4"
  },
  {
   "title": "Trupmenos kodas",
   "eq": "33⅓ % skaičiaus = 3",
   "q": "33⅓ % (tai 1/3) skaičiaus lygu 3. Koks visas skaičius?",
   "ans": 9,
   "sol": "33⅓ % = 1/3, tad visas = 3 · 3 = 9"
  },
  {
   "title": "Penketuko skląstis",
   "eq": "5 % skaičiaus = 2",
   "q": "5 % skaičiaus lygu 2. Koks visas skaičius? Įrašyk jo dešimčių skaitmenį.",
   "ans": 4,
   "sol": "2 : 5 · 100 = 40; dešimčių skaitmuo 4"
  },
  {
   "title": "Sargybos mįslė",
   "eq": "",
   "q": "Sargybos mįslė: prekė atpigo 50 % ir tai sudarė 2 Eur. Kiek prekė kainavo be nuolaidos?",
   "ans": 4,
   "sol": "50 % = pusė kainos, tad kaina = 2 · 2 = 4 Eur"
  },
  {
   "title": "Aštuntadalio spyna",
   "eq": "12,5 % skaičiaus = 4",
   "q": "12,5 % (tai 1/8) skaičiaus lygu 4. Koks visas skaičius? Įrašyk jo dešimčių skaitmenį.",
   "ans": 3,
   "sol": "12,5 % = 1/8, tad visas = 4 · 8 = 32; dešimčių skaitmuo 3"
  },
  {
   "title": "Dešimtukų grotelės",
   "eq": "10 % skaičiaus = 7",
   "q": "10 % skaičiaus lygu 7. Koks visas skaičius? Įrašyk jo dešimčių skaitmenį.",
   "ans": 7,
   "sol": "7 : 10 · 100 = 70; dešimčių skaitmuo 7"
  },
  {
   "title": "Pabėgimo mįslė",
   "eq": "",
   "q": "Paskutinis ratukas! Prekė atpigo 33⅓ % ir tai sudarė 8 Eur. Kiek prekė kainavo be nuolaidos? Įrašyk atsakymo vienetų skaitmenį.",
   "ans": 4,
   "sol": "33⅓ % = 1/3, tad kaina = 8 · 3 = 24 Eur; vienetų skaitmuo 4"
  }
 ],
 [
  {
   "title": "Seifo ratukas Nr. 1",
   "eq": "50 % skaičiaus = 1",
   "q": "Pirmasis seifo ratukas. 50 % kažkokio skaičiaus lygu 1. Koks tas visas skaičius?",
   "ans": 2,
   "sol": "1 : 50 · 100 = 2"
  },
  {
   "title": "Dešimtukų grotelės",
   "eq": "10 % skaičiaus = 8",
   "q": "10 % skaičiaus lygu 8. Koks visas skaičius? Įrašyk jo dešimčių skaitmenį.",
   "ans": 8,
   "sol": "8 : 10 · 100 = 80; dešimčių skaitmuo 8"
  },
  {
   "title": "Ketvirčio spyna",
   "eq": "25 % skaičiaus = 1",
   "q": "25 % skaičiaus lygu 1. Koks visas skaičius?",
   "ans": 4,
   "sol": "1 : 25 · 100 = 4  (25 % = 1/4, tad 1 · 4)"
  },
  {
   "title": "Šimtų užraktas",
   "eq": "1 % skaičiaus = 6",
   "q": "1 % skaičiaus lygu 6. Koks visas skaičius? Įrašyk jo šimtų skaitmenį.",
   "ans": 6,
   "sol": "6 · 100 = 600; šimtų skaitmuo 6"
  },
  {
   "title": "Trupmenos kodas",
   "eq": "33⅓ % skaičiaus = 1",
   "q": "33⅓ % (tai 1/3) skaičiaus lygu 1. Koks visas skaičius?",
   "ans": 3,
   "sol": "33⅓ % = 1/3, tad visas = 1 · 3 = 3"
  },
  {
   "title": "Penketuko skląstis",
   "eq": "5 % skaičiaus = 3",
   "q": "5 % skaičiaus lygu 3. Koks visas skaičius? Įrašyk jo dešimčių skaitmenį.",
   "ans": 6,
   "sol": "3 : 5 · 100 = 60; dešimčių skaitmuo 6"
  },
  {
   "title": "Sargybos mįslė",
   "eq": "",
   "q": "Sargybos mįslė: prekė atpigo 50 % ir tai sudarė 3 Eur. Kiek prekė kainavo be nuolaidos?",
   "ans": 6,
   "sol": "50 % = pusė kainos, tad kaina = 3 · 2 = 6 Eur"
  },
  {
   "title": "Aštuntadalio spyna",
   "eq": "12,5 % skaičiaus = 5",
   "q": "12,5 % (tai 1/8) skaičiaus lygu 5. Koks visas skaičius? Įrašyk jo dešimčių skaitmenį.",
   "ans": 4,
   "sol": "12,5 % = 1/8, tad visas = 5 · 8 = 40; dešimčių skaitmuo 4"
  },
  {
   "title": "Dešimtukų grotelės",
   "eq": "10 % skaičiaus = 5",
   "q": "10 % skaičiaus lygu 5. Koks visas skaičius? Įrašyk jo dešimčių skaitmenį.",
   "ans": 5,
   "sol": "5 : 10 · 100 = 50; dešimčių skaitmuo 5"
  },
  {
   "title": "Pabėgimo mįslė",
   "eq": "",
   "q": "Paskutinis ratukas! Prekė atpigo 33⅓ % ir tai sudarė 4 Eur. Kiek prekė kainavo be nuolaidos? Įrašyk atsakymo vienetų skaitmenį.",
   "ans": 2,
   "sol": "33⅓ % = 1/3, tad kaina = 4 · 3 = 12 Eur; vienetų skaitmuo 2"
  }
 ],
 [
  {
   "title": "Seifo ratukas Nr. 1",
   "eq": "50 % skaičiaus = 4",
   "q": "Pirmasis seifo ratukas. 50 % kažkokio skaičiaus lygu 4. Koks tas visas skaičius?",
   "ans": 8,
   "sol": "4 : 50 · 100 = 8"
  },
  {
   "title": "Dešimtukų grotelės",
   "eq": "10 % skaičiaus = 2",
   "q": "10 % skaičiaus lygu 2. Koks visas skaičius? Įrašyk jo dešimčių skaitmenį.",
   "ans": 2,
   "sol": "2 : 10 · 100 = 20; dešimčių skaitmuo 2"
  },
  {
   "title": "Ketvirčio spyna",
   "eq": "25 % skaičiaus = 2",
   "q": "25 % skaičiaus lygu 2. Koks visas skaičius?",
   "ans": 8,
   "sol": "2 : 25 · 100 = 8  (25 % = 1/4, tad 2 · 4)"
  },
  {
   "title": "Šimtų užraktas",
   "eq": "1 % skaičiaus = 9",
   "q": "1 % skaičiaus lygu 9. Koks visas skaičius? Įrašyk jo šimtų skaitmenį.",
   "ans": 9,
   "sol": "9 · 100 = 900; šimtų skaitmuo 9"
  },
  {
   "title": "Trupmenos kodas",
   "eq": "33⅓ % skaičiaus = 2",
   "q": "33⅓ % (tai 1/3) skaičiaus lygu 2. Koks visas skaičius?",
   "ans": 6,
   "sol": "33⅓ % = 1/3, tad visas = 2 · 3 = 6"
  },
  {
   "title": "Penketuko skląstis",
   "eq": "5 % skaičiaus = 4",
   "q": "5 % skaičiaus lygu 4. Koks visas skaičius? Įrašyk jo dešimčių skaitmenį.",
   "ans": 8,
   "sol": "4 : 5 · 100 = 80; dešimčių skaitmuo 8"
  },
  {
   "title": "Sargybos mįslė",
   "eq": "",
   "q": "Sargybos mįslė: prekė atpigo 50 % ir tai sudarė 1 Eur. Kiek prekė kainavo be nuolaidos?",
   "ans": 2,
   "sol": "50 % = pusė kainos, tad kaina = 1 · 2 = 2 Eur"
  },
  {
   "title": "Aštuntadalio spyna",
   "eq": "12,5 % skaičiaus = 2",
   "q": "12,5 % (tai 1/8) skaičiaus lygu 2. Koks visas skaičius? Įrašyk jo dešimčių skaitmenį.",
   "ans": 1,
   "sol": "12,5 % = 1/8, tad visas = 2 · 8 = 16; dešimčių skaitmuo 1"
  },
  {
   "title": "Dešimtukų grotelės",
   "eq": "10 % skaičiaus = 6",
   "q": "10 % skaičiaus lygu 6. Koks visas skaičius? Įrašyk jo dešimčių skaitmenį.",
   "ans": 6,
   "sol": "6 : 10 · 100 = 60; dešimčių skaitmuo 6"
  },
  {
   "title": "Pabėgimo mįslė",
   "eq": "",
   "q": "Paskutinis ratukas! Prekė atpigo 33⅓ % ir tai sudarė 7 Eur. Kiek prekė kainavo be nuolaidos? Įrašyk atsakymo vienetų skaitmenį.",
   "ans": 1,
   "sol": "33⅓ % = 1/3, tad kaina = 7 · 3 = 21 Eur; vienetų skaitmuo 1"
  }
 ]
];
