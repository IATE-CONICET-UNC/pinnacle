import numpy as np
import pickle
import pandas as pd

from matplotlib import pyplot as plt
from plot_styles import *


# #################################################################
# Load data
# #################################################################

byauth = pickle.load(open('../dat/byauth.pk', 'rb'))

df_papers_iate = pickle.load(open('../dat/df_papers_iate.pk', 'rb'))
df_papers_unique = pickle.load(open('../dat/df_papers_unique.pk', 'rb'))
df_papers_unique_top = pickle.load(open('../dat/df_papers_unique_top.pk', 'rb'))



# number of papers per year per author ··························

tedges = np.arange(1999.5, 2021.5, 1)
years = np.arange(2000, 2021, 1)
dfa = pd.DataFrame()
dfa['year'] = years

for a in auth_names:

    df = df_papers_iate[df_papers_iate['author1'].isin([a])]
    y = [int(i) for i in df.year.values]
    if len(y)==0:
        H = [[0]*(len(tedges)-1), None]
    else:
        y = np.array(y)
        H = np.histogram(y, bins=tedges)
    dfa[a] = H[0]

dfa.to_excel('tabla.xlsx')


