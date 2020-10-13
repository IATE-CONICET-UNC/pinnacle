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



# #################################################################
# Visualization of metrics
# #################################################################

# Number of papers and proceedings per year ··························

y = df_papers_unique.year.values
y = [int(a) for a in y]

t = np.arange(int(min(y))-0.5, int(max(y))+0.5, 1)

fig = plt.figure(figsize=(8, 5))
ax = fig.add_subplot()

ax.hist(y, bins=t)
ax.set_xlabel('year')
ax.set_ylabel('published works')
ax.set_title('works published by IATE')
 
fout = ("../plt/papers_per_year.png")
fig.savefig(fout)
plt.close()

# Number of papers in top journals per year ·································

y = df_papers_unique_top.year.values
y = [int(a) for a in y]

t = np.arange(int(min(y))-0.5, int(max(y))+0.5, 1)

fig = plt.figure(figsize=(8, 5))
ax = fig.add_subplot()

ax.hist(y, bins=t)
ax.set_xlabel('year')
ax.set_ylabel('published papers')
ax.set_title('Papers published by IATE in top journals')
 
fout = ("../plt/papers_top_per_year.png")
fig.savefig(fout)
plt.close()


# cumulative number of papers per author ··························
# including proceedings

tedges = np.arange(-0.5, 20.5, 1)
tmeans = np.arange(0, 20, 1)

fig = plt.figure(figsize=(14, 7))
ax = fig.add_subplot()
cycling_attrs()
      
auth_names = list(byauth.authors)
for a in auth_names:

    df = df_papers_iate[df_papers_iate['author1'].isin([a])]

    y = [int(i) for i in df.year.values]
    if len(y)==0:
        continue
    y = np.array(y)
    y = y - min(y)

    H = np.histogram(y, bins=tedges)
    ac = H[0].cumsum()

    aesthetics = aes_attrs()
    ax.plot(tmeans, ac, label=a, **aesthetics)

ax.set_title('Cumulative papers published by IATE researchers')
ax.set_xlabel('years since first publication')
ax.set_ylabel('cumulative number of papers')
ax.legend(loc=2, ncol=2, fontsize='x-small', frameon=False,
          handlelength=6)
fout = ("../plt/papers_by_author.png")
fig.savefig(fout)
plt.close()


# cumulative number of papers per author ··························
# excluding proceedings

tedges = np.arange(-0.5, 20.5, 1)
tmeans = np.arange(0, 20, 1)

fig = plt.figure(figsize=(14, 7))
ax = fig.add_subplot()
cycling_attrs()

for a in auth_names:

    df = df_papers_unique_top[df_papers_unique_top['author1'].isin([a])]

    y = [int(i) for i in df.year.values]
    if len(y)==0:
        continue
    y = np.array(y)
    y = y - min(y)

    H = np.histogram(y, bins=tedges)
    ac = H[0].cumsum()

    aesthetics = aes_attrs()
    ax.plot(tmeans, ac, label=a, **aesthetics)

ax.set_title('Cumulative papers published by IATE researchers')
ax.set_xlabel('years since first publication')
ax.set_ylabel('cumulative number of papers')
ax.legend(loc=2, ncol=2, fontsize='x-small', frameon=False,
          handlelength=6)
fout = ("../plt/papers_by_author_top.png")
fig.savefig(fout)
plt.close()  


# number of authors vs citations vs years ·······················

npapers = df_papers_unique_top.shape[0]

na = []
nc = []
ye = []
for i in range(npapers):
    df = df_papers_unique_top.iloc[i]

    nauths = len(df.authors)
    ncitas = df.citation_count
    year = df.year
    na.append(nauths)
    nc.append(ncitas+1)
    ye.append(int(year))

y = ((np.array(ye)-1980)*0.5)**2

fig = plt.figure(figsize=(14, 7))
ax = fig.add_subplot()
ax.scatter(na, nc, s=y, color=(0, 0, 1, 0.3))

ax.set_xscale('log')
ax.set_yscale('log')
ax.set_xlabel('Number of authors')
ax.set_ylabel('Number of citations + 1')
ax.legend(loc='center left', bbox_to_anchor=(1.1, 0.5), labelspacing=3)

fout = ("../plt/nauth_ncitas_year.png")
fig.savefig(fout)
plt.close()  

