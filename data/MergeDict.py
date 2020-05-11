# -*- coding: utf-8 -*-
from pypinyin import lazy_pinyin
from tqdm import tqdm
import re
from config import *

#Wordlib Format: [word]\t[count]\t[firstLetters]\t[pinyin]
freq_wordlib = []
freq_worddict = {}
base_wordlib = []
single_letters = []

# Get freq_wordlib, Saving As freq_dictionary.txt
news_wordlib = open(NEWS_WORD_LIB_PATH,encoding='utf-8').readlines()
f = open(FREQ_WORD_LIB_PATH,'w+',encoding='utf-8')
for i,line in tqdm(enumerate(news_wordlib)):
    word, _, freq = line[:-1].split('\t')
    if int(freq)>=90:
        f.write('{}\t{}\n'.format(word,freq))
        freq_wordlib.append([word,freq,'',''])
    else:
        print(i)
        break
        #f.write('{}\t{}\n'.format(word[:-1],''.join(lazy_pinyin(word[:-1]))))
f.close()

# Get, Merge & Save diff_wordlist, eng_wordlist
base_wordlist = LoadTxtToList(BASE_WORD_LIB_PATH)
freq_worddict = dict([line[:2] for line in freq_wordlib])
diff_wordlist = list(set(base_wordlist).difference(set(list(freq_worddict))))
print(len(diff_wordlist))

eng_wordlist = []
for word in tqdm(diff_wordlist):
    if re.findall(r'[a-zA-Z]+',word):
        eng_wordlist.append(word)
print(len(eng_wordlist))
single_letters = LoadTxtToList(MERGED_LETTERS_PATH)
WriteListToTxt(single_letters+eng_wordlist,LETTER_ENG_PATH)

# --- After Run GetSearchResNum.py ---
# Merge & Zoom resNum ==> est_cntNews
# Get Final DB Results
unit = 1500
freq_wordlib = []
for line in tqdm(open(FREQ_WORD_LIB_PATH,encoding='utf-8').readlines()):
    word,count = line[:-1].split('\t')
    pylist = [py.lower() for py in lazy_pinyin(word)]
    freq_wordlib.append([word,count,''.join([py[0] for py in pylist]),''.join(pylist)])
le_wordlib = []
for i in tqdm(range(10)):
    src_file = '{}/{}-{}.txt'.format(RES_DIR,unit*i+1,unit*(i+1))
    for line in open(src_file).readlines():
        word,count = line[:-1].split('\t')
        pylist = [py.lower() for py in lazy_pinyin(word)]
        le_wordlib.append([word,str(round(int(count)*SCALE)),''.join([py[0] for py in pylist]),''.join(pylist)])
merged_wordlib = le_wordlib + freq_wordlib
WriteListToTxt(merged_wordlib,MERGED_WORD_LIB_PATH,'utf-8')

#100%|██████████| 727374/727374 [00:30<00:00, 23946.47it/s]
#100%|██████████| 10/10 [00:00<00:00, 43.47it/s]
#100%|██████████| 742286/742286 [00:00<00:00, 749759.46it/s]
#Written 742286 lines To merged_dict.txt
