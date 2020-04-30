
import requests
import pandas

class WorldInfo:
	__pandasData=pandas.DataFrame()

	def __init__(self):
		self.__url="https://www.worldometers.info/world-population/population-by-country/"
		htmlContent=requests.get(self.__url).content
		self.__pandasData=pandas.read_html(htmlContent)[0][['Country (or dependency)','Population (2020)','Land Area (Km²)']]
		self.__pandasData.columns=['Country','Population','Area']

	def getData(self):
		return self.__pandasData

    