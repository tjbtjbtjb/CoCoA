
# -*- coding: utf-8 -*-

""" 
Project : CoCoA
Date :    april/may 2020
Authors : Olivier Dadoun, Julien Browaeys, Tristan Beau
Copyright © CoCoa-team-17
License: See joint LICENSE file

Module : cocoaplot.easy
About : 

The aim is providing very simple class or function to produce in few line of codes plots of covid19 datasets.

"""

import cocoa.covid19 as cc
import matplotlib.pyplot as plt

class plot:
	def __init__(self):
		self.__d=cc.JHUCSSEdata()
		self.__p=cc.Parser(self.__d)
		#self.__w=cw.WorldInfo()

	def go(self,c): # c for country
		plt.plot(self.__p.getDates(),self.__p.getMaskedPoint()['deaths'][c])
