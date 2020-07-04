# -*- coding: utf-8 -*-
""" Project : CoCoA
Date :    april-july 2020
Authors : Olivier Dadoun, Julien Browaeys, Tristan Beau
Copyright © CoCoa-team-17
License: See joint LICENSE file

Module : cocoa.geo
About : 

Geo Management classes within the cocoa framework.
It provides translations between naming normalisations of countries.
"""

from cocoa.error import *
import pycountry as pc
import pandas as pd
import warnings

class GeoManager():
    
    _list_standard=['iso2',   # Iso2 standard, default
            'iso3',           # Iso3 standard
            'name',           # Standard name ( != Official, caution )
            'num']            # Numeric standard
            
    _list_db=[None,'JHU','worldometers'] # first is default
    _list_output=['list','dict','pandas'] # first is default
    
    _standard = None # currently used normalisation standard
    
    def __init__(self,standard=_list_standard[0]):
        self.set_standard(standard)
    
    def get_list_standard(self):
        return self._list_standard
        
    def get_list_output(self):
        return self._list_output
        
    def get_list_db(self):
        return self._list_db
        
    def get_standard(self):
        return self._standard
        
    def set_standard(self,standard):
        if not isinstance(standard,str):
            raise CocoaTypeError('GeoManager error, the standard argument'
                ' must be a string') 
        if standard not in self.get_list_standard():
            raise CocoaKeyError('GeoManager.set_standard error, "'+\
                                    standard+' not managed. Please see '\
                                    'get_list_standard() function')
        self._standard=standard
        return self.get_standard()

    def get_standard(self):
        return self._standard
    
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
