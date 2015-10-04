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
            self.wordSet = set(re.findall(r'\w+',open(file, encoding='utf-8').read().lower().replace("'", ""))) #creates a set with unique, lowercase words from the file
            for word in self.wordSet:
                if word in self.stopWords or len(word) <= 1:
                    continue
                elif word in self.wordDict:                    #if the word is already in the dict, count up by one
                    self.wordDict[word] = self.wordDict[word] + 1
                else:                                        #if the word is not already in the dict, add it, and add 1
                    self.wordDict[word] = 1


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
        self.countDict = posDict
        self.popularityDict = {}
        self.infoValue = {}
        self.positiveReviews = nP
        self.totalReviews = nT

    def popularity(self, negDict):
        for word in self.countDict:
            if self.countDict[word] + negDict[word]/self.totalReviews > 0.01:
                self.popularityDict[word] = self.countDict[word]/self.positiveReviews

    def informationValue(self, negDict):
        for word in self.countDict.keys():
            if self.countDict[word]+ negDict[word]/self.totalReviews > 0.01:
                self.infoValue[word] = self.countDict[word]/(self.countDict[word] + negDict[word])






class NegAnalyzer(Analyzer):


    def __init__(self, negDict, nN, nT):
        self.countDict = negDict
        self.popularityDict = {}
        self.infoValue = {}
        self.negativeReviews = nN
        self.totalReviews = nT

    def popularity(self, posDict):
        for word in self.countDict:
            if self.countDict[word] + posDict[word]/self.totalReviews > 0.01:
                self.popularityDict[word] = self.countDict[word]/self.negativeReviews

    def informationValue(self, posDict):
        for word in self.countDict.keys():
            if self.countDict[word]+ posDict[word]/self.totalReviews > 0.01:
                self.infoValue[word] = self.countDict[word]/(self.countDict[word] + posDict[word])





pa = PosAnalyzer(frP.wordDict, frP.reviews, (frP.reviews + frN.reviews))
na = NegAnalyzer(frN.wordDict, frN.reviews, (frP.reviews + frN.reviews))
pa.popularity(na.countDict)
na.popularity(pa.countDict)
pos25 = sorted(pa.popularityDict, key=pa.popularityDict.get,reverse=True)[:25]
neg25 = sorted(na.popularityDict, key=na.popularityDict.get,reverse=True)[:25]
print(pos25)
print(neg25)












