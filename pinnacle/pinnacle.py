"""
PINNACLE.

Publications from an Institute: Numbers, Networks, Authors and
Citations Looking for Excellence.

Copyright (c) 2020, Marcelo Lares
MIT License:
https://github.com/IATE-CONICET-UNC/pinnacle/blob/master/LICENSE
"""

import ads
import pandas as pd
import pickle
import numpy as np


class inst_adsentries:
    """
    inst_adsentries (class): Statistics of publications in an Institute.

    Several methods to download and analyze bibliographic data.
    """

    def __init__(self, config):
        """
        Initialize an inst_adsentries object.

        Parameters
        ----------
        config:
        staff:
        pub_auth_all:
        pub_auth_top:
        pub_inst_all:
        pub_inst_top:
        """
        self.config = config.config
        self.staff = []
        self.history = {}
        self.pub_auth_all = {}
        self.pub_auth_top = {}
        self.pub_inst_all = {}
        self.pub_inst_top = {}

    def sanity_check(self):
        """
        Check if config parameters are OK.

        Check if:
        - directories exist
        - files exist
        - required parameters are defined

        COMPLETAR
        """
        return True

    def data_loaded_check(self):
        """
        Check if data has been loaded.

        COMPLETAR.
        """
        return True

    def load_history(self, n_list, year_start):
        """
        Load history for the number of staff members for an institute.

        if interactive (bool) the list is returned.
        """
        self.sanity_check()

        year_end = year_start + len(n_list)
        a = pd.to_datetime(range(year_start, year_end), format='%Y').year

        df = pd.DataFrame()

        df['pop'] = n_list
        df.index = a

        self.history = df

    def load_staff(self, interactive=True):
        """
        Load staff members for an institute.

        if interactive (bool) the list is returned.
        """
        self.sanity_check()

        fname_staff = ''.join([self.config.dir_data, '/',
                               self.config.fname_staff])

        with open(fname_staff) as f:
            auth_names = f.read()
        auth_names = auth_names.split('\n')
        auth_names = auth_names[:-1]

        self.staff = auth_names
        if interactive:
            return auth_names

    def load_inst(self):
        """
        Load bibliographic data from a pickle file.

        Pickle file must be of the type writen by save_inst().
        """
        self.sanity_check()

        fname_pub_auth_all = ''.join([self.config.dir_data, '/',
                                      self.config.fname_pub_auth_all, '_',
                                      self.config.experiment_id, '.pk'])
        fname_pub_auth_top = ''.join([self.config.dir_data, '/',
                                      self.config.fname_pub_auth_top, '_',
                                      self.config.experiment_id, '.pk'])
        fname_pub_inst_all = ''.join([self.config.dir_data, '/',
                                      self.config.fname_pub_inst_all, '_',
                                      self.config.experiment_id, '.pk'])
        fname_pub_inst_top = ''.join([self.config.dir_data, '/',
                                      self.config.fname_pub_inst_top, '_',
                                      self.config.experiment_id, '.pk'])
        self.pub_auth_all = pickle.load(open(fname_pub_auth_all, 'rb'))
        self.pub_auth_top = pickle.load(open(fname_pub_auth_top, 'rb'))
        self.pub_inst_all = pickle.load(open(fname_pub_inst_all, 'rb'))
        self.pub_inst_top = pickle.load(open(fname_pub_inst_top, 'rb'))

        fname_pub_history = ''.join([self.config.dir_data, '/history_',
                                     self.config.experiment_id, '.pk'])
        self.history = pickle.load(open(fname_pub_history, 'rb'))

        fname_pub_staff = ''.join([self.config.dir_data, '/staff_',
                                   self.config.experiment_id, '.pk'])
        self.staff = pickle.load(open(fname_pub_staff, 'rb'))

    def download_inst(self, authors_list=[], rows_max=200):
        """
        download_inst, function.

        Given a list of author names, return a pandas dataframe
        with the list of papers retrieved by the ADSABS service.

        Parameters
        ----------
        authors_list: list or string
            A list containing the names of the authors.

        Returns
        -------
        byauth: dataframe
           A data frame containing the list of authors, number of papers
           and the list of papers as "Article" instances.
        """
        self.staff = authors_list
        fl = ['id', 'bibcode', 'title', 'citation_count',
              'aff', 'author', 'citation', 'pub', 'reference',
              'metrics', 'year', 'read_count', 'pubdate']

        authors = []
        for auth in authors_list:
            print(f"searching ADS for author: {auth}")
            papers = list(ads.SearchQuery(author=auth, rows=rows_max, fl=fl))
            authors.append(papers)

        byauth = pd.DataFrame()
        byauth['authors'] = authors_list
        byauth['ppr_list'] = authors

        # cantidad de papers por autor:
        npprs = []
        for p in authors:
            npprs.append(len(p))
        byauth['n_papers'] = npprs

        # self.byauth = byauth

        return byauth

    def save_inst(self):
        """
        Write bibliographic data to a pickle file.

        The name of the file is taken from self.config.
        """
        self.sanity_check()
        self.data_loaded_check()

        fname_pub_auth_all = ''.join([self.config.dir_data, '/',
                                      self.config.fname_pub_auth_all, '_',
                                      self.config.experiment_id, '.pk'])
        fname_pub_auth_top = ''.join([self.config.dir_data, '/',
                                      self.config.fname_pub_auth_top, '_',
                                      self.config.experiment_id, '.pk'])
        fname_pub_inst_all = ''.join([self.config.dir_data, '/',
                                      self.config.fname_pub_inst_all, '_',
                                      self.config.experiment_id, '.pk'])
        fname_pub_inst_top = ''.join([self.config.dir_data, '/',
                                      self.config.fname_pub_inst_top, '_',
                                      self.config.experiment_id, '.pk'])

        pickle.dump(self.pub_auth_all, open(fname_pub_auth_all, 'wb'))
        pickle.dump(self.pub_auth_top, open(fname_pub_auth_top, 'wb'))
        pickle.dump(self.pub_inst_all, open(fname_pub_inst_all, 'wb'))
        pickle.dump(self.pub_inst_top, open(fname_pub_inst_top, 'wb'))

        fname_pub_history = ''.join([self.config.dir_data, '/history_',
                                     self.config.experiment_id, '.pk'])
        pickle.dump(self.history, open(fname_pub_history, 'wb'))

        fname_pub_staff = ''.join([self.config.dir_data, '/staff_',
                                   self.config.experiment_id, '.pk'])
        pickle.dump(self.staff, open(fname_pub_staff, 'wb'))

    def save_table(self, table_name=None,
                   year_start=None, year_end=None):
        """
        Write bibliographic data to a XLSX file.

        The name of the file is taken from ?
        """
        import pandas as pd

        self.sanity_check()
        self.data_loaded_check()

        if table_name is None:
            table_name = (f"{self.config.dir_data}/"
                          f"table_{self.config.experiment_id}.xlsx")

        print(table_name)

        writer = pd.ExcelWriter(table_name)

        if (year_start is not None) and (year_end is not None):
            tedges = np.arange(1999.5, 2021.5, 1)
            years = np.arange(2000, 2021, 1)
        else:
            tedges = np.arange(self.history.index[0] - 0.5,
                               self.history.index[-1] + 1.5, 1)
            years = np.arange(self.history.index[0],
                              self.history.index[-1] + 1, 1)

        dfa = pd.DataFrame()
        dfa['year'] = years

        Ht = np.zeros(len(years))
        auth_names = list(self.pub_auth_all.author1.unique())
        for a in auth_names:
            df = self.pub_auth_all[self.pub_auth_all['author1'].isin([a])]
            y = [int(i) for i in df.year.values]
            if len(y) == 0:
                H = [[0] * (len(tedges) - 1), None]
            else:
                y = np.array(y)
                H = np.histogram(y, bins=tedges)
            dfa[a] = H[0]
            Ht = Ht + H[0]
        self.history['npapers_all'] = Ht
        dfa.to_excel(writer, sheet_name='top')

        Ht = np.zeros(len(years))
        auth_names = list(self.pub_auth_top.author1.unique())
        for a in auth_names:
            df = self.pub_auth_top[self.pub_auth_top['author1'].isin([a])]
            y = [int(i) for i in df.year.values]
            if len(y) == 0:
                H = [[0] * (len(tedges) - 1), None]
            else:
                y = np.array(y)
                H = np.histogram(y, bins=tedges)
            dfa[a] = H[0]
            Ht = Ht + H[0]
        self.history['npapers_top'] = Ht
        dfa.to_excel(writer, sheet_name='top')

        writer.save()

    def journal_quality(self, custom_list=False):
        """
        Filter non-indexed journals and proceedings.

        This is based on a data file with a journals name list.
        """
        # Obtain the list of all journals and write it to a file
        # df_index = df_papers_inst[~df_papers_inst.duplicated(subset='pub')]
        # filename = '../dat/journals.txt'
        # with open(filename, 'w') as f:
        #     for item in df_index.pub:
        #         f.write("%s\n" % item)

        # edit the file to leave only top indexed journals
        # (delete proceedings, BAAA, etc.)
        if custom_list:
            filename = '../dat/journals_top.txt'
            with open(filename) as f:
                jnames = f.read()
            jnames = jnames.split('\n')
            jnames.pop()

            filt_top_journals = self.pub_auth_all.pub.isin(jnames)
            self.pub_auth_top = self.pub_auth_all[filt_top_journals]

            filt_top_journals = self.pub_inst_all.pub.isin(jnames)
            self.pub_inst_top = self.pub_inst_all[filt_top_journals]

    def reduce_article_list(self, dfi, institution_keys=None):
        """
        Return a DataFrame with a paper-based list of publications.

        Parameters
        ----------
        dfi: DataFrame, with the list of authors.

        f: function
           Given an ads.Article object, return criteria for author
           membership with True/False.

        Returns
        -------
        dfo: DataFrame, with the list of articles.
        """
        self.sanity_check()

        if institution_keys is None:
            institution_keys = self.config.inst_strings

        Ps = []
        for a, x in zip(dfi.authors, dfi.ppr_list):
            for p in x:

                isinst = False
                for aff in p.aff:
                    ncoinc = sum([word in aff for word in institution_keys])
                    thisis = ncoinc > 1
                    isinst = isinst or thisis

                if isinst:
                    t = [a, p.id, p.bibcode, p.title, p.aff, p.author,
                         p.citation, p.pub, p.reference, p.year, p.pubdate,
                         p.citation_count, p.read_count]
                    Ps.append(t)

        names = ['author1', 'id', 'bibcode', 'title', 'aff', 'authors',
                 'citation', 'pub', 'reference', 'year', 'pubdate',
                 'citation_count', 'read_count']
        dfo = pd.DataFrame(Ps, columns=names)

        self.pub_auth_all = dfo

    def get_pub_scores(self, subset='auth_all'):
        """
        Add to the DataFrames information about the quality of the journal.

        Parameters
        ----------
        self
        """
        from nltk.corpus import stopwords
        from nltk.tokenize import word_tokenize
        import csv
        from difflib import SequenceMatcher
        import jellyfish
