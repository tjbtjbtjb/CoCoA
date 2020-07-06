# -*- coding: utf-8 -*-
"""Project : CoCoA - Copyright © CoCoa-team-17 
Date :    april-june 2020
Authors : Olivier Dadoun, Julien Browaeys, Tristan Beau
License: See joint LICENSE file

About
----- 

This is the CoCoA front end functions. It provides easy access and 
use of the whole CoCoA framework in a simplified way.

The use can change the database, the type of data, the output format
with keywords (see help of functions below).

Basic usage
-----------

** plotting covid deaths (default value) vs. time **

    import cocoa.cocoa as cc
    cc.plot(where='France')  # where keyword is mandatory

** getting recovered data for some countries **
    
    cc.get(where=['Spain','Italy'],which='recovered')

** listing available database and which data can be used **
    cc.listwhom()
    cc.setwhom('JHU')     # return available keywords (aka 'which' data)
    cc.listwhich()   # idem
    cc.listwhat()    # return available time serie type (total, 
                     # daily...)
    
"""

# --- Imports ----------------------------------------------------------
import warnings
import matplotlib.pyplot as plt 

import cocoa.world as cowo
import cocoa.covid19 as coco
from cocoa.error import * 

# --- Needed global private variables ----------------------------------
_listwhom=['JHU',    # John Hopkins University first base, default
            'SPF']   # Sante publique France
_whom = _listwhom[0] # default base

_db = coco.db()
_p = coco.Parser()   # will be the parser (pseudo) private variable

_listwhat=['Cumul','Diff','cumul',  # first one is default but we must avoid uppercases
            'daily',
            'weekly']

# _w = cowo.WorldInfo() # not yet implemented in this cocoa frontend functions

# --- Front end functions -000------------------------------------------


# ----------------------------------------------------------------------
# --- listwhom() -------------------------------------------------------
# ----------------------------------------------------------------------

def listwhom():
    """Return the list of currently avalailable databases for covid19
     data in CoCoA.
     The first one is the default one.
    """
    return _listwhom

# ----------------------------------------------------------------------
# --- setwhom() --------------------------------------------------------
# ----------------------------------------------------------------------

def setwhom(base):
    """Set the covid19 database used, given as a string.
    Please see cocoa.listbase() for the available current list.
    
    By default, the listbase()[0] is the default base used in other
    functions.
    """
    warnings.warn("cocoa.setbase() function not yet fully implemented")
    if base not in listwhom():
        raise CocoaDbError(base+' is not a supported database. '
            'See cocoa.listbase() for the full list.')
    _db = coco.db(base) 
    return _db.getFields()
    
# ----------------------------------------------------------------------
# --- listwhich() ------------------------------------------------------
# ----------------------------------------------------------------------

def listwhich(dbname=None):
    """Get which are the available fields for the current or specified
    base. Output is a list of string.
    
    By default, the listwhich()[0] is the default which field in other
    functions.
    """
    if dbname == None:
        dbname=_whom
    if dbname not in listwhom():
        raise CocoaDbError(dbname+' is not a supported database name. ' 
            'See cocoa.listwhom() for the full list.')
    return coco.db(dbname).getFields()

# ----------------------------------------------------------------------
# --- listwhat() -------------------------------------------------------
# ----------------------------------------------------------------------
    
def listwhat():
    """Get what sort of time series data are available.
    
    By default, the listwhat()[0] is the default what field in other
    functions.
    """
    return _listwhat

# ----------------------------------------------------------------------
# --- get(**kwargs) ----------------------------------------------------
# ----------------------------------------------------------------------
    
def get(**kwargs):
    """Return covid19 data in specified format output (default, by list) 
    for specified locations ('where' keyword). 
    The used database is set by the setbase() function but can be
    changed on the fly ('whom' keyword)

    Keyword arguments
    -----------------
    
    where  --   a single string of location, or list of (mandatory, 
                no default value)
    what   --   what sort of data to deliver ( 'death','confirmed',
                'recovered' …). See getwhat() function for full
                list according to the used database.
    which  --   which data are computed, either in cumulative mode 
                ( 'cumul', default value) or 'daily' or other. See 
                getwhich() for fullist of available 
                Full list of which keyword with the 
    whom   --   Database specification (overload the setbase() 
                function)
             
    output --   output format returned ( list (default), dict or pandas)
    """
    where=kwargs.get('where',None)
    what=kwargs.get('what',None)
    which=kwargs.get('which',None)
    whom=kwargs.get('whom',None)
    
    output=kwargs.get('output',None)

    if not where:
        raise CocoaKeyError('No where keyword given')

    if not whom:
        whom=_whom
    elif whom not in listwhom():
        raise CocoaKeyError('Whom option '+whom+' not supported'
                            'See listwhom() for list.')
    else:
        warnings.warn('whom keyword not yet implemented. Using default')
         
    if not what:
        what=listwhat()[0]
    elif what not in listwhat():
        raise CocoaKeyError('What option '+what+' not supported'
                            'See listwhat() for list.')
        
    if not which:
        which=listwhich()[0]
    elif which not in listwhich():
        raise CocoaKeyError('Which option '+which+' not supported. '
                            'See listwhich() for list.')
            
    return _p.getStats(which=which,type=what,country=where,output=output)

# ----------------------------------------------------------------------
# --- plot(**kwargs) ---------------------------------------------------
# ----------------------------------------------------------------------
    
def plot(**kwargs):
    """Plot data according to arguments (same as the get function) 
    and options.
    
    Keyword arguments
    -----------------
    
    where (mandatory), what, which, whom : (see help(get))
    
    yscale --   'lin' (linear) or 'log' (logarithmic) vertical y scale. 
                If log scale is selected null values are hidden.
              
    input  --   input data to plot within the cocoa framework (e.g. 
                after some analysis or filtering). Default is None which
                means that we use the basic raw data through the get 
                function.
                When the 'input' keyword is set, where, what, which,
                whom keywords are ignored.
    """
    t=get(**kwargs,output='pandas')
    #yscale=lin or log…
    
    yscale=kwargs.get('yscale','lin')
    if yscale=='lin':
        fplot=plt.plot
    elif yscale=='log':
        fplot=plt.semilogy
    else:
        raise CocoaKeyError('yscale option "'+yscale+'" is not valid. See help.')
    
    for k in t.country.unique():
        
        fplot(t[t.country==k].date,t[t.country==k].cases,label=k)
    
    plt.legend()
    plt.xlabel('time')
    plt.show()

# ----------------------------------------------------------------------
# --- hist(**kwargs) ---------------------------------------------------
# ----------------------------------------------------------------------

def hist(**kwargs):
    """Create histogram according to arguments (same as the get
    function) and options.
    
    Keyword arguments
    ----------------- 
    
    where (mandatory), what, which, whom : (see help(get))

    input  --   input data to plot within the cocoa framework (e.g. 
                after some analysis or filtering). Default is None which
                means that we use the basic raw data through the get 
                function.
                When the 'input' keyword is set, where, what, which,
                whom keywords are ignored.
    """
    plt.hist(get(**kwargs))
    plt.show()

# ----------------------------------------------------------------------
# --- map(**kwargs) ----------------------------------------------------
# ----------------------------------------------------------------------
    
def map(**kwargs):
    """Create a map according to arguments and options. 
    See help(hist).
    """
    return None
