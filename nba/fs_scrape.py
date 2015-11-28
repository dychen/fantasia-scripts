from bs4 import BeautifulSoup
import csv
import datetime
import requests

def scrape():

    def get_filename():
        date = datetime.date.today() - datetime.timedelta(days=1)
        return 'fs_nba_ownership_%s.tsv' % date.strftime('%Y_%m_%d')

    response = requests.get('http://fantasyscore.com/top-players/basketball')
    outfile = 'ownership/%s' % get_filename()
    soup = BeautifulSoup(response.text, 'html5lib')
    rows = []
    for tr in soup.find_all('tbody')[0].children:
        rows.append([td.string for td in tr.children])
    with open(outfile, 'w') as f:
        writer = csv.writer(f, delimiter='\t', quotechar='"',
                            quoting=csv.QUOTE_MINIMAL)
        for row in rows:
            writer.writerow(row)

if __name__=='__main__':
    scrape()
