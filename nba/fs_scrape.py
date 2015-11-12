from bs4 import BeautifulSoup
import csv
import requests

response = requests.get('http://fantasyscore.com/top-players/basketball')
outfile = 'tmp_fs_scrape.csv'
soup = BeautifulSoup(response.text, 'html5lib')
rows = []
for tr in soup.find_all('tbody')[0].children:
    rows.append([td.string for td in tr.children])
with open(outfile, 'w') as f:
    writer = csv.writer(f, delimiter='\t', quotechar='"',
                        quoting=csv.QUOTE_MINIMAL)
    for row in rows:
        writer.writerow(row)
