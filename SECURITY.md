# Politică de Securitate

## Versiuni Suportate

Următoarele versiuni ale proiectului primesc în prezent actualizări de securitate:

| Versiune | Suportat          |
| -------- | -----------------|
| 1.0.x    | :white_check_mark: |
| < 1.0    | :x:                |

## Raportarea Vulnerabilităților

Luăm în serios securitatea proiectului nostru. Dacă descoperiți o vulnerabilitate de securitate, vă rugăm să o raportați în mod responsabil.

### Cum să raportați o vulnerabilitate

**NU raportați vulnerabilitățile de securitate prin GitHub Issues publice.**

În schimb, vă rugăm să:

1. **Trimiteți un email** la: [security@example.com] cu subiectul "Security Vulnerability in Proiect_Calitate_Aer"
2. **Descrieți vulnerabilitatea** în detaliu, inclusiv:
   - Tipul vulnerabilității
   - Pașii de reproducere
   - Impactul potențial
   - Orice soluții sugerate

### Ce ne putem aștepta

- **Confirmare**: Veți primi o confirmare în maxim 48 de ore
- **Actualizări**: Vă vom ține la curent cu progresul investigației
- **Rezolvare**: Vom lucra la o soluție și vom lansa un patch cât mai curând posibil
- **Credit**: Dacă doriți, vă vom menționa în secțiunea de mulțumiri

## Bune Practici de Securitate

### Pentru Utilizatori

1. **Protejați cheia API**
   - Nu includeți niciodată cheia API în cod
   - Folosiți fișierul `.env` (ignorat de Git)
   - Nu împărtășiți fișierul `.env`

2. **Actualizați dependențele**
   ```bash
   pip install --upgrade -r requirements.txt
   ```

3. **Verificați actualizări de securitate**
   ```bash
   pip-audit
   ```

### Pentru Dezvoltatori

1. **Code Review**: Toate modificările trebuie revizuite
2. **Dependency Scanning**: Rulați scanări regulate pentru vulnerabilități
3. **Input Validation**: Validați toate input-urile utilizatorului
4. **Error Handling**: Nu expuneți informații sensibile în mesaje de eroare

## Vulnerabilități Cunoscute

În prezent, nu sunt vulnerabilități de securitate cunoscute în această versiune.

Ultima actualizare: 16 Ianuarie 2026
