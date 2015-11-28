"""
Automate the data collection process:
1. Export CSV data for the previous day's DK Sharpshooter and Quarter Arcade contests.
2. Run the `fs_scrape.py` task to get ownership and points from [fantasyscore.com](http://fantasyscore.com/top-players/basketball)
3. Run the `injuries.py` task to get injury updates from [espn.com](http://espn.go.com/nba/injuries).
(Manual): Export the salaries for the next day's contests.
"""

import argparse
import os
import re
import zipfile
import requests
import fs_scrape
import injuries

def get_dk_results(results_recent=False):

    def get_contest_urls():
        with open('%s/README.md' % os.environ['ROOT_DIR']) as f:
            text = ''.join([line for line in f])
        urls = re.findall(r'https://www.draftkings.com/[^ ]*', text)
        return urls[-2:] if results_recent else urls[-4:-2]

    def get_data(url):
        HEADERS = {
            'referer': url,
            'cookie': os.environ['DK_AUTH_COOKIES']
        }
        OUTFILE = 'out.zip'
        OUTPATH = 'results'

        def read_response(response):
            print 'Downloading and unzipping file from %s' % response.url
            with open(OUTFILE, 'wb') as f:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)

        def unzip_data():
            with open(OUTFILE, 'rb') as f:
                z = zipfile.ZipFile(f)
                for name in z.namelist():
                    z.extract(name, OUTPATH)

        export_url = url.replace('gamecenter', 'exportfullstandingscsv')
        read_response(requests.get(export_url, headers=HEADERS))
        unzip_data()

    for url in get_contest_urls():
        get_data(url)
    return

def get_fs_ownerships():
    fs_scrape.scrape()

def get_injury_updates():
    injuries.scrape()

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--results-recent', action='store_const', const=True,
                        help=('Take the most recent two urls in the README,'
                              ' otherwise defaults to the next most recent'))
    args = parser.parse_args()

    get_dk_results(args.results_recent)
    get_fs_ownerships()
    get_injury_updates()
