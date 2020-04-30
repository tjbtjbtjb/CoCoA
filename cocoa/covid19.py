import requests
import pandas

class JHUCSSEdata:

	def __init__(self):
		self.__baseUrl="https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/"
		self.__baseUrl+="csse_covid_19_data/csse_covid_19_time_series/"
		self.whichDataList=["deaths","confirmed","recovered"] 
		self.__pandasData={}

		for w in  self.whichDataList:
			fileName="time_series_covid19_" + w + "_global.csv"
			url=self.__baseUrl+fileName
			self.__pandasData[w] = pandas.read_csv(url)

	def getBaseUrl(self):
		return self.__baseUrl

	def getRawData(self):
		return self.__pandasData
