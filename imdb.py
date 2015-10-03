__author__ = 'Marius'

import glob, os
from abc import abstractmethod
from heapq import heappush, heappop
import re


class FileReader():

    def __init__(self):
        self.wordSet = []
        self.wordDict = {}
        self.reviews = 0
        self.stopWords = open('C:/Users/mariu_000/PycharmProjects/imdb/data/data/stop_words.txt', encoding='utf-8').read()




    def read_words(self, path):
        os.chdir(path)
        for file in glob.glob('*.txt'):
            self.reviews = self.reviews + 1
            self.wordSet = set([self.strip_words(word.lower()) for line in open(file, encoding='utf-8') for word in line.split()])   #creates a set with unique, lowercase words from the file
            for word in self.wordSet:
                if word in self.wordDict:                    #if the word is already in the dict, count up by one
                    self.wordDict[word] = self.wordDict[word] + 1
                else:                                        #if the word is not already in the dict, add it, and add 1
                    self.wordDict[word] = 1


    def strip_words(self, str):                                #method that removes the characters in the table from the string
        trans_table = dict.fromkeys(map(ord, '$/<>?!"\'"´*=[]\+-%&`:;_")(,. '), None)
        str = str.translate(trans_table)
        str = re.sub('[0-9]', "", str)
        return str


fr = FileReader()
fr.read_words('C:/Users/mariu_000/PycharmProjects/imdb/data/data/subset/train/neg')
#print (fr.wordDict)
print (fr.reviews)
print(fr.stopWords)

class Analyzer():

    @abstractmethod
    def popularity(self):
        pass




class PosAnalyzer(Analyzer):

    def __init__(self, d, n):
        self.countDict = d
        self.popDict = {}
        self.reviews = n

    def popularity(self):
        for word in self.countDict:
            self.popDict[word] = self.countDict[word]/self.reviews



class NegAnalyzer(Analyzer):


    def __init__(self, dictionary, number):
        self.countDict = dictionary
        self.popDict = {}
        self.reviews = number

    def popularity(self):
        for word in self.countDict:
            self.popDict[word] = self.countDict[word]/self.reviews





pa = PosAnalyzer(fr.wordDict, fr.reviews)
na = NegAnalyzer(fr.wordDict, fr.reviews)
pos25 = sorted(pa.countDict, key=pa.countDict.get,reverse=True)[:25]
print(pos25)










