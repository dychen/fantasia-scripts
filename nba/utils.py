from csv import reader
import datetime
import os
import re

STOP_WORDS = set(['PG', 'SG', 'SF', 'PF', 'C', 'F', 'G', 'UTIL'])

PRIZES_38K = {
    1: 10000.00,
    2: 7500.00,
    3: 5000.00,
    4: 3000.00,
    5: 2000.00,
    6: 1000.00,
    7: 750.00,
    8: 500.00,
    9: 400.00,
    10: 300.00,
    11: 200.00,
    16: 150.00,
    21: 100.00,
    31: 60.00,
    41: 50.00,
    61: 40.00,
    81: 35.00,
    101: 30.00,
    121: 25.00,
    141: 20.00,
    201: 17.00,
    301: 15.00,
    401: 14.00,
    501: 13.00,
    701: 12.00,
    1001: 11.00,
    1501: 10.00,
    2001: 9.00,
    2501: 8.00,
    3501: 7.00,
    5001: 6.00,
    7851: 0
}

PRIZES_48K = {
    1: 10000.00,
    2: 7000.00,
    3: 5000.00,
    4: 4000.00,
    5: 3000.00,
    6: 2000.00,
    7: 1500.00,
    9: 1000.00,
    11: 700.00,
    13: 500.00,
    16: 300.00,
    21: 200.00,
    26: 100.00,
    31: 75.00,
    46: 60.00,
    61: 50.00,
    81: 40.00,
    101: 35.00,
    126: 30.00,
    176: 25.00,
    226: 20.00,
    276: 17.00,
    376: 15.00,
    526: 14.00,
    726: 13.00,
    926: 12.00,
    1226: 11.00,
    1726: 10.00,
    2226: 9.00,
    3226: 8.00,
    4226: 7.00,
    6026: 6.00,
    9626: 0
}

PRIZES_57K = {
    1: 12000.00,
    2: 8000.00,
    3: 5000.00,
    4: 4000.00,
    5: 3000.00,
    6: 2000.00,
    7: 1000.00,
    9: 750.00,
    11: 500.00,
    16: 400.00,
    21: 300.00,
    31: 200.00,
    41: 100.00,
    61: 80.00,
    81: 60.00,
    101: 50.00,
    131: 40.00,
    171: 35.00,
    221: 30.00,
    291: 25.00,
    381: 20.00,
    581: 15.00,
    981: 12.00,
    1481: 10.00,
    2281: 9.00,
    3281: 8.00,
    4781: 7.00,
    6781: 6.00,
    11781: 0
}

PRIZES_77K = {
    1: 15000.00,
    2: 10000.00,
    3: 7000.00,
    4: 5000.00,
    5: 4000.00,
    6: 3000.00,
    7: 2000.00,
    9: 1000.00,
    11: 750.00,
    16: 500.00,
    21: 400.00,
    31: 300.00,
    41: 200.00,
    61: 100.00,
    81: 75.00,
    101: 60.00,
    151: 50.00,
    201: 40.00,
    251: 30.00,
    341: 25.00,
    451: 20.00,
    701: 15.00,
    1001: 12.00,
    1501: 10.00,
    2001: 9.00,
    3001: 8.00,
    4001: 7.00,
    9001: 6.00,
    16301: 0
}

PRIZES_96K = {
    1: 20000.00,
    2: 15000.00,
    3: 10000.00,
    4: 7500.00,
    5: 5000.00,
    6: 3000.00,
    7: 2000.00,
    8: 1000.00,
    9: 750.00,
    11: 600.00,
    16: 500.00,
    21: 400.00,
    26: 300.00,
    31: 200.00,
    41: 150.00,
    61: 100.00,
    101: 75.00,
    141: 60.00,
    201: 50.00,
    301: 40.00,
    501: 30.00,
    751: 20.00,
    1051: 15.00,
    1451: 12.00,
    1901: 10.00,
    2551: 9.00,
    3551: 8.00,
    6551: 7.00,
    11551: 6.00,
    19551: 0
}

PRIZES_115K = {
    1: 20000.00,
    2: 15000.00,
    3: 10000.00,
    4: 7000.00,
    5: 5000.00,
    6: 4000.00,
    7: 3000.00,
    8: 2000.00,
    9: 1500.00,
    11: 1000.00,
    16: 700.00,
    21: 500.00,
    26: 400.00,
    31: 300.00,
    41: 200.00,
    51: 175.00,
    61: 150.00,
    71: 125.00,
    81: 100.00,
    101: 90.00,
    121: 80.00,
    141: 70.00,
    171: 60.00,
    221: 50.00,
    281: 45.00,
    361: 40.00,
    461: 35.00,
    561: 30.00,
    811: 25.00,
    1061: 20.00,
    1361: 15.00,
    1861: 12.00,
    2461: 10.00,
    3461: 9.00,
    5961: 8.00,
    8961: 7.00,
    13961: 6.00,
    23536: 0
}

