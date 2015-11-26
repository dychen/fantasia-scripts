import operator
from csv import reader
import numpy

dk_salaries = {}
fd_salaries = {}

def percent_to_float(percent_str):
    try:
        return float(percent_str[:-1])
    except ValueError:
        return 0.0

def pretty_print(tuplelist):
    for player, value in tuplelist:
        print '\t%s %f' % (player, value)

def zscore(value, mean, stdev):
    return (value - mean) / stdev

def load_ownership(filename):
    ownership = { 'd': {}, 'w': {}, 'm': {}, 'y': {} }
    with open(filename) as f:
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
    return ownership

def load_winpercent(filename):
    winpercent = { 'd': {}, 'w': {}, 'm': {}, 'y': {} }
    with open(filename) as f:
        tsvreader = reader(f, delimiter='\t', quotechar='"')
        for i, row in enumerate(tsvreader):
            # [Last, First], [Team], [Post],
            # [PPG], [Own], [Win], (d)
            # [Gms], [PPG], [Own], [Win] (x3: w, m, y)
            player = ' '.join(row[0].split(', ')[::-1])
            win = {
                'd': percent_to_float(row[5]),
                'w': percent_to_float(row[9]),
                'm': percent_to_float(row[13]),
                'y': percent_to_float(row[17])
            }
            winpercent['d'][player] = win['d']
            winpercent['w'][player] = win['w']
            winpercent['m'][player] = win['m']
            winpercent['y'][player] = win['y']
    return winpercent

def own_win_diff(ownership, winpercent):
    diffs = {}
    for player in ownership:
        if (player in winpercent
            and ownership[player] > 0 and winpercent[player] > 0):
            diff = winpercent[player] - ownership[player]
            diffs[player] = diff
    mean = numpy.mean(diffs.values())
    std = numpy.std(diffs.values())
    zscores = { player: zscore(diffs[player], mean, std) for player in diffs }
    sorted_zscores = sorted(zscores.items(), key=operator.itemgetter(1))
    print 'Top'
    pretty_print(sorted_zscores[-20:][::-1])
    print 'Bottom'
    pretty_print(sorted_zscores[:20])
    return zscores

def zscore_delta(curr_zscore, prev_zscore):
    deltas = {}
    for player in curr_zscore:
        if (player in prev_zscore
            and curr_zscore[player] > 0 and prev_zscore[player] > 0):
            delta = curr_zscore[player] - prev_zscore[player]
            deltas[player] = delta
    mean = numpy.mean(deltas.values())
    std = numpy.std(deltas.values())
    zdeltas = { player: zscore(deltas[player], mean, std) for player in deltas }
    sorted_zdeltas = sorted(zdeltas.items(), key=operator.itemgetter(1))
    print 'Top'
    pretty_print(sorted_zdeltas[-20:][::-1])
    print 'Bottom'
    pretty_print(sorted_zdeltas[:20])
    return deltas

def construct_lineup(zscores, salaries):
    sorted_zscores = sorted(zscores.items(), key=operator.itemgetter(1))
    #filtered_ownership = [x for x in sorted_ownership if x[1] > 0]
    for player, zscore in sorted_zscores:
        if player in salaries:
            print player, zscore, salaries[player]
    # Contraints:
    # sum(salary) < X, lineup restrictions, maximize salary / ownership

with open('salaries/dk_nba_salaries_2015_11_07.csv') as f:
    csvreader = reader(f, delimiter=',', quotechar='"')
    for i, row in enumerate(csvreader):
        if i != 0:
            dk_salaries[row[1]] = (int(row[2]), row[0])

with open('salaries/fd_nba_salaries_2015_11_04.csv') as f:
    csvreader = reader(f, delimiter=',', quotechar='"')
    for i, row in enumerate(csvreader):
        if i != 0:
            fd_salaries['%s %s' % (row[2], row[3])] = (int(row[6]), row[1])

ownership = load_ownership('ownership/fs_nba_ownership_2015_11_06.tsv')
winpercent = load_winpercent('ownership/fs_nba_ownership_2015_11_06.tsv')
prev_ownership = load_ownership('ownership/fs_nba_ownership_2015_11_05.tsv')
prev_winpercent = load_winpercent('ownership/fs_nba_ownership_2015_11_05.tsv')

print 'Daily'
zscores_d = own_win_diff(ownership['d'], winpercent['d'])
zscores_d_prev = own_win_diff(prev_ownership['d'], prev_winpercent['d'])
print 'Weekly'
zscores_w = own_win_diff(ownership['w'], winpercent['w'])
#print 'Monthly'
#zscore_m = own_win_diff(ownership['m'], winpercent['m'])

print 'Deltas'
zscore_delta(winpercent['d'], prev_winpercent['d'])

construct_lineup(zscores_w, dk_salaries)
