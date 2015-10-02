__author__ = 'Marius'

import glob, os




def read_words(words_file):
    return [word for line in open(words_file, 'r') for word in line.split()]


l = []
os.chdir("C:/Users/mariu_000/PycharmProjects/imdb/data/data/subset/train/neg")
for file in glob.glob("0_3.txt"):
    print(read_words(file))


