from heapq import heapify, heappush, heappop, heappushpop
from nltk.stem.lancaster import LancasterStemmer as LS
from nltk.stem.wordnet import WordNetLemmatizer as WNL
import os
import re
import sys


class TypoPolice:

    dict = set()
    # Mininum length of word to check typo
    min_len = 3
    # Minimum length of combination word 
    min_combi_len = 8
    # Maximum edit distance length of suggestion
    suggestion_dist = 2
    # Heap size for suggestion
    heap_size = 5

    def __init__(self):
        self.wnl = WNL()
        self.ls = LS()

    def load_dict(self, path):
        if os.path.isfile(path):
            self.load_file(path)
        elif os.path.isdir(path):
            for item in os.listdir(path):
                self.load_dict(os.path.join(path, item))

    def load_file(self, path):
        with open(path) as file:
            line = file.read()
            line = line.strip()
            words = re.split(ptn_space, line)
            for word in words:
                if word != '':
                    self.dict.add(word.lower())
        file.close()

    def is_ok(self, word, maybeCombination = True):
        word = word.lower()
        if maybeCombination and len(word) <= self.min_len:
            return True
        if word in self.dict:
            return True
        for pos in ['n', 'v', 'a', 'r']:
            lemma = self.wnl.lemmatize(word, pos)
            if lemma in self.dict:
                return True
        stem = self.ls.stem(word)
        if stem in self.dict:
            return True
        # Might be Britain English (colour, metre, etc.)
        br_word = self.to_britain(word)
        if br_word in self.dict:
            return True
        # Might be a combination word (timestamp, etc.)
        if maybeCombination and len(word) >= self.min_combi_len:
            for i in range(self.min_len, len(word) - self.min_len + 1):
                if self.is_ok(word[:i], False) and self.is_ok(word[i:], False):
                    return True
        return False

    def to_britain(self, word):
        for pos in ['n', 'v', 'a', 'r']:
            lemma = self.wnl.lemmatize(word, pos)
            if re.match(r'.+re$', lemma):
                return re.sub('re$', 'er', lemma)
            if re.match(r'.+our$', lemma):
                return re.sub('our$', 'or', lemma)
        return word

    def get_suggestion(self, word):
        heap = []
        heapify(heap)
        for cand in self.dict:
            if abs(len(cand) - len(word)) > self.suggestion_dist:
                continue
            dist = self.get_edit_distance(word, cand)
            if dist <= self.suggestion_dist:
                if (len(heap) >= self.heap_size):
                    heappushpop(heap, (-dist, cand))
                else:
                    heappush(heap, (-dist, cand))
        suggestions = []
        for i in range(len(heap)):
            suggestions.insert(0, heappop(heap)[1])
        return suggestions

    def get_edit_distance(self, word1, word2):
        m = len(word1)
        n = len(word2)
        dp = [[0 for j in range(n+1)] for i in range(m+1)]
        for i in range(0, m + 1):
            dp[i][0] = i
        for j in range(0, n + 1):
            dp[0][j] = j
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                cost = 0
                if word1[i-1] != word2[j-1]:
                    cost = 1
                dp[i][j] = min(dp[i-1][j] + 1, dp[i][j-1] + 1, dp[i-1][j-1] + cost)
        return dp[m][n]


# Patterns
ptn_space = re.compile(r'\s+')
ptn_delimeter = re.compile(r'[^a-zA-Z]+')
ptn_camel_case = re.compile(r'[A-Z]?(?:[A-Z]*(?=$|[A-Z][a-z])|[a-z]*)')

# Load dictionaries from command line args
tp = TypoPolice()
for path in sys.argv[1:]:
  tp.load_dict(path)

typos = set()

# Parse words from STDIN
for line in sys.stdin:
    new_line = line.strip()
    if new_line == '':
        continue
    strs = re.split(ptn_delimeter, new_line)
    for s in strs:
        # Camel case
        words = re.findall(ptn_camel_case, s)
        for word in words:
            if tp.is_ok(word):
                continue
            typos.add(word)

# Suggestions for typo
for typo in typos:
    print(typo)
    suggestions = tp.get_suggestion(typo.lower())
    print(suggestions)
print(str(len(typos)) + ' typo(s) found.')
