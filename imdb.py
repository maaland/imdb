__author__ = 'Marius'

import glob, os



class FileReader():

    wordlist = []
    posDict = {}


    def read_words(self, path):
        os.chdir(path)
        for file in glob.glob('1_1.txt'):
            wordSet = set([word.lower() for line in open(file, encoding='utf-8') for word in line.split()])   #creates a set with unique, lowercase words from the file
            for word in wordSet:
                if word in self.posDict:                    #if the word is already in the dict, count up by one
                    self.posDict[word] = self.posDict[word] + 1
                else:                                        #if the word is not already in the dict, add it, and add 1
                    self.posDict[word] = 1



fr = FileReader()
fr.read_words('C:/Users/mariu_000/PycharmProjects/imdb/data/data/subset/train/neg')
print (fr.posDict.keys())





