import numbers
import statistics
from math import log, ceil
from tabulate import tabulate

class Table:
    def print(self):
        raise NotImplementedError("Method print() not implemented.")

    def format_number(self, value):
        if isinstance(value, numbers.Number):
            return f'{value:.1f}'
        else:
            return value

    def format_numbers(self, values):
        return [self.format_number(value) for value in values]


class StatisticsTable(Table):

    def __init__(self, values = list[float]) -> None:
        self.values = values
        self.arithmetic_mean = None
        self.geometric_mean = None
        self.mode = None
        self.median = None
        self.sample_stdev = None
        self.sample_variance = None

        self.__calc_statistics()

    def print(self):

        statistics = [
            'Média Aritmética',
            'Média Geométrica',
            'Moda',
            'Mediana',
            'Desvio Padrão da Amostra',
            'Variância da Amostra'
        ]

        values = [
            self.arithmetic_mean,
            self.geometric_mean,
            self.mode,
            self.median,
            self.sample_stdev,
            self.sample_variance
        ]

        table_data = {
            'Estatística': statistics,
            'Valor': self.format_numbers(values)
        }

        print('Tabela de Estatísticas')
        print(tabulate(table_data, headers='keys', tablefmt='fancy_grid',
                        colalign=['left', 'right'],
                        floatfmt='.1f'))

    def __calc_mode(self):
        multimodes = statistics.multimode(self.values)

        if len(multimodes) == 1 and len(self.values) > 1:
            return multimodes[0]
        elif len(multimodes) == len(self.values):
            return 'Amodal'
        else:
            return 'Multimodal'

    def __calc_statistics(self):
        self.arithmetic_mean = statistics.mean(self.values)
        self.geometric_mean = statistics.geometric_mean(self.values)
        self.mode = self.__calc_mode()
        self.median = statistics.median(self.values)
        self.sample_stdev = statistics.stdev(self.values)
        self.sample_variance = statistics.variance(self.values)


class FrequencyDistributionTable(Table):

    def __init__(self, values: list[float]) -> None:
        self.values = values
        self.ranges = None
        self.range_pairs = None
        self.labels = None
        self.frequencies = None
        self.medians = None
        self.freq_acc = None
        self.freq_percent = None
        self.freq_percent_acc = None

        self.__calc_table_data()
    
    def print(self):

        table_data = {
            'Valores': self.labels + ['Total'],
            'Fi': self.frequencies + [sum(self.frequencies)],
            'xi': self.format_numbers(self.medians + ['-']),
            'Fac': self.freq_acc + ['-'],
            'Fi (%)': self.format_numbers(self.freq_percent + [sum(self.freq_percent)]),
            'FacR (%)': self.format_numbers(self.freq_percent_acc + ['-'])
        }

        print('Tabela de Distribuição de Frequências')
        print(tabulate(table_data, headers='keys', tablefmt='fancy_grid',
                        colalign=('left',) + ('right',) * 5,
                        floatfmt='.1f'))

    def __calc_ranges(self):
        min_value = min(self.values)
        max_value = max(self.values)

        r = max_value - min_value
        k = 1 + 3.22 * log(len(self.values), 10)
        h = ceil(r / k)

        ranges = []
        bound = min_value

        while True:    
            ranges.append(bound)
            if bound > max_value:
                break
            bound += h

        range_pairs = []
        for idx in range(len(ranges) - 1):
            range_pairs.append([ranges[idx], ranges[idx + 1]])

        self.ranges = ranges
        self.range_pairs = range_pairs

        self.labels = [f'{pair[0]} ├ {pair[1]}' for pair in self.range_pairs]

    def __calc_frequencies(self):
        frequencies = []
        current_count = 0

        for range in self.range_pairs:
            for value in self.values:
                if range[0] <= value and value < range[1]:
                    current_count += 1
            frequencies.append(current_count)
            current_count = 0

        self.frequencies = frequencies

    def __calc_medians(self):
        medians = []

        for range in self.range_pairs:
            median = (range[0] + range[1]) / 2
            medians.append(median)

        self.medians = medians

    def __calc_freq_acc(self):
        freq_acc = []
        freq_acc.append(self.frequencies[0])

        for idx in range(1, len(self.frequencies)):
            acc = self.frequencies[idx] + freq_acc[idx - 1]
            freq_acc.append(acc)

        self.freq_acc = freq_acc

    def __calc_freq_percent(self):
        self.freq_percent = [freq / sum(self.frequencies) * 100.
                                for freq in self.frequencies]

    def __calc_freq_percent_acc(self):
        freq_percent_acc = []
        freq_percent_acc.append(self.freq_percent[0])

        for idx in range(1, len(self.freq_percent)):
            acc = self.freq_percent[idx] + freq_percent_acc[idx - 1]
            freq_percent_acc.append(acc)

        self.freq_percent_acc = freq_percent_acc

    def __calc_table_data(self):
        self.__calc_ranges()
        self.__calc_frequencies()
        self.__calc_medians()
        self.__calc_freq_acc()
        self.__calc_freq_percent()
        self.__calc_freq_percent_acc()
        