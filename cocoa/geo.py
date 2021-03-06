# -*- coding: utf-8 -*-
""" Project : CoCoA
Date :    april-november 2020
Authors : Olivier Dadoun, Julien Browaeys, Tristan Beau
Copyright © CoCoa-team-17
License: See joint LICENSE file

Module : cocoa.geo
About :

Geo classes within the cocoa framework.

GeoManager class provides translations between naming normalisations
of countries. It's based on the pycountry module.

GeoInfo class allow to add new fields to a pandas DataFrame about
statistical information for countries.

GeoRegion class helps returning list of countries in a specified region
"""

import warnings

import pycountry as pc
import pycountry_convert as pcc
import pandas as pd
import geopandas as gpd
import requests

from cocoa.tools import verb,kwargs_test
from cocoa.error import *

# ---------------------------------------------------------------------
# --- GeoManager class ------------------------------------------------
# ---------------------------------------------------------------------

class GeoManager():
    """GeoManager class definition. No inheritance from any other class.

    It should raise only CocoaError and derived exceptions in case
    of errors (see cocoa.error)
    """

    _list_standard=['iso2',   # Iso2 standard, default
            'iso3',           # Iso3 standard
            'name',           # Standard name ( != Official, caution )
            'num']            # Numeric standard

    _list_db=[None,'jhu','worldometers','owid'] # first is default
    _list_output=['list','dict','pandas'] # first is default

    _standard = None # currently used normalisation standard

    def __init__(self,standard=_list_standard[0]):
        """ __init__ member function, with default definition of
        the used standard. To get the current default standard,
        see get_list_standard()[0].
        """
        verb("Init of GeoManager()")
        self.set_standard(standard)
        self._gr=GeoRegion()

    def get_list_standard(self):
        """ return the list of supported standard name of countries.
        First one is default for the class
        """
        return self._list_standard

    def get_list_output(self):
        """ return supported list of output type. First one is default
        for the class
        """
        return self._list_output

    def get_list_db(self):
        """ return supported list of database name for translation of
        country names to standard.
        """
        return self._list_db

    def get_standard(self):
        """ return current standard use within the GeoManager class
        """
        return self._standard

    def set_standard(self,standard):
        """ set the working standard type within the GeoManager class.
        The standard should meet the get_list_standard() requirement
        """
        if not isinstance(standard,str):
            raise CocoaTypeError('GeoManager error, the standard argument'
                ' must be a string')
        if standard not in self.get_list_standard():
            raise CocoaKeyError('GeoManager.set_standard error, "'+\
                                    standard+' not managed. Please see '\
                                    'get_list_standard() function')
        self._standard=standard
        return self.get_standard()

    def to_standard(self, w, **kwargs):
        """Given a list of string of locations (countries), returns a
        normalised list according to the used standard (defined
        via the setStandard() or __init__ function. Current default is iso2.

        Arguments
        -----------------
        first arg        --  w, list of string of locations (or single string)
                             to convert to standard one

        output           -- 'list' (default), 'dict' or 'pandas'
        db               -- database name to help conversion.
                            Default : None, meaning best effort to convert.
                            Known database : jhu, wordometer
        interpret_region -- Boolean, default=False. If yes, the output should
                            be only 'list'.
        """

        kwargs_test(kwargs,['output','db','interpret_region'],'Bad args used in the to_standard() function.')

        output=kwargs.get('output',self.get_list_output()[0])
        if output not in self.get_list_output():
            raise CocoaKeyError('Incorrect output type. See get_list_output()'
                ' or help.')

        db=kwargs.get('db',self.get_list_db()[0])
        if db not in self.get_list_db():
            raise CocoaDbError('Unknown database "'+db+'" for translation to '
                'standardized location names. See get_list_db() or help.')

        interpret_region=kwargs.get('interpret_region',False)
        if not isinstance(interpret_region,bool):
            raise CocoaTypeError('The interpret_region argument is a boolean, '
                'not a '+str(type(interpret_region)))

        if interpret_region==True and output!='list':
            raise CocoaKeyError('The interpret_region True argument is incompatible '
                'with non list output option.')

        if isinstance(w,str):
            w=[w]
        elif not isinstance(w,list):
            raise CocoaTypeError('Waiting for str, list of str or pandas'
                'as input of get_standard function member of GeoManager')

        w=[v.title() for v in w] # capitalize first letter of each name

        w0=w.copy()

        if db:
            w=self.first_db_translation(w,db)

        n=[] # will contain standardized name of countries (if possible)

        #for c in w:
        while len(w)>0:
            c=w.pop(0)
            if type(c)==int:
                c=str(c)
            elif type(c)!=str:
                raise CocoaTypeError('Locations should be given as '
                    'strings or integers only')
            if (c in self._gr.get_region_list()) and interpret_region == True:
                w=self._gr.get_countries_from_region(c)+w
            else:
                if len(c)==0:
                    n1='' #None
                else:
                    try:
                        n0=pc.countries.lookup(c)
                    except LookupError:
                        try:
                            nf=pc.countries.search_fuzzy(c)
                            if len(nf)>1:
                                warnings.warn('Caution. More than one country match the key "'+\
                                c+'" : '+str([ (k.name+', ') for k in nf])+\
                                ', using first one.\n')
                            n0=nf[0]
                        except LookupError:
                            raise CocoaLookupError('No country match the key "'+c+'". Error.')
                        except Exception as e1:
                            raise CocoaNotManagedError('Not managed error '+type(e1))
                    except Exception as e2:
                        raise CocoaNotManagedError('Not managed error'+type(e1))

                    if self._standard=='iso2':
                        n1=n0.alpha_2
                    elif self._standard=='iso3':
                        n1=n0.alpha_3
                    elif self._standard=='name':
                        n1=n0.name
                    elif self._standard=='num':
                        n1=n0.numeric
                    else:
                        raise CocoaKeyError('Current standard is '+self._standard+\
                            ' which is not managed. Error.')

                n.append(n1)

        if output=='list':
            return n
        elif output=='dict':
            return dict(zip(w0, n))
        elif output=='pandas':
            return pd.DataFrame({'inputname':w0,self._standard:n})
        else:
            return None # should not be here

    def first_db_translation(self,w,db):
        """ This function helps to translate from country name to
        standard for specific databases. It's the first step
        before final translation.

        One can easily add some database support adding some new rules
        for specific databases
        """
        translation_dict={}
        # Caution : keys need to be in title mode, i.e. first letter capitalized
        if db=='jhu':
            translation_dict.update({\
                "Congo (Brazzaville)":"Republic of the Congo",\
                "Congo (Kinshasa)":"COD",\
                "Korea, South":"KOR",\
                "Taiwan*":"Taiwan",\
                "Laos":"LAO",\
                "West Bank And Gaza":"PSE",\
                "Burma":"Myanmar",\
                "Iran":"IRN",\
                "Diamond Princess":"",\
                "Ms Zaandam":"",\
                    })  # last two are names of boats
        elif db=='worldometers':
            translation_dict.update({\
                "Dr Congo":"COD",\
                "Congo":"COG",\
                "Iran":"IRN",\
                "South Korea":"KOR",\
                "North Korea":"PRK",\
                "Czech Republic (Czechia)":"CZE",\
                "Laos":"LAO",\
                "Sao Tome & Principe":"STP",\
                "Channel Islands":"JEY",\
                "St. Vincent & Grenadines":"VCT",\
                "U.S. Virgin Islands":"VIR",\
                "Saint Kitts & Nevis":"KNA",\
                "Faeroe Islands":"FRO",\
                "Caribbean Netherlands":"BES",\
                "Wallis & Futuna":"WLF",\
                "Saint Pierre & Miquelon":"SPM",\
                "Sint Maarten":"SXM",\
                } )
        elif db=='owid':
            translation_dict.update({\
                    "Bonaire Sint Eustatius And Saba":"BES",\
                    "Cape Verde":"CPV",\
                    "Democratic Republic Of Congo":"COD",\
                    "Faeroe Islands":"FRO",\
                    "Laos":"LAO",\
                    "South Korea":"KOR",\
                    "Swaziland":"SWZ",\
                    "United States Virgin Islands":"VIR",\
                })
        return [translation_dict.get(k,k) for k in w]

