# Predicție Calitate Aer
## Aplicație Web bazată pe Machine Learning

**Echipa 421 B**

Berciu Antonio | Munteanu Radu | Roman Silviu

Ianuarie 2026

---

# Ce am creat?

## Problema
**Poluarea aerului** afectează sănătatea noastră în fiecare zi
- PM2.5 = particule foarte mici în aer (< 2.5 micrometri)
- Cauze: mașini, fabrici, fum
- **Impact**: probleme respiratorii și cardiovasculare

## Soluția
✨ **Dashboard web** care prezice calitatea aerului pentru următoarele 24 de ore

## De ce este util?
- Planifici când să ieși la alergat
- Protejezi persoanele vulnerabile
- Vezi când aerul este mai curat

---

# 🛠️ Cum funcționează?

## Tehnologii folosite

**Python** - Limbajul principal
- **pandas** - Prelucrare date
- **scikit-learn** - Inteligență artificială
- **Streamlit** - Interface web
- **Plotly** - Grafice colorate

**Surse de date**
- **OpenAQ** - Date despre poluare
- **OpenWeatherMap** - Date meteo (temperatură, vânt, etc.)

---

# 🏗️ Cum am împărțit munca?

## 3 Module Principale

**1. Colectare Date** (Berciu Antonio)
- Preia date despre poluare de pe internet
- Preia date meteo (temperatură, vânt)
- Salvează tot într-un fișier CSV

**2. Model Inteligență Artificială** (Munteanu Radu)
- Învață din datele istorice
- Prezice poluarea pentru următoarele 24h
- Verifică cât de precise sunt predicțiile

**3. Interface Web** (Roman Silviu)
- Dashboard frumos și ușor de folosit
- Grafice colorate și interactive
- Predicții + Date istorice + Analize

---

# 🧠 Modelul de Predicție

## Cum funcționează "creierul" aplicației?

**Random Forest** = mulți "arbori de decizie" care votează împreună

**Ce analizează:**
- Temperatura
- Umiditatea
- Viteza vântului
- Ora din zi
- Luna din an

**Rezultat:** Prezice poluarea pentru următoarele 24 de ore

**Performanță:** ~85% acuratețe pe date de test

---

# ⚠️ Probleme întâlnite și soluții

## 🔴 Problema 1: Date incomplete

**Ce s-a întâmplat:**
- Site-urile de unde luam datele nu aveau mereu informații
- Uneori lipseau date pentru București
- Aveam limite la câte date puteam lua pe minut

**Cum am rezolvat:**
- Am creat date simulate realiste când lipseau cele reale
- Am pus pauze între request-uri ca să nu depășim limita
- Am salvat datele odată luate, ca să nu le mai cerem din nou

---

# ⚠️ Probleme întâlnite și soluții (cont.)

## 🔴 Problema 2: Modelul învăța greșit

**Ce s-a întâmplat:**
- Modelul nu știa să prezică bine cu puține date
- Uneori "memoriza" prea mult și nu generaliza
- Predicțiile erau inexacte pentru situații extreme

**Cum am rezolvat:**
- Am generat date sintetice pentru antrenare
- Am ajustat parametrii modelului (mai mulți arbori, mai adânci)
- Am adăugat informații despre ora zilei și luna

---

# ⚠️ Probleme întâlnite și soluții (cont.)

## 🔴 Problema 3: Colaborare în echipă

**Ce s-a întâmplat:**
- Când lucram simultan, codul se suprapunea
- Aveam conflicte când încercam să combinăm munca
- Fiecare scria cod puțin diferit

**Cum am rezolvat:**
- Am folosit Git branches (fiecare pe ramura lui)
- Am făcut code review înainte de a combina codul
- Am scris documentație și comentarii clare
- Am împărțit proiectul în module separate

---

# ⚠️ Probleme întâlnite și soluții (cont.)

## 🔴 Problema 4: Interface-ul se comporta ciudat

**Ce s-a întâmplat:**
- Aplicația "uita" datele când reîncărcam pagina
- Se reîncărca prea des și era lentă
- Graficele nu arătau bine pe toate ecranele

**Cum am rezolvat:**
- Am folosit "session state" să păstreze datele
- Am organizat layout-ul mai eficient
- Am testat pe diferite rezoluții de ecran

---

# 📈 Ce am realizat?

## Aplicație funcțională cu:

✅ **Predicții** pentru următoarele 24 de ore
✅ **Grafice colorate** și ușor de înțeles
✅ **Categorii calitate aer** (Bună, Moderată, Nesănătoasă, etc.)
✅ **Date istorice** și analiză

## Performanță:

- Precizie ~85% pe date de test
- Răspuns rapid (< 2 secunde)
- 3 module separate care funcționează împreună
- 10+ teste pentru a verifica că totul merge bine

## Bonus:

✅ Documentație completă pe GitHub
✅ Cod bine organizat și comentat

---

# 🔮 Ce urmează?

## Îmbunătățiri planificate:

🔹 Predicții pentru mai multe orașe
🔹 Notificări prin email când aerul devine periculos
🔹 Export rapoarte PDF
🔹 Predicții pentru 7 zile (nu doar 24h)
🔹 Aplicație pentru telefon

---

# 🎓 Ce am învățat?

## Tehnic
- Cum să lucrezi cu API-uri și date din exterior
- Cum să creezi un model de inteligență artificială
- Cum să faci o aplicație web interactivă

## Lucru în echipă
- Cum să folosim Git pentru colaborare
- Importanța documentației clare
- Cum să rezolvăm probleme împreună
- Cum să ne împărțim munca eficient

---

# 👥 Echipa noastră

## Cine a făcut ce?

| Student | Responsabilitate |
|---------|------------------|
| **Berciu Antonio** | Colectare date de pe internet (API-uri) |
| **Munteanu Radu** | Modelul de inteligență artificială |
| **Roman Silviu** | Dashboard-ul web și graficele |

**Toți:** Documentație, teste, rezolvare probleme împreună!

---

# 🙏 Mulțumim!

## Întrebări?

💻 **GitHub**: https://github.com/radustst/Proiect_Calitate_Aer

---

**Echipa 421 B**

Berciu Antonio | Munteanu Radu | Roman Silviu

🌍 Împreună pentru un aer mai curat!

Ianuarie 2026
