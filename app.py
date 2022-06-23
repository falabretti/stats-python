import os
import sys
from tables import FrequencyDistributionTable, StatisticsTable

def read_values():
    if len(sys.argv) < 2:
        print('No input file specified!')
        exit()

    file = sys.argv[1]

    if not os.path.isfile(file):
        print('The provided file is invalid!')
        exit()

    with open(file, 'r') as f:
        values = f.readlines()
        values = [float(v.replace('\n', '')) for v in values]

    return values

values = read_values()
print(f'Valores: {values}\n')

statistics_table = StatisticsTable(values)
statistics_table.print()

print()

frequency_distribution_table = FrequencyDistributionTable(values)
frequency_distribution_table.print()

print(f'\nMédia Ponderada: {frequency_distribution_table.weighted_mean:.1f}')

frequency_distribution_table.show_frequency_polygon()
