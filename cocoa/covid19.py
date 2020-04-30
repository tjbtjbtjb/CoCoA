import requests
import pandas
from collections import defaultdict
import numpy as np

#class EpidemiologicalData:
#	# empty parent class
#	def __init__(self):
#		# do nothing

class JHUCSSEdata(): 
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

class UsefullFunction():
  def __init__(self):
    pass

  def flat_list(self,matrix):
    flatten_matrix=[]
    for sublist in matrix: 
        for val in sublist: 
            flatten_matrix.append(val)
    return flatten_matrix

  def str2bool(self,v):
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')   

class Parser():
    def __init__(self,d):
      
      self.dates={}
      self.dicos_countries={}
      self.dict_sum_data={}
      self.total_current_cases={}
      self.masked_points={}
      self.diff_days={}
    
      self.which_data_list=d.whichDataList 

      df=d.getRawData()
    
      #nb_notfound=0
      for w in self.which_data_list:
        self.dicos_countries[w]=defaultdict(list)
        self.dates[w]  = list(df[w].head(0))[4:]
      
        for index, row in df[w].iterrows():
          country=row["Country/Region"]
          #if country in list(Population_Tab["Country (or dependency)"]) :
          value=[int(i) if i is not '' else -1 for i in \
                   row[self.dates[w]].values]
          self.dicos_countries[w][country].append(value)
          #else:
            #print(' ===>>> ',country,' not found')
          #  nb_notfound+=1
      
        self.dict_sum_data[w]=defaultdict(list)
        self.total_current_cases[w]=defaultdict(list)
        i_start = 0

        self.masked_points[w]=defaultdict(list)
        self.diff_days[w]=defaultdict(list)

        for keys in self.dicos_countries[w]:
          # Using list comprehension
          res = [sum(i) for i in zip(*self.dicos_countries[w][keys])] 
          self.dict_sum_data[w][keys].append(res)   
        
          self.dict_sum_data[w][keys]=\
              UsefullFunction().flat_list(self.dict_sum_data[w][keys])
          #masked non existing value , it could happen ...
          self.masked_points[w][keys]=\
              np.ma.array(self.dict_sum_data[w][keys][i_start:])
          self.diff_days[w][keys]=[j-i for i, j in zip(self.masked_points[w][keys][:-1],\
                                                     self.masked_points[w][keys][1:])] 
          self.diff_days[w][keys].insert(0,0)
          self.diff_days[w][keys]=np.array(self.diff_days[w][keys])

    def getMaskedPoint(self):
        return self.masked_points
    
    def getDiffDays(self):
        return self.diff_days            
    
    def getDates(self):
    	return self.dates[self.which_data_list[0]]
    	