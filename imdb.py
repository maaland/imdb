__author__ = 'Marius'

import glob, os
from abc import abstractmethod
from heapq import heappush, heappop
import re
from collections import defaultdict
import math


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


frTrainP = FileReader()
frTrainN = FileReader()
frTrainP.read_words('C:/Users/mariu_000/PycharmProjects/imdb/data/data/subset/train/pos')
frTrainN.read_words('C:/Users/mariu_000/PycharmProjects/imdb/data/data/subset/train/neg')
#print (frP.wordDict)
#print(frP.wordSet)
#print(frN.wordDict)
print (frTrainP.reviews)
print (frTrainN.reviews)


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
        self.multiplied = 0

    def popularity(self, neg_words):
        for word in self.pos_words:
            if (self.pos_words[word] + neg_words[word])/self.totalReviews > 0.02:
                self.popularityDict[word] = self.pos_words[word]/self.positiveReviews

    def informationValue(self, neg_words):
        for word in self.pos_words.keys():
            if (self.pos_words[word]+ neg_words[word])/self.totalReviews > 0.05:
                self.infoValue[word] = self.pos_words[word]/(self.pos_words[word] + neg_words[word])

    def prune(self, pos_words, neg_words):              #not required
        pos_vocab = {}
        for word in pos_words.keys():
            if (pos_words[word] + neg_words[word])/self.totalReviews > 0.01:
                pos_vocab[word] = pos_words[word]
        self.pos_vocab = pos_vocab

    def multiply(self):
        for word in self.popularityDict.keys():
            self.multiplied = self.multiplied + math.log10(self.popularityDict[word])




class NegAnalyzer(Analyzer):


    def __init__(self, negDict, nN, nT):
        self.neg_words = negDict
        self.popularityDict = {}
        self.infoValue = {}
        self.negativeReviews = nN
        self.totalReviews = nT
        self.multiplied = 0

    def popularity(self, pos_words):
        for word in self.neg_words:
            if (self.neg_words[word] + pos_words[word])/self.totalReviews > 0.02:
                self.popularityDict[word] = self.neg_words[word]/self.negativeReviews

    def informationValue(self, pos_words):
        for word in self.neg_words.keys():
            if (self.neg_words[word]+ pos_words[word])/self.totalReviews > 0.05:
                self.infoValue[word] = self.neg_words[word]/(self.neg_words[word] + pos_words[word])

    def multiply(self):
        for word in self.popularityDict.keys():
            self.multiplied = self.multiplied + math.log10(self.popularityDict[word])


class Evaluator():

    def __init__(self, posAnalyzer, negAnalyzer):
        self.posMultiplied = posAnalyzer.multiplied
        self.negMultiplied = negAnalyzer.multiplied
        self.pos_train_pop = posAnalyzer.popularityDict
        self.neg_train_pop = negAnalyzer.popularityDict
        self.pos_train_words = posAnalyzer.pos_words
        self.neg_train_words = negAnalyzer.neg_words
        self.positiveReviews = posAnalyzer.positiveReviews
        self.negativeReviews = negAnalyzer.negativeReviews
        self.word_count = {}
        self.reviews = 0
        self.posPopularityDict = {}
        self.negPopularityDict = {}
        self.stopWords = open('C:/Users/mariu_000/PycharmProjects/imdb/data/data/stop_words.txt', encoding='utf-8').read()


    def read_document(self, path):
        os.chdir(path)
        for file in glob.glob('7_9.txt'):
            self.reviews = self.reviews +1
            self.wordSet = set(re.findall(r'\w+',open(file, encoding='utf-8').read().lower().replace("'", "")))
            for word in self.wordSet:
                if word in self.stopWords or len(word) <= 1:     #doesn't add the word if its a stopword or one-letter word
                    continue
                elif word not in self.pos_train_pop or word not in self.neg_train_pop:  #doesnt add word if it's not in the training population
                    continue
                elif word in self.word_count:                    #if the word is already in the dict, count up by one
                    self.word_count[word] = self.word_count[word] + 1
                else:                                        #if the word is not already in the dict, add it, and add 1
                    self.word_count[word] = 1

    def posPopularity(self):
        for word in self.word_count:
            self.posPopularityDict[word] = self.pos_train_words[word]/self.positiveReviews

    def negPopularity(self):
        for word in self.word_count:
            self.negPopularityDict[word] = self.neg_train_words[word]/self.negativeReviews

    def evaluate(self, path, rating):
        self.read_document(path)
        self.posPopularity()
        self.negPopularity()
        posNess = 0
        negNess = 0
        correct = 0
        for word in self.posPopularityDict.keys():
            posNess = posNess + math.log10(self.posPopularityDict[word])
        for word in self.negPopularityDict.keys():
            negNess = negNess + math.log10(self.negPopularityDict[word])
        if posNess > negNess:
            if rating == 'pos':
                correct = correct + 1
        elif posNess < negNess:
            if rating == 'neg':
                correct = correct + 1
        else:
            print ('Indecisive')
        return ((correct/self.reviews)*100)









pa = PosAnalyzer(frTrainP.wordDict, frTrainP.reviews, (frTrainP.reviews + frTrainN.reviews))
na = NegAnalyzer(frTrainN.wordDict, frTrainN.reviews, (frTrainP.reviews + frTrainN.reviews))
pa.popularity(na.neg_words)
na.popularity(pa.pos_words)
pos25 = sorted(pa.infoValue, key=pa.infoValue.get,reverse=True)[:25]
neg25 = sorted(na.infoValue, key=na.infoValue.get,reverse=True)[:25]
ev = Evaluator(pa, na)

print (ev.evaluate('C:/Users/mariu_000/PycharmProjects/imdb/data/data/subset/test/pos', 'pos'))














