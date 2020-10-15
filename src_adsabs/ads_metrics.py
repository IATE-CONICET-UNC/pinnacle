import numpy as np
import pickle
import pandas as pd

from matplotlib import pyplot as plt
from plot_styles import *


# #################################################################
# Load data
# #################################################################

df_papers_auth = pickle.load(open('../dat/df_papers_auth.pk', 'rb'))
df_papers_auth_top = pickle.load(open('../dat/df_papers_auth_top.pk', 'rb'))
df_papers_inst = pickle.load(open('../dat/df_papers_inst.pk', 'rb'))
df_papers_inst_top = pickle.load(open('../dat/df_papers_inst_top.pk', 'rb'))



# number of papers per year per author ··························

writer = pd.ExcelWriter('tabla.xlsx') #, engine='xlsxwriter')

tedges = np.arange(1999.5, 2021.5, 1)
years = np.arange(2000, 2021, 1)


# --- all journals and proceedings

dfa = pd.DataFrame()
dfa['year'] = years

auth_names = list(df_papers_inst.author1.unique())
for a in auth_names:

    df = df_papers_auth[df_papers_auth['author1'].isin([a])]
    y = [int(i) for i in df.year.values]
    if len(y)==0:
        H = [[0]*(len(tedges)-1), None]
    else:
        y = np.array(y)
        H = np.histogram(y, bins=tedges)
    dfa[a] = H[0]

dfa.to_excel(writer, sheet_name='all')

            
# --- top journals

dfa = pd.DataFrame()
dfa['year'] = years

for a in auth_names:

    df = df_papers_auth_top[df_papers_auth_top['author1'].isin([a])]
    y = [int(i) for i in df.year.values]
    if len(y)==0:
        H = [[0]*(len(tedges)-1), None]
    else:
        y = np.array(y)
        H = np.histogram(y, bins=tedges)
    dfa[a] = H[0]

dfa.to_excel(writer, sheet_name='top')

writer.save()


# sumar totales
# https://pbpython.com/excel-pandas-comp.html
