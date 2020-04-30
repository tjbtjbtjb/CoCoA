import requests
import pandas

class JHUCSSEdata:
	__pandasData={}

	def __init__(self):
		self.__baseUrl="https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/"
		self.__baseUrl+="csse_covid_19_data/csse_covid_19_time_series/"
		self.whichDataList=["deaths","confirmed","recovered"] 

		for w in  self.whichDataList:
			name_file="time_series_covid19_" + w + "_global.csv"
			url=self.__baseUrl+name_file
			self.__pandasData[w] = pandas.read_csv(url)

	def getRawData(self):
		return self.__pandasData
