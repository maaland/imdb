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
            self.wordSet = set([self.strip_words(word.lower()) for line in open(file, encoding='utf-8') for word in line.split()])   #creates a set with unique, lowercase words from the file
            for word in self.wordSet:
                if word in self.stopWords:
                    continue
                elif word in self.wordDict:                    #if the word is already in the dict, count up by one
                    self.wordDict[word] = self.wordDict[word] + 1
                else:                                        #if the word is not already in the dict, add it, and add 1
                    self.wordDict[word] = 1


    def strip_words(self, str):                                #method that removes the characters in the table from the string
        trans_table = dict.fromkeys(map(ord, '$/<>?!"\'"´*=[]\+-%&`:;_")(,. '), None)
        str = str.translate(trans_table)
        str = re.sub('[0-9]', "", str)
        if str[-2:] == 'br':
            str = str.replace('br', "")
        return str


frP = FileReader()
frN = FileReader()
frP.read_words('C:/Users/mariu_000/PycharmProjects/imdb/data/data/subset/train/pos')
frN.read_words('C:/Users/mariu_000/PycharmProjects/imdb/data/data/subset/train/neg')
#print (fr.wordDict)
print (frP.reviews)
print (frN.reviews)


class Analyzer():

    @abstractmethod
    def popularity(self):
        pass
    @abstractmethod
    def informationValue(self, dictionary):
        pass


class PosAnalyzer(Analyzer):

    def __init__(self, posDict, nP, nT):
        self.countDict = posDict
        self.popDict = {}
        self.infoValue = {}
        self.positiveReviews = nP
        self.totalReviews = nT

    def popularity(self):
        for word in self.countDict:
            self.popDict[word] = self.countDict[word]/self.positiveReviews

    def informationValue(self, negDict):
        for word in self.countDict.keys():
            self.infoValue[word] = self.countDict[word]/(self.countDict[word] + negDict[word])






class NegAnalyzer(Analyzer):


    def __init__(self, negDict, nN, nT):
        self.countDict = negDict
        self.popDict = {}
        self.infoValue = {}
        self.negativeReviews = nN
        self.totalReviews = nT

    def popularity(self):
        for word in self.countDict:
            self.popDict[word] = self.countDict[word]/self.totalReviews

    def informationValue(self, posDict):
        for word in self.countDict.keys():
            self.infoValue[word] = self.countDict[word]/(self.countDict[word] + posDict[word])





pa = PosAnalyzer(frP.wordDict, frP.reviews, (frP.reviews + frN.reviews))
na = NegAnalyzer(frN.wordDict, frN.reviews, (frP.reviews + frN.reviews))
pa.informationValue(na.countDict)
na.informationValue(pa.countDict)
pos25 = sorted(pa.infoValue, key=pa.infoValue.get,reverse=True)[:25]
neg25 = sorted(na.infoValue, key=na.infoValue.get,reverse=True)[:25]
print(pos25)
print(neg25)











