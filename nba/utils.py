from csv import reader

STOP_WORDS = set(['PG', 'SG', 'SF', 'PF', 'C', 'F', 'G', 'UTIL'])

def get_weighted_score(index):
    rank = index + 1
    # Weigh by dollar returns
    if rank > 23535:
        return -3
    elif rank > 13960:
        return 6
    elif rank > 8960:
        return 7
    elif rank > 5960:
        return 8
    elif rank > 3460:
        return 9
    elif rank > 2460:
        return 10
    elif rank > 1860:
        return 12
    elif rank > 1360:
        return 15
    elif rank > 1060:
        return 20
    elif rank > 810:
        return 25
    elif rank > 560:
        return 30
    elif rank > 460:
        return 35
    elif rank > 360:
        return 40
    elif rank > 280:
        return 45
    elif rank > 220:
        return 50
    elif rank > 170:
        return 60
    elif rank > 140:
        return 70
    elif rank > 120:
        return 80
    elif rank > 100:
        return 90
    elif rank > 80:
        return 100
    elif rank > 70:
        return 125
    elif rank > 60:
        return 150
    elif rank > 50:
        return 175
    elif rank > 40:
        return 200
    elif rank > 30:
        return 300
    elif rank > 25:
        return 400
    elif rank > 20:
        return 500
    elif rank > 15:
        return 700
    elif rank > 10:
        return 1000
    elif rank > 8:
        return 1500
    elif rank == 8:
        return 2000
    elif rank == 7:
        return 3000
    elif rank == 6:
        return 4000
    elif rank == 5:
        return 5000
    elif rank == 4:
        return 7500
    elif rank == 3:
        return 10000
    elif rank == 2:
        return 15000
    elif rank == 1:
        return 20000

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
