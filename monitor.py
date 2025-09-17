import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re

url = "http://mosir-lancut.pl/asp/pl_start.asp?typ=14&menu=135&strona=1"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

pattern = re.compile(r"AKTUALNA LICZBA OSÓB NA BASENIE.*?(\d{1,2}) / (\d{1,3})")
text = soup.get_text()
match = pattern.search(text)

if match:
    aktualna = match.group(1)
    maksymalna = match.group(2)
else:
    aktualna = "Brak"
    maksymalna = "Brak"

timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

with open("frekwencja.csv", "a") as f:
    f.write(f"{timestamp},{aktualna},{maksymalna}\n")
