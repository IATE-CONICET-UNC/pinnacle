***************************
Configuration
***************************

All the parameters for the analysis of a set of authors (e.g., an
Institute) can be maintained in one place with a configuration file.

These files are loaded and used as follows::

   ini = 'configuration_file.ini'
   config = Parser(ini)
   df = pinnacle.inst_adsentries(config) 

The content of a configuration file has several sections (the name of
these sections should not be changed).

The first section containts the name for a given ``experiment``.  This is
used for the creation of data files and plots filenames::


   # _____________________________________________________
   [experiment] # EXPERIMENT ID

   # Experiment ID.  Useful to compare and save experiments.
   # A directory will be created with this name under [out]dir_output
   experiment_ID = IATE_ALL


The directories and filenames for data sources and outputs are set in
the ``files`` section::

   # _____________________________________________________
   [files] # DIRECTORIES AND FILE NAMES

   # directory for data
   dir_data = ../dat

   # directory for plots
   dir_plot = ../plt/iate/

   # reload ADS query?
   qreload = False

   # overwrite pickle files?
   clobber = False

   # maximum number of ADS entries
   nrowsmax = 200       

   # filename for staff
   fname_staff = staff_iate_iate.csv

   # load from file ("file") or download from ADS ("ads")
   data_source = file

   # roots for data filenames
   fname_pub_auth_all = pub_auth_all
   fname_pub_auth_top = pub_auth_top
   fname_pub_inst_all = pub_inst_all
   fname_pub_inst_top = pub_inst_top
   fname_pub = pub

The selection of authors by affiliation keywords or keyphrases is made
with a number of strings in the ``keys`` section::

   # _____________________________________________________
   [keys] # KEY STRINGS FOR AFFILIATION FILTERING

   # add as many strins as needed, but use a different index (aff1, aff2, ...)
   aff1 = IATE
   aff2 = Córdoba
   aff3 = Laprida 854
   aff4 = X5000BGR
   aff5 = Universidad Nacional de Córdoba
   aff6 = Instituto de Astronomía Teórica y Experimental


Finally, some flags for the behavior of the standard output::

   # _____________________________________________________
   [UX] # USER EXPERIENCE

   # Show progress bars
   # options: Y/N
   show_progress = y

   # Show messages for partial computations
   # options: Y/N
   verbose = y

   # Return objects (N: only write to files)
   # options: Y/N
   interactive = n 

