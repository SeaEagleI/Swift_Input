# -*- coding: utf-8 -*-
from pypinyin import lazy_pinyin
from tqdm import tqdm

WORD_LIB_PATH  = 'wordlib.txt'
DATABASE_PATH = 'wordlib.csv'

wordlib = open(WORD_LIB_PATH).readlines()
f = open(DATABASE_PATH,'w+')
for word in tqdm(wordlib):
    f.write('{}\t{}\n'.format(word[:-1],''.join(lazy_pinyin(word[:-1]))))
f.close()
