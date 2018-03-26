# -*- coding: utf-8 -*-
"""
Query metadata. Get id's of books with given
- language
- author
- subject
- date
- ...

"""

import os 
import pandas as pd
import numpy as np
from collections import Counter


class meta_query(object):

    def __init__(self,path = '../metadata/metadata.csv'):
        self.df = pd.read_csv(path) ## the dataframe on which we apply filters
        self.df_original = self.df ## keep the original dataframe

    def reset(self):
        '''reset df to original dataframe (remove all filters)
        '''
        self.df = self.df_original

    def get_ids(self):
        '''return list of PG-ids of filtered dataframe
        '''
        list_book_ids = self.df['id']
        return list(list_book_ids)

    def get_df(self):
        '''return the filtered dataframe
        '''
        return self.df

    def get_lang(self):
        list_lang = [[k for k in h.strip("[]")[1:-1].replace("', '","_").split('_')] for h in self.df['language'].dropna()]
        list_lang_flat = [item for sublist in list_lang for item in sublist]
        list_lang_set = sorted(list(set(list_lang_flat)))
        return list_lang_set

    def get_subjects(self):
        list_subjects = [[k for k in h.strip("{}")[1:-1].replace("', '","_").split('_')] for h in self.df['subjects'].replace('set()',np.nan).dropna()]
        list_subjects_flat = [item for sublist in list_subjects for item in sublist]
        list_subjects_set = sorted(list(set(list_subjects_flat)))
        return list_subjects_set

    def get_subjects_counts(self):
        list_subjects = [[k for k in h.strip("{}")[1:-1].replace("', '","_").split('_')] for h in self.df['subjects'].replace('set()',np.nan).dropna()]
        list_subjects_flat = [item for sublist in list_subjects for item in sublist]
        return Counter(list_subjects_flat)


    def filter_lang(self,lang_sel,how='only'):
        ## filter metadata for language
        ## how == 'only', books that only contain lang_sel
        ## how == 'any', all books that contain lang_sel (and potentially others too)
        if how == 'only':
            s = self.df[self.df['language'] == "['%s']"%(lang_sel)]
        elif how =='any':
            s = self.df[self.df['language'].str.contains("'%s'"%(lang_sel)).replace(np.nan,False)]
        else:
            s = meta
        self.df = s

    def filter_subject(self,subject_sel,how='only'):
        ## filter metadata for subjects
        ## how == 'only', books that only contain subject
        ## how == 'any', all books that contain subject (and potentially others too)
        if how == 'only':
            s = self.df[self.df['subjects'] == "{'%s'}"%(subject_sel)]
        elif how =='any':
            s = self.df[self.df['subjects'].str.contains("'%s'"%(subject_sel)).replace(np.nan,False)]
        else:
            s = meta
        self.df = s




