from difflib import SequenceMatcher
import jellyfish
from pinnacle import pinnacle
from pinnacle import pub_dataviz
from openpyxl import load_workbook
import pandas as pd
from pinnacle.Configure import Parser
 

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize 
# download stowords the first time

stop_words = set(stopwords.words('english')) 

journals = []
with open('scimagojr.csv', newline='') as csvfile:
    s = csv.reader(csvfile, delimiter=';')
    for row in s:

        jname = row[2].lower()
        word_tokens = word_tokenize(jname)
        fname = [w for w in word_tokens if not w in stop_words]
        sent1 = ' '.join(fname)
        sent1 = sent1.replace('/', '')
        journals.append(sent1)
    


ini = 'iate.ini'
config = Parser(ini)
df = pinnacle.inst_adsentries(config)
df.load_inst()
df.save_table()

d = df.pub_inst_top

N = d.shape[0]

k = 0
for i in range(N):
    p = d.pub.values[i]

    jname = p.lower()
    word_tokens = word_tokenize(jname)
    fname = [w for w in word_tokens if not w in stop_words]
    sent1 = ' '.join(fname)
    sent1 = sent1.replace('/', '')

    print(p)
    print(sent1)

    for journal in journals:
        s1 = similar(sent1, journal)
        s2 = jellyfish.hamming_distance(sent1, journal)
        s3 = jellyfish.jaro_winkler(sent1, journal)
        #if s1>0.9 and s2<2 and s3>0.9:
        if s1>0.9 and s3>0.9:
            print('        ',journal)
            print('------->', sent1)
    input()


# dos2unix los dos archivos
#cat scimagojr\ 2019\ \ Subject\ Area\ -\ Earth\ and\ Planetary\ Sciences.csv scimagojr\ 2019\ \ Subject\ Area\ -\ Physics\ and\ Astronomy.csv > scimagojr.csv
#awk -F';' 'BEGIN {OFS = FS} {first = $1; $1 = ""; print $0}' scimagojr.csv > aux
#sort -t\; -k 3 aux | uniq > aux2
#mv aux2 scimagojr.csv






