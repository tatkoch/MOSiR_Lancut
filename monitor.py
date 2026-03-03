from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup
from datetime import datetime
from pytz import timezone
import re
import unicodedata
import requests


# --------- FUNKCJE POMOCNICZE ---------

def normalize_text(s: str) -> str:
    """Normalizuje tekst: usuwa polskie znaki, spacje wielokrotne, lowercase."""
    s = unicodedata.normalize("NFKD", s)
    s = "".join(ch for ch in s if not unicodedata.combining(ch))  # osób -> osob
    s = re.sub(r"\s+", " ", s).strip().lower()
    return s


def extract_pool_counts(soup: BeautifulSoup):
    """
    Idioto-odporne wyciąganie aktualna/maksymalna:
    1) Szuka X/Y w HTML.
    2) Sprawdza kontekst (basen/osób/liczba/aktualna/frekwencja/obłożenie).
    3) Ma fallback po nagłówku typu "LICZBA7" / "AKTUALNA LICZBA" itd.
    """
    ratio_re = re.compile(r"(\d{1,3})\s*/\s*(\d{1,3})")
    context_keywords = ["basen", "osob", "liczba", "aktualna", "frekwencja", "oblozen", "oblozenie"]

    # 1) Najpierw: znajdź elementy z X/Y i sprawdź kontekst (rodzic + sąsiedzi)
    for node in soup.find_all(string=True):
        raw = str(node)
        m = ratio_re.search(raw)
        if not m:
            continue

        parent_text = node.parent.get_text(" ", strip=True) if node.parent else ""
        prev_text = node.find_previous(string=True)
        next_text = node.find_next(string=True)

        context = " ".join([
            raw,
            parent_text,
            str(prev_text) if prev_text else "",
            str(next_text) if next_text else ""
        ])

        norm = normalize_text(context)

        if any(k in norm for k in context_keywords):
            return m.group(1), m.group(2)

    # 2) Fallback: znajdź "nagłówek" po elastycznym regexie (np. LICZBA7) i dopiero potem X/Y dalej
    header_re = re.compile(r"(aktualna\s*liczba|liczba\s*\d+|liczba|frekwencja|obloz)", re.IGNORECASE)
    header = soup.find(string=header_re)
    if header:
        nxt = header.find_next(string=ratio_re)
        if nxt:
            m = ratio_re.search(str(nxt))
            if m:
                return m.group(1), m.group(2)

    return "Brak", "Brak"


# --------- KONFIGURACJA SELENIUM ---------

options = Options()
options.add_argument("--headless=new")   # nowszy tryb headless (jak nie działa, zmień na "--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920x1080")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

try:
    # ✅ POPRAWIONY URL: &amp; -> &
    driver.get("http://mosir-lancut.pl/asp/pl_start.asp?typ=14&menu=135&strona=1")

    # ✅ Lepsze czekanie zamiast sleep: czekamy aż strona faktycznie ma jakiś tekst
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )

    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    # --------- WYCIĄGANIE FREKWENCJI (ODPORNE) ---------
    aktualna, maksymalna = extract_pool_counts(soup)

    # --------- CZAS LOKALNY ---------
    timestamp = datetime.now(timezone("Europe/Warsaw")).strftime("%Y-%m-%d %H:%M:%S")

    # --------- POGODA (Open-Meteo) ---------
    temperatura = "Brak"
    warunki = "Brak"

    try:
        # ✅ POPRAWIONY URL: &amp; -> &
        url = "https://api.open-meteo.com/v1/forecast?latitude=50.068&longitude=22.231&current_weather=true"
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        data = response.json()
        weather = data.get("current_weather", {})
        temperatura = weather.get("temperature", "Brak")
        kod = weather.get("weathercode", None)

        kody_pogody = {
            0: "Bezchmurnie",
            1: "Głównie słonecznie",
            2: "Częściowo pochmurno",
            3: "Zachmurzenie całkowite",
            45: "Mgła",
            48: "Osadzająca się mgła",
            51: "Mżawka lekka",
            53: "Mżawka umiarkowana",
            55: "Mżawka gęsta",
            61: "Deszcz lekki",
            63: "Deszcz umiarkowany",
            65: "Deszcz intensywny",
            71: "Śnieg lekki",
            73: "Śnieg umiarkowany",
            75: "Śnieg intensywny",
            80: "Przelotne opady deszczu",
            81: "Przelotne opady umiarkowane",
            82: "Przelotne opady intensywne",
            95: "Burza",
            96: "Burza z lekkim gradem",
            99: "Burza z silnym gradem"
        }

        if kod is not None:
            opis = kody_pogody.get(kod, "Nieznane")
            warunki = f"{kod} - {opis}"

    except Exception:
        temperatura = "Brak"
        warunki = "Brak"

    # --------- ZAPIS DO CSV ---------
    # UTF-8, żeby polskie znaki nie robiły problemów
    with open("frekwencja.csv", "a", encoding="utf-8") as f:
        f.write(f"{timestamp},{aktualna},{maksymalna},{temperatura},{warunki}\n")

    # --------- LOG TECHNICZNY ---------
    with open("log.txt", "a", encoding="utf-8") as log:
        log.write(f"{timestamp} - uruchomiono monitor | frekwencja: {aktualna}/{maksymalna}\n")

finally:
    driver.quit()
