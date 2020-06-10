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
import pandas as pd


class JHUCSSEdata():
    def __init__(self, **kwargs):
        self.__baseUrl = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/"
        self.__baseUrl += "csse_covid_19_data/csse_covid_19_time_series/"
        self.whichDataList = ["deaths", "confirmed", "recovered"]
        self.__pandasData = {}

        aphpdata = kwargs.get('aphpdata', None)
        if aphpdata:
            self.__pandasData = self.convertAPHP()
        else:
            for w in self.whichDataList:
                fileName = "time_series_covid19_" + w + "_global.csv"
                url = self.__baseUrl+fileName
                self.__pandasData[w] = pandas.read_csv(url)

    def getBaseUrl(self):
        return self.__baseUrl

    def getRawData(self):
        return self.__pandasData

        
class Parser():
    def __init__(self, d=0):

        if not d:
            d = JHUCSSEdata()

        self.dates = {}
        self.dicos_countries = {}
        self.dict_sum_data = {}
        self.total_current_cases = {}
        self.masked_points = {}
        self.diff_days = {}

        self.which_data_list = d.whichDataList

        df = d.getRawData()

        for w in self.which_data_list:
            self.dicos_countries[w] = defaultdict(list)

            self.dates[w] = list(df[w].head(0))[4:]

            for index, row in df[w].iterrows():
                country = row["Country/Region"]
                # if country in list(Population_Tab["Country (or dependency)"]) :
                value = [int(i) if i != '' else -1 for i in
                         row[self.dates[w]].values]
                self.dicos_countries[w][country].append(value)
                # else:
                #print(' ===>>> ',country,' not found')
                #  nb_notfound+=1

            self.dict_sum_data[w] = defaultdict(list)
            self.total_current_cases[w] = defaultdict(list)

            self.masked_points[w] = defaultdict(list)
            self.diff_days[w] = defaultdict(list)

            for keys in self.dicos_countries[w]:
                # Using list comprehension
                res = [sum(i) for i in zip(*self.dicos_countries[w][keys])]
                self.dict_sum_data[w][keys].append(res)
                self.dict_sum_data[w][keys] =\
                    self.flat_list(self.dict_sum_data[w][keys])
                # masked non existing value , it could happen ...
                self.masked_points[w][keys] =\
                    np.ma.array(self.dict_sum_data[w][keys])

                self.diff_days[w][keys] = [j-i for i, j in zip(self.masked_points[w][keys][:-1],
                                                               self.masked_points[w][keys][1:])]

                self.diff_days[w][keys].insert(0, 0)
                self.diff_days[w][keys] = np.array(self.diff_days[w][keys])

    def flat_list(self, matrix):
        flatten_matrix = []
        for sublist in matrix:
            for val in sublist:
                flatten_matrix.append(val)
        return flatten_matrix

    def getMaskedPoint(self):
        return self.masked_points

    def getDiffDays(self):
        return self.diff_days

    def getStats(self, **kwargs):
        if not isinstance(kwargs['country'], list):
            clist = [kwargs['country']]
        else:
            clist = kwargs['country']

        clist = [cName.replace('Czech Republic (Czechia)', 'Czechia')
                 for cName in clist]

        diffout = np.array(
            tuple(dict((c, self.getDiffDays()[kwargs['which']][c]) for c in clist).values()))
        sumout = np.array(tuple(dict(
            (c, self.getMaskedPoint()[kwargs['which']][c].data) for c in clist).values()))

        option = kwargs.get('option', None)
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

        if output == "pandas":
            d = []
            for enum, coun in enumerate(clist):
                i = 0
                for datos in self.getDates():
                    d.append(
                        {
                            'country': coun,
                            'date': dt.strptime(datos, '%m/%d/%y'),
                            'cases': out[enum, :][i]
                        }
                    )
                    i += 1
            babypandas = pd.DataFrame(d)
            return babypandas
        else:
            if out.shape[0] == 1:
                return out[0]
            else:
                return out.T

    def getCountries(self):
        return np.array(tuple(self.getMaskedPoint()[self.which_data_list[0]].keys()))

    def getDates(self):
        return np.array(self.dates[self.which_data_list[0]])
