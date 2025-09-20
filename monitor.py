from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from datetime import datetime
import re
import time

options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920x1080")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get("http://mosir-lancut.pl/asp/pl_start.asp?typ=14&menu=135&strona=1")
time.sleep(3)  # poczekaj na załadowanie strony

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

timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
with open("frekwencja.csv", "a") as f:
    f.write(f"{timestamp},{aktualna},{maksymalna}\n")

driver.quit()
