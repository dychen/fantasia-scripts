import math
from csv import reader
import numpy
from utils import get_weighted_score, load_salaries, load_results

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

def run_weighted():
    salaries = load_salaries('salaries/dk_nba_salaries_2015_11_13.csv')
    # sum(log(dollars_per_player_i) / N for i in N)
    scores_weighted_all = {}
    ids = ['13772929', '13876064', '13986906', '14116266', '14199909',
           '14306948', '14407111']
    for i, contest_id in enumerate(ids):
        results = load_results('results/contest-standings-%s.csv' % contest_id)
        numentries = len(results)
        scores_weighted = analyze_results(
            results,
            lambda x: sum([get_weighted_score(y, numentries) for y in x])
                      / float(len(x))
        )
        for player, score in scores_weighted.iteritems():
            if player in scores_weighted_all:
                scores_weighted_all[player].append(score)
            else:
                scores_weighted_all[player] = [score]
    for player, scores in scores_weighted_all.iteritems():
        scores_weighted_all[player] = (
            #numpy.mean([math.log(abs(s)) * numpy.sign(s) for s in scores]),
            numpy.mean(scores),
            len(scores)
        )
    sorted_scores = sorted(scores_weighted_all.items(), key=lambda x: x[1],
                           reverse=True)
    for player, score in sorted_scores:
        if player in salaries:
            print ('\t%s\t%.4f\t%d\t%s' % (player[:15], score[0], score[1],
                                           salaries[player]))
        else:
            print '\t%s\t%.4f\t%d' % (player[:15], score[0], score[1])

def run():
    salaries = load_salaries('salaries/dk_nba_salaries_2015_11_07.csv')
    results = load_results('results/contest-standings-13876064.csv')
    numentries = len(results)
    scores_mean = analyze_results(
        results, lambda x: numpy.mean(x) / len(results)
    )
    scores_own = analyze_results(
        results, lambda x: len(x) / float(len(results))
    )
    scores_weighted = analyze_results(
        results,
        lambda x: sum([get_weighted_score(y, numentries) for y in x])
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

run_weighted()
