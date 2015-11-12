import operator
from csv import reader

dk_salaries = {}
fd_salaries = {}
diffs = {}

with open('salaries/dk_nba_salaries_2015_11_04.csv') as f:
    csvreader = reader(f, delimiter=',', quotechar='"')
    for i, row in enumerate(csvreader):
        if i != 0:
            dk_salaries[row[1]] = (int(row[2]), row[0])

with open('salaries/fd_nba_salaries_2015_11_04.csv') as f:
    csvreader = reader(f, delimiter=',', quotechar='"')
    for i, row in enumerate(csvreader):
        if i != 0:
            fd_salaries['%s %s' % (row[2], row[3])] = (int(row[6]), row[1])

players = set(dk_salaries.keys() + fd_salaries.keys())

for player in sorted(list(players)):
    dk_player = dk_salaries[player] if player in dk_salaries else None
    fd_player = fd_salaries[player] if player in fd_salaries else None
    if not dk_player:
        print 'No DK player found for %s' % player
    elif not fd_player:
        print 'No FD player found for %s' % player
    else:
        # Positive means DK-expensive/FD-cheap, negative means DK-cheap
        diff = dk_player[0] - fd_player[0]
        print '%s: %d' % (player, diff)
        diffs[player] = diff

sorted_diffs = sorted(diffs.items(), key=operator.itemgetter(1))
dk_cheap = sorted_diffs[-30:]
fd_cheap = sorted_diffs[:30]

print '===DK CHEAP==='
for player, diff in dk_cheap:
    dk_player = dk_salaries[player]
    fd_player = fd_salaries[player]
    print ('%s %d (DK: %d) (FD: %d) (POS: %s)'
           % (player, diff, dk_player[0], fd_player[0], dk_player[1]))

print '===FD CHEAP==='
for player, diff in fd_cheap:
    dk_player = dk_salaries[player]
    fd_player = fd_salaries[player]
    print ('%s %d (DK: %d) (FD: %d) (POS: %s)'
           % (player, diff, dk_player[0], fd_player[0], fd_player[1]))

