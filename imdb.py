__author__ = 'Marius'

import glob, os
from abc import abstractmethod
from heapq import heappush, heappop
import re
from collections import defaultdict


class FileReader():

    def __init__(self):
        self.wordSet = []
        self.wordDict = defaultdict(int)
        self.reviews = 0
        self.stopWords = open('C:/Users/mariu_000/PycharmProjects/imdb/data/data/stop_words.txt', encoding='utf-8').read()




    def read_words(self, path):
        os.chdir(path)
        for file in glob.glob('*.txt'):
            self.reviews = self.reviews + 1
            self.wordSet = set(self.n_grams(list(re.findall(r'\w+',open(file, encoding='utf-8').read().lower().replace("'", ""))), 2)) #creates a set with unique, lowercase words from the file
            for word in self.wordSet:
                if word in self.stopWords or len(word) <= 1:
                    continue
                elif word in self.wordDict:                    #if the word is already in the dict, count up by one
                    self.wordDict[word] = self.wordDict[word] + 1
                else:                                        #if the word is not already in the dict, add it, and add 1
                    self.wordDict[word] = 1


    def n_grams(self, wordList, nValue):    #makes nValue-grams of the words in the wordlist
        ngram_list = []
        for idx in range(1+len(wordList)- nValue):
            if wordList[idx] in self.stopWords and wordList[idx+nValue-1] in self.stopWords:    #skips the n-gram if both the words are stopwords
                continue
            ngram_list.append('_'.join(wordList[idx:idx+nValue]))
        return ngram_list



    '''def strip_words(self, str):                                #method that removes the characters in the table from the string
        trans_table = dict.fromkeys(map(ord, '$/<>?!"\'"´*=~[]\+-%&`:;_")(,. '), None)
        str = str.translate(trans_table)
        str = re.sub('[0-9]', "", str)
        if str[-2:] == 'br':
            str = str.replace('br', "")
        return str'''


frP = FileReader()
frN = FileReader()
frP.read_words('C:/Users/mariu_000/PycharmProjects/imdb/data/data/subset/train/pos')
frN.read_words('C:/Users/mariu_000/PycharmProjects/imdb/data/data/subset/train/neg')
#print (frP.wordDict)
#print(frP.wordSet)
#print(frN.wordDict)
print (frP.reviews)
print (frN.reviews)


class Analyzer():

    @abstractmethod
    def popularity(self, dictionary):
        pass
    @abstractmethod
    def informationValue(self, dictionary):
        pass


class PosAnalyzer(Analyzer):

    def __init__(self, posDict, nP, nT):
        self.pos_words = posDict
        self.popularityDict = {}
        self.infoValue = {}
        self.pos_vocab = {}
        self.positiveReviews = nP
        self.totalReviews = nT

    def popularity(self, neg_words):
        for word in self.pos_words:
            if (self.pos_words[word] + neg_words[word])/self.totalReviews > 0.05:
                self.popularityDict[word] = self.pos_words[word]/self.positiveReviews

    def informationValue(self, neg_words):
        for word in self.pos_words.keys():
            if (self.pos_words[word]+ neg_words[word])/self.totalReviews > 0.05:
                self.infoValue[word] = self.pos_words[word]/(self.pos_words[word] + neg_words[word])

    def prune(self, pos_words, neg_words):
        pos_vocab = {}
        for word in pos_words.keys():
            if (pos_words[word] + neg_words[word])/self.totalReviews > 0.01:
                pos_vocab[word] = pos_words[word]
        self.pos_vocab = pos_vocab






class NegAnalyzer(Analyzer):


    def __init__(self, negDict, nN, nT):
        self.neg_words = negDict
        self.popularityDict = {}
        self.infoValue = {}
        self.negativeReviews = nN
        self.totalReviews = nT

    def popularity(self, pos_words):
        for word in self.neg_words:
            if (self.neg_words[word] + pos_words[word])/self.totalReviews > 0.05:
                self.popularityDict[word] = self.neg_words[word]/self.negativeReviews

    def informationValue(self, pos_words):
        for word in self.neg_words.keys():
            if (self.neg_words[word]+ pos_words[word])/self.totalReviews > 0.05:
                self.infoValue[word] = self.neg_words[word]/(self.neg_words[word] + pos_words[word])





pa = PosAnalyzer(frP.wordDict, frP.reviews, (frP.reviews + frN.reviews))
na = NegAnalyzer(frN.wordDict, frN.reviews, (frP.reviews + frN.reviews))
pa.informationValue(na.neg_words)
na.informationValue(pa.pos_words)
pos25 = sorted(pa.infoValue, key=pa.infoValue.get,reverse=True)[:25]
neg25 = sorted(na.infoValue, key=na.infoValue.get,reverse=True)[:25]
print(pos25)
print(pa.infoValue['the_best'])
print(pa.infoValue['as_well'])
print(neg25)
print(na.infoValue['could_have'])
print(na.infoValue['the_worst'])












