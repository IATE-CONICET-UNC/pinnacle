from pinnacle import pinnacle
from pinnacle import pub_dataviz
from openpyxl import load_workbook
import pandas as pd
from pinnacle.Configure import Parser

# Load data from institute --------------------------------
wb = load_workbook('staff_iate.xlsx', data_only=True)

data = wb['becarios'].values
columns = next(data)[0:]
df = pd.DataFrame(data, columns=columns)
staff_becarios = df['ADS_search'].values

data = wb['cic'].values
columns = next(data)[0:]
df = pd.DataFrame(data, columns=columns)
staff_cics = df['ADS_search'].values

ws = wb['staff']
data = ws.values
columns = next(data)[0:]
nstaff = list(filter(None, next(data)[1:]))


# Load papers ----------------------------------------------------
config_becarios = Parser('becarios.ini')
becarios = pinnacle.inst_adsentries(config_becarios)
DF = becarios.download_inst(staff_becarios)
becarios.reduce_article_list(DF)
becarios.eliminate_repeated('bibcode')

#becarios.journal_quality()
becarios.get_pub_scores('inst_all')
becarios.get_pub_scores('inst_top')
becarios.get_pub_scores('auth_all')
becarios.get_pub_scores('auth_top')

becarios.load_history(nstaff, int(columns[1]))
becarios.save_inst()



config_cics = Parser('cics.ini')
cics = pinnacle.inst_adsentries(config_cics)
DF = cics.download_inst(staff_cics)
cics.reduce_article_list(DF)
cics.eliminate_repeated('bibcode')

#cics.journal_quality()
cics.get_pub_scores('inst_all')
cics.get_pub_scores('inst_top')
cics.get_pub_scores('auth_all')
cics.get_pub_scores('auth_top')

cics.load_history(nstaff, int(columns[1]))
cics.save_inst()

# ALL ---------------------------------------------
config_iate = Parser('iate.ini')
iate = pinnacle.inst_adsentries(config_iate)
iate.load_history(nstaff, int(columns[1]))
iate.pub_auth_all = pd.concat([cics.pub_auth_all,
                               becarios.pub_auth_all])
iate.pub_auth_top = pd.concat([cics.pub_auth_top,
                               becarios.pub_auth_top])
iate.pub_inst_all = pd.concat([cics.pub_inst_all,
                               becarios.pub_inst_all])
iate.pub_inst_top = pd.concat([cics.pub_inst_top,
                               becarios.pub_inst_top])


iate.load_history(nstaff, int(columns[1]))
iate.save_inst()
