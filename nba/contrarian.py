import operator
from csv import reader

dk_salaries = {}
fd_salaries = {}
ownership = {
    'd': {},
    'w': {},
    'm': {},
    'y': {}
}

def percent_to_float(percent_str):
    try:
        return float(percent_str[:-1])
    except ValueError:
        return 0.0

def construct_lineup(ownership, salaries):
    sorted_ownership = sorted(ownership.items(), key=operator.itemgetter(1))
    filtered_ownership = [x for x in sorted_ownership if x[1] > 0]
    for player, ownership in filtered_ownership:
        if player in salaries:
            print player, ownership, salaries[player]
    # Contraints:
    # sum(salary) < X, lineup restrictions, maximize salary / ownership

with open('salaries/dk_nba_salaries_2015_11_05.csv') as f:
    csvreader = reader(f, delimiter=',', quotechar='"')
    for i, row in enumerate(csvreader):
        if i != 0:
            dk_salaries[row[1]] = (int(row[2]), row[0])

with open('salaries/fd_nba_salaries_2015_11_04.csv') as f:
    csvreader = reader(f, delimiter=',', quotechar='"')
    for i, row in enumerate(csvreader):
        if i != 0:
            fd_salaries['%s %s' % (row[2], row[3])] = (int(row[6]), row[1])

with open('ownership/fs_nba_ownership_2015_11_06.tsv') as f:
    tsvreader = reader(f, delimiter='\t', quotechar='"')
    for i, row in enumerate(tsvreader):
        # [Last, First], [Team], [Post],
        # [PPG], [Own], [Win], (d)
        # [Gms], [PPG], [Own], [Win] (x3: w, m, y)
        player = ' '.join(row[0].split(', ')[::-1])
        own = {
            'd': percent_to_float(row[4]),
            'w': percent_to_float(row[8]),
            'm': percent_to_float(row[12]),
            'y': percent_to_float(row[16])
        }
        ownership['d'][player] = own['d']
        ownership['w'][player] = own['w']
        ownership['m'][player] = own['m']
        ownership['y'][player] = own['y']

construct_lineup(ownership['d'], dk_salaries)
