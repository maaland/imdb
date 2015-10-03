__author__ = 'Marius'

import glob, os
from abc import abstractmethod
import re



class FileReader():

    def __init__(self):
        self.wordSet = []
        self.posDict = {}
        self.reviews = 0


    def read_words(self, path):
        os.chdir(path)
        for file in glob.glob('*.txt'):
            self.reviews = self.reviews + 1
            self.wordSet = set([self.strip_words(word.lower()) for line in open(file, encoding='utf-8') for word in line.split()])   #creates a set with unique, lowercase words from the file
            for word in self.wordSet:
                if word in self.posDict:                    #if the word is already in the dict, count up by one
                    self.posDict[word] = self.posDict[word] + 1
                else:                                        #if the word is not already in the dict, add it, and add 1
                    self.posDict[word] = 1


    def strip_words(self, str):                                #method that removes the characters in the table from the string
        trans_table = dict.fromkeys(map(ord, '$/<>?!:;_")(,. '), None)
        str = str.translate(trans_table)
        str = str.replace("'", "")
        return str


fr = FileReader()
fr.read_words('C:/Users/mariu_000/PycharmProjects/imdb/data/data/subset/train/neg')
print (fr.posDict)
print (fr.reviews)

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




pa = PosAnalyzer(fr.posDict, fr.reviews)
pa.popularity()
print (pa.popDict)





