import argparse
from results import get_scores_with_freq
from utils import load_salaries, get_ids

TOTAL_SALARY = 50000
LINEUP_SIZE = 8
POSITIONS = ['PG', 'SG', 'SF', 'PF', 'C']

def generate(scores, salaries, top=10, prefill_players=[], ignore_players=[],
             min_score=-1.5):
    """
    Strategy:
        1. Get all players for each position that satisfy some constraints
           (score > X)
        2. Prefill positions with @prefill_players and remove players in
           @ignore_players from
        3. Iterate through all combinations of positions, constructing lineups
        4. Print top @top unique lineups by score

    @param scores [dict]: { [player]: ([score], [freq]) }
    @param salaries [dict]: { [player]: ([salary], [position]) }
    @param top [int]: Top X lineups to show
    @param prefill_players [list]: Players to include in the lineup
    @param ignore_players [list]: Players to ignore when making the lineup
    @param min_score [int]: Limits the number of player scores to consider
    """

    def prefill(players):
        return {
            pos: [player for player in players if pfilter(player, pos, -10000)]
            for pos in ['PG', 'SG', 'SF', 'PF', 'C']
        }

    def pfilter(player, pos=None, min_score=-10000):
        res = True
        if min_score != None:
            res = res and player in scores and scores[player][0] > min_score
        if pos:
            res = res and salaries[player][1] == pos
        if ignore_players:
            res = res and player not in ignore_players
        return res

    def get_and_print_pos_list(pos, min_score=0):
        pos_list = [(player, scores[player][0], scores[player][1])
                    for player in salaries if pfilter(player, pos, min_score)]
        pos_list_sorted = sorted(pos_list, key=lambda x: x[1], reverse=True)
        print ('%ss:\n%s' %
               (pos, '\n'.join('\t%s (%s, %s games)' % (player, score, freq)
                               for (player, score, freq) in pos_list_sorted)))
        return [x[0] for x in pos_list]

    def get_salary(lineup):
        return sum([salaries[player][0] for player in lineup])

    def is_valid_lineup(lineup, salary):
        return (salary < TOTAL_SALARY
                and salary >= TOTAL_SALARY - 200
                and len(set(lineup)) == LINEUP_SIZE)

    def lineup_score(lineup):
        return sum([scores[player][0] for player in lineup])

    def filter_unique_lineups(lineups):
        lineups_dict = {}
        for lineup in lineups:
            key = ','.join(sorted(lineup[0]))
            if key not in lineups_dict:
                lineups_dict[key] = lineup
        return lineups_dict.values()

    pos_lists = { 'PG': [], 'SG': [], 'SF': [], 'SG': [], 'C': [], 'G': [],
                  'F': [], 'UTIL': [] }
    lineups = [] # [([player list], [score], [salary])]
    print '+----+'
    print '|Data|'
    print '+----+'

    # 1. Get list of all eligible players for each position
    prefill_dict = prefill(prefill_players)

    for pos in POSITIONS:
        pos_lists[pos] = get_and_print_pos_list(pos, min_score=min_score)
    pos_lists['G'] = pos_lists['PG'] + pos_lists['SG']
    pos_lists['F'] = pos_lists['SF'] + pos_lists['PF']
    pos_lists['UTIL'] = pos_lists['G'] + pos_lists['F']
    # Overwrite lists with prefill - do this after the initial setup so you
    # don't overwrite the flex positions (G, F, UTIL)
    for pos in POSITIONS:
        if prefill_dict[pos]:
            pos_lists[pos] = prefill_dict[pos]

    print 'Prefilled players:'
    for player in prefill_players:
        if player in scores:
            print ('\t%s (%s, %s) (%s, %s games)' %
                   (player, salaries[player][1], salaries[player][0],
                    scores[player][0], scores[player][1]))
        else:
            print ('\t%s (%s, %s) (Not enough games played)' %
                   (player, salaries[player][1], salaries[player][0]))

    print 'Ignored players:'
    for player in ignore_players:
        if player in scores:
            print ('\t%s (%s, %s) (%s, %s games)' %
                   (player, salaries[player][1], salaries[player][0],
                    scores[player][0], scores[player][1]))
        else:
            print ('\t%s (%s, %s) (Not enough games played)' %
                   (player, salaries[player][1], salaries[player][0]))

    # 2. Find all eligible lineups
    for pg in pos_lists['PG']:
        for sg in pos_lists['SG']:
            for sf in pos_lists['SF']:
                for pf in pos_lists['PF']:
                    for c in pos_lists['C']:
                        for g in pos_lists['G']:
                            for f in pos_lists['F']:
                                for util in pos_lists['UTIL']:
                                    lineup = [pg, sg, sf, pf, c, g, f, util]
                                    salary = get_salary(lineup)
                                    if is_valid_lineup(lineup, salary):
                                        lineups.append((
                                            set(lineup),
                                            lineup_score(lineup),
                                            salary
                                        ))

    # 3. Get unique lineups and print results
    print '+-------+'
    print '|Lineups|'
    print '+-------+'
    filtered = filter_unique_lineups(lineups)
    for lineup in sorted(filtered, key=lambda x: x[1], reverse=True)[:top]:
        players, score, salary = lineup
        player_strs = ['%s (%s)' % (player, salaries[player][1])
                       for player in sorted(players)]
        print '%s %s' % (score, salary)
        print '\t%s' % (', '.join(player_strs[:4]))
        print '\t%s' % (', '.join(player_strs[-4:]))

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--salaries', type=str)
    parser.add_argument('-p', '--prefill', type=str,
                        help=('Quoted list of comma-separated player names'
                              ' (e.g. "Stephen Curry, James Harden")'))
    parser.add_argument('-i', '--ignore', type=str,
                        help=('Quoted list of comma-separated player names'
                              ' (e.g. "Stephen Curry, James Harden")'))
    parser.add_argument('-m', '--min_score', type=float)
    args = parser.parse_args()

    if args.salaries:
        print 'Loading score data...'
        scores = get_scores_with_freq(get_ids(limit=7), min_games=3)
        salaries = load_salaries(args.salaries)
        prefill_players = ([x.strip() for x in args.prefill.split(',')]
                           if args.prefill else [])
        ignore_players = ([x.strip() for x in args.ignore.split(',')]
                          if args.ignore else [])
        min_score = args.min_score if args.min_score != None else -1
        generate(scores, salaries, prefill_players=prefill_players,
                 ignore_players=ignore_players, min_score=min_score)
    else:
        print 'Unable to run script: requires a --salaries argument'
