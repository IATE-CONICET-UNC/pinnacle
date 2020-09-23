import ads
import pandas as pd

# no olvidar hacer:
# $ export ADS_DEV_KEY=`echo more ADS_API_Token`

# Correr una busqueda por cada autor::::::::::::::::::::::::::::

filename = '../dat/investigadores_iate_LF.csv'

with open(filename) as f:
    auths = f.read()

auths = auths.split('\n')
auths = auths[:-1]

iate = pd.DataFrame()
iate['authors'] = auths

pprs = []
for auth in auths:
    papers = list(ads.SearchQuery(author=auth, max_pages=10))
    pprs.append(papers)

# cantidad de papers por autor:

npprs = []
for p in pprs:
    npprs.append(len(p))


# Lista de papers.

ps = []
for a in pprs:
    for p in a:
        t = [p.aff, p.author, p.bibcode, p.citation, p.citation_count,
                p.first_author, p.metrics, p.title, p.year]
        #ps.append(t)



# Buscar por institucion::::::::::::::::::::::::::::::::::::::

#  papers = list(ads.SearchQuery(aff="IATE"))
#  for p in papers:
#      print(p.author)
#      #print(f"Paper from year {p.year} with {len(p.author)} authors and {p.citation_count} citations.")
#      input()
#  
