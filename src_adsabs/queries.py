import ads
import pandas as pd
import pickle
from os import path
import itertools as it

# save the string for the ADS API key in the file "ADS_API_Token".
# $ export ADS_DEV_KEY=`more ADS_API_Token`
# more info: https://github.com/adsabs/adsabs-dev-api


def get_papers_by_authors(authors_list):
    """
    get_papers_by_authors, function

    Given a list of author names, return a pandas dataframe
    with the list of papers retrieved by the ADSABS service.

    Parameters
    ----------
    authors_list: list or string
        A list containing the names of the authors.

    Returns
    -------
    byauth: dataframe
       A data frame containing the list of authors, number of papers
       and the list of papers as "Article" instances.
    """
 
    fl = ['id', 'bibcode', 'title', 'citation_count',
          'aff', 'author', 'citation', 'pub', 'reference',
          'metrics', 'year', 'read_count', 'pubdate']

    authors = []
    for auth in authors_list:
        print(auth)
        papers = list(ads.SearchQuery(author=auth, rows=500, fl=fl))
        authors.append(papers)

    byauth = pd.DataFrame()
    byauth['authors'] = authors_list
    byauth['ppr_list'] = authors
 
    # cantidad de papers por autor:
    npprs = []
    for p in authors:
        npprs.append(len(p))
    byauth['n_papers'] = npprs

    return byauth
             

def get_papers_by_institution(inst_names):
    """
    get_papers_by_institution, function

    Given a list of institution names, return a pandas dataframe
    with the list of papers retrieved by the ADSABS service.

    Parameters
    ----------
    inst_names: list or string
        A list containing the alternative names for an institution.

    Returns
    -------
    byauth: dataframe
       A data frame containing the list of papers as "Article" instances.
    """
 
    papers = list(ads.SearchQuery(aff="IATE"))
    for p in papers:
        print(p.author)
        print(f"Paper from year {p.year} with "
              f"{len(p.author)} authors and "
              f"{p.citation_count} citations.")
        input() 

# #################################################################

# Settings

# run query again?
qreload = False

# overwrite file?
clobber = False
  

# #################################################################
  

# Correr una busqueda por cada autor::::::::::::::::::::::::::::

if path.isfile('../dat/authors.pk'):

    if dataload:
        byauth = pickle.load( open( '../dat/byauth.pk', 'rb' ) )

else:

    filename = '../dat/investigadores_iate_LF.csv'
    with open(filename) as f:
        auth_names = f.read()
    auth_names = auth_names.split('\n')
    auth_names = auth_names[:-1]

    byauth = get_papers_by_authors(auth_names)

    pickle.dump(byauth, open('../dat/byauth.pk', 'wb'))


# ======================================================================

# Lista de papers.

names = ['author', 'id', 'bibcode', 'title', 'aff', 'authors',
         'citation', 'pub', 'reference', 'year', 'pubdate']

nauth = byauth.shape[0]

# Bibliograhic record

iate = ['IATE', 'Experimental', 'Córdoba', 'Laprida', '854',
        'X5000BGR',
        'Universidad Nacional de Córdoba',
        'Instituto de Astronomía Teórica y Experimental'
       ]

filter_iate = []
ps = []
for i in range(nauth):

    # papers list for a given author
    plst = byauth.ppr_list[i]

    author = auth_names[i]

    f = []
    for p in plst:

        isiate = False
        for afs in p.aff:
            isiate = isiate or any(word in afs for word in iate)

        # override filter!!!!
        isiate = True


        f.append(isiate)

        if not isiate:
            continue

        t = [author,
             p.id,
             p.bibcode,
             p.title,
             p.aff,
             p.author,
             p.citation,
             p.pub,
             p.reference,
             p.year,
             p.pubdate]
        ps.append(t)
    filter_iate.append(f)

df_papers = pd.DataFrame(ps, columns=names)


# Impact metrics

cc = []
rc = []
mr = []
for i in range(nauth):

    # papers list for a given author
    plst = byauth.ppr_list[i]

    filter_paper = filter_iate[i]

    for i, p in enumerate(plst):

        if filter_paper[i]:
            cc.append(p.citation_count)
            rc.append(p.read_count)

        # A esta parte no la puedo correr por esto:
        # APIResponseError: '{\n  "error": "Too many requests"\n}\n'
        #b = p.bibcode
        #metrics_query = ads.MetricsQuery(bibcodes=b)
        #metrics_response = metrics_query.execute()
        #mr.append(metrics_response)
 

df_papers['citation_counts'] = cc
df_papers['read_counts'] = rc
#df_papers['metrics'] = mr


# Clean the list for duplicated entries

dup = df_papers.duplicated(subset='bibcode')
ndup = [not l for l in dup]


# DataFrame with the cleaned list of papers
df_papers_unique = df_papers[ndup]



# #################################################################
# Visualization of metrics
# #################################################################


# Number of papers per year ·····································

y = df_papers_unique.year.values
y = [int(a) for a in y]

from matplotlib import pyplot as plt
import numpy as np

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

    mfc = aesthetics["markerfacecolor"]
    mew = aesthetics["markeredgewidth"]
    color=aesthetics["color"],
    linewidth=aesthetics["linewidth"],
    linestyle=aesthetics["linestyle"],
    marker=aesthetics["marker"],
    markerfacecolor=mfc,
    markeredgewidth=mew,
    markersize=aesthetics["markersize"],
    markevery=aesthetics["markevery"],
    alpha=aesthetics["alpha"]
 

    ax.plot(tmeans, ac, label=a, **aesthetics)

ax.set_title('Cumulative papers published by IATE researchers')
ax.set_xlabel('years since first publication')
ax.set_ylabel('cumulative number of papers')
ax.legend(loc=2, ncol=2, fontsize='x-small', frameon=False,
          handlelength=4)
fout = ("../plt/papers_by_author.png")
fig.savefig(fout)
plt.close()


