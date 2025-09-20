from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from datetime import datetime
import re

options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920x1080")
options.binary_location = "/usr/bin/google-chrome"

service = Service("/usr/bin/chromedriver")
driver = webdriver.Chrome(service=service, options=options)

driver.get("http://mosir-lancut.pl/asp/pl_start.asp?typ=14&menu=135&strona=1")
driver.implicitly_wait(5)

html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

match = soup.find(string=re.compile(r"\d{1,2} / \d{1,3}"))
if match:
    liczby = re.findall(r"\d{1,3}", match)
    aktualna = liczby[0]
    maksymalna = liczby[1]
else:
    aktualna = "Brak"
    maksymalna = "Brak"

timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
with open("frekwencja.csv", "a") as f:
    f.write(f"{timestamp},{aktualna},{maksymalna}\n")

driver.quit()
