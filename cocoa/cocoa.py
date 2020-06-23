
import cocoa.world as wc
import cocoa.covid19 as cc

import matplotlib.pyplot as plt 

_w = wc.WorldInfo()
_p = cc.Parser()

def setbase():
    return "setbase"
    
def get(**kwargs):
    output=kwargs.get('output',None)
    location=kwargs.get('location',None)
    which=kwargs.get('which',None)
    atype=kwargs.get('type',None)
    
    if not location:
        print('bof')
        
    if not which:
        which='deaths'
        
    if not atype:
        atype='Cumul'
        
    return _p.getStats(which=which,type=atype,country=location),which,atype
    
def hist(**kwargs):
    plt.hist(get(**kwargs))
    plt.show()
    
def plot(**kwargs):
    t,w,a=get(**kwargs)
    lineObjects=plt.plot(t)
    plt.legend(iter(lineObjects),kwargs.get('location',None))
    plt.ylabel(a+' of '+w)
    plt.xlabel('time')
    plt.show()
