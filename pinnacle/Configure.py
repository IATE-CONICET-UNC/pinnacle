from configparser import ConfigParser

DEFAULT_INI = '../set/configure_template.ini'


def is_number(string):
    try:
        float(string)
        return True
    except ValueError:
        return False
    except TypeError:
        return False


def choice_yn(string, default_choice=None):
    if string.lower() in 'yesitrue':
        choice = True
    elif string.lower() in 'nofalse':
        choice = False
    else:
        if isinstance(default_choice, bool):
            choice = default_choice
        else:
            raise AttributeError('Check Y/N choice')
    return choice


def is_iterable(obj):
    from collections.abc import Iterable
    return isinstance(obj, Iterable)

# Idea: change named tuple by class:
# class parameters:
# initialize with default parameters.


class Parser(ConfigParser):
    """parser class.

    Manipulation of configuration parameters. This method allows to read a
    configuration file or to set parameters
    """

    def __init__(self, argv=None, *args, **kwargs):
        """Initialize a parser.

        Parameters
        ----------
            None
        Returns
        -------
            None
        Raises
        ------
            Instantiate a Parser object.
        """
        super().__init__()
        self.check_file(argv)
        self.read_config_file()

        self.load_config(*args, **kwargs)
        self.check_settings()

    def check_file(self, sys_args=""):
        """Parse paramenters for the simulation from a .ini file.

        Parameters
        ----------
            None

        Raises
        ------
            None

        Returns
        -------
            Updates 'filename' variable in Parser class object.
        """
        from os.path import isfile

        mess = ("Configuration file expected:"
                "\n\t filename or CLI input"
                "\n\t example:  python run_experiment.py"
                f"\n\t {DEFAULT_INI}"
                "\n\t Using default configuration file")
        if isinstance(sys_args, str):
            if isfile(sys_args):
                msg = f"Loading configuration parameters from {sys_args}"
                self.message = msg
                filename = sys_args
            else:
                self.message = "Input argument is not a valid file\
                                Using default configuration file instead"
                filename = DEFAULT_INI

        elif isinstance(sys_args, list):

            if len(sys_args) == 2:
                filename = sys_args[1]

                if isfile(filename):
                    msg = f"Loading configuration parameters from {filename}"
                    self.message = msg
                else:
                    self.message = mess
                    filename = DEFAULT_INI
            else:
                self.message = mess
                filename = DEFAULT_INI

        else:
            self.message = mess
            filename = DEFAULT_INI

        self.filename = filename

    def read_config_file(self):
        """Parse paramenters for the simulation from a .ini file.

        Parameters
        ----------
            None

        Raises
        ------
            None

        Returns
        -------
            None
        """
        self.read(self.filename)

    def load_config(self, keys=None, values=None, *args, **kwargs):
        """Make filenames based on info in config file.

        Parameters
        ----------
            None

        Raises
        ------
            None

        Returns
        -------
        self.filenames: named tuple
            Updates the list of filenames and the list of parameters
            in a Parser class object.
        """
        from collections import namedtuple

        experiment_id = self['experiment']['experiment_ID']

        dir_data = self['files']['dir_data']
        dir_plot = self['files']['dir_plot']           
        qreload = self['files']['qreload']            
        clobber = self['files']['clobber']            
        nrowsmax = self['files']['nrowsmax']           
        fname_staff = self['files']['fname_staff']        
        data_source = self['files']['data_source']        
        fname_pub_auth_all = self['files']['fname_pub_auth_all'] 
        fname_pub_auth_top = self['files']['fname_pub_auth_top'] 
        fname_pub_inst_all = self['files']['fname_pub_inst_all'] 
        fname_pub_inst_top = self['files']['fname_pub_inst_top'] 
        fname_pub = self['files']['fname_pub'] 

        show_progress = self['UX']['show_progress']
        verbose = self['UX']['verbose']
        interactive = self['UX']['interactive']

        inst_strings = []
        for k in self['keys']:
            inst_strings.append(self['keys'][k])

        names = ['experiment_id',
                 'dir_data',
                 'dir_plot',
                 'qreload',
                 'clobber',
                 'nrowsmax',
                 'fname_staff',
                 'data_source',
                 'fname_pub_auth_all',
                 'fname_pub_auth_top',
                 'fname_pub_inst_all',
                 'fname_pub_inst_top',
                 'fname_pub',
                 'inst_strings',
                 'show_progress',
                 'verbose',
                 'interactive'
                 ]

        names = ' '.join(names)
        parset = namedtuple('pars', names)

        res = parset(experiment_id,
                     dir_data,           
                     dir_plot,           
                     qreload,            
                     clobber,            
                     nrowsmax,           
                     fname_staff,        
                     data_source,        
                     fname_pub_auth_all, 
                     fname_pub_auth_top, 
                     fname_pub_inst_all, 
                     fname_pub_inst_top,
                     fname_pub,
                     inst_strings,
                     show_progress,
                     verbose,
                     interactive
                     )

        self.config = res


    def check_settings(self):
        """Check if parameters make sense.

        Parameters
        ----------
            None

        Raises
        ------
            None

        Returns
        -------
            Exception if settings have inconsistencies.
        """
        from os import path, makedirs

        if self.config.verbose:
            print(self.message)
            print('Checking settings...')
