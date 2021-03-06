#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# PUB_DATAVIZ: Visualization tools for PINNACLE
# Copyright (c) 2020, Marcelo Lares
#
# MIT License:
# https://github.com/IATE-CONICET-UNC/pinnacle/blob/master/LICENSE

from matplotlib import pyplot as plt
from pinnacle.plot_styles import cycling_attrs, aes_attrs

import numpy as np
import random


class pub_dataviz:

    def __init__(self, inst):
        '''
        Initialize an instance of a visualizerbecariosthods)
        ----------------

        - papers_histogram: histogram of the years of publications
        - cumulative_per_author: cumulative number of papers per author
        - authors_citations_years: scatter for number of authors and
          citations.
        - top_proceedings: relation between total number of
          publications and papers.
        - number_authors: distribution of the number of authors with
          time.
        '''

        self.inst = inst
        self.config = inst.config

    # def filter_quality(self):

    def papers_histogram(self, top=False, per_auth=False, quality=5):
        '''
        Papers_histogram: histogram of the years of publications

        Parameters
        ----------

        top: bool
             If True, paper in selected journals are used, otherwise,
             all papers.
        '''

        if top:
            y = self.inst.pub_inst_top.year.values
        else:

            # ACA HACER UNA FUNCION PARA FILTRAR CON EL Q

            y = self.inst.pub_inst_all.year.values

        if per_auth:
            y = list(self.inst.history.index)
            Ht = []
            for a in y:
                k = self.inst.history.loc[a][0]
                Ht.append(k)
            w = []
            for i in range(len(Ht)):
                w.append(1/(max(1, Ht[i])))
            sufix = '_norm'
        else:
            y = [int(a) for a in y]
            Ht = np.ones(len(y))
            w = np.ones(len(Ht))
            sufix = ''

        tbreaks = np.arange(int(min(y))-0.5, int(max(y)+1)+0.5, 1)

        fig = plt.figure(figsize=(8, 5))
        ax = fig.add_subplot()

        H = ax.hist(y, bins=tbreaks, weights=w)

        ymax = max(H[0])
        ax.set_ylim(0, ymax)
        ax.grid()

        ax.set_xlabel('year')

        if top:
            ax.set_ylabel('number of papers')
            ax.set_title('publications by IATE')
            fout = (f"{self.config.dir_plot}/"
                    f"papers_per_year_top{sufix}.png")
        else:
            ax.set_ylabel('number of published works')
            ax.set_title('papers published by IATE')
            fout = (f"{self.config.dir_plot}/"
                    f"papers_per_year_all{sufix}.png")

        fig.savefig(fout)
        plt.close()

    def papers_histogram2(self, top=False, per_auth=False):
        '''
        Papers_histogram: histogram of the years of publications

        Parameters
        ----------

        top: bool
             If True, paper in selected journals are used, otherwise,
             all papers.
        '''

        if per_auth:
            y = list(self.inst.history.index)
            npp = []
            for a in y:
                k = self.inst.history.loc[a]
                if top:
                    npp.append(k[2]/max(1, k[0]))
                else:
                    npp.append(k[1]/max(1, k[0]))
            sufix = '_norm'
            hist = npp
        else:
            y = list(self.inst.history.index)
            y = [int(a) for a in y]
            sufix = ''
            tbreaks = np.arange(int(min(y))-0.5, int(max(y)+1)+0.5, 1)
            H = np.histogram(y, bins=tbreaks)
            hist = H[0]

        fig = plt.figure(figsize=(8, 5))
        ax = fig.add_subplot()

        ax.step(y, hist)

        ymax = max(hist)*1.05
        ax.set_ylim(0, ymax)
        ax.grid()

        ax.set_xlabel('year')

        if top:
            ax.set_ylabel('number of papers')
            ax.set_title('publications by IATE')
            fout = (f"{self.config.dir_plot}/"
                    f"papers_per_year_top{sufix}.png")
        else:
            ax.set_ylabel('number of published works')
            ax.set_title('papers published by IATE')
            fout = (f"{self.config.dir_plot}/"
                    f"papers_per_year_all{sufix}.png")

        fig.savefig(fout)
        plt.close()

    def cumulative_per_author(self, top=False, normalize_first=False):
        '''
        Parameters
        ----------

        top: bool
             Use all works or papers from selected journals

        normalize_first: bool
             Normalize to the year of the first publication

        '''
        import datetime
        now = datetime.datetime.now()
        current_year = now.year

        if normalize_first:
            tedges = np.arange(-0.5, 20.5, 1)
            tmeans = np.arange(0, 20, 1)
            fout = (f"{self.config.dir_plot}/papers_by_author_zero.png")
            titlen = 'normalized to first'
            xlab = 'years from first publication'
        else:
            tedges = np.arange(1995, 2021, 1)
            tmeans = np.arange(1995, 2020, 1)
            fout = (f"{self.config.dir_plot}/papers_by_author_year.png")
            titlen = ''
            xlab = 'year'

        if top:
            df = self.inst.pub_auth_top
            titlet = 'papers'
        else:
            df = self.inst.pub_auth_all
            titlet = 'publications'

        fig = plt.figure(figsize=(14, 7))
        ax = fig.add_subplot()
        cycling_attrs()

        y_max = 0
        auth_names = list(df.author1.unique())
        for a in auth_names:

            d = df[df['author1'].isin([a])]

            y = [int(i) for i in d.year.values]
            if len(y) == 0:
                continue
            y = np.array(y)
            if normalize_first:
                active = current_year - min(y) + 1
                y = y - min(y)
                tedges = np.arange(-0.5, active + 0.5, 1)
                tmeans = np.arange(0, active, 1)

            H = np.histogram(y, bins=tedges)
            ac = H[0].cumsum()
            y_max = max(y_max, max(ac))

            aesthetics = aes_attrs()
            ax.plot(tmeans, ac, label=a, **aesthetics)

        title = f'Cumulative {titlet} by IATE researchers {titlen}'
        ax.set_title(title)
        ax.set_xlabel(xlab)
        ax.set_ylabel('cumulative number')
        ax.legend(loc=2, ncol=2, fontsize='small', frameon=False,
                  handlelength=6)
        fig.savefig(fout)
        plt.close()

    def authors_citations_years(self, top=True):
        '''
        Plot a scatter of number of authors and number of citations

        Parameters
        ----------

        top: bool
             Use all works or papers from selected journals
        '''

        if top:
            df = self.inst.pub_inst_top
        else:
            df = self.inst.pub_inst_all

        npapers = df.shape[0]

        na = []
        nc = []
        ye = []
        for i in range(npapers):
            pprs = df.iloc[i]

            nauths = len(pprs.authors)
            ncitas = pprs.citation_count
            year = pprs.year

            r = random.random()*0.6 - 0.3
            na.append(nauths+r)
            r = random.random()*0.6 - 0.3
            nc.append(ncitas+1+r)
            ye.append(int(year))

        y = ((np.array(ye)-1980)*0.2)**2.6

        fig = plt.figure(figsize=(10, 5))
        ax = fig.add_subplot()
        ax.scatter(na, nc, s=y, color=(0, 0, 1, 0.3))

        ax.set_xscale('log')
        ax.set_yscale('log')
        ax.set_xlabel('Number of authors')
        ax.set_ylabel('Number of citations + 1')
        ax.legend(loc='center left', bbox_to_anchor=(1.1, 0.5), labelspacing=3)

        fout = (f"{self.config.dir_plot}/nauth_ncitas_year.png")
        fig.savefig(fout)
        plt.close()

    def top_proceedings(self):
        '''
        Plot a scatter of number of publications vs number of papers

        '''
        tod = []
        top = []

        auth_names = list(self.inst.pub_inst_all.author1.unique())
        for a in auth_names:

            df = self.inst.pub_inst_all
            dfa = df[df['author1'].isin([a])]
            df = self.inst.pub_inst_top
            dft = df[df['author1'].isin([a])]

            tod.append(dfa.shape[0])
            top.append(dft.shape[0])

        fig = plt.figure(figsize=(10, 5))
        ax = fig.add_subplot()
        ax.scatter(tod, top)
        m = max(tod)
        ax.plot([0, m], [0, m])

        ax.set_title('all works vs. top papers')
        ax.set_xlabel('all works')
        ax.set_ylabel('papers top')

        fout = (f"{self.config.dir_plot}/top_vs_all.png")
        fig.savefig(fout)
        plt.close()

    def number_authors(self, top=True):
        '''
        Plot a scatter for the number of authors as a function of time

        Parameters
        ----------

        top: bool
             Use all works or papers from selected journals
        '''

        if top:
            df = self.inst.pub_inst_top
        else:
            df = self.inst.pub_inst_all

        nauth = []
        for i, p in df.iterrows():
            nauth.append(len(p.authors))

        fig = plt.figure(figsize=(10, 5))
        ax = fig.add_subplot()

        years = [int(y) for y in df.year.values]

        ax.scatter(years, nauth)
        ax.set_yscale('log')

        ax.set_title('number of authors per year')
        ax.set_xlabel('year')
        ax.set_ylabel('N authors')

        fout = (f"{self.config.dir_plot}/year_nauth.png")
        fig.savefig(fout)
        plt.close()

    def nauth_npprs(self, top=True):
        fig = plt.figure(figsize=(10, 5))
        ax = fig.add_subplot()

        x = list(self.inst.history.index)
        y = self.inst.history['pop']

        if top:
            z = self.inst.history['npapers_top']
        else:
            z = self.inst.history['npapers_all']

        ax.plot(x, y, label='authors')
        ax.plot(x, z, label='papers')
        ax.legend()
        ax.set_title('number of authors per paper')
        ax.set_xlabel('year')
        ax.set_ylabel('N authors / paper')

        if top:
            ax.set_title('publications by IATE, top papers')
            fout = (f"{self.config.dir_plot}/nauth_npprs_years_top.png")
        else:
            ax.set_title('papers published by IATE, all works')
            fout = (f"{self.config.dir_plot}/nauth_npprs_years_all.png")

        fig.savefig(fout)
        plt.close()

    def plot_all(self):
        '''
        Make all the plots.

        '''
        self.papers_histogram2(top=True)
        self.papers_histogram2(top=False)
        self.papers_histogram2(top=True, per_auth=True)
        self.papers_histogram2(top=False, per_auth=True)

        self.cumulative_per_author(top=False, normalize_first=False)
        self.cumulative_per_author(top=False, normalize_first=True)
        self.cumulative_per_author(top=True, normalize_first=False)
        self.cumulative_per_author(top=True, normalize_first=True)

        self.authors_citations_years()
        self.top_proceedings()
        self.nauth_npprs()
