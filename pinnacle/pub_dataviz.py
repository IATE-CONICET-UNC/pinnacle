#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# PUB_DATAVIZ: Visualization tools for PINNACLE
# Copyright (c) 2020, Marcelo Lares
#
# MIT License:
# https://github.com/IATE-CONICET-UNC/pinnacle/blob/master/LICENSE

from pinnacle import pinnacle
from matplotlib import pyplot as plt
from pinnacle.plot_styles import *

import numpy as np
import pickle
import pandas as pd
import random

class pub_dataviz:

    def __init__(self, inst):
        '''
        Initialize an instance of a visualizer

        Plots: (methods)
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

    def papers_histogram(self, top=False):
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
            y = self.inst.pub_inst_all.year.values


        y = [int(a) for a in y]

        t = np.arange(int(min(y))-0.5, int(max(y))+0.5, 1)

        fig = plt.figure(figsize=(8, 5))
        ax = fig.add_subplot()

        H = ax.hist(y, bins=t)

        ymax = max(H[0])
        ax.set_ylim(0, ymax)
        ax.grid()

        ax.set_xlabel('year')
        
        if top:
            ax.set_ylabel('number of papers')
            ax.set_title('publications by IATE')
            fout = ("../plt/papers_per_year_top.png")
        else:
            ax.set_ylabel('number of published works')
            ax.set_title('papers published by IATE')
            fout = ("../plt/papers_per_year_all.png")

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

        if normalize_first:
            tedges = np.arange(-0.5, 20.5, 1)
            tmeans = np.arange(0, 20, 1)
            fout = ("../plt/papers_by_author_zero.png")
            titlen = 'normalized to first'
            xlab = 'years from first publication'
        else:
            tedges = np.arange(1995, 2021, 1)
            tmeans = np.arange(1995, 2020, 1)
            fout = ("../plt/papers_by_author.png")
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
            if len(y)==0:
                continue
            y = np.array(y)
            y = y - min(y)

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

        fout = ("../plt/nauth_ncitas_year.png")
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
        ax.plot([0,m],[0,m])

        ax.set_title('all works vs. top papers')
        ax.set_xlabel('all works')
        ax.set_ylabel('papers top')

        fout = ("../plt/top_vs_all.png")
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

        fout = ("../plt/year_nauth.png")
        fig.savefig(fout)
        plt.close()  

    def plot_all(self):
        '''
        Make all the plots.

        '''
        self.papers_histogram(top=True)                              
        self.papers_histogram(top=False)                             
        self.cumulative_per_author(top=False, normalize_first=False) 
        self.cumulative_per_author(top=False, normalize_first=True)  
        self.cumulative_per_author(top=True, normalize_first=False)  
        self.cumulative_per_author(top=True, normalize_first=True)   
        self.authors_citations_years()                               
        self.top_proceedings()                                       
 