# ---------------------------------------------------------------------
# --- GeoInfo class ---------------------------------------------------
# ---------------------------------------------------------------------

class GeoInfo():
    """GeoInfo class definition. No inheritance from any other class.

    It should raise only CocoaError and derived exceptions in case
    of errors (see cocoa.error)
    """

    _list_field={\
        'continent_code':'pycountry_convert (https://pypi.org/project/pycountry-convert/)',\
        'continent_name':'pycountry_convert (https://pypi.org/project/pycountry-convert/)' ,\
        'country_name':'pycountry_convert (https://pypi.org/project/pycountry-convert/)' ,\
        'population':'https://www.worldometers.info/world-population/population-by-country/',\
        'area':'https://www.worldometers.info/world-population/population-by-country/',\
        'fertility':'https://www.worldometers.info/world-population/population-by-country/',\
        'median_age':'https://www.worldometers.info/world-population/population-by-country/',\
        'urban_rate':'https://www.worldometers.info/world-population/population-by-country/',\
        'geometry':'https://github.com/johan/world.geo.json/',\
        'region_code_list':'https://en.wikipedia.org/wiki/List_of_countries_by_United_Nations_geoscheme',\
        'region_name_list':'https://en.wikipedia.org/wiki/List_of_countries_by_United_Nations_geoscheme',\
        'capital':'https://en.wikipedia.org/wiki/List_of_countries_by_United_Nations_geoscheme'}

    _data_geometry = pd.DataFrame()
    _data_population = pd.DataFrame()

    def __init__(self,gm=0):
        """ __init__ member function.
        """
        verb("Init of GeoInfo()")
        if gm != 0:
            self._gm=gm
        else:
            self._gm=GeoManager()
            
        self._grp=self._gm._gr.get_pandas()

    def get_list_field(self):
        """ return the list of supported additionnal fields available
        """
        return sorted(list(self._list_field.keys()))

    def get_source(self,field=None):
        """ return the source of the information provided for a given
        field.
        """
        if field==None:
            return self._list_field
        elif field not in self.get_list_field():
            raise CocoaKeyError('The field "'+str(field)+'" is not '
                'a supported field of GeoInfo(). Please see help or '
                'the get_list_field() output.')
        return field+' : '+self._list_field[field]

    def add_field(self,**kwargs):
        """ this is the main function of the GeoInfo class. It adds to
        the input pandas dataframe some fields according to
        the geofield field of input.
        The return value is the pandas dataframe.

        Arguments :
        field    -- should be given as a string of list of strings and
                    should be valid fields (see get_list_field() )
                    Mandatory.
        input    -- provide the input pandas dataframe. Mandatory.
        geofield -- provide the field name in the pandas where the
                    location is stored. Default : 'location'
        overload -- Allow to overload a field. Boolean value.
                    Default : False
        """

        # --- kwargs analysis ---

        kwargs_test(kwargs,['field','input','geofield','overload'],
            'Bad args used in the add_field() function.')

        p=kwargs.get('input',None) # the panda
        if not isinstance(p,pd.DataFrame):
            raise CocoaTypeError('You should provide a valid input pandas'
                ' DataFrame as input. See help.')
        p=p.copy()

        overload=kwargs.get('overload',False)
        if not isinstance(overload,bool):
            raise CocoaTypeError('The overload option should be a boolean.')

        fl=kwargs.get('field',None) # field list
        if fl == None:
            raise CocoaKeyError('No field given. See help.')
        if not isinstance(fl,list):
            fl=[fl]
        if not all(f in self.get_list_field() for f in fl):
            raise CocoaKeyError('All fields are not valid or supported '
                'ones. Please see help of get_list_field()')

        if not overload and not all(f not in p.columns.tolist() for f in fl):
            raise CocoaKeyError('Some fields already exist in you panda '
                'dataframe columns. You may set overload to True.')

        geofield=kwargs.get('geofield','location')

        if not isinstance(geofield,str):
            raise CocoaTypeError('The geofield should be given as a '
                'string.')
        if geofield not in p.columns.tolist():
            raise CocoaKeyError('The geofield "'+geofield+'" given is '
                'not a valid column name of the input pandas dataframe.')

        self._gm.set_standard('iso2')
        countries_iso2=self._gm.to_standard(p[geofield].tolist())
        self._gm.set_standard('iso3')
        countries_iso3=self._gm.to_standard(p[geofield].tolist())

        p['iso2_tmp']=countries_iso2
        p['iso3_tmp']=countries_iso3

        # --- loop over all needed fields ---
        for f in fl:
            if f in p.columns.tolist():
                p=p.drop(f,axis=1)
            # ----------------------------------------------------------
            if f == 'continent_code':
                p[f] = [pcc.country_alpha2_to_continent_code(k) for k in countries_iso2]
            # ----------------------------------------------------------
            elif f == 'continent_name':
                p[f] = [pcc.convert_continent_code_to_continent_name( \
                    pcc.country_alpha2_to_continent_code(k) ) for k in countries_iso2 ]
            # ----------------------------------------------------------
            elif f == 'country_name':
                p[f] = [pcc.country_alpha2_to_country_name(k) for k in countries_iso2]
            # ----------------------------------------------------------
            elif f in ['population','area','fertility','median_age','urban_rate']:
                if self._data_population.empty:
                    url_worldometers="https://www.worldometers.info/world-population/population-by-country/"
                    try:
                        htmlContent = requests.get(url_worldometers).content
                    except:
                        raise CocoaConnectionError('Cannot connect to the database '
                                'worldometers.info. '
                                'Please check your connection or availabilty of the db')

                    field_descr=( (0,'','idx'),
                        (1,'Country','country'),
                        (2,'Population','population'),
                        (6,'Land Area','area'),
                        (8,'Fert','fertility'),
                        (9,'Med','median_age'),
                        (10,'Urban','urban_rate'),
                        ) # containts tuples with position in table, name of column, new name of field

                    # get data
                    self._data_population = pd.read_html(htmlContent)[0].iloc[:,[x[0] for x in field_descr]]

                    # test that field order hasn't changed in the db
                    if not all (col.startswith(field_descr[i][1]) for i,col in enumerate(self._data_population.columns) ):
                        raise CocoaDbError('The worldometers database changed its field names. '
                            'The GeoInfo should be updated. Please contact developers.')

                    # change field name
                    self._data_population.columns = [x[2] for x in field_descr]

                    # standardization of country name
                    self._data_population['iso3_tmp2']=\
                        self._gm.to_standard(self._data_population['country'].tolist(),\
                        db='worldometers')

                p=p.merge(self._data_population[["iso3_tmp2",f]],how='left',\
                        left_on='iso3_tmp',right_on='iso3_tmp2',\
                        suffixes=('','_tmp')).drop(['iso3_tmp2'],axis=1)
            # ----------------------------------------------------------
            elif f in ['region_code_list','region_name_list']:

                if f == 'region_code_list':
                    ff = 'region'
                elif f == 'region_name_list':
                    ff = 'region_name'

                p[f]=p.merge(self._grp[['iso3',ff]],how='left',\
                    left_on='iso3_tmp',right_on='iso3',\
                    suffixes=('','_tmp')) \
                    .groupby('iso3_tmp')[ff].apply(list).to_list()
            # ----------------------------------------------------------
            elif f in ['capital']:
                p[f]=p.merge(self._grp[['iso3',f]].drop_duplicates(), \
                    how='left',left_on='iso3_tmp',right_on='iso3',\
                    suffixes=('','_tmp'))[f]

            # ----------------------------------------------------------
            elif f == 'geometry':
                if self._data_geometry.empty:
                    geojsondatafile = 'https://raw.githubusercontent.com/johan/world.geo.json/master/countries.geo.json'
                    try:
                        self._data_geometry = gpd.read_file(geojsondatafile)[["id","geometry"]]
                        self._data_geometry.columns=["id_tmp","geometry"]
                        # countains id as iso3 , country name , geometry
                    except:
                        raise CocoaConnectionError('Cannot access to the '
                            'geo json data for countries. '
                            'Check internet connection.')

                p=p.merge(self._data_geometry,how='left',\
                    left_on='iso3_tmp',right_on='id_tmp',\
                    suffixes=('','_tmp')).drop(['id_tmp'],axis=1)

        return p.drop(['iso2_tmp','iso3_tmp'],axis=1,errors='ignore')

