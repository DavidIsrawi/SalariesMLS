import csv
import re
import os
import json

def processSalary(fileName):

    # Load csv
    fl = open(fileName, 'r')
    fil = csv.reader(fl, delimiter=',')

    # Save the year for dicts
    year = fileName[-8:-4]

    # Make a dictionary of positions per year
    salary_sum[year] = dict()
    counter[year] = dict()

    stats['overall'][year] = dict()
    stats['overall'][year]['salary_avg'] = dict()
    stats['overall'][year]['salary_max'] = dict()
    stats['overall'][year]['salary_max_player'] = dict()

    stats['teams'][year] = dict()

    next(fil)
    for row in fil:

        # A player may be considered for more than one position
        if row[3] == 'MF':
            positions = ['M','F']
        else:
            positions = re.split('-|/',row[3])

        # Data from CSV
        team = row[0]
        player = row[2] + ' ' + row[1]

        if not team:
            continue

        if team not in stats['teams'][year]:
            stats['teams'][year][team] = dict()
            stats['teams'][year][team]['salary_avg'] = dict()
            stats['teams'][year][team]['budget'] = 0
            stats['teams'][year][team]['salary_max_player'] = ''
            stats['teams'][year][team]['salary_max'] = 0

        if team not in salary_sum[year]:
            salary_sum[year][team] = dict();
            counter[year][team] = dict()

        if not row[4] or not row[5]:
            continue

        # Salary from MLS to a player constitutes Salary + Guaranteed Compensation
        base_salary = float(row[4])
        g_compensation = float(row[5])
        pay = int(base_salary + g_compensation)

        # Budget per team per year
        stats['teams'][year][team]['budget'] += pay

        # Salary max per team per year
        if pay > stats['teams'][year][team]['salary_max']:
            stats['teams'][year][team]['salary_max_player'] = player
            stats['teams'][year][team]['salary_max'] = pay
            stats['teams'][year][team]['salary_max_position'] = row[3]

        for position in positions:

            # If empty cell, continue
            if not position:
                continue

            # If position not yet in year->team, add it
            if position in salary_sum[year][team]:
                salary_sum[year][team][position] += pay
                counter[year][team][position] += 1
            else:
                salary_sum[year][team][position] = pay
                counter[year][team][position] = 1

            if position in stats['overall'][year]['salary_max']:
                if pay > stats['overall'][year]['salary_max'][position]:
                    stats['overall'][year]['salary_max'][position] = pay
                    stats['overall'][year]['salary_max_player'][position] = player
            else:
                stats['overall'][year]['salary_max'][position] = pay
                stats['overall'][year]['salary_max_player'][position] = player


    print('\nIn {}'.format(year))
    # for position in salary_sum[year]:
    #     stats['overall'][year]['salary_avg'][position] = int(salary_sum[year][position] / counter[year][position])
    #
    #     print('{} makes {} a season'.format(position,stats['overall'][year]['salary_avg'][position]))
    #     print('Highest payed player: {} \nSalary:  {}'.format(stats['overall'][year]['salary_max_player'][position],stats['overall'][year]['salary_max'][position]))

    salary_sum_overall = dict()
    counter_sum_overall = dict()

    for team in salary_sum[year]:
        for position in salary_sum[year][team]:
            stats['teams'][year][team]['salary_avg'][position] = int(salary_sum[year][team][position] / counter[year][team][position])

            if position not in salary_sum_overall:
                salary_sum_overall[position] = salary_sum[year][team][position]
                counter_sum_overall[position] = counter[year][team][position]
            else:
                salary_sum_overall[position] += salary_sum[year][team][position]
                counter_sum_overall[position] += counter[year][team][position]

    for position in stats['overall'][year]['salary_max']:
        stats['overall'][year]['salary_avg'][position] = int(salary_sum_overall[position] / counter_sum_overall[position])
        print('{} makes {} a season'.format(position,stats['overall'][year]['salary_avg'][position]))
        print('Highest payed player: {} \nSalary:  {}'.format(stats['overall'][year]['salary_max_player'][position],stats['overall'][year]['salary_max'][position]))

stats = dict()
stats['overall'] = dict()
stats['teams'] = dict()
salary_sum = dict()
counter = dict()

for fileName in os.listdir('./'):
    if '.csv' in fileName:
        processSalary(fileName)

with open('DataMLS.json', 'w') as outfile:
    json.dump(stats, outfile)
