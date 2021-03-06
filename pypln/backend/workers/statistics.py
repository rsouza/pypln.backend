# coding: utf-8
#
# Copyright 2012 NAMD-EMAP-FGV
#
# This file is part of PyPLN. You can get more information at: http://pypln.org/.
#
# PyPLN is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PyPLN is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with PyPLN.  If not, see <http://www.gnu.org/licenses/>.

from collections import Counter

from pypelinin import Worker


def _get_momenta(distribution):
    total, momentum_1, momentum_2, momentum_3, momentum_4 = 0, 0, 0, 0, 0
    for x, y in distribution:
        momentum_1 += y * x
        momentum_2 += y * x * x
        momentum_3 += y * x * x * x
        momentum_4 += y * x * x * x * x
        total += y
    total = float(total)
    return (momentum_1 / total, momentum_2 / total, momentum_3 / total,
            momentum_4 / total)

def _histogram(freqdist):
    counter = Counter()
    for x, y in freqdist:
        counter[y] += 1
    return sorted(counter.most_common())

class Statistics(Worker):
    requires = ['freqdist', 'sentences']

    def process(self, document):
        freqdist = document['freqdist'] # eg: [('word', 100), ('other', 97)]
        sentences = document['sentences'] # eg: [['1st', 'sentence.'], ['2nd!']]
        momenta = _get_momenta(_histogram(freqdist))
        total_tokens = float(sum(dict(freqdist).values()))
        repertoire = len(freqdist) / total_tokens
        sentence_repertoire_sum = 0
        for sentence in sentences:
            sentence_repertoire_sum += len(set(sentence)) / float(len(sentence))
        number_of_sentences = len(sentences)
        average_sentence_length = total_tokens / number_of_sentences
        sentence_repertoire = sentence_repertoire_sum / number_of_sentences
        return {'momentum_1': momenta[0], 'momentum_2': momenta[1],
                'momentum_3': momenta[2], 'momentum_4': momenta[3],
                'repertoire': repertoire,
                'average_sentence_length': average_sentence_length,
                'average_sentence_repertoire': sentence_repertoire}
