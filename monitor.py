from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from datetime import datetime
from pytz import timezone
import re
import time
import requests

# Konfiguracja przeglądarki
options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920x1080")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get("http://mosir-lancut.pl/asp/pl_start.asp?typ=14&menu=135&strona=1")
time.sleep(3)

html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

naglowek = soup.find(string=re.compile("AKTUALNA LICZBA OSÓB NA BASENIE"))
if naglowek:
    next_element = naglowek.find_next(string=re.compile(r"\d{1,3} ?/ ?\d{1,3}"))
    if next_element:
        liczby = re.findall(r"\d{1,3}", next_element)
        aktualna = liczby[0]
        maksymalna = liczby[1]
    else:
        aktualna = "Brak"
        maksymalna = "Brak"
else:
    aktualna = "Brak"
    maksymalna = "Brak"

# Czas lokalny
timestamp = datetime.now(timezone('Europe/Warsaw')).strftime("%Y-%m-%d %H:%M:%S")

# Pogoda z Open-Meteo
try:
    url = "https://api.open-meteo.com/v1/forecast?latitude=50.068&longitude=22.231&current_weather=true"
    response = requests.get(url)
    weather = response.json()["current_weather"]
    temperatura = weather["temperature"]
    kod = weather["weathercode"]

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

    opis = kody_pogody.get(kod, "Nieznane")
    warunki = f"{kod} - {opis}"
except Exception as e:
    temperatura = "Brak"
    warunki = "Brak"

# Zapis danych do CSV
with open("frekwencja.csv", "a") as f:
    f.write(f"{timestamp},{aktualna},{maksymalna},{temperatura},{warunki}\n")

# Log techniczny
with open("log.txt", "a") as log:
    log.write(f"{timestamp} - uruchomiono monitor\n")

driver.quit()
