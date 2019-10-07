from numpy.core.multiarray import ndarray
import nltk
from collections import Counter
from math import sqrt
import difflib
import re


class MLHelpers:
    @staticmethod
    def cosine_similarity(key: str, word: str):
        return MLHelpers.cosdis(MLHelpers.word2vec(key), MLHelpers.word2vec(word)) * 100

    @staticmethod
    def levenstein_distance(key: str, word: str):
        return nltk.edit_distance(key, word)

    @staticmethod
    def sequence_matcher(key: str, word: str):
        seq = difflib.SequenceMatcher(None, key, word)
        return seq.ratio() * 100

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


class WordSimilarityML:
    """
    Word Similarity Machine Learning engine

    Parameters:
    @Source Dataset: that will be used to match words by similarity
    @Target Dataset: that will provide a mapping for every matched word
    @Algorithm: that specifies the ML algorithm that will be used to evaluate word similarity (cos, lev, seq)
    @Validation Dataset (var):  the engine adds to it the not recognized words
    """
    algorithm = None
    algorithm_fullname: str = None
    algorithm_treshold: int = None
    algorithm_maximize: bool = None
    algorithms: dict = {
        'cos': ['cosine similarity', True, 95, MLHelpers.cosine_similarity],
        'lev': ['levenstein distance', False, 4, MLHelpers.levenstein_distance],
        'seq': ['sequence matcher', True, 95, MLHelpers.sequence_matcher]
    }
    dataset_source: ndarray = None
    dataset_target: ndarray = None
    sanitize_array: list = None

    def __init__(self, dataset_source: ndarray = None, dataset_target: ndarray = None,
                 algorithm: str = 'seq', sanitize_array: list = None):
        if algorithm not in self.algorithms.keys():
            raise Exception('Error: Unknown ML algorithm requested')
        if dataset_source is None or dataset_target is None:
            raise Exception('Error: No dataset provided to the ML algorithm')
        self.algorithm_fullname = self.algorithms[algorithm][0]
        self.algorithm_maximize = self.algorithms[algorithm][1]
        self.algorithm_treshold = self.algorithms[algorithm][2]
        self.algorithm = self.algorithms[algorithm][3]

        self.dataset_source = dataset_source
        self.dataset_target = dataset_target
        self.sanitize_array = sanitize_array

    def get(self, key: str, threshold: int = None):
        key = self.sanitize(key, self.sanitize_array)
        result = MLSimilarityResult(key)
        if not threshold:
            threshold = self.algorithm_treshold

        print("ML ==> testing '{}'".format(key))

        index = -1
        found = []
        for word in self.dataset_source:
            index += 1
            try:
                score: float = self.algorithm(key, word)
                if (self.algorithm_maximize and score > threshold) \
                        or (not self.algorithm_maximize and score < threshold):
                    target_word = self.dataset_target[index]
                    print("The {} between : {} and {} ({}) is: {}"
                          .format(self.algorithm_fullname, key, word, target_word, score))
                    found.append(MLSimilarityResult(key, word, target_word, score))
            except IndexError:
                pass

        if len(found) > 0:
            # If at least one word with an high similarity has been found, takes the best one
            result = sorted(found, key=lambda k: k.score, reverse=self.algorithm_maximize)[0]
            print("Best result: {}".format(result))

        return result

    @staticmethod
    def sanitize(key, sanitize_array: list = None):
        # Sanitizing the input word for better comparison:

        # Remove all the special characters
        key = re.sub(r'\W', ' ', key)
        # Transform the string lower case, so that next rules can apply correctly
        key = key.lower()
        # Applies custom sanitation rules (removes all the isolated occurrences of these words)
        if sanitize_array:
            for s in sanitize_array:
                key = re.sub(r'((?<!\w)' + s + r'(?!\w))', '', key, flags=re.I)
        # Substitute multiple spaces with single space
        key = re.sub(r'\s+', ' ', key, flags=re.I)

        # Finally we trim and return
        return key.strip()


class MLSimilarityResult:
    key_word: str
    matched_word: str
    mapped_word: str
    score: float

    def __init__(self, key_word: str = None, matched_word: str = None, mapped_word: str = None, score: float = 0):
        self.key_word = key_word
        self.matched_word = matched_word
        self.mapped_word = mapped_word
        self.score = score

    def __str__(self):
        return "[ Key Word: {}, Matched Word: {}, Mapped Word: {}, Score: {} ]".format(self.key_word, self.matched_word,
                                                                                       self.mapped_word, self.score)
