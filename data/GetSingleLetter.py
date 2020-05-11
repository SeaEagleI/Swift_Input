# -*- coding: utf-8 -*-
import os,os.path as op

Sogou_WORD_LIB_PATH = 'SogouCoreWordlib-v9.2.txt'
RAW_LETTERS_PATH    = 'XinhuaLettersDic.txt'
MERGED_LETTERS_PATH = 'merged_letters.txt'
BASE_WORD_LIB_PATH  = 'wordlib.txt'

sogouWordlibTxt = open(Sogou_WORD_LIB_PATH).read()[:-1]
sentence = sogouWordlibTxt.replace('\n','')
lettersFromWL = list(set(list(sentence)))
print(len(lettersFromWL))

lettersFromLL = list(open(RAW_LETTERS_PATH).read().replace('\n',''))
print(len(lettersFromLL))
print(len(set(lettersFromLL)))

# Get & Save letters & wordlist
letters = list(set(lettersFromWL).union(set(lettersFromLL)))
open(MERGED_LETTERS_PATH,'w+').write('\n'.join(letters)+'\n')
wordlist = sogouWordlibTxt.split('\n')
open(BASE_WORD_LIB_PATH,'w+').write('\n'.join(wordlist)+'\n')
print('Letters: {}\tWords: {}'.format(len(letters),len(wordlist)))
