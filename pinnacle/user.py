from pinnacle import pinnacle
from pinnacle import pub_dataviz

config = {}
config['dir_data'] = '../dat'  # directory for data
config['dir_plot'] = '../plt'  # directory for plots
config['qreload'] = False      # reload ADS query?
config['clobber'] = False      # overwrite pickle files?
config['nrowsmax'] = 200       # maximu number of ADS entries
config['fname_staff'] = 'staff_iate.csv'  # file with staff member names

# load from file ("file") or download from ADS ("ads")
config['data_source'] = 'file'

# roots for data filenames
config['fname_pub_auth_all'] = 'pub_auth_all' 
config['fname_pub_auth_top'] = 'pub_auth_top' 
config['fname_pub_inst_all'] = 'pub_inst_all' 
config['fname_pub_inst_top'] = 'pub_inst_top' 
#----


# Initialize publications container
iate = pinnacle.inst_adsentries(config)

if config['data_source'] == 'file':
    # LOAD FROM FILE
    # load papers from pickle files
    iate.load_inst()

if config['data_source'] == 'ads':
    # QUERY AND DOWNLOAD
    # load staff member names
    staff = iate.load_staff(interactive=True)
    # query and download from ADS server
    DF = iate.download_inst(staf)
    iate_strings = ['IATE', 'Córdoba', 'Laprida 854', 'X5000BGR',
                    'Universidad Nacional de Córdoba',
                    'Instituto de Astronomía Teórica y Experimental']
    #f = partial(iate.is_staff_institute, institution_keys=iate_strings)
    iate.reduce_article_list(DF, iate_strings)  # -> pub_auth_all
    iate.eliminate_repeated('bibcode')          # -> pub_inst_all

    iate.journal_quality()  # -> pub_auth_top, pub_inst_top

    #iate.save_inst()


# PLOTS ··································

viz = pub_dataviz(iate)

viz.papers_histogram(top=True)
viz.papers_histogram(top=False)

viz.cumulative_per_author(top=False, normalize_first=False)
viz.cumulative_per_author(top=False, normalize_first=True)
viz.cumulative_per_author(top=True, normalize_first=False)
viz.cumulative_per_author(top=True, normalize_first=True)

viz.authors_citations_years()
viz.top_proceedings()
