# -*- coding: utf-8 -*-
"""
Created on Wed Oct 28 15:46:20 2015

@authors: 

Shubham Mahajan
Max Levine
Sai Jyothi Lanka

"""

################################## Sources ####################################
# Data for analysis - http://dinosaurstop.com/learn/
# Including only text files - https://github.com/shubh29/InformationRetrievalSystem2/blob/master/InformationRetrievalSystem.py
# Using shell commands directly(Prevents me from writing an extra function) - https://docs.python.org/2/library/glob.html


################################## Imports ####################################

from glob import glob
import math
import re
import string

################################## Storage ####################################

# setup some structures to store our data

word_counts = {
    "crypto": {},
    "dino": {}
}

priors = {
    "crypto": 0.,
    "dino": 0.
}

docs = []


################################ Initialize ###################################

vocab = {}

wordCount = {}


################################## Methods ####################################

def removePunctuation(s):
    exclude = set(string.punctuation)
    return ''.join(ch for ch in s if ch not in exclude)

def tokenize(text):
    text = removePunctuation(text)
    text = text.lower()
    return re.split("\W+", text)

def countWords(words):
    for word in words:
        wordCount[word] = wordCount.get(word, 0.0) + 1.0
    return wordCount

s = "Hello my name, is Shubham. My favorite food is pizza."
countWords(tokenize(s))
{'favorite': 1.0, 'food': 1.0, 'shubham': 1.0, 'hello': 1.0, 'is': 2.0, 'my': 2.0, 'name': 1.0, 'pizza': 1.0}

for g in glob("sample-data"):
    g = g.strip()
    print(g)
    if not g.endswith(".txt"):
        # skip non .txt files
        continue
    elif "cryptid" in g:
        category = "crypto"
    else:
        category = "dino"
    docs.append((category, g))
    # ok time to start counting stuff...
    priors[category] += 1
    text = open(g).read()
    words = tokenize(text)
    counts = countWords(words)
    for word, count in list(counts.items()):
        # if we haven't seen a word yet, let's add it to our dictionaries with a count of 0
        if word not in vocab:
            vocab[word] = 0.0  # use 0.0 here so Python does "correct" math
        if word not in word_counts[category]:
            word_counts[category][word] = 0.0
        vocab[word] += count
        word_counts[category][word] += count


newDocument = open("examples/Allosaurus.txt").read()
newDocument = open("examples/Python.txt").read()
newDocument = open("examples/Yeti.txt").read()
words = tokenize(newDocument)
counts = countWords(words)

prior_dino = (priors["dino"] / sum(priors.values()))
prior_crypto = (priors["crypto"] / sum(priors.values()))

logProbabilityOfCrypto = 0.0
logProbabilityOfDino = 0.0
for w, cnt in list(counts.items()):
    # skip words that we haven't seen before, or words less than 3 letters long
    if w not in vocab or len(w) <= 3:
        continue
    
    # calculate the probability that the word occurs at all
    probabilityOfWord = vocab[w] / sum(vocab.values())

    # for both categories, calculate P(word|category), or the probability a 
    # word will appear, given that we know that the document is <category>
    probabilityWordGivenDino = word_counts["dino"].get(w, 0.0) / sum(word_counts["dino"].values())
    probabilityWordGivenCrypto = word_counts["crypto"].get(w, 0.0) / sum(word_counts["crypto"].values())

    # add new probability to our running total: log_prob_<category>. if the probability 
    # is 0 (i.e. the word never appears for the category), then skip it    
    if probabilityWordGivenDino > 0:
        logProbabilityOfDino += math.log(cnt * probabilityWordGivenDino / probabilityOfWord)
    if probabilityWordGivenCrypto > 0:
        logProbabilityOfCrypto += math.log(cnt * probabilityWordGivenCrypto / probabilityOfWord)
# print out the reuslts; we need to go from logspace back to "regular" space,
# so we take the EXP of the log_prob (don't believe me? try this: math.exp(log(10) + log(3)))
print("Score(dino)  :", math.exp(logProbabilityOfDino + math.log(prior_dino)))
print("Score(crypto):", math.exp(logProbabilityOfCrypto + math.log(prior_crypto)))

# Score(dino)  : 2601.76647058
# Score(crypto): 25239.089932

################################ End of File ##################################