PRIZES_134K = {
    1: 50000.00,
    2: 25000.00,
    3: 15000.00,
    4: 10000.00,
    5: 7500.00,
    6: 5000.00,
    7: 3000.00,
    9: 2000.00,
    11: 1000.00,
    16: 750.00,
    21: 500.00,
    31: 300.00,
    41: 200.00,
    56: 150.00,
    76: 100.00,
    101: 75.00,
    131: 60.00,
    181: 50.00,
    231: 40.00,
    331: 30.00,
    481: 20.00,
    681: 15.00,
    981: 12.00,
    1481: 10.00,
    2281: 9.00,
    3481: 8.00,
    5281: 7.00,
    8781: 6.00,
    15781: 5.00,
    30141: 0
}

PRIZES_153K = {
    1: 50000.00,
    2: 30000.00,
    3: 20000.00,
    4: 15000.00,
    5: 10000.00,
    6: 7500.00,
    7: 5000.00,
    9: 3000.00,
    11: 2000.00,
    16: 1000.00,
    21: 750.00,
    26: 500.00,
    36: 300.00,
    46: 200.00,
    66: 150.00,
    86: 100.00,
    111: 75.00,
    141: 60.00,
    191: 50.00,
    241: 40.00,
    341: 30.00,
    491: 20.00,
    691: 15.00,
    991: 12.00,
    1491: 10.00,
    2491: 9.00,
    3991: 8.00,
    5991: 7.00,
    9991: 6.00,
    16991: 5.00,
    31991: 0
}

def get_prize_map(numentries):
    if numentries < 39000:
        print numentries, 'PRIZES_38K'
        return PRIZES_38K
    elif numentries < 49000:
        print numentries, 'PRIZES_48K'
        return PRIZES_48K
    elif numentries < 58000:
        print numentries, 'PRIZES_57K'
        return PRIZES_57K
    elif numentries < 78000:
        print numentries, 'PRIZES_77K'
        return PRIZES_77K
    elif numentries < 97000:
        print numentries, 'PRIZES_96K'
        return PRIZES_96K
    elif numentries < 116000:
        print numentries, 'PRIZES_115K'
        return PRIZES_115K
    elif numentries < 135000:
        print numentries, 'PRIZES_134K'
        return PRIZES_134K
    else:
        print numentries, 'PRIZES_153K'
        return PRIZES_153K

def get_weighted_score(index, prize_map):
    target_rank = index + 1
    for rank in sorted(prize_map.keys())[::-1]:
        if target_rank >= rank:
            return prize_map[rank] - 3
    return -3

def load_salaries(filename):
    salaries = {}
    with open(filename) as f:
        csvreader = reader(f, delimiter=',', quotechar='"')
        for i, row in enumerate(csvreader):
            if i != 0:
                salaries[row[1]] = (int(row[2]), row[0])
    return salaries

def load_results(filename):
    results = []
    with open(filename) as f:
        csvreader = reader(f, delimiter=',', quotechar='"')
        for i, row in enumerate(csvreader):
            if i != 0:
                # Rank, EntryId, EntryName, TimeRemaining, Points, Lineup
                lineup = row[-1].split()
                for i, word in enumerate(lineup[:]):
                    if word in STOP_WORDS:
                        lineup[i] = '\t'
                players = [word.strip()
                           for word in ' '.join(lineup).split('\t')
                           if word.strip()]
                if players:
                    results.append(players)
    return results

def get_ids(limit=7, until=None):
    # Defaults to today
    until = until or datetime.date.today().strftime('%m/%d/%Y').lstrip('0')

    # Get the first contest id after each date (the Daily Sharpshooter ids)
    REGEX = r'\d{1,2}\/\d{1,2}\/\d{4}\nhttps://www.draftkings.com/[^ ]*/(\d*)'

    def strip_text(text):
        left_bound = 'Contest Results (script parse)'
        right_bound = until
        return text.split(left_bound)[1].split(right_bound)[0]

    with open('%s/README.md' % os.environ['ROOT_DIR']) as f:
        text = strip_text(''.join([line for line in f]))
    ids = re.findall(REGEX, text)
    return ids[-limit:]

