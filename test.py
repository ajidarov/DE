import requests
import pandas as pd
from bs4 import BeautifulSoup

url = "https://www.goszakup.gov.kz/ru/registry/rqc"

querystring = {"count_record": "500"}

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/98.0.4758.82 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,"
              "application/signed-exchange;v=b3;q=0.9",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-User": "?1",
    "Sec-Fetch-Dest": "document",
    "Referer": "https://www.goszakup.gov.kz/ru/registry/rqc",
    "Accept-Language": "en-US,en;q=0.9,ru-RU;q=0.8,ru;q=0.7"
}

session = requests.Session()
session.verify = False
response = session.request("GET", url, headers=headers, params=querystring)

html = BeautifulSoup(response.content, 'html.parser')
items = html.find("tbody").find_all("tr")
columns = ['Номер', 'Наименование потенциального поставщика', 'БИН/ИИН',
           'Наименование, номер и дата выдачи документа']
df = pd.DataFrame()
for i in items:

    new_data = dict()
    for td, c in zip(i.find_all("td"), columns):
        new_data[c] = td.text.strip()

    new_row = pd.Series(new_data)
    df = df.append(new_row, ignore_index=True)

print(df.shape)
df = df.drop_duplicates(
    subset=['Наименование потенциального поставщика', 'БИН/ИИН', 'Наименование, номер и дата выдачи документа'],
    keep='first')
print(df.shape)
df.to_excel('GosZakup.xlsx', index=False)
# print(response.text)

