# pinnacle

Full documentation here:
[![Documentation Status](https://readthedocs.org/projects/pinnacle/badge/?version=latest)](https://pinnacle.readthedocs.io/en/latest/?badge=latest)


run the statistics and create some plots:

Create or load an ADS API key, and save it in a environment variable ADS_DEV_KEY 

```
import pinnacle

# create a config dictionary

iate = pinnacle.inst_adsentries(config)

iate.load_inst()

viz = pub_dataviz(iate)

viz.plot_all()

```

The task of this project is to analyze the publication metrics in the IATE.
