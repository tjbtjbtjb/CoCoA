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

import pandas
from collections import defaultdict
import numpy as np
from datetime import datetime as dt
import pandas as pd
import sys
from cocoa.verb import info,verb
import cocoa.geo as coge
from cocoa.error import *
from scipy import stats as sps
import random

class DataBase():
    ''' Parse the chosen database and a return a pandas '''
    def __init__(self,db_name):
        verb("Init of covid19.DataBase()")
        self.database_name=['jhu','spf','owid','opencovid19']
        self.pandas_datase = {}
        self.available_keys_words=[]
        self.dates = []
        self.dicos_countries = {}
        self.dict_current_days = {}
        self.dict_cumul_days = {}
        self.dict_diff_days = {}
        self.location_more_info={}
        self.database_columns_not_computed={}
        self.db =  db_name
        if self.db != 'spf' and self.db != 'opencovid19':
            self.geo = coge.GeoManager('name')

        if self.db not in self.database_name:
            raise CocoaDbError('Unknown ' + self.db + '. Available database so far in CoCoa are : ' + str(self.database_name) ,file=sys.stderr)
        else:
            if self.db == 'jhu':
                info('JHU aka Johns Hopkins database selected ...')
                self.pandas_datase = self.parse_convert_jhu()
            elif self.db == 'spf':
                info('SPF aka Sante Publique France database selected ...')
                info('... tree differents db from SPF will be parsed ...')
                # https://www.data.gouv.fr/fr/datasets/donnees-hospitalieres-relatives-a-lepidemie-de-covid-19/
                # Parse and convert spf data structure to JHU one for historical raison
                # hosp Number of people currently hospitalized
                # rea  Number of people currently in resuscitation or critical care
                # rad      Total amount of patient that returned home
                # dc       Total amout of deaths at the hospital
                # 'sexe' == 0 male + female
                cast={'dep':'string'}
                rename={'jour':'date','dep':'location'}
                constraints={'sexe':0}
                spf1=self.csv_to_pandas_index_location_date("https://www.data.gouv.fr/fr/datasets/r/63352e38-d353-4b54-bfd1-f1b3ee1cabd7",
                              rename_columns=rename,constraints=constraints,cast=cast)
                # https://www.data.gouv.fr/fr/datasets/donnees-hospitalieres-relatives-a-lepidemie-de-covid-19/
                # incid_hosp	string 	Nombre quotidien de personnes nouvellement hospitalisées
                # incid_rea	integer	Nombre quotidien de nouvelles admissions en réanimation
                # incid_dc	integer	Nombre quotidien de personnes nouvellement décédées
                # incid_rad	integer	Nombre quotidien de nouveaux retours à domicile
                spf2=self.csv_to_pandas_index_location_date("https://www.data.gouv.fr/fr/datasets/r/6fadff46-9efd-4c53-942a-54aca783c30c",
                              rename_columns=rename,cast=cast)
                # https://www.data.gouv.fr/fr/datasets/donnees-relatives-aux-resultats-des-tests-virologiques-covid-19/
                # T       Number of tests performed
                # P       Number of positive tests
                constraints={'cl_age90':0}
                spf3=self.csv_to_pandas_index_location_date("https://www.data.gouv.fr/fr/datasets/r/406c6a23-e283-4300-9484-54e78c8ae675",
                              rename_columns=rename,constraints=constraints,cast=cast)

                #https://www.data.gouv.fr/fr/datasets/indicateurs-de-suivi-de-lepidemie-de-covid-19/#_
                # tension hospitaliere
                # Vert : taux d’occupation compris entre 0 et 40% ;
                # Orange : taux d’occupation compris entre 40 et 60% ;
                # Rouge : taux d'occupation supérieur à 60%.
                # R0
                # vert : R0 entre 0 et 1 ;
                # Orange : R0 entre 1 et 1,5 ;
                # Rouge : R0 supérieur à 1,5.
                cast={'departement':'string'}
                rename={'extract_date':'date','departement':'location'}
                columns_skipped=['region','libelle_reg','libelle_dep','tx_incid_couleur','R_couleur',\
                'taux_occupation_sae_couleur','tx_pos_couleur','nb_orange','nb_rouge']
                spf4=self.csv_to_pandas_index_location_date("https://www.data.gouv.fr/fr/datasets/r/4acad602-d8b1-4516-bc71-7d5574d5f33e",
                            rename_columns=rename, separator=',', encoding = "ISO-8859-1",cast=cast)
                result = pd.concat([spf1, spf2,spf3,spf4], axis=1, sort=False)
                self.pandas_datase = self.pandas_index_location_date_to_jhu_format(result,columns_skipped=columns_skipped)
            elif self.db == 'opencovid19':
                info('OPENCOVID19 selected ...')
                rename={'jour':'date','maille_nom':'location'}
                constraints={'granularite':'pays'}
                columns_skipped = ['maille_code','source_nom','source_url','source_archive','source_type']
                opencovid19 = self.csv_to_pandas_index_location_date('https://raw.githubusercontent.com/opencovid19-fr/data/master/dist/chiffres-cles.csv',
                           constraints=constraints,rename_columns=rename,separator=',')
                self.pandas_datase = self.pandas_index_location_date_to_jhu_format(opencovid19,columns_skipped=columns_skipped)
            elif self.db == 'owid':
                info('OWID aka \"Our World in Data\" database selected ...')
                columns_keeped = ['total_cases', 'new_cases', 'total_deaths','new_deaths', 'total_cases_per_million',
                'new_cases_per_million', 'total_deaths_per_million','new_deaths_per_million', 'total_tests', 'new_tests',
                'total_tests_per_thousand', 'new_tests_per_thousand', 'new_tests_smoothed', 'new_tests_smoothed_per_thousand','stringency_index']
                drop_field = {'location':['International','World']}
                owid = self.csv_to_pandas_index_location_date("https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv",
                separator=',',drop_field=drop_field)
                self.pandas_datase = self.pandas_index_location_date_to_jhu_format(owid,columns_keeped=columns_keeped)
            self.fill_cocoa_field()
            info('Few information concernant the selected database : ', self.get_db())
            info('Available which key-words for: ',self.get_available_keys_words())
            if self.get_db() != 'opencovid19':
                info('Example of location : ',  ', '.join(random.choices(self.get_locations(), k=5)), ' ...')
            else:
                info('Only available location: ', self.get_locations())
            info('Last date data ', self.get_dates()[-1])


    def get_db(self):
        ''' Return database name '''
        return self.db

    def get_available_database(self):
        ''' Return available COVID database '''
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
        self.dates=[i.strftime('%m/%d/%y') for i in self.dates]
        return pandas_jhu

    def csv_to_pandas_index_location_date(self,url,**kwargs):
        '''
        Parse and convert CSV file to a pandas with location+date as an index
        '''
        self.database_url=url
        cast = kwargs.get('cast', None)
        dico_cast = {}
        if cast:
            for key,val in cast.items():
                dico_cast[key] = val
        separator = kwargs.get('separator', ';')
        if separator:
            separator = separator
        encoding = kwargs.get('encoding', None)
        if encoding:
            encoding = encoding
        pandas_db = pandas.read_csv(self.database_url,sep=separator,dtype=dico_cast, encoding = encoding )

        constraints = kwargs.get('constraints', None)
        rename_columns = kwargs.get('rename_columns', None)
        drop_field = kwargs.get('drop_field', None)
        if constraints:
            for key,val in constraints.items():
                pandas_db = pandas_db.loc[pandas_db[key] == val]
                pandas_db = pandas_db.drop(columns=key)
        if drop_field:
            for key,val in drop_field.items():
                for i in val:
                    pandas_db =  pandas_db[pandas_db[key] != i ]
        if rename_columns:
            for key,val in rename_columns.items():
                pandas_db = pandas_db.rename(columns={key:val})
        pandas_db['date'] = pandas.to_datetime(pandas_db['date'],errors='coerce')
        #pandas_db['date'] = pandas_db['date'].dt.strftime("%m/%d/%y")
        pandas_db = pandas_db.sort_values(['location','date'])
        pandas_db = pandas_db.groupby(['location','date']).first()

        return pandas_db

    def pandas_index_location_date_to_jhu_format(self,mypandas,**kwargs):
        '''
        Return a pandas in CoCoa Structure
        '''
        columns_skipped = kwargs.get('columns_skipped', None)
        columns_keeped  = kwargs.get('columns_keeped', None)
        database_columns_not_computed = ['date','location']
        available_keys_words_pub = [i for i in mypandas.columns.values.tolist() if i not in database_columns_not_computed]
        if columns_skipped:
            for col in columns_skipped:
                database_columns_not_computed.append(col)
            available_keys_words_pub = [i for i in mypandas.columns.values.tolist() if i not in database_columns_not_computed]
        if columns_keeped:
           available_keys_words_pub = columns_keeped
        self.available_keys_words = available_keys_words_pub
        mypandas.reset_index(inplace=True)
        pandas_dico = {}
        for w in available_keys_words_pub:
            pandas_temp   = mypandas[['location','date',w]]
            pandas_temp.reset_index(inplace=True)
            pandas_temp   = pandas_temp.pivot_table(index='location',values=w,columns='date',dropna=False)
            #pandas_temp   = pandas_temp.rename(columns=lambda x: x.strftime('%m/%d/%y'))
            pandas_dico[w] = pandas_temp
            self.dates    = pandas.to_datetime(pandas_dico[w].columns,errors='coerce')
            self.dates    = [i.strftime('%m/%d/%y') for i in self.dates]
        return pandas_dico

    def fill_cocoa_field(self):
        ''' Fill CoCoA variables with database data '''
        df = self.get_rawdata()
        #self.dicos_countries = defaultdict(list)

        one_time_enough = False
        for keys_words in self.available_keys_words:
                self.dicos_countries[keys_words] = defaultdict(list)
                self.dict_current_days[keys_words] = defaultdict(list)
                self.dict_cumul_days[keys_words] = defaultdict(list)
                self.dict_diff_days[keys_words] = defaultdict(list)

                if self.db != 'jhu' : # needed since not same nb of rows for deaths,recovered and confirmed
                    if one_time_enough == False:
                        d_loc  = df[keys_words].to_dict('split')['index']
                        if self.db != 'spf' and self.db != 'opencovid19' and one_time_enough == False:
                            d_loc=self.geo.to_standard(list(d_loc),output='list',db=self.get_db(),interpret_region=True)
                        one_time_enough = True
                else :
                    d_loc  = df[keys_words].to_dict('split')['index']
                    if self.db != 'spf' and self.db != 'opencovid19' and one_time_enough == False:
                        d_loc=self.geo.to_standard(list(d_loc),output='list',db=self.get_db(),interpret_region=True)

                d_data = df[keys_words].to_dict('split')['data']
                {self.dicos_countries[keys_words][loc].append(data) for loc,data in zip(d_loc,d_data)}

                self.dict_current_days[keys_words] = {loc:list(np.sum(data, 0)) for loc,data in \
                self.dicos_countries[keys_words].items()}

                self.dict_cumul_days[keys_words] = {loc: np.nancumsum(data) for loc,data in \
                self.dict_current_days[keys_words].items()}

                self.dict_diff_days[keys_words] = {loc: np.insert(np.diff(data),0,0) for loc,data in \
                self.dict_current_days[keys_words].items()}


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

    def get_current_days(self):
        return self.dict_current_days

    def get_cumul_days(self):
        return self.dict_cumul_days

    def get_diff_days(self):
        return self.dict_diff_days

    def get_dates(self):
        ''' Return all dates available in the current database'''
        return self.dates

    def get_locations(self):
        ''' Return available location countries / regions in the current database '''
        return np.array(tuple(self.get_diff_days()[self.available_keys_words[0]].keys()))

    def get_stats(self, **kwargs):
        if not isinstance(kwargs['location'], list):
            clist = ([kwargs['location']]).copy()
        else:
            clist = (kwargs['location']).copy()

        if self.db != 'spf' and self.db != 'opencovid19':
            clist=self.geo.to_standard(clist,output='list',interpret_region=True)

        output = kwargs.get('output','pandas')
        process_data = kwargs.get('type', None)

        if kwargs['which'] not in self.get_available_keys_words() :
            raise CocoaKeyError(kwargs['which']+' is not a available for' + self.db + 'database name. '
            'See get_available_keys_words() for the full list.')

        diff_locations = list(set(clist) - set(self.get_locations()))
        clist = [i for i in clist if i not in diff_locations]
        currentout = np.array(tuple(dict(
            (c, (self.get_current_days()[kwargs['which']][c])) for c in clist).values()))
        cumulout = np.array(tuple(dict(
            (c, (self.get_cumul_days()[kwargs['which']][c])) for c in clist).values()))
        diffout = np.array(tuple(dict(
            (c, self.get_diff_days()[kwargs['which']][c]) for c in clist).values()))

        option = kwargs.get('option', None)
        if option == 'nonneg':
            diffout = np.array(diffout, dtype=float)
            currentout = np.array(currentout, dtype=float)
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
                currentout[c, :] = np.cumsum(yy)
                cumulout[c, :] = np.cumsum(np.cumsum(yy))
        datos=[dt.strptime(d, '%m/%d/%y') for d in self.get_dates()]
        i = 0
        temp=[]
        for coun in clist:
            if len(currentout[i]):
                val1,val2,val3 = currentout[i], cumulout[i], diffout[i]

            else:
                val1 = val2 = val3 = [np.nan]*len(datos)
            data = {
                'location':[coun]*len(datos),
                'date': datos,
                kwargs['which']:val1,
                'cumul':val2,
                'diff': val3
                }

            temp.append(pd.DataFrame(data))
            i+=1

        if output == "array":
            if process_data == 'cumul':
                out = cumulout
            elif process_data == 'diff':
	            out = diffout
            else:
                out =  currentout
            if out.shape[0] == 1:
                return out[0]
            else:
                return out.T

        #if len(clist) == 1 :
        #    temp[0] = temp[0].drop(columns=['location'])

        return pd.concat(temp)

    ## https://www.kaggle.com/freealf/estimation-of-rt-from-cases
    def smooth_cases(self,cases):
        new_cases = cases

        smoothed = new_cases.rolling(7,
            win_type='gaussian',
            min_periods=1,
            center=True).mean(std=2).round()
            #center=False).mean(std=2).round()

        zeros = smoothed.index[smoothed.eq(0)]
        if len(zeros) == 0:
            idx_start = 0
        else:
            last_zero = zeros.max()
            idx_start = smoothed.index.get_loc(last_zero) + 1
        smoothed = smoothed.iloc[idx_start:]
        original = new_cases.loc[smoothed.index]

        return smoothed


    def get_posteriors(self,sr, window=7, min_periods=1):
        # We create an array for every possible value of Rt
        R_T_MAX = 12
        r_t_range = np.linspace(0, R_T_MAX, R_T_MAX*100+1)

        # Gamma is 1/serial interval
        # https://wwwnc.cdc.gov/eid/article/26/6/20-0357_article
        GAMMA = 1/7

        lam = sr[:-1].values * np.exp(GAMMA * (r_t_range[:, None] - 1))

        # Note: if you want to have a Uniform prior you can use the following line instead.
        # I chose the gamma distribution because of our prior knowledge of the likely value
        # of R_t.

        # prior0 = np.full(len(r_t_range), np.log(1/len(r_t_range)))
        prior0 = np.log(sps.gamma(a=3).pdf(r_t_range) + 1e-14)

        likelihoods = pd.DataFrame(
            # Short-hand way of concatenating the prior and likelihoods
            data = np.c_[prior0, sps.poisson.logpmf(sr[1:].values, lam)],
            index = r_t_range,
            columns = sr.index)

        # Perform a rolling sum of log likelihoods. This is the equivalent
        # of multiplying the original distributions. Exponentiate to move
        # out of log.
        posteriors = likelihoods.rolling(window,
                                     axis=1,
                                     min_periods=min_periods).sum()
        posteriors = np.exp(posteriors)

        # Normalize to 1.0
        posteriors = posteriors.div(posteriors.sum(axis=0), axis=1)

        return posteriors
