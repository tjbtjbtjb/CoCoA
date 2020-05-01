# -*- coding: utf-8 -*-

""" 
Project : CoCoA
Date :    april/may 2020
Authors : Olivier Dadoun, Julien Browaeys, Tristan Beau

Module : cocoa.world
About : 

Provide simple quantitative information about countries in the worlds for normalisation purpuses of the CoCoA project.
The database in use is explicitly available throuh the getBaseUrl() method.
The European country list has been added for CoCoa specific needs.

"""

import requests
import pandas

class WorldInfo:
	__pandasData=pandas.DataFrame()

	def __init__(self):
		self.__url="https://www.worldometers.info/world-population/population-by-country/"
		htmlContent=requests.get(self.__url).content
		self.__pandasData=pandas.read_html(htmlContent)[0][['Country (or dependency)','Population (2020)','Land Area (Km²)']]
		self.__pandasData.columns=['Country','Population','Area']

	def getBaseUrl(self):
		return self.__url

	def getData(self):
		return self.__pandasData

	def getEuropeanCountries(self):
		return ['Portugal','Spain','Ireland','United Kingdom','France','Italy','Germany','Belgium', \
			'Netherlands','Luxembourg','Austria','Denmark','Swenden','Finland', \
			'Estonia','Lettonia','Lituania','Czech Republic','Poland','Slovakia','Hungary','Slovenia', \
			'Croatia','Romania','Bulgaria','Greece','Malta','Cyprus']