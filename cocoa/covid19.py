# -*- coding: utf-8 -*-

"""
Project : CoCoA
Date :    april-june 2020
Authors : Olivier Dadoun, Julien Browaeys, Tristan Beau
Copyright © CoCoa-team-17
License: See joint LICENSE file

Module : cocoa.covid19
About :

Main class definitions for covid19 dataset access. Currently, we are only using the JHU CSSE data.
The parser class gives a simplier access through an already filled dict of data

"""

import requests
import pandas
from collections import defaultdict
import numpy as np
from datetime import datetime as dt
from datetime import datetime
import datetime
from datetime import timedelta
import pandas as pd
import sys
import cocoa.geo as coge

class DataBase():
    ''' Parse the chosen database and a return a pandas '''
    def __init__(self,db_name):
        self.database_name=['jhu','aphp','owid']
        self.pandas_datase = {}
        self.available_keys_words=[]
        self.dates = []
        self.dicos_countries = {}
        self.dict_sum_data = {}
        self.total_current_cases = {}
        self.diff_days = {}
        self.location_more_info={}
        self.database_columns_not_computed={}
        self.db =  db_name
        if self.db != 'aphp':
            self.geo = coge.GeoManager('name')

        if self.db not in self.database_name:
            print('Unknown ' + self.db + '. Available database so far in CoCoa are : ' + str(self.database_name) ,file=sys.stderr)
        else:
            if self.db == 'jhu':
                print('JHU aka Johns Hopkins database selected ...')
                self.pandas_datase = self.parse_convert_jhu()
            elif self.db == 'aphp':
                print('APHP database selected ...')
                full_pandas = {}
                self.pandas_datase=self.parse_convert_aphp()
                print('... Sante Public will be also parsed ...')
                pandas_santepublic = self.parse_convert_santepublic()
                self.pandas_datase.update(pandas_santepublic)
            elif self.db == 'owid':
                print('OWID aka \"Our World in Data\" database selected ...')
                self.pandas_datase  = self.parse_convert_owid()
            self.fill_cocoa_field()
            print('Available keys words are : ',self.get_available_keys_words())

    def get_db(self):
       return self.db

    def available_keys_wordsbase_name(self):
        ''' Return available database '''
        return self.database_name

    def get_available_keys_words(self):
        ''' Return available keys words for the database selected '''
        return self.available_keys_words

    def get_database_url(self):
        ''' Return the url associated with chosen database '''
        return self.database_url

    def get_rawdata(self):
        ''' Return raw data associated with chosen database '''
        return self.pandas_datase

    def parse_convert_jhu(self):
        ''' For center for Systems Science and Engineering (CSSE) at Johns Hopkins University
            COVID-19 Data Repository by the see homepage: https://github.com/CSSEGISandData/COVID-19 '''
        self.database_url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/"+\
        "csse_covid_19_data/csse_covid_19_time_series/"
        jhu_files_ext = ['deaths', 'confirmed', 'recovered']
        pandas_jhu = {}
        self.available_keys_words = jhu_files_ext
        for ext in jhu_files_ext:
            fileName = "time_series_covid19_" + ext + "_global.csv"
            url = self.database_url + fileName
            pandas_jhu_db = pandas.read_csv(url, sep = ',')
            pandas_jhu_db = pandas_jhu_db.drop(columns=['Province/State','Lat','Long'])
            pandas_jhu_db = pandas_jhu_db.rename(columns={'Country/Region':'location'})
            pandas_jhu_db = pandas_jhu_db.sort_values(by=['location'])
            pandas_jhu_db = pandas_jhu_db.set_index('location')
            self.dates    = pandas.to_datetime(pandas_jhu_db.columns,errors='coerce')
            pandas_jhu[ext] = pandas_jhu_db
        self.dates=[i.strftime('%-m/%-d/%y') for i in self.dates]
        return pandas_jhu

    def parse_convert_aphp(self):
        ''' French data.gouv : APHP hospital data
        homepage: https://www.data.gouv.fr/fr/datasets/donnees-hospitalieres-relatives-a-lepidemie-de-covid-19/
        Parse and convert APHP data structure to JHU one for historical raison
        hosp	Number of people currently hospitalized
        rea  Number of people currently in resuscitation or critical care
        rad	Total amount of patient that returned home
        dc	Total amout of deaths at the hospital
        '''
        self.database_url="https://www.data.gouv.fr/fr/datasets/r/63352e38-d353-4b54-bfd1-f1b3ee1cabd7"
        pandas_aphp_db = pandas.read_csv(self.database_url,sep = ';')

        pandas_aphp_db = pandas_aphp_db.loc[pandas_aphp_db['sexe'] == 0].rename(columns={'dep':'location'})\
        .rename(columns={'jour':'date'}).rename(columns={'rea':'resuscitation'}).rename(columns={'rad':'recovered'}).\
            rename(columns={'dc':'deaths'})
        pandas_aphp_db['date'] = pandas.to_datetime(pandas_aphp_db['date'],errors='coerce')
        self.aphp_date_min , self.aphp_date_max = 0, 0
        self.aphp_date_min,self.aphp_date_max = min(pandas_aphp_db['date']),max(pandas_aphp_db['date'])
        database_columns_not_computed=['date','location','sexe']
        self.available_keys_words = [i for i in pandas_aphp_db.columns.values.tolist() if i not in database_columns_not_computed]
        pandas_aphp={}
        for w in self.available_keys_words:
            pandas_temp   = pandas_aphp_db[['location','date',w]]
            pandas_temp=pandas_temp.groupby(['location','date']).sum()
            pandas_temp.reset_index(inplace=True)
            pandas_temp   = pandas_temp.pivot_table(index='location',values=w,columns='date',dropna=False)
            pandas_temp   = pandas_temp.rename(columns=lambda x: x.strftime('%m/%d/%y'))
            pandas_aphp[w] = pandas_temp
            self.dates    = pandas.to_datetime(pandas_aphp[w].columns,errors='coerce')
        self.dates=[i.strftime('%-m/%-d/%y') for i in self.dates]
        return pandas_aphp


    def parse_convert_santepublic(self):
        ''' French data.gouv : Sante Public
        homepage: https://www.data.gouv.fr/fr/datasets/donnees-relatives-aux-resultats-des-tests-virologiques-covid-19/
        Parse and convert Sante Public data structure to JHU one for historical raison
        T	Number of tests performed
        P	Number of positive tests
        cl_age90	Age class

        '''
        self.database_url="https://www.data.gouv.fr/fr/datasets/r/406c6a23-e283-4300-9484-54e78c8ae675"
        pandas_santepublic_db = pandas.read_csv(self.database_url,sep = ';')
        pandas_santepublic_db=pandas_santepublic_db.loc[pandas_santepublic_db["cl_age90"]==0]
        pandas_santepublic_db = pandas_santepublic_db.rename(columns={'dep':'location'}).rename(columns={'jour':'date'}).\
        rename(columns={'P':'total_cases'}).rename(columns={'T':'total_tests'})
        pandas_santepublic_db['date'] = pandas.to_datetime(pandas_santepublic_db['date'],errors='coerce')
        database_columns_not_computed = ['date','location','cl_age90']
        available_keys_words_pub = [i for i in pandas_santepublic_db.columns.values.tolist() if i not in database_columns_not_computed]
        if min(pandas_santepublic_db['date']) < self.aphp_date_min or max(pandas_santepublic_db['date']) > self.aphp_date_max:
            print("Check the APHP and SantePublique dates ! You shouln't be here ...")
            exit()
        delta_min = min(pandas_santepublic_db['date']) -  self.aphp_date_min
        delta_max = self.aphp_date_max - max(pandas_santepublic_db['date'])
        cp_pandas_santepublic = pandas_santepublic_db.copy()
        cp_pandas_santepublic['date'] = cp_pandas_santepublic['date'].dt.strftime("%m/%d/%y")
        cp_pandas_santepublic = (cp_pandas_santepublic.groupby(['location','date']).sum())
        cp_pandas_santepublic.reset_index(inplace=True)
        pandas_santepublic={}
        for w in available_keys_words_pub:
            pandas_temp   = cp_pandas_santepublic[['location','date',w]]
            pandas_temp.reset_index(inplace=True)
            pandas_temp   = pandas_temp.pivot_table(index='location',values=w,columns='date',dropna=False)
            a= np.nan*pandas_temp.shape[0]
            for i in range(delta_min.days):
                days=self.aphp_date_min + timedelta(days=i)
                pandas_temp.insert(loc=0+i,column=days.strftime("%m/%d/%y"),value=a)
                last_column=len(pandas_temp.columns)
            for i in range(0,delta_max.days):
                days=max(pandas_santepublic_db['date']) + timedelta(days=i+1)
                pandas_temp.insert(loc=last_column+i,column=days.strftime("%m/%d/%y"),value=a)
            pandas_santepublic[w] = pandas_temp
            self.dates    = pandas.to_datetime(pandas_santepublic[w].columns,errors='coerce')
            self.dates=[i.strftime('%-m/%-d/%y') for i in self.dates]
        self.available_keys_words += available_keys_words_pub
        return pandas_santepublic


    def parse_convert_owid(self):
        ''' Our World in Data
        homepage: https://ourworldindata.org/coronavirus
        Parse and convert OWID aka \"Our World in Data\"  to JHU one for historical raison
        https://github.com/owid/covid-19-data/blob/master/public/data/owid-covid-data-codebook.md '''
        self.pandas_datase = {}
        self.database_url="https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv"
        pandas_owid_db   = pandas.read_csv(self.database_url,sep = ',')
        pandas_owid_db   = pandas_owid_db.sort_values(by=['location','date'])
        pandas_owid_db['date'] = pd.to_datetime(pandas_owid_db['date'],errors='coerce')
        # Drop tests_units : Units used by the location to report its testing data
        pandas_owid_db  = pandas_owid_db.drop(columns=['tests_units'])
        self.available_keys_words = ['total_cases', 'new_cases', 'total_deaths','new_deaths', 'total_cases_per_million',
        'new_cases_per_million', 'total_deaths_per_million','new_deaths_per_million',  'new_tests',
        'total_tests_per_thousand', 'new_tests_per_thousand', 'new_tests_smoothed', 'new_tests_smoothed_per_thousand','stringency_index']
        self.database_columns_for_index = [i for i in pandas_owid_db.columns.values.tolist() if i not in self.available_keys_words]
        pandas_owid =  {}
        pandas_owid_db = pandas_owid_db[pandas_owid_db['location'] != 'International' ]
        pandas_owid_db = pandas_owid_db[pandas_owid_db['location'] != 'World' ]

        for w in self.get_available_keys_words():
            pandas_owid_temp = pandas_owid_db[['location','date',w]]
            pandas_owid_temp = pandas_owid_temp.set_index('location')
            pandas_owid_temp = pandas_owid_temp.pivot_table(index='location',values=w,columns='date',dropna=False)
            pandas_owid_temp = pandas_owid_temp.rename(columns=lambda x: x.strftime('%m/%d/%y'))
            pandas_owid[w] = pandas_owid_temp
            self.dates    = pandas.to_datetime(pandas_owid[w] .columns,errors='coerce')
        self.dates=[i.strftime('%-m/%-d/%y') for i in self.dates]
        return pandas_owid

    def fill_cocoa_field(self):
        ''' Fill CoCoA variables with database data '''
        df = self.get_rawdata()
        for w in self.get_available_keys_words():
            self.dicos_countries[w] = defaultdict(list)
            #for index, row in df[w].iterrows():iterows to slow
            dict_copy = df[w].to_dict('split')
            d_loca = dict_copy['index']
            d_date = dict_copy['columns']
            d_data = dict_copy['data']
            if self.db != 'aphp':
                d_loca=self.geo.to_standard(list(d_loca),output='list',db=self.get_db(),interpret_region=True)
            for i in range(len(d_loca)):
                location=d_loca[i]
                temp=[]
                val=d_data[i]
                self.dicos_countries[w][d_loca[i]].append(d_data[i])
            self.dict_sum_data[w] = defaultdict(list)
            self.total_current_cases[w] = defaultdict(list)
            self.diff_days[w] = defaultdict(list)
            for location in self.dicos_countries[w]:
                res = [sum(i) for i in zip(*self.dicos_countries[w][location])]
                self.dict_sum_data[w][location].append(res)
                self.dict_sum_data[w][location] = self.flat_list(self.dict_sum_data[w][location])
                self.diff_days[w][location] = [j-i for i, j in zip(self.dict_sum_data[w][location][:-1],self.dict_sum_data[w][location][1:])]
                self.diff_days[w][location].insert(0, 0)
                self.diff_days[w][location] = np.array(self.diff_days[w][location])

    def set_more_db_info(self,country,val):
        self.location_more_info[country]=val

    def get_more_db_info(self,country):
        return self.location_more_info[country]

    def flat_list(self, matrix):
        flatten_matrix = []
        for sublist in matrix:
            for val in sublist:
                flatten_matrix.append(val)
        return flatten_matrix

    def get_cumul_days(self):
        return self.dict_sum_data

    def get_diff_days(self):
        return self.diff_days

    def get_dates(self):
        return self.dates

    def get_locations(self):
        return np.array(tuple(self.get_diff_days()[self.available_keys_words[0]].keys()))

    def get_stats(self, **kwargs):
        if not isinstance(kwargs['location'], list):
            clist = [kwargs['location']]
        else:
            clist = kwargs['location']

        if self.db != 'aphp':
            clist=self.geo.to_standard(clist,output='list',interpret_region=True)

        diffout = np.array(
            tuple(dict((c, self.get_diff_days()[kwargs['which']][c]) for c in clist).values()))
        sumout = np.array(tuple(dict(
            (c, (self.get_cumul_days()[kwargs['which']][c])) for c in clist).values()))

        option = kwargs.get('option', None)
        ascend = kwargs.get('ascending', True)
        if option == 'nonneg':
            diffout = np.array(diffout, dtype=float)
            sumout = np.array(sumout, dtype=float)
            for c in range(diffout.shape[0]):
                yy = np.array(diffout[c, :], dtype=float)
                for kk in np.where(yy < 0)[0]:
                    k = int(kk)
                    val_to_repart = -yy[k]
                    if k < np.size(yy)-1:
                        yy[k] = (yy[k+1]+yy[k-1])/2
                    else:
                        yy[k] = yy[k-1]
                    val_to_repart = val_to_repart + yy[k]
                    s = np.sum(yy[0:k])
                    yy[0:k] = yy[0:k]*(1-float(val_to_repart)/s)
                diffout[c, :] = yy
                sumout[c, :] = np.cumsum(yy)
        output = kwargs.get('output',None)
        if kwargs['type'] == 'Cumul':
            out = sumout
        elif kwargs['type'] == 'Diff':
            out = diffout
        else:
            raise TypeError(
                "Invalid keyword type argument %s , waiting for Cumul or Diff." % key)

        datos=[dt.strptime(d, '%m/%d/%y') for d in self.get_dates()]
        if ascend == False:
            datos = datos[::-1]
            if out.shape[0] == 1:
                out = out[0][::-1]
                out = np.array(out)
            else:
                out = out[::-1]

        if output == "pandas":
            i = 0
            temp=[]
            for coun in clist:
                if len(out[i]):
                    data = {
                        'location':[coun]*len(out[i]),
                        'date': datos,
                        kwargs['which']: out[i]
                        }
                    temp.append(pd.DataFrame(data))
                i+=1
            return pd.concat(temp)
        else:
            if out.shape[0] == 1:
                return out[0]
            else:
                return out.T

    def coherent_remove_nan(self,df):
        ''' Find all dates where there are a NaN value and remove all row
        according to this date , this is for coherent sum analyse stuff '''
        which=df.columns[-1]
        index = df[df[which].apply(np.isnan)]
        if index.empty == False:
            to_remove=(index['date'].values)
            df = df.loc[~df['date'].isin(to_remove)]
        return df

    def cumul_over_several_days(self,df,nb_days):
        ''' return a cumulative pandas sum over nb_days'''
        which=df.columns[-1]
        df=self.coherent_remove_nan(df)
        df = df.groupby('date').agg({which:'sum'})
        df=df.reset_index()
        return df.sort_values('date',ascending=True).rolling(str(nb_days)+'D', on='date').sum()
