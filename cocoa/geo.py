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
    
    _list_standard=['iso2',    # Iso2 standard, default
            'iso3',           # Iso3 standard
            'name',           # Standard name ( != Official, caution )
            'num']            # Numeric standard
    _standard = None
    
    def __init__(self,standard=_list_standard[0]):
        self.set_standard(standard)
    
    def get_list_standard(self):
        return self._list_standard
        
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
    
    def to_standard(self, w, output='list'):
        """Given a list of string of locations (countries), returns a
        normalised list according to the used standard (defined
        via the setStandard() or __init__ function. Current default is iso2.
        
        Arguments
        -----------------
        first arg  --   w, list of string of locations (or single string)
                        to convert to standard one
        
        output    --    'list' (default), 'dict' or 'pandas' 
        
        """
        if isinstance(w,str):
            w=[w]
        elif not isinstance(w,list):
            raise CocoaTypeError('Waiting for str, list of str or pandas'
                'as input of get_standard function member of GeoManager')
                
        n=[] # will contain standardized name of countries (if possible)
        
        for c in w:
            if type(c)==int:
                c=str(c)
            elif type(c)!=str:
                raise CocoaTypeError('Locations should be given as '
                    'strings or integers only')
                    
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
            return dict(zip(w, n))
        elif output=='pandas':
            return pd.DataFrame({'inputname':w,self._standard:n})
        else:
            raise CocoaKeyError('Output should be "list", "dict" or "pandas"'+\
                ' only, whereas "'+output+'" is given.')
