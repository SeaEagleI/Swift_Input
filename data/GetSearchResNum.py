# *-* coding: utf-8 *-*
import os,os.path as op
import requests,re,time
from bs4 import BeautifulSoup
from selenium import webdriver
from tqdm import tqdm
import random
from pypinyin import lazy_pinyin
from config import *

result_num_xpath = '/html/body/div/div[3]/div[1]/div[2]/div/div[2]/span'
#driver = webdriver.Chrome()

def GetIndexNum(key_word):
    url = 'https://www.sogou.com/web?query={}'.format(key_word)
#    url = 'https://www.baidu.com/s?wd={}'.format(key_word)
#    headers["Referer"] = url
    r = requests.get(url,headers=headers)
    r.encoding = r.apparent_encoding
    #Get HTML Content
    soup = BeautifulSoup(r.text, 'html.parser')
    indexInfo = soup('p',attrs={'class':'num-tips'})[0].string
#    print(indexInfo)
    indexNum = int(''.join(re.findall(r'(\d+)',indexInfo)))/1e4
    return round(indexNum/EPS)*EPS
def GetIndexNumBySelenium(key_word,driver=driver):
    url = 'https://www.baidu.com/s?wd={}'.format(key_word)
    driver.get(url)
    #Get HTML Content
    try:
        resInfo = driver.find_element_by_xpath(result_num_xpath).text
        resNum = int(''.join(re.findall(r'(\d+)',resInfo)))
        return resNum
    except:
        return -1
def GetResNumInParallel(src_file=LETTER_ENG_PATH,dest_dir=RES_DIR,crawl_func=GetIndexNumBySelenium,start=0,unit=1500):
    wordlist = open(src_file).read()[:-1].split('\n')
    dest_file = '{}/{}-{}.txt'.format(dest_dir,unit*start+1,unit*(start+1))
    print('GetResNum: [{} ==> {}]'.format(src_file,dest_file))
    print('[{}]: {} --- {}'.format(start,unit*start,unit*(start+1)))
    f = open(dest_file,'w+')
    for word in tqdm(wordlist[unit*start:unit*(start+1)]):
        #ResNumList.append(GetIndexNumbySelenium(word[:-1]))
        try:
            indexNum = crawl_func(word)
            if indexNum!=-1:
                f.write('{}\t{}\n'.format(word,indexNum))
            else:            
                while indexNum==-1:
                    input('Connection Error! Manual Override?')
                    indexNum = crawl_func(word)
                f.write('{}\t{}\n'.format(word,indexNum))
        except:
            f.close()
    f.close()
    print('Over')

# Get All 10 Parallel Running Results (14192 Cases).
GetResNumInParallel(start=4)
driver.close()

# Compare Freq Res & Baidu Search ResNum
freq_worddict = dict([line[:-1].split('\t') for line in tqdm(open(FREQ_WORD_LIB_PATH,encoding='utf-8').readlines())])
freq_wordlist = list(freq_worddict.keys())
print('{}\t{}\t{}\t{}\t{}'.format('word','resNum','cntNews','cntNews/resNum','est_cntNews'))
for i in range(50):
    word = random.choice(freq_wordlist)
    resNum = GetIndexNumBySelenium(word,driver)
    cntNews = int(freq_worddict[word])
    print('{}\t{}\t{}\t{:.6f}\t{}'.format(word,resNum,cntNews,cntNews/resNum,1.5e-3*resNum))
# For SogouWordlib is more Effective than NewsWordlib, We set SACLE=cntNews/resNum=1.5e-3,
# So that est_cntNews will be little above real cntNews at most cases.


