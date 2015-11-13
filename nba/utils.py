from csv import reader

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
    5001: 6.00
}

PRIZES_47K = {
    1: 500.00,
    2: 300.00,
    3: 200.00,
    4: 150.00,
    5: 100.00,
    6: 80.00,
    7: 60.00,
    9: 50.00,
    11: 35.00,
    16: 25.00,
    21: 20.00,
    26: 15.00,
    31: 10.00,
    41: 7.50,
    51: 5.00,
    76: 4.00,
    101: 3.00,
    201: 2.50,
    301: 2.00,
    501: 1.50,
    1001: 1.00,
    2501: 0.75,
    5001: 0.50
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
    11551: 6.00
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
    13961: 6.00
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
    15781: 5.00
}

def get_weighted_score(index, numentries):
    if numentries > 133000:
        prize_map = PRIZES_134K
    elif numentries > 114000:
        prize_map = PRIZES_115K
    elif numentries > 95000:
        prize_map = PRIZES_96K
    elif numentries > 37000:
        prize_map = PRIZES_38K
    target_rank = index + 1
    for rank in sorted(prize_map.keys()):
        if target_rank <= rank:
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
