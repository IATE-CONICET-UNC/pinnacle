# pinnacle


Run the statistics and create some plots:

Create or load an ADS API key, and save it in a environment variable ADS_DEV_KEY 

::

   import pinnacle
   # create a config dictionary
   iate = pinnacle.inst_adsentries(config)
   iate.load_inst()
   viz = pub_dataviz(iate)
   viz.plot_all()


The task of this project is to analyze the publication metrics in the IATE.
 


Autor
-----

Project by Marcelo Lares (IATE, UNC).  Developed in 2020.      
