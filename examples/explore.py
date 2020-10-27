from pinnacle import pinnacle
from pinnacle import pub_dataviz
from openpyxl import load_workbook
import pandas as pd
from pinnacle.Configure import Parser

ini = 'iate.ini'
config = Parser(ini)
df = pinnacle.inst_adsentries(config)
df.load_inst()
df.save_table()

d = df.pub_inst_top

N = d.shape[0]

k = 0
for i in range(N):
    t = d.title.values[i]
    a = d.author1.values[i]
    s = d.authors.values[i]
    j = d.aff.values[i]
    p = d.pub.values[i]
    y = int(d.year.values[i])
    if y==2020:
        k+=1
        #print(t)
        #print(a)
        print(s)
        print(p)
        #print(j)
        input()


