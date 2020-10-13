import pandas as pd
import pickle
from os import path
from functools import partial
import ads_utils

"""
The purpose of this code is to make pandas DataFrames containing data
from publications at IATE.

ADS scraping
------------

save the string for the ADS API key in the file "ADS_API_Token".
$ export ADS_DEV_KEY=`more ADS_API_Token`
more info: https://github.com/adsabs/adsabs-dev-api

From this code
--------------

byauth: List of publications for each researcher.
        Keys: 1) author 2) list of papers 3) number of papers

df_papers: Full list of papers retrieved by ADS

df_papers_iate: List of unique papers from all researchers.

df_papers_unique: List of unique papers from all researchers.

df_papers_unique_top: List of unique papers in top indexed journals.


Pipeline
--------

1) Load ADS query
   Download or reload list of papers from ADS query, by author
   -> byauth (dataframe)
2) Make list of all papers from the query
   -> all_papers (list of article objects)
3) Make a filter for non-IATE paper
   -> isiate (list of logicals)
4) Make a dataframe for paper entries and apply IATE filter
   -> df_papers_iate (dataframe)
5) Eliminate duplicated entries
   -> df_papers_unique (dataframe)
6) Filter non-indexed journals and proceedings
   -> df_papers_unique_top (dataframe)

"""

# #################################################################
# Settings
# #################################################################

# run ADS query again?
# WARNING: (if True) This may take some time and run against query limits
qreload = False

# overwrite files?
clobber = False

# make plots?
makeplots = True


# #################################################################
# ( 1 ) Load ADS query
# #################################################################

filename = '../dat/investigadores_iate_LF.csv'
with open(filename) as f:
    auth_names = f.read()
auth_names = auth_names.split('\n')
auth_names = auth_names[:-1]

if path.isfile('../dat/byauth.pk'):
    if qreload:
        byauth = ads_utils.get_papers_by_authors(auth_names)
        if clobber:
            pickle.dump(byauth, open('../dat/byauth.pk', 'wb'))
    else:
        byauth = pickle.load(open('../dat/byauth.pk', 'rb'))
else:
    byauth = ads_utils.get_papers_by_authors(auth_names)
    pickle.dump(byauth, open('../dat/byauth.pk', 'wb'))

# ################################################################
# ( 2 ) Make list of papers
# #################################################################

all_papers = [y for x in byauth.ppr_list for y in x]

author1 = []
for a, n in zip(byauth.authors, byauth.n_papers):
    for i in range(n):
        author1.append(a)

# #################################################################
# ( 3 ) Make a filter for non-IATE papers
# #################################################################

iate = ['IATE', 'Córdoba', 'Laprida 854', 'X5000BGR',
        'Universidad Nacional de Córdoba',
        'Instituto de Astronomía Teórica y Experimental']

f = partial(ads_utils.staff_institute, institution_keys=iate)
isiate = list(map(f, all_papers))
# save this filter for later
pickle.dump(isiate, open('../dat/isiate.pk', 'wb'))

# #################################################################
# ( 4 ) Make dataframe for paper entries and apply iate filter
# #################################################################

# It is easier to clean duplicated entries on a pandas dataframe

names = ['id', 'bibcode', 'title', 'aff', 'authors',
         'citation', 'pub', 'reference', 'year', 'pubdate',
         'citation_count', 'read_count']
nauth = byauth.shape[0]

# Bibliographic records
Ps = []
for i in range(nauth):
    # papers list for a given author
    plst = byauth.ppr_list[i]

    f = []
    for p in plst:

        t = [p.id, p.bibcode, p.title, p.aff, p.author, p.citation,
             p.pub, p.reference, p.year, p.pubdate,
             p.citation_count, p.read_count]
        Ps.append(t)

df_papers = pd.DataFrame(Ps, columns=names)
df_papers['author1'] = author1

# NOTE:
# the df_papers dataframe constains repeated entries, but is usefull to
# analyze metrics by author, using the field author1.

df_papers_iate = df_papers[isiate]

pickle.dump(df_papers_iate, open('../dat/df_papers_iate.pk', 'wb'))

# NOTE:
# Additional impact metrics can be obtained with more queries:
# mr = []
# for i in range(nauth):
#     # papers list for a given author
#     plst = byauth.ppr_list[i]
#     for i, p in enumerate(plst):
#         # A esta parte no la puedo correr por esto:
#         # APIResponseError: '{\n  "error": "Too many requests"\n}\n'
#         b = p.bibcode
#         metrics_query = ads.MetricsQuery(bibcodes=b)
#         metrics_response = metrics_query.execute()
#         mr.append(metrics_response)
# df_papers['metrics'] = mr


# #################################################################
# ( 5 ) Eliminate duplicated entries
# #################################################################

dup = df_papers_iate.duplicated(subset='bibcode')
ndup = [not boolean for boolean in dup]


# DataFrame with the cleaned list of papers
df_papers_unique = df_papers_iate[ndup]

pickle.dump(df_papers_unique, open('../dat/df_papers_unique.pk', 'wb'))


# #################################################################
# ( 6 ) Filter non-indexed journals and proceedings
# #################################################################

# Obtain the list of all journals and write it to a file
df_index = df_papers[~df_papers.duplicated(subset='pub')]
filename = '../dat/journals.txt'
with open(filename, 'w') as f:
    for item in df_index.pub:
        f.write("%s\n" % item)


# edit the file to leave only top indexed journals
# (delete proceedings, BAAA, etc.)
filename = '../dat/journals_top.txt'
with open(filename) as f:
    jnames = f.read()
jnames = jnames.split('\n')
jnames.pop()

filt_top_journals = df_papers_unique.pub.isin(jnames)
df_papers_unique_top = df_papers_unique[filt_top_journals]

pickle.dump(df_papers_unique_top, open('../dat/df_papers_unique_top.pk', 'wb'))
