import argparse
from results import get_scores_with_freq
from utils import load_salaries, get_ids

TOTAL_SALARY = 50000
LINEUP_SIZE = 8

def generate(scores, salaries, top=10):
    """
    @param scores [dict]: { [player]: ([score], [freq]) }
    @param salaries [dict]: { [player]: ([salary], [position]) }
    """

    def pfilter(player, pos=None, min_score=0):
        res = True
        if min_score != None:
            res = res and player in scores and scores[player][0] > min_score
        if pos:
            res = res and salaries[player][1] == pos
        return res

    def get_and_print_pos_list(pos, min_score=0):
        pos_list = [(player, scores[player][0], scores[player][1])
                   for player in salaries if pfilter(player, pos, -1)]
        pos_list_sorted = sorted(pos_list, key=lambda x: x[1], reverse=True)
        print ('%ss:\n%s' %
               (pos, '\n'.join('\t%s (%s - %s)' % (player, score, freq)
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


    pg_list = get_and_print_pos_list('PG', min_score=-1)
    sg_list = get_and_print_pos_list('SG', min_score=-1)
    sf_list = get_and_print_pos_list('SF', min_score=-1)
    pf_list = get_and_print_pos_list('PF', min_score=-1)
    c_list = get_and_print_pos_list('C', min_score=-1)
    g_list = pg_list + sg_list
    f_list = sf_list + pf_list
    util_list = pg_list + sg_list + sf_list + pf_list + c_list

    lineups = [] # [([player list], [score], [salary])]

    for pg in pg_list:
        for sg in sg_list:
            for sf in sf_list:
                for pf in pf_list:
                    for c in c_list:
                        for g in g_list:
                            for f in f_list:
                                for util in util_list:
                                    lineup = [pg, sg, sf, pf, c, g, f, util]
                                    salary = get_salary(lineup)
                                    if is_valid_lineup(lineup, salary):
                                        lineups.append((
                                            set(lineup),
                                            lineup_score(lineup),
                                            salary
                                        ))

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
    parser.add_argument('--salaries', type=str)
    args = parser.parse_args()

    if args.salaries:
        scores = get_scores_with_freq(get_ids(limit=7), min_games=3)
        salaries = load_salaries(args.salaries)
        generate(scores, salaries)
    else:
        print 'Unable to run script: requires a --salaries argument'
