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

    stats[year] = dict()
    stats[year]['salary_avg'] = dict()
    stats[year]['salary_max'] = dict()
    stats[year]['salary_max_player'] = dict()

    next(fil)
    for row in fil:

        # A player may be considered for more than one position
        if row[3] == 'MF':
            positions = ['M','F']
        else:
            positions = re.split('-|/',row[3])

        for position in positions:

            # If empty cell, continue
            if not row[4] or not row[5] or not position:
                continue

            # Salary from MLS to a player constitutes Salary + Guaranteed Compensation
            base_salary = float(row[4])
            g_compensation = float(row[5])
            player = row[2] + ' ' + row[1]
            pay = int(base_salary + g_compensation)

            # If position not yet in year, add it
            if position in salary_sum[year]:
                salary_sum[year][position] += pay
                counter[year][position] += 1
                if pay > stats[year]['salary_max'][position]:
                    stats[year]['salary_max'][position] = pay
                    stats[year]['salary_max_player'][position] = player
            else:
                salary_sum[year][position] = pay
                stats[year]['salary_max'][position] = pay
                stats[year]['salary_max_player'][position] = player
                counter[year][position] = 1

    print('\nIn {}'.format(year))
    for position in salary_sum[year]:
        stats[year]['salary_avg'][position] = int(salary_sum[year][position] / counter[year][position])
        print('{} makes {} a season'.format(position,stats[year]['salary_avg'][position]))
        print('Highest payed player: {} \nSalary:  {}'.format(stats[year]['salary_max_player'][position],stats[year]['salary_max'][position]))


stats = dict()
salary_sum = dict()
counter = dict()

for fileName in os.listdir('./'):
    if '.csv' in fileName:
        processSalary(fileName)

with open('DataMLH.json', 'w') as outfile:
    json.dump(stats, outfile)
