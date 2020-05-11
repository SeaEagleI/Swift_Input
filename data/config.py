# -*- coding: utf-8 -*-
from tqdm import tqdm
import os,os.path as op

BASE_WORD_LIB_PATH   = 'wordlib.txt'
NEWS_WORD_LIB_PATH   = 'WordlibFromNews/dictionary.txt'
FREQ_WORD_LIB_PATH   = 'WordlibFromNews/freq_dictionary.txt'
MERGED_LETTERS_PATH  = 'merged_letters.txt'
MERGED_WORD_LIB_PATH = 'merged_dict.txt'
RES_DIR              = 'TmpResNum'
LETTER_ENG_PATH      = 'WordlibFromNews/letter_eng.txt'
DATABASE_PATH        = 'wordlib.csv'
SQLITE_DB_PATH       = 'core_wordlib.db'

SCALE = 1.5e-3 #cntNews/resNum
EPS   = 1e-1

#伪装浏览器头部
headers = {
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:75.0) Gecko/20100101 Firefox/75.0",
"Referer": "",
"Sec-Fetch-Mode": "no-cors",
"Connection": "keep-alive"
}

def LoadTxtToList(txt_path,codec='gbk'):
    return [line[:-1] for line in open(txt_path,encoding=codec).readlines()]

def LoadTxtToLib(txt_path,codec='gbk'):
    return [line[:-1].split('\t') for line in open(txt_path,encoding=codec).readlines()]

def WriteListToTxt(_list,txt_path,codec='gbk'):
    f = open(txt_path,'w+',encoding=codec)
    for line in tqdm(_list):
        f.write('\t'.join(line)+'\n')
    f.close()
    print('Written {} lines To {}'.format(len(_list),txt_path))
