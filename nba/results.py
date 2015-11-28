import argparse
import math
from csv import reader
import numpy
from utils import get_prize_map, get_weighted_score, load_salaries,\
    load_results, get_ids

def analyze_results(results, f):
    scores = {}
    scores_aggregate = {}
    for i, row in enumerate(results):
        for player in row:
            if player in scores:
                scores[player].append(i)
            else:
                scores[player] = [i]
    for player, scorelist in scores.iteritems():
        if len(scorelist) * 5000 > float(len(results)): # > 0.5%
            scores_aggregate[player] = f(scorelist)
    return scores_aggregate

def get_weighted_scores(ids):
    # sum(log(dollars_per_player_i) / N for i in N)
    scores_weighted_all = {}
    mean = numpy.mean([i for i, _ in enumerate(ids)])
    for i, contest_id in enumerate(ids):
        results = load_results('results/contest-standings-%s.csv' % contest_id)
        numentries = len(results)
        prize_map = get_prize_map(numentries)
        print contest_id, numentries
        # Weights: [0, ..., 2]
        weight = 1 # i / mean
        scores_weighted = analyze_results(
            results,
            lambda x: sum([get_weighted_score(y, prize_map) for y in x])
                      / float(len(x)) * weight
        )
        for player, score in scores_weighted.iteritems():
            if player in scores_weighted_all:
                scores_weighted_all[player].append(score)
            else:
                scores_weighted_all[player] = [score]
    for player, scores in scores_weighted_all.iteritems():
        scores_weighted_all[player] = (
            numpy.median(scores),
            #numpy.mean(scores),
            len(scores)
        )
    # Return { player: (score, num data) }
    return scores_weighted_all

def run_weighted(ids, filename, verbose=False):
    print "Calculated weighted scores..."
    salaries = load_salaries(filename)
    weighted_scores = get_weighted_scores(ids)
    sorted_scores = sorted(weighted_scores.items(), key=lambda x: x[1],
                           reverse=True)
    for player, score in sorted_scores:
        if player in salaries:
            print ('\t%s\t%.4f\t%d\t%s' % (player[:15], score[0], score[1],
                                           salaries[player]))
        elif verbose:
            print '\t%s\t%.4f\t%d' % (player[:15], score[0], score[1])

def run_deltas(curr_ids, prev_ids, filename, verbose=False):
    print "Calculating deltas..."
    scores_curr = get_weighted_scores(curr_ids)
    scores_prev = get_weighted_scores(prev_ids)
    deltas = {}
    for player in scores_curr:
        if player in scores_curr and player in scores_prev:
            deltas[player] = (scores_curr[player][0] - scores_prev[player][0],
                              scores_curr[player][1])
    salaries = load_salaries(filename)
    sorted_deltas = sorted(deltas.items(), key=lambda x: x[1], reverse=True)
    for player, delta in sorted_deltas:
        if delta[0] > 0:
            if player in salaries:
                print ('\t%s\t%.4f\t%d\t%s' % (player[:15], delta[0], delta[1],
                                               salaries[player]))
            elif verbose:
                print '\t%s\t%.4f\t%d' % (player[:15], delta[0], delta[1])
    return deltas

def run():
    salaries = load_salaries('salaries/dk_nba_salaries_2015_11_07.csv')
    results = load_results('results/contest-standings-13876064.csv')
    numentries = len(results)
    prize_map = get_prize_map(numentries)
    scores_mean = analyze_results(
        results, lambda x: numpy.mean(x) / len(results)
    )
    scores_own = analyze_results(
        results, lambda x: len(x) / float(len(results))
    )
    scores_weighted = analyze_results(
        results,
        lambda x: sum([get_weighted_score(y, prize_map) for y in x])
                  / float(len(x))
    )
    sorted_mean = sorted(scores_mean.items(), key=lambda x: x[1],
                         reverse=False)
    sorted_own = sorted(scores_own.items(), key=lambda x: x[1], reverse=True)
    sorted_weighted = sorted(scores_weighted.items(), key=lambda x: x[1],
                             reverse=True)

    print 'Sorted by score:'
    print '\tPlayer\t\tScore\tOwn\tWeighted'
    for player, score in sorted_mean[:30]:
        if player in salaries:
            print ('\t%s\t%.4f\t%.2f\t%.4f\t%s'
                   % (player[:15], score, scores_own[player] * 100,
                      scores_weighted[player], salaries[player]))
        else:
            print ('\t%s\t%.4f\t%.2f\t%.4f'
                   % (player[:15], score, scores_own[player] * 100,
                      scores_weighted[player]))

    print 'Sorted by ownership:'
    print '\tPlayer\t\tScore\tOwn\tWeighted'
    for player, own in sorted_own[:30]:
        if player in salaries:
            print ('\t%s\t%.4f\t%.2f\t%.4f\t%s'
                   % (player[:15], scores_mean[player], own * 100,
                      scores_weighted[player], salaries[player]))
        else:
            print ('\t%s\t%.4f\t%.2f\t%.4f'
                   % (player[:15], scores_mean[player], own * 100,
                      scores_weighted[player]))

    print 'Sorted by weighted score:'
    print '\tPlayer\t\tScore\tOwn\tWeighted'
    for player, weighted_score in sorted_weighted[:50]:
        if player in salaries:
            print ('\t%s\t%.4f\t%.2f\t%.4f\t%s'
                   % (player[:15], scores_mean[player],
                      scores_own[player] * 100, weighted_score,
                      salaries[player]))
        else:
            print ('\t%s\t%.4f\t%.2f\t%.4f'
                   % (player[:15], scores_mean[player],
                      scores_own[player] * 100, weighted_score))

"""
Public API
"""

def get_scores(ids):
    return {
        player: score_tup[0]
        for player, score_tup in get_weighted_scores(ids).iteritems()
    }


if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--weighted', action='store_const', const=True)
    parser.add_argument('--deltas', action='store_const', const=True)
    parser.add_argument('--limit', type=int)
    parser.add_argument('--salaries', type=str)
    parser.add_argument('--verbose', action='store_const', const=True)
    args = parser.parse_args()

    ids = get_ids(args.limit) if args.limit else get_ids()
    print 'Computing results with contests: %s' % ', '.join(ids)

    if args.weighted:
        if args.limit:
            run_weighted(ids[-args.limit:], args.salaries, args.verbose)
        else:
            run_weighted(ids, args.salaries, args.verbose)
    if args.deltas:
        limit = args.limit if args.limit else 7
        run_deltas(ids[-limit+2:], ids[-limit:-2], args.salaries, args.verbose)
