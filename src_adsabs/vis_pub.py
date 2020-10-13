from matplotlib import pyplot as plt
import numpy as np
import itertools as it
from plot_styles import *


# #################################################################
# Visualization of metrics
# #################################################################

# Number of papers per year ·····································

y = df_papers_unique.year.values
y = [int(a) for a in y]


t = np.arange(int(min(y))-0.5, int(max(y))+0.5, 1)

fig = plt.figure(figsize=(8, 5))
ax = fig.add_subplot()

ax.hist(y, bins=t)
ax.set_xlabel('year')
ax.set_ylabel('published papers')
ax.set_title('Papers published by IATE')
 
fout = ("../plt/papers_per_year.png")
fig.savefig(fout)
plt.close()


# cumulative number of papers per author ··························
# including proceedings

tedges = np.arange(-0.5, 20.5, 1)
tmeans = np.arange(0, 20, 1)

ccolors = ["steelblue"] * 10 + ["peru"] * 10 + ["darkmagenta"] * 10
cmarkers = ["o", ".", "o", "x", "D"]
cstyles = ["-", "-", "--", "--", ":"]
cwidths = [2, 1, 1, 1, 2]
cwidths = [3] * 2 + [1] * 7
cfaces = ccolors[:]
for i, _ in enumerate(cfaces):
    if i % 5 == 0 or i % 5 == 4:
        cfaces[i] = "white"
calpha = [1.0] * 5 + [1.0] * 5 + [1.0] * 5
cmrkevry = [(2, 3), (3, 2), (1, 5)]
icolors = it.cycle(ccolors)
imarkers = it.cycle(cmarkers)
istyles = it.cycle(cstyles)
iwidths = it.cycle(cwidths)
ifaces = it.cycle(cfaces)
ialpha = it.cycle(calpha)
imrkevry = it.cycle(cmrkevry)
aesthetics = {}


fig = plt.figure(figsize=(14, 7))
ax = fig.add_subplot()

for a in auth_names:

    df = df_papers[df_papers['author'].isin([a])]

    y = [int(i) for i in df.year.values]
    y = np.array(y)
    y = y - min(y)

    H = np.histogram(y, bins=tedges)
    ac = H[0].cumsum()

    aesthetics["color"] = next(icolors)
    aesthetics["linewidth"] = next(iwidths)
    aesthetics["linestyle"] = next(istyles)
    aesthetics["marker"] = next(imarkers)
    aesthetics["markerfacecolor"] = next(ifaces)
    aesthetics["markeredgewidth"] = 1
    aesthetics["markersize"] = 6
    aesthetics["markevery"] = next(imrkevry)
    aesthetics["alpha"] = next(ialpha)

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

for a in auth_names:

    df = df_papers_unique_top[df_papers_unique_top['author'].isin([a])]

    y = [int(i) for i in df.year.values]
    if len(y)==0:
        continue
    y = np.array(y)
    y = y - min(y)

    H = np.histogram(y, bins=tedges)
    ac = H[0].cumsum()

    aesthetics["color"] = next(icolors)
    aesthetics["linewidth"] = next(iwidths)
    aesthetics["linestyle"] = next(istyles)
    aesthetics["marker"] = next(imarkers)
    aesthetics["markerfacecolor"] = next(ifaces)
    aesthetics["markeredgewidth"] = 1
    aesthetics["markersize"] = 6
    aesthetics["markevery"] = next(imrkevry)
    aesthetics["alpha"] = next(ialpha)

    ax.plot(tmeans, ac, label=a, **aesthetics)

ax.set_title('Cumulative papers published by IATE researchers')
ax.set_xlabel('years since first publication')
ax.set_ylabel('cumulative number of papers')
ax.legend(loc=2, ncol=2, fontsize='x-small', frameon=False,
          handlelength=6)
fout = ("../plt/papers_by_author_top.png")
fig.savefig(fout)
plt.close()  
