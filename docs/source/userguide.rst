***********************
User's guide
***********************

The code is based on the ads package, that allows to perform queries
through a python code.  Objects in pinnacle include the Article class
from ads.

We aim at exploring the publication metrics, relations and networks
for researchers at an institute, in order to design strategies to
increase impact and productivity.

The process basically consists on creating four datasets:

- pub_auth_all
- pub_auth_top
- pub_inst_all
- pub_inst_top


Installation
------------


To install the latest stable version from the Pithon
Package Index::

   pip install pinnacle-pub

To install the development version, download the last version of the code from the GitHub page, and run::

   pip install .



The analysis of a set of authors can be made easily with the following
steps.

First, load the package:

.. code-block:: python

   from pinnacle import pinnacle

For the configuration, create a dictionary with the following fields:

.. code-block:: python

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


Then, it is possible to load the names of the researchers from a file
('fname_staff' entry of config) and load all the publications:

.. code-block:: python

   # Initialize publications container
   iate = pinnacle.inst_adsentries(config)

   if config['data_source'] == 'ads':
       # QUERY AND DOWNLOAD
       # load staff member names
       staff = iate.load_staff(interactive=True)
       staf = staff[4:6]
       # query and download from ADS server
       DF = iate.download_inst(staf)
       iate_strings = ['IATE', 'Córdoba', 'Laprida 854', 'X5000BGR',
                       'Universidad Nacional de Córdoba',
                       'Instituto de Astronomía Teórica y Experimental']
       #f = partial(iate.is_staff_institute, institution_keys=iate_strings)
       iate.reduce_article_list(DF, iate_strings)  # -> pub_auth_all
       iate.eliminate_repeated('bibcode')          # -> pub_inst_all

       iate.journal_quality()  # -> pub_auth_top, pub_inst_top

       iate.save_inst()


The last line creates files with the pickle objects for the datasets.

If the ADS entries have been previously read, the data files can be
loaded easily:

.. code-block:: python

    iate.load_inst()


The plots can be run as follows:

.. code-block:: python

   from pinnacle import pub_dataviz

   viz = pub_dataviz(iate)

   viz.papers_histogram(top=True)
   viz.papers_histogram(top=False)

   viz.cumulative_per_author(top=False, normalize_first=False)
   viz.cumulative_per_author(top=False, normalize_first=True)
   viz.cumulative_per_author(top=True, normalize_first=False)
   viz.cumulative_per_author(top=True, normalize_first=True)

   viz.authors_citations_years()
   viz.top_proceedings()
    
