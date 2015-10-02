__author__ = 'Marius'

import glob, os



class FileReader():

    wordlist = []


    def read_words(self, path):
        os.chdir(path)
        for file in glob.glob('0_3.txt'):
            return set([word for line in open(file, encoding='utf-8') for word in line.split()])


fr = FileReader()
print(fr.read_words('C:/Users/mariu_000/PycharmProjects/imdb/data/data/subset/train/neg'))





