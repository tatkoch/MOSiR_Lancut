# 📊 Interaktywne wykresy frekwencji basenu MOSiR Łańcut

Ten projekt prezentuje interaktywne wykresy frekwencji na basenie MOSiR w Łańcucie, generowane na podstawie danych z pliku `frekwencja.csv`. Wykresy aktualizują się automatycznie przy każdym uruchomieniu — dane są pobierane na żywo z GitHub.

---

## 🔗 Uruchom interaktywnie

### ▶️ Google Colab (bez instalacji)
[![Otwórz w Google Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/tatkoch/MOSiR_Lancut/blob/main/MOSiR_wykresy.ipynb)

### 🟦 Binder (pełna interaktywność, bez logowania)
[![Uruchom w Binderze](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/tatkoch/MOSiR_Lancut/HEAD?filepath=MOSiR_wykresy.ipynb)

---

## 📁 Zawartość repozytorium

- `frekwencja.csv` — aktualne dane z monitoringu frekwencji
- `MOSiR_wykresy.ipynb` — notebook z wykresami:
  - Nakładające się wykresy dla każdego dnia tygodnia
  - Średnia frekwencja godzinowa (6:00–22:00)
  - Interaktywne dropdowny
  - Linie ryzyka (70) i maksymalna (80)

---

## 📦 Wymagane biblioteki (dla Binder)

Plik `requirements.txt` zawiera:
pandas 
plotly

Dzięki temu środowisko uruchomieniowe automatycznie zainstaluje potrzebne pakiety.

---

## 📣 Autor

Projekt: [tatkoch](https://github.com/tatkoch)  
Dane: MOSiR Łańcut  
Wizualizacja: Python + Plotly  
Notebook: Google Colab / Binder

---

## 📬 Kontakt

Masz pomysł na ulepszenie wykresów? Chcesz dodać prognozy, alerty lub wersję mobilną?  
Zgłoś propozycję przez [Issues](https://github.com/tatkoch/MOSiR_Lancut/issues) lub stwórz Pull Request!
