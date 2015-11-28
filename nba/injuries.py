from bs4 import BeautifulSoup
import csv
import datetime
import requests
from database import Player, Injury, InjuryComment, get_model, update_or_create

MONTHS = {
    'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6, 'Jul': 7,
    'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12
}

TODAY = datetime.date.today()

URL = 'http://espn.go.com/nba/injuries'

def get_date(datestr):
    """
    Return a date from a datestring. Make sure that it wraps around to the
    previous year if the datestring is greater than the current date (e.g. data
    for Dec 31 when 'today' is Jan 1).
    @param datestr [str]: [Month] [Date] (e.g. 'Nov 11')
    @return [datetime.date]
    """
    month, day = datestr.split(' ')
    month = MONTHS[month]
    year = TODAY.year
    date = datetime.date(year, month, int(day))
    return date if date <= TODAY else datetime.date(year-1, month, int(day))

def scrape():
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, 'html5lib')
    rows = []
    injury = None
    for tr in soup.find_all('tbody')[0].children:
        row = [td for td in tr if hasattr(tr, 'children')]
        if len(row) == 3:
            name, status, datestr = [r.string for r in row]
            if name != 'NAME' and status != 'STATUS' and datestr != 'DATE':
                date = get_date(datestr)
                player = get_model(Player, name=name)
                injury, _ = update_or_create(Injury,
                                             player_id=player.id,
                                             date=date,
                                             defaults={ 'status': status })
        elif len(row) == 1:
            if 'Comment:' in row[0].contents[0].string and injury:
                update_or_create(InjuryComment, injury_id=injury.id,
                                 comment=unicode(row[0].contents[-1]))

if __name__=='__main__':
    scrape()
