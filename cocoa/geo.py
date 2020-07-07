# -*- coding: utf-8 -*-
""" Project : CoCoA
Date :    april-july 2020
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
"""

from cocoa.error import *
import pycountry as pc
import pycountry_convert as pcc
import pandas as pd
import warnings
from copy import copy

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
            
    _list_db=[None,'JHU','worldometers'] # first is default
    _list_output=['list','dict','pandas'] # first is default
    
    _standard = None # currently used normalisation standard
    
    def __init__(self,standard=_list_standard[0]):
        """ __init__ member function, with default definition of 
        the used standard. To get the current default standard, 
        see get_list_standard()[0].
        """
        self.set_standard(standard)
    
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
        first arg  --   w, list of string of locations (or single string)
                        to convert to standard one
        
        output     --   'list' (default), 'dict' or 'pandas' 
        db         --   database name to help conversion. 
                        Default : None, meaning best effort to convert.
                        Known database : JHU, wordometer
        """
        
        output=kwargs.get('output',self.get_list_output()[0])
        if output not in self.get_list_output():
            raise CocoaKeyError('Incorrect output type. See get_list_output()'
                ' or help.')
            
        db=kwargs.get('db',self.get_list_db()[0])
        if db not in self.get_list_db():
            raise CocoaDbError('Unknown database for translation to '
                'standardized location names. See get_list_db() or help.')
        
        w0=w
        if isinstance(w,str):
            w=[w]
        elif not isinstance(w,list):
            raise CocoaTypeError('Waiting for str, list of str or pandas'
                'as input of get_standard function member of GeoManager')
        
        if db:
            w=self.first_db_translation(w,db)
                
        n=[] # will contain standardized name of countries (if possible)
        
        for c in w:
            if type(c)==int:
                c=str(c)
            elif type(c)!=str:
                raise CocoaTypeError('Locations should be given as '
                    'strings or integers only')
            
            if len(c)==0:
                n1=None
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
            return pd.DataFrame({'inputname':w,self._standard:n})
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
        if db=='JHU':
            translation_dict={\
                "Congo (Brazzaville)":"Republic of the Congo",\
                "Congo (Kinshasa)":"COD",\
                "Korea, South":"KOR",\
                "Taiwan*":"Taiwan",\
                "Laos":"LAO",\
                "West Bank and Gaza":"PSE",\
                "Burma":"Myanmar",\
                "Iran":"IRN",\
                "Diamond Princess":"",\
                "MS Zaandam":""           
                    }  # last two are names of boats
        elif db=='worldometers':
            translation_dict={\
                "DR Congo":"COD",\
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
                } 
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
        'population':'truc',\
        'surface':'bidule'}
    
    def __init__(self):
        """ __init__ member function.
        """
        self._g=GeoManager('iso2')

    def get_list_field(self):
        """ return the list of supported additionnal fields available
        """
        return list(self._list_field.keys())
        
    def get_source(self,field):
        """ return the source of the information provided for a given
        field.
        """
        if field not in self.get_list_field():
            raise CocoaKeyError('The field "'+str(field)+'" is not '
                'a supported field of GeoInfo(). Please see help or '
                'the get_list_field() output.')
        return field+' : '+self._list_field[field]
        
    def add_field(self,**kwargs):
        """ this is the main function of the GeoInfo class. It adds to 
        the input pandas dataframe some fields according to 
        the country field of input. 
        The return value is the pandas dataframe.
        
        Arguments :
        field    -- should be given as a string of list of strings and 
                    should be valid fields (see get_list_field() )
                    Mandatory.
        input    -- provide the input pandas dataframe. Mandatory.
        geofield -- provide the field name in the pandas where the
                    location is stored. Default : 'country'
        """
        p=kwargs.get('input',None).copy() # the panda
        if not isinstance(p,pd.DataFrame):
            raise CocoaTypeError('You should provide a valid input pandas'
                ' DataFrame as input. See help.')
        
        fl=kwargs.get('field',None) # field list
        if fl == None:
            raise CocoaKeyError('No field given. See help.')
        if not isinstance(fl,list):
            fl=[fl]
        if not all(f in self.get_list_field() for f in fl):
            raise CocoaKeyError('All fields are not valid or supported '
                'ones. Please see help of get_list_field()')
        if not all(f not in p.columns.tolist() for f in fl):
            raise CocoaKeyError('Some fields already exist in you panda '
                'dataframe columns. ')
                
        geofield=kwargs.get('geofield','country')
        if not isinstance(geofield,str):
            raise CocoaTypeError('The geofield should be given as a '
                'string.')
        if geofield not in p.columns.tolist():
            raise CocoaKeyError('The geofield "'+geofield+'" given is '
                'not a valid column name of the input pandas dataframe.')
                
        countries=self._g.to_standard(p[geofield].tolist())

        for f in fl:
            if f == 'continent_code':
                p[f] = [pcc.country_alpha2_to_continent_code(k) for k in countries]
            elif f == 'continent_name':
                p[f] = [pcc.convert_continent_code_to_continent_name( \
                    pcc.country_alpha2_to_continent_code(k)) for k in countries]
            elif f == 'country_name':
                p[f] = [pcc.country_alpha2_to_country_name(k) for k in countries]
            elif f == 'population':
                p[f] = [0 for k in countries]
            elif f == 'surface':
                p[f] = [0 for k in countries]
                
        return p
