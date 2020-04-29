
def getInfo():
    return "info"

def getVersion():
    return 0.1

import requests
import pandas

def getPopulationTab(): 
    Population_Url="https://www.worldometers.info/world-population/population-by-country/"
    Population_HTML=requests.get(Population_Url).content
    return pandas.read_html(Population_HTML)[0]