# ---------------------------------------------------------------------
# --- GeoInfo class ---------------------------------------------------
# ---------------------------------------------------------------------

class GeoRegion():
    """GeoRegion class definition. Does not inheritate from any other
    class.

    It should raise only CocoaError and derived exceptions in case
    of errors (see cocoa.error)
    """

    _source_dict={"UN_M49":"https://en.wikipedia.org/wiki/UN_M49",\
        "GeoScheme":"https://en.wikipedia.org/wiki/List_of_countries_by_United_Nations_geoscheme",\
        "European Union":"https://europa.eu/european-union/about-eu/countries/member-countries_en",\
        "G7":"https://en.wikipedia.org/wiki/Group_of_Seven",\
        "G8":"https://en.wikipedia.org/wiki/Group_of_Eight",\
        "G20":"https://en.wikipedia.org/wiki/G20",\
        "G77":"https://www.g77.org/doc/members.html",\
        "OECD":"https://en.wikipedia.org/wiki/OECD"}

    _region_dict={}
    _p_gs = pd.DataFrame()

    def __init__(self,):
        """ __init__ member function.
        """
        #if 'XK' in self._country_list:
        #    del self._country_list['XK'] # creates bugs in pycountry and is currently a contested country as country


        # --- get the UN M49 information and organize the data in the _region_dict
        
        verb("Init of GeoRegion()")
        try:
            p_m49=pd.read_html(self._source_dict["UN_M49"])[1]
        except:
            raise CocoaConnectionError('Cannot connect to the UN_M49 '
                    'wikipedia page. '
                    'Please check your connection or availability of the page.')

        p_m49.columns=['code','region_name']
        p_m49['region_name']=[r.split('(')[0].rstrip() for r in p_m49.region_name]  # suppress information in parenthesis in region name
        p_m49.set_index('code')

        self._region_dict.update(p_m49.to_dict('split')['data'])
        self._region_dict.update({  "UE":"European Union",
                                    "G7":"G7",
                                    "G8":"G8",
                                    "G20":"G20",
                                    "OECD":"Oecd",
                                    "G77":"G77",
                                    })  # add UE for other analysis


        # --- get the UnitedNation GeoScheme and organize the data
        try:
            p_gs=pd.read_html(self._source_dict["GeoScheme"])[0]
        except:
            raise CocoaConnectionError('Cannot connect to the UN GeoScheme '
                    'wikipedia page. '
                    'Please check your connection or availability of the page.')
        p_gs.columns=['country','capital','iso2','iso3','num','m49']

        idx=[]
        reg=[]
        cap=[]

        for index, row in p_gs.iterrows():
            if row.iso3 != '–' : # meaning a non standard iso in wikipedia UN GeoScheme
                for r in row.m49.replace(" ","").split('<'):
                    idx.append(row.iso3)
                    reg.append(int(r))
                    cap.append(row.capital)
        self._p_gs=pd.DataFrame({'iso3':idx,'capital':cap,'region':reg})
        self._p_gs=self._p_gs.merge(p_m49,how='left',left_on='region',\
                            right_on='code').drop(["code"],axis=1)

    def get_source(self):
        return self._source_dict

    def get_region_list(self):
        return list(self._region_dict.values())

    def get_countries_from_region(self,region):
        """ it returns a list of countries for the given region name.
        The standard used is iso3. To convert to another standard,
        use the GeoManager class.
        """

        if type(region) != str:
            raise CocoaKeyError("The given region is not a str type.")

        region=region.title()  # if not properly capitalized
        
        if region not in self.get_region_list():
            raise CocoaKeyError('The given region "'+str(region)+'" is unknown.')

        clist=[]

        if region=='European Union':
            clist=['AUT','BEL','BGR','CYP','CZE','DEU','DNK','EST',\
                        'ESP','FIN','FRA','GRC','HRV','HUN','IRL','ITA',\
                        'LTU','LUX','LVA','MLT','NLD','POL','PRT','ROU',\
                        'SWE','SVN','SVK']
        elif region=='G7':
            clist=['DEU','CAN','USA','FRA','ITA','JAP','GBR']
        elif region=='G8':
            clist=['DEU','CAN','USA','FRA','ITA','JAP','GBR','RUS']
        elif region=='G20':
            clist=['ZAF','SAU','ARG','AUS','BRA','CAN','CHN','KOR','USA',\
                'IND','IDN','JAP','MEX','GBR','RUS','TUR',\
                'AUT','BEL','BGR','CYP','CZE','DEU','DNK','EST',\
                'ESP','FIN','FRA','GRC','HRV','HUN','IRL','ITA',\
                'LTU','LUX','LVA','MLT','NLD','POL','PRT','ROU',\
                'SWE','SVN','SVK']
        elif region=='Oecd': # OCDE in french
            clist=['DEU','AUS','AUT','BEL','CAN','CHL','COL','KOR','DNK',\
                'ESP','EST','USA','FIN','FRA','GRC','HUN','IRL','ISL','ISR',\
                'ITA','JAP','LVA','LTU','LUX','MEX','NOR','NZL','NLD','POL',\
                'PRT','SVK','SVN','SWE','CHE','GBR','CZE','TUR']
        elif region=='G77':
            clist=['AFG','DZA','AGO','ATG','ARG','AZE','BHS','BHR','BGD','BRB','BLZ',
                'BEN','BTN','BOL','BWA','BRA','BRN','BFA','BDI','CPV','KHM','CMR',
                'CAF','TCD','CHL','CHN','COL','COM','COG','CRI','CIV','CUB','PRK',
                'COD','DJI','DMA','DOM','ECU','EGY','SLV','GNQ','ERI','SWZ','ETH',
                'FJI','GAB','GMB','GHA','GRD','GTM','GIN','GNB','GUY','HTI','HND',
                'IND','IDN','IRN','IRQ','JAM','JOR','KEN','KIR','KWT','LAO','LBN',
                'LSO','LBR','LBY','MDG','MWI','MYS','MDV','MLI','MHL','MRT','MUS',
                'FSM','MNG','MAR','MOZ','MMR','NAM','NRU','NPL','NIC','NER','NGA',
                'OMN','PAK','PAN','PNG','PRY','PER','PHL','QAT','RWA','KNA','LCA',
                'VCT','WSM','STP','SAU','SEN','SYC','SLE','SGP','SLB','SOM','ZAF',
                'SSD','LKA','PSE','SDN','SUR','SYR','TJK','THA','TLS','TGO','TON',
                'TTO','TUN','TKM','UGA','ARE','TZA','URY','VUT','VEN','VNM','YEM',
                'ZMB','ZWE']
        else:
            clist=self._p_gs[self._p_gs['region_name']==region]['iso3'].to_list()

        return sorted(clist)

    def get_pandas(self):
        return self._p_gs
