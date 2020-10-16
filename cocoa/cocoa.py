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
    cc.setwhom('JHU') # return available keywords (aka 'which' data)
    cc.listwhich()   # idem
    cc.listwhat()    # return available time serie type (total,
                     # daily...)

"""

# --- Imports ----------------------------------------------------------
import warnings
from copy import copy
import matplotlib.pyplot as plt
import pandas as pd
import geopandas as gpd

import cocoa.world as cowo
import cocoa.covid19 as coco
import cocoa.geo as coge
from cocoa.error import *

from bokeh.io import output_notebook, show, output_file
from bokeh.plotting import figure
from bokeh.models import GeoJSONDataSource, LinearColorMapper,LogColorMapper, ColorBar, HoverTool,LogTicker
from bokeh.palettes import brewer
import json

# --- Needed global private variables ----------------------------------
_listwhom=['jhu',    # John Hopkins University first base, default
            'owid', # Our World in Data
            'spf',   # Sante publique France
            'opencovid19'] #  see data.gouv.fr
_whom = _listwhom[0] # default base


_db = coco.DataBase('jhu')

_info = coge.GeoInfo() # will be the info (pseudo) private variable
_reg = coge.GeoRegion()

_listwhat=['cumul','diff',  # first one is default but we must avoid uppercases
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
# --- listwhat() -------------------------------------------------------
# ----------------------------------------------------------------------

def listwhat():
    """Return the list of currently avalailable type of series available.
     The first one is the default one.
    """
    return _listwhat

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
    _db = coco.DataBase(base)
    return _db.get_available_keys_words()

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
    return _db.get_available_keys_words()

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
    which  --   what sort of data to deliver ( 'death','confirmed',
                'recovered' …). See listwhat() function for full
                list according to the used database.
    what   --   which data are computed, either in cumulative mode
                ( 'cumul', default value) or 'daily' or other. See
                listwhich() for fullist of available
                Full list of which keyword with the listwhich() function.
    whom   --   Database specification (overload the setbase()
                function). See listwhom() for supported list
                function). See listwhom() for supported list

    output --   output format returned ( list (default), dict or pandas)
    """
    where=kwargs.get('where',None)
    what=kwargs.get('what',None)
    which=kwargs.get('which',None)
    whom=kwargs.get('whom',None)

    output=kwargs.get('output',None)

    if not where:
        raise CocoaKeyError('No where keyword given')

    if whom:
        _db = coco.DataBase(whom)    
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

    print("-W _db" , _db.get_db())
    if not which:
        which=listwhich()[0]
    elif which not in setwhom(whom):
        raise CocoaKeyError('Which option '+which+' not supported. '
                            'See listwhich() for list.')
    return _db.get_stats(which=which,type=what,location=where,output=output)


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
                input should be given as valid cocoa pandas dataframe.
    """

    input_arg=kwargs.get('input',None)
    if input_arg != None:
        if not isinstance(input_arg,pd.DataFrame):
            raise CocoaTypeError('Waiting input as valid cocoa pandas '
                'dataframe. See help.')
        t=input_arg
    else:
        t=get(**kwargs,output='pandas')

    which=kwargs.get('which',listwhich()[0])
    yscale=kwargs.get('yscale','lin')
    if yscale=='lin':
        fplot=plt.plot
    elif yscale=='log':
        fplot=plt.semilogy
    else:
        raise CocoaKeyError('yscale option "'+yscale+'" is not valid. See help.')
    for k in t.location.unique():
        fplot(t[t.location==k].date,t[t.location==k][which],label=k)

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
    input_arg=kwargs.get('input',None)
    which=kwargs.get('which',listwhich()[0])
    if input_arg != None:
        if not isinstance(input_arg,pd.DataFrame):
            raise CocoaTypeError('Waiting input as valid cocoa pandas '
                'dataframe. See help.')
        t=input_arg
    else:
        t=get(**kwargs,output='pandas')

    val=[]
    coun=[]
    for _, grp in t.groupby(pd.Grouper(key='location')):
        val.append(grp[which].values)
        coun.append(grp.location.values[0])
    plt.hist(val,label=coun)
    plt.legend(prop={'size': 10})
    plt.title(str(which))
    plt.show()

# ----------------------------------------------------------------------
# --- map(**kwargs) ----------------------------------------------------
# ----------------------------------------------------------------------

def map(**kwargs):
    """Create a map according to arguments and options.
    See help(hist).
    """
    wlist=copy(kwargs.get('where',None))
    p=get(**kwargs)

    which=kwargs.get('which',None)

    if which == None:
        which = listwhich()[0]

    lastdate=p["date"].max()
    p=gpd.GeoDataFrame(_info.add_field(input=p[p["date"]==lastdate],\
        geofield='location',field=['geometry','country_name'])[[which,"geometry","country_name","location"]])

    p=p[p['geometry']!=None] # if some countries does not have an available geometry


    for k in [wlist]:
        if k in _reg.get_region_list():
            k_lst=_reg.get_countries_from_region(k)
            p.loc[p["location"].isin(k_lst),"location"]=k
            p=p.dissolve(aggfunc='sum',by='location') # merge the geometry and sum the cases for region

    p["cname"]=p.index
    #Read data to json
    merged_json = json.loads(p.to_json())

    #Convert to str like object
    json_data = json.dumps(merged_json)
    geosource = GeoJSONDataSource(geojson = json_data)

    #Define a sequential multi-hue color palette.
    palette = brewer['RdYlGn'][10] # see https://docs.bokeh.org/en/latest/docs/reference/palettes.html

    hover = HoverTool(tooltips = [ ('Country','@cname'),
                              ('Cases', '@'+str(which)) ] )

    #Instantiate LinearColorMapper that linearly maps numbers in a range, into a sequence of colors.
    color_mapper = LinearColorMapper(palette = palette)#, low = -50, high=50)

    #Define custom tick labels for color bar.
    #tick_labels = {'0': '0%', '5': '5%', '10':'10%', '15':'15%', '20':'20%'}#, '25':'25%', '30':'30%','35':'35%', '40': '>40%'}

    #Create color bar.
    color_bar = ColorBar(color_mapper=color_mapper, label_standoff=8,width = 500, height = 20,
    border_line_color=None,location = (0,0), orientation = 'horizontal')#, major_label_overrides = tick_labels)

    #Create figure object.
    f = figure(title = 'CocoaPlot', \
        plot_height = 700 , plot_width = 950,tools = [hover])#, toolbar_location = None)
    f.xgrid.grid_line_color = None
    f.ygrid.grid_line_color = None

    #Add patch renderer to figure.
    f.patches('xs','ys', source = geosource,fill_color = {'field' :which, 'transform' : color_mapper},\
          line_color = 'black', line_width = 0.25, fill_alpha = 1)

    #Specify figure layout.
    f.add_layout(color_bar, 'below')

    #Display figure.
    output_notebook()
    show(f)
