# this code is for development purposes


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
import csv
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

        row[2] = sent1

        journals.append(row)
    


ini = 'iate.ini'
config = Parser(ini)
df = pinnacle.inst_adsentries(config)
df.load_inst()
df.save_table()

d = df.pub_inst_top

N = d.shape[0]


def get_q(s):
    q = 0
    if "Q4" in s:
        q = 4
    if "Q3" in s:
        q = 3
    if "Q2" in s:
        q = 2
    if "Q1" in s:
        q = 1
    return q




k = 0
for i in range(N):
    p = d.pub.values[i]

    jname = p.lower()
    word_tokens = word_tokenize(jname)
    fname = [w for w in word_tokens if not w in stop_words]
    sent1 = ' '.join(fname)
    sent1 = sent1.replace('/', '')

    match = 0
    J = ""
    for Journal in journals:
        journal = Journal[2]
        s1 = similar(sent1, journal)
        s2 = jellyfish.jaro_winkler(sent1, journal)
        if s1>0.9 and s2>0.9:
            match += 1
            J = Journal[-1]
    print(get_q(J), p)


# dos2unix los dos archivos
#cat scimagojr\ 2019\ \ Subject\ Area\ -\ Earth\ and\ Planetary\ Sciences.csv scimagojr\ 2019\ \ Subject\ Area\ -\ Physics\ and\ Astronomy.csv > scimagojr.csv
#awk -F';' 'BEGIN {OFS = FS} {first = $1; $1 = ""; print $0}' scimagojr.csv > aux
#sort -t\; -k 3 aux | uniq > aux2
#mv aux2 scimagojr.csv
