import pandas as pd
import pickle
from functools import partial
import ads_utils

"""
The purpose of this code is to make pandas DataFrames containing data
for publications from a given institute staff members.

ADS scraping
------------

save the string for the ADS API key in the file "ADS_API_Token".
$ export ADS_DEV_KEY=`more ADS_API_Token`
more info: https://github.com/adsabs/adsabs-dev-api

From this code
--------------

df_papers_auth: List of papers from all researchers (repeated).

df_papers_auth_top: List of papers from all researchers (repeated)
                    in selected (top) journals.

df_papers_inst: List of unique papers from all researchers in the
                institute.

df_papers_inst_top: List of unique papers in selected journals.


Pipeline
--------

1) Load ADS query
   Download or reload list of papers from ADS query, by author
   -> DF (dataframe)
2) Make a dataframe for paper entries from IATE members
   -> df_papers_auth (dataframe)
3) Eliminate duplicated entries
   -> df_papers_inst (dataframe)
4) Filter non-indexed journals and proceedings
   -> df_papers_auth_top
   -> df_papers_inst_top
"""

# #################################################################
# Settings
# #################################################################

# run ADS query again?
# WARNING: (if True) This may take some time and run against query limits
qreload = True

# overwrite files?
clobber = False


# #################################################################
# ( 1 ) Load ADS query
# #################################################################

filename = '../dat/staff_iate.csv'
byauths = ads_utils.ads_query(filename, 200, qreload, clobber)

filename = '../dat/staff_iate_LF_long.csv'
byauthl = ads_utils.ads_query(filename, 999, qreload, clobber)

DF = pd.concat([byauths, byauthl], ignore_index=True)


# ################################################################
# ( 2 ) Make dataframe for paper entries and apply iate filter
# #################################################################

iate = ['IATE', 'Córdoba', 'Laprida 854', 'X5000BGR',
        'Universidad Nacional de Córdoba',
        'Instituto de Astronomía Teórica y Experimental']

f = partial(ads_utils.staff_institute, institution_keys=iate) 

df_papers_auth = ads_utils.reduce_article_list(DF, f)

# NOTE:
# the df_papers dataframe constains repeated entries, but is usefull to
# analyze metrics by author, using the field author1.

pickle.dump(df_papers_auth, open('../dat/df_papers_auth.pk', 'wb'))

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

dup = df_papers_auth.duplicated(subset='bibcode')
ndup = [not boolean for boolean in dup]

# DataFrame with the cleaned list of papers
df_papers_inst = df_papers_auth[ndup]

pickle.dump(df_papers_inst, open('../dat/df_papers_inst.pk', 'wb'))


# #################################################################
# ( 6 ) Filter non-indexed journals and proceedings
# #################################################################

# Obtain the list of all journals and write it to a file
df_index = df_papers_inst[~df_papers_inst.duplicated(subset='pub')]
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

filt_top_journals = df_papers_auth.pub.isin(jnames)
df_papers_auth_top = df_papers_auth[filt_top_journals]
pickle.dump(df_papers_auth_top, open('../dat/df_papers_auth_top.pk', 'wb'))

filt_top_journals = df_papers_inst.pub.isin(jnames)
df_papers_inst_top = df_papers_inst[filt_top_journals]
pickle.dump(df_papers_inst_top, open('../dat/df_papers_inst_top.pk', 'wb'))
