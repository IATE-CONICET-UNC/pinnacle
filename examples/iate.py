from pinnacle import pinnacle
from pinnacle import pub_dataviz
from openpyxl import load_workbook
import pandas as pd
from pinnacle.Configure import Parser

#for ini in ['becarios.ini', 'cics.ini', 'iate.ini']:
for ini in ['iate.ini']:
    config = Parser(ini)
    df = pinnacle.inst_adsentries(config)
    df.load_inst()
    df.save_table()
    viz = pub_dataviz.pub_dataviz(df)
    viz.plot_all()


#v=df.pub_inst_all[(df.pub_inst_all['Q']==1) & (df.pub_inst_all['year']=='2020')]
# 
# for p in v.iterrows():
#     print(p)
#     input()
# 
# 

