import csv
import re
import os

def processSalary(fileName):

    # Load csv
    fl = open(fileName, 'r')
    fil = csv.reader(fl, delimiter=',')

    # Save the year for dicts
    year = fileName[-8:-4]
    salary_sum[year] = dict()
    salary_avg[year] = dict()
    counter[year] = dict()

    next(fil)
    for row in fil:

        # A player may be considered for more than one position
        positions = re.split('-|/',row[3])
        for position in positions:

            # If empty cell, continue
            if not row[4] or not row[5] or not position:
                continue

            # Salary from MLS to a player constitutes Salary + Guaranteed Compensation
            base_salary = float(row[4])
            g_compensation = float(row[5])
            pay = base_salary + g_compensation
            if position in salary_sum[year]:
                salary_sum[year][position] += pay
                counter[year][position] += 1
            else:
                salary_sum[year][position] = pay
                counter[year][position] = 1

    print('In {}'.format(year))
    for position in salary_sum[year]:
        salary_avg[year][position] = int(salary_sum[year][position] / counter[year][position])
        print('{} makes {} a season'.format(position,salary_avg[year][position]))


salary_sum = dict()
salary_avg = dict()
counter = dict()

for fileName in os.listdir('./'):
    if '.csv' in fileName:
        processSalary(fileName)
