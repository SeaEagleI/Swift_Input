# -*- coding: utf-8 -*-
import re
import sqlite3
from PinyinInput.config import *
from tkinter import _flatten

SPLIT_REGEX = '[^aoeiuv]?h?[iuv]?(ai|ei|ao|ou|er|ang?|eng?|ong|a|o|e|i|u|ng|n)?'
SELECT_FORMULA = "select distinct word from relate where firstLetters ='{}' and pinyin like '{}'" \
                 + " order by click desc, count desc, length(pinyin) limit {};"


class PinyinInput:
    def __init__(self):
        self.conn = sqlite3.connect(SQLITE_DB_PATH)
        self.cursor = self.conn.cursor()

    # 修复了REGEX中可能出现的两个错误分割"hng"和"hn";
    # 同时支持手动纠错(手动添加'表示分隔).
    def SplitSubSentence(self, sub_s):
        words = []
        while sub_s != '':
            m = re.match(SPLIT_REGEX, sub_s)
            words.append(m.group())
            sub_s = sub_s[len(m.group()):]
        return words

    def SplitSentence(self, s):
        s = s.replace("hng", "h'n'g").replace("hn", "h'n").lower()
        sub_slist = [self.SplitSubSentence(sub_s) for sub_s in s.split("'")]
        return list(_flatten(sub_slist))

    def Application(self, sentence, cands=6, limit=100):
        pylist = self.SplitSentence(sentence)
        firstLetters = ''.join([py[0] for py in pylist])
        py_regex = ''.join([py + '%' for py in pylist])
        sql = SELECT_FORMULA.format(firstLetters, py_regex, limit)
        self.cursor.execute(sql)
        return [row[0] for row in self.cursor][:cands]

    def Update(self):
        pass

# print(Application('szhen'))
# print(Application('sz'))
# print(Application('shizheng'))
# print(Application('lianggehuanglimingcuiliu'))
# print(Application('chuangqianmingyueguang'))
# print(Application('python'))
# print(Application('aishangta'))
# print(Application('hng'))
# print(Application('hn'))
# print(Application('hb'))
# print(Application("xian"))
# print(Application("xi'an"))
# print(Application('fir'))
# print(Application('chrom'))
