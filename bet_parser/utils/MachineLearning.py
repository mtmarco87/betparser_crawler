import re

import nltk
from numpy import genfromtxt
from collections import Counter
from math import sqrt
from bet_parser.settings import *
import difflib

teams_path = BOT_PATH + "/libs/ml_data/team_names.csv"
columns = ['source', 'target']
dataset = genfromtxt(teams_path, dtype=str, delimiter=',')
dataset_sources = dataset[:, 0]
dataset_target = dataset[:, 1]


class ML:
    algorithm: str = None

    def __init__(self, algorithm: str = 'cosine'):
        self.algorithm = algorithm

    def get_by_similarity(self, team_name, threshold: int = None):
        result = team_name
        if 'cos' in self.algorithm:
            result = self.cosine_similarity(team_name, threshold)
        elif 'lev' in self.algorithm:
            result = self.levenstein_distance(team_name, threshold)
        elif 'seq' in self.algorithm:
            result = self.sequence_matcher(team_name, threshold)
        return result

    @staticmethod
    def cosine_similarity(team_name: str, threshold: int = None):
        result = team_name
        key = re.sub(r'\s+', ' ', team_name.strip().lower(), flags=re.I)
        if not threshold:
            threshold = 95

        index = -1
        best_results = []
        for word in dataset_sources:
            index += 1
            try:
                res = MLHelpers.cosdis(MLHelpers.word2vec(key), MLHelpers.word2vec(word)) * 100
                if res > threshold:
                    target_word = dataset_target[index]
                    msg = "The cosine similarity between : {} and : {} is: {}. Mapping => {}"
                    print(msg.format(word, key, res, target_word))
                    best_results.append({
                        'Matched': word,
                        'Mapping': target_word,
                        'Score': res
                    })
            except IndexError:
                pass

        if len(best_results) > 0:
            result = sorted(best_results, key=lambda k: k['Score'], reverse=True)[:1][0]
            print("Best result: {}".format(result))
            result = str(result['Mapping'])

        return result

    @staticmethod
    def levenstein_distance(team_name: str, threshold: int = None):
        result = team_name
        key = re.sub(r'\s+', ' ', team_name.strip().lower(), flags=re.I)
        if not threshold:
            threshold = 4

        index = -1
        best_results = []
        for word in dataset_sources:
            index += 1
            res = nltk.edit_distance(key, word)
            if res < threshold:
                target_word = dataset_target[index]
                msg = "The levenstein distance between : {} and : {} is: {}. Mapping => {}"
                print(msg.format(word, key, res, target_word))
                best_results.append({
                    'Matched': word,
                    'Mapping': target_word,
                    'Score': res
                })

        if len(best_results) > 0:
            result = sorted(best_results, key=lambda k: k['Score'])[:1][0]
            print("Best result: {}".format(result))
            result = str(result['Mapping'])

        return result

    @staticmethod
    def sequence_matcher(team_name: str, threshold: int = None):
        result = team_name
        key = re.sub(r'\s+', ' ', team_name.strip().lower(), flags=re.I)
        if not threshold:
            threshold = 85

        index = -1
        best_results = []
        for word in dataset_sources:
            index += 1
            seq = difflib.SequenceMatcher(None, key, word)
            res = seq.ratio() * 100
            if res > threshold:
                target_word = dataset_target[index]
                msg = "The sequence-matcher similarity between : {} and : {} is: {}. Mapping => {}"
                print(msg.format(word, key, res, target_word))
                best_results.append({
                    'Matched': word,
                    'Mapping': target_word,
                    'Score': res
                })

        if len(best_results) > 0:
            result = sorted(best_results, key=lambda k: k['Score'])[:1][0]
            print("Best result: {}".format(result))
            result = str(result['Mapping'])

        return result


class MLHelpers:
    @staticmethod
    def word2vec(word):
        # count the characters in word
        cw = Counter(word)
        # precomputes a set of the different characters
        sw = set(cw)
        # precomputes the "length" of the word vector
        lw = sqrt(sum(c * c for c in cw.values()))

        # return a tuple
        return cw, sw, lw

    @staticmethod
    def cosdis(v1, v2):
        # which characters are common to the two words?
        common = v1[1].intersection(v2[1])
        # by definition of cosine distance we have
        return sum(v1[0][ch] * v2[0][ch] for ch in common) / v1[2] / v2[2]
