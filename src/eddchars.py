# coding: utf-8

'''
Created on 2017/02/04

@author: rindybell
'''

import numpy as np
import itertools
import sys


class EddChars (object):
    '''
    classdocs
    '''

    def __init__(self, sub_cost=1, ins_cost=1, del_cost=1):
        '''
        Constructor
        '''

        self.del_cost = del_cost
        self.sub_cost = sub_cost
        self.ins_cost = ins_cost

    @staticmethod
    def toutf8(x):
        if isinstance(x, str):
            return x.decode("utf-8", "ignore")
        elif isinstance(x, unicode):
            return x
        else:
            sys.stderr.write("")

    def calc_cost_matrix(self, x, y):
        x_utf8, y_utf8 = self.toutf8(x), self.toutf8(y)
        x_len, y_len = len(x_utf8), len(y_utf8)
        cost_matrix = np.zeros((x_len + 1, y_len + 1))

        # init matrix
        for i1 in xrange(x_len + 1):
            cost_matrix[i1, 0] = i1

        for i2 in xrange(y_len + 1):
            cost_matrix[0, i2] = i2

        for (i1, i2) in itertools.product(xrange(1, x_len + 1),
                                          xrange(1, y_len + 1)):
            if x_utf8[i1 - 1] == y_utf8[i2 - 1]:
                current_sub_cost = 0
            else:
                current_sub_cost = self.sub_cost

            cost_list = [cost_matrix[i1 - 1, i2] + self.ins_cost,
                         cost_matrix[i1, i2 - 1] + self.del_cost,
                         cost_matrix[i1 - 1, i2 - 1] + current_sub_cost]

            cost_matrix[i1, i2] = min(cost_list)

        return cost_matrix

    def trace(self, cost_matrix):
        (max_i1, max_i2) = cost_matrix.shape

        def trace_sub(i1, i2, stacked_item_list):
            assert i1 < max_i1 and i2 < max_i2

            if (i1, i2) == (max_i1 - 1, max_i2 - 1):
                return stacked_item_list
            else:
                key_list = [
                    (i1 + 1, i2, 2), (i1, i2 + 1, 1), (i1 + 1, i2 + 1, 0)]
                key_list = filter(
                    lambda x: x[0] < max_i1 and x[1] < max_i2, key_list)
                cost_list = map(lambda x:
                                (cost_matrix[x[0], x[1]], x[0], x[1], x[2]),
                                key_list)
                sorted_list = sorted(cost_list, key=lambda x: (x[0], x[3]))
                next_i1, next_i2 = sorted_list[0][1], sorted_list[0][2]
                return trace_sub(next_i1, next_i2,
                                 stacked_item_list + [sorted_list[0]])

        return trace_sub(0, 0, [])

    def concatenate_subchars(self, traced_items, word_index, x):
        x_utf8 = self.toutf8(x)
        current_char = u""
        stacked_seq = []
        last_item = (-1, -1, -1 - 1)
        for traced_item in traced_items:
            if last_item[word_index] == traced_item[word_index]:
                continue
            if traced_item[3] == 0:
                stacked_seq.append(current_char)
                current_char = x_utf8[traced_item[word_index] - 1]
            else:
                current_char += x_utf8[traced_item[word_index] - 1]

            last_item = traced_item

        stacked_seq.append(current_char)
        return stacked_seq[1:]

    def aligned_subchars(self, x, y):
        cost_matrix = self.calc_cost_matrix(x, y)
        x_chars = self.concatenate_subchars(self.trace(cost_matrix), 1, x)
        y_chars = self.concatenate_subchars(self.trace(cost_matrix), 2, y)

        return zip(x_chars, y_chars)

    def distance(self, x, y):
        cost_matrix = self.calc_cost_matrix(x, y)
        return cost_matrix[-1, -1]


def main():
    levs = EddChars(sub_cost=2.0)
    print levs.calc_cost_matrix("played", "play")
    print levs.aligned_subchars("played", "play")
    print levs.calc_cost_matrix("studied", "study")
    print levs.trace(levs.calc_cost_matrix("studied", "study"))
    print levs.aligned_subchars("studied", "study")
    print levs.trace(levs.calc_cost_matrix("ジョナサン", "ジョンソン"))
    print levs.aligned_subchars("ジョナサンズ", "ジョンソン")
    print levs.calc_cost_matrix("baa", "baaaaa")
    print levs.distance("baa", "baaaaaa")
    print levs.aligned_subchars("baa", "baaaiaa")

main()
