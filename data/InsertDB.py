# -*- coding: utf-8 -*-
import os,os.path as op
import sqlite3
from config import *
from tqdm import tqdm

#连接数据库，创建游标和SQL格式
conn = sqlite3.connect(SQLITE_DB_PATH)
cur = conn.cursor()
sql = 'insert into relate (id,word,count,firstLetters,pinyin,click) values (?,?,?,?,?,?)'

#批量导入，减少提交事务的次数，可以提高速度
tuples = []
wordlib = LoadTxtToLib(MERGED_WORD_LIB_PATH,'utf-8')
for i,line in tqdm(enumerate(wordlib)):
    word,count,firstLetters,pinyin = line
    tuples.append((i+1,word,count,firstLetters,pinyin,0))
    if (i+1)%1e4==0 or i+1==len(wordlib):
        cur.executemany(sql,tuples)
        conn.commit()
        tuples = []

# --- Execution Result ---
#Reloaded modules: config
#742286it [00:13, 57037.24it/s]