#        self.sanity_check()

        if subset == 'auth_top':
            pubs = self.pub_auth_top['pub']
        elif subset == 'auth_all':
            pubs = self.pub_auth_all['pub']
        elif subset == 'inst_top':
            pubs = self.pub_inst_top['pub']
        elif subset == 'inst_all':
            pubs = self.pub_inst_all['pub']

        # load publication metrics

        # download stowords the first time
        def similar(a, b):
            return SequenceMatcher(None, a, b).ratio()

        def get_q(s):
            q = 0
            if "Q4" in s:
                q = 4
            if "Q3" in s:
                q = 3
            if "Q2" in s:
                q = 2
            if "Q1" in s:
                q = 1
            return q

        stop_words = set(stopwords.words('english'))

        journals = []
        with open('scimagojr.csv', newline='') as csvfile:
            s = csv.reader(csvfile, delimiter=';')
            for row in s:
                jname = row[2].lower()
                word_tokens = word_tokenize(jname)
                fname = [w for w in word_tokens if w not in stop_words]
                sent1 = ' '.join(fname)
                sent1 = sent1.replace('/', '')
                row[2] = sent1
                journals.append(row)

        Q = []
        for p in pubs:
            jname = p.lower()
            word_tokens = word_tokenize(jname)
            fname = [w for w in word_tokens if w not in stop_words]
            sent1 = ' '.join(fname)
            sent1 = sent1.replace('/', '')

            match = 0
            J = ""
            for Journal in journals:
                journal = Journal[2]
                s1 = similar(sent1, journal)
                s2 = jellyfish.jaro_winkler(sent1, journal)
                if s1 > 0.9 and s2 > 0.9:
                    match += 1
                    J = Journal[-1]
            Q.append(get_q(J))

        if subset == 'auth_top':
            self.pub_auth_top['Q'] = Q
        elif subset == 'auth_all':
            self.pub_auth_all['Q'] = Q
        elif subset == 'inst_top':
            self.pub_inst_top['Q'] = Q
        elif subset == 'inst_all':
            self.pub_inst_all['Q'] = Q

    def get_papers_by_authors(authors_list, rows_max=999):
        """
        get_papers_by_authors, function.

        Make a fresh load of bibliographic data from ADS.
        Given a list of author names, return a pandas dataframe
        with the list of papers retrieved by the ADSABS service.

        Parameters
        ----------
        authors_list: list or string
            A list containing the names of the authors.

        Returns
        -------
        byauth: dataframe
           A data frame containing the list of authors, number of papers
           and the list of papers as "Article" instances.
        """
        fl = ['id', 'bibcode', 'title', 'citation_count',
              'aff', 'author', 'citation', 'pub', 'reference',
              'metrics', 'year', 'read_count', 'pubdate']

        authors = []
        for auth in authors_list:
            print(auth)
            papers = list(ads.SearchQuery(author=auth, rows=rows_max, fl=fl))
            authors.append(papers)

        byauth = pd.DataFrame()
        byauth['authors'] = authors_list
        byauth['ppr_list'] = authors

        # cantidad de papers por autor:
        npprs = []
        for p in authors:
            npprs.append(len(p))
        byauth['n_papers'] = npprs

        return byauth

    def get_papers_by_institution(inst_names):
        """
        get_papers_by_institution, function.

        Given a list of institution names, return a pandas dataframe
        with the list of papers retrieved by the ADSABS service.

        Parameters
        ----------
        inst_names: list or string
            A list containing the alternative names for an institution.

        Returns
        -------
        byauth: dataframe
           A data frame containing the list of papers as "Article" instances.
        """
        papers = list(ads.SearchQuery(aff="IATE"))
        for p in papers:
            print(p.author)
            print(f"Paper from year {p.year} with "
                  f"{len(p.author)} authors and "
                  f"{p.citation_count} citations.")
            input()

    def is_staff_institute(article, institution_keys):
        """
        staff_iate, function.

        Given a paper (python ads class Article), check if there is at
        least one author which is a member of an institution

        Parameters
        ----------
        article: a class Article object (not a list).
            An object with all the information for an article.

        institution_keys: list of strings
        Keywords that the affilliation can contain for a given
        institution.

        Returns
        -------
        isiate: logical
        If True, there is at least one author which is a member of an
        institution.
        """
        isinst = False
        for aff in article.aff:
            thisis = any(word in aff for word in institution_keys)
            isinst = isinst or thisis

        return isinst

    def eliminate_repeated(self, ID):
        """
        eliminate_repeated: function.

        Eliminate repeated entries in a list of papers.

        Parameters
        ----------
        df: Pandas DataFrame

        ID: string
            DataFrame field to be used as identifier for repeated
            entries.

        Returns
        -------
        df_uniq: Pandas DataFrame with the list of papers
        """
        dup = self.pub_auth_all.duplicated(subset='bibcode')
        ndup = [not boolean for boolean in dup]

        # DataFrame with the cleaned list of papers
        self.pub_inst_all = self.pub_auth_all[ndup]
