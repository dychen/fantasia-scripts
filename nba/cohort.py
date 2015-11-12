import numpy
import matplotlib.pyplot as plt
from utils import load_salaries, load_results

"""
To run (fix for matplotlib in venv):
(venv)$ frameworkpython cohort.py
See: http://matplotlib.org/faq/virtualenv_faq.html
"""

def run(results_file, salaries, start=0, end=-1):
    positions = { 'PG': [], 'SG': [], 'SF': [], 'PF': [], 'C': [], 'F': [],
                  'G': [], 'UTIL': []}
    position_index_map = { 'PG': 0, 'SG': 1, 'SF': 2, 'PF': 3, 'C': 4, 'F': 5,
                           'G': 6, 'UTIL': 7}
    results = load_results(results_file)
    salary_means = {}
    for result in results[start:end]:
        for position in positions.keys():
            positions[position].append(result[position_index_map[position]])
    for position, players in positions.iteritems():
        pos_salaries = [salaries[player][0] for player in players]
        salary_means[position] = numpy.mean(pos_salaries)
    return salary_means

def run_and_plot(intervals, salaries):
    POSITIONS = ['PG', 'SG', 'SF', 'PF', 'C', 'F', 'G', 'UTIL']
    data = []
    for i, end in enumerate(intervals[1:]):
        start = intervals[i]
        print start, end
        data.append(run('results/contest-standings-13876064.csv',
                        salaries, start=start, end=end))
    lines = {}
    for pos in POSITIONS:
        lines[pos], = plt.plot(intervals[1:], [x[pos] for x in data], label=pos)
    plt.legend([lines[pos] for pos in POSITIONS], POSITIONS)
    plt.show()

if __name__=='__main__':
    salaries = load_salaries('salaries/dk_nba_salaries_2015_11_07.csv')
    for salary in sorted(salaries.items(), key=lambda x: x[1][0], reverse=True)[:20]:
        print salary
    run_and_plot(range(0, 1001, 100), salaries)
    run_and_plot(range(0, 10001, 1000), salaries)
    run_and_plot(range(0, 100001, 10000), salaries)
