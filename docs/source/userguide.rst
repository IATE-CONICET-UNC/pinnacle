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

along with entries with data for the institute and the authors:

- history
- staff


Installation
------------

To install the `latest stable <https://pypi.org/project/pinnacle-pub/>`_ version from the Python
Package Index::

   pip install pinnacle_pub

To install the development version, 
`download the last version <https://github.com/IATE-CONICET-UNC/pinnacle>`_
of the code from the GitHub page, and run::

   pip install .


API usage
------------

The analysis of a set of authors can be made easily with the following
steps.

First, load the package:

.. code-block:: python

   from pinnacle import pinnacle

For the configuration, edit a configuration file following the
template in the set directory, and load it with the Parser.

.. code-block:: python

    ini = 'my_institute.ini'
    config = Parser(ini)
    df = pinnacle.inst_adsentries(config)

The set of the names of the researchers can be loaded with different
tools, from Excell spreadsheets, CSV files, or entered manually as
lists.

.. code-block:: python

   DF = staff.download_inst(staff_staff)
   staff.reduce_article_list(DF)
   staff.eliminate_repeated('bibcode')
   staff.journal_quality()
   staff.load_history(nstaff, int(columns[1]))
   staff.save_inst() 

It not necesary to make this every time, since pickle files are saved.
After the first run, the dataset can be loaded simply using::

    staff.load_inst()

The number of papers per author per year can be obtained in a
dataframe or an XLSX file with::

    staff.save_table()

Finally, plotting tools are available with the ``pub_dataviz`` class,
that inherites the data from a ``inst_adsentries`` class::

    viz = pub_dataviz.pub_dataviz(df)

There are several plots that can be obtained.  The full set is
produced with::

    viz.plot_all()

Or, alternatiely, individual plots using the function in the class.



