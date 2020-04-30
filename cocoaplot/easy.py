#import cocoa.world as cw
import cocoa.covid19 as cc
import matplotlib.pyplot as plt

class plot:
	def __init__(self):
		self.__d=cc.JHUCSSEdata()
		self.__p=cc.Parser(self.__d)
		#self.__w=cw.WorldInfo()

	def go(self,c): # c for country
		plt.plot(self.__p.getDates(),self.__p.getMaskedPoint()['deaths'][c])
