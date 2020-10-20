from pinnacle import pinnacle
from pinnacle import pub_dataviz
from openpyxl import load_workbook
import pandas as pd
from pinnacle.Configure import Parser


config_becarios = Parser('becarios.ini')
becarios = pinnacle.inst_adsentries(config_becarios)

if config_becarios.config.data_source=='ads':

    # LOAD staff: becarios
    wb = load_workbook('../dat/staff_iate.xlsx')
    s = wb['Becarios']
    data = s.values
    cols = next(data)
    data = list(data)
    idx = range(len(data))
    staff_becarios = pd.DataFrame(data, index=idx, columns=cols)  
    DF = becarios.download_inst(staff_becarios['ADS_search'].values)
    iate_strings = ['IATE', 'Córdoba', 'Laprida 854', 'X5000BGR',
                    'Universidad Nacional de Córdoba',
                    'Instituto de Astronomía Teórica y Experimental']
    becarios.reduce_article_list(DF, iate_strings)  # -> pub_auth_all
    becarios.eliminate_repeated('bibcode')          # -> pub_inst_all
    becarios.journal_quality()  # -> pub_auth_top, pub_inst_top
    becarios.save_inst()
     
elif config_becarios.config.data_source=='file':

    becarios.load_inst()


config_investigadores = Parser('investigadores.ini')
investigadores = pinnacle.inst_adsentries(config_investigadores)

if config_investigadores.config.data_source=='ads':

    wb = load_workbook('../dat/staff_iate.xlsx')
    s = wb['investigadores']
    data = s.values
    cols = next(data)
    data = list(data)
    idx = range(len(data))
    staff_investigadores = pd.DataFrame(data, index=idx, columns=cols)  
    DF = investigadores.download_inst(staff_investigadores['ADS_search'].values )
    iate_strings = ['IATE', 'Córdoba', 'Laprida 854', 'X5000BGR',
                    'Universidad Nacional de Córdoba',
                    'Instituto de Astronomía Teórica y Experimental']
    investigadores.reduce_article_list(DF, iate_strings)
    investigadores.eliminate_repeated('bibcode')
    investigadores.journal_quality()
    investigadores.save_inst()
     
elif config_investigadores.config.data_source=='file':

    investigadores.load_inst()




# PLOTS: investigadores ····························

investigadores.save_table('table_invetigadores.xlsx')
becarios.save_table('table_becarios.xlsx')

viz = pub_dataviz.pub_dataviz(investigadores)

viz.papers_histogram(top=True)
viz.papers_histogram(top=False)

viz.cumulative_per_author(top=False, normalize_first=False)
viz.cumulative_per_author(top=False, normalize_first=True)
viz.cumulative_per_author(top=True, normalize_first=False)
viz.cumulative_per_author(top=True, normalize_first=True)

viz.authors_citations_years()
viz.top_proceedings()

# PLOTS: becarios ··································

viz = pub_dataviz.pub_dataviz(becarios)

viz.papers_histogram(top=True)
viz.papers_histogram(top=False)

viz.cumulative_per_author(top=False, normalize_first=False)
viz.cumulative_per_author(top=False, normalize_first=True)
viz.cumulative_per_author(top=True, normalize_first=False)
viz.cumulative_per_author(top=True, normalize_first=True)

viz.authors_citations_years()
viz.top_proceedings()      
