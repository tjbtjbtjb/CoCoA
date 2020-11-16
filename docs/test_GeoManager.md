# Testing cocoa.geo.GeoManager (cocoa release 1.0)

Within the cocoa.geo, the GeoManager provides method to manage the name translation and standardization, needed to join various databases.

## Making CoCoA available
If executed locally


```python
import sys
sys.path.insert(1, '..')
```

If executed on a server (e.g. [Google Colab](https://colab.research.google.com/) ), you should install cocoa via `pip3`


```python
!pip3 install -q git+https://github.com/tjbtjbtjb/CoCoA.git
```


```python
from cocoa.geo import GeoManager as gm
```

## Getting some help


```python
help(gm)
```

    Help on class GeoManager in module cocoa.geo:
    
    class GeoManager(builtins.object)
     |  GeoManager(standard='iso2')
     |  
     |  GeoManager class definition. No inheritance from any other class.
     |  
     |  It should raise only CocoaError and derived exceptions in case
     |  of errors (see cocoa.error)
     |  
     |  Methods defined here:
     |  
     |  __init__(self, standard='iso2')
     |      __init__ member function, with default definition of
     |      the used standard. To get the current default standard,
     |      see get_list_standard()[0].
     |  
     |  first_db_translation(self, w, db)
     |      This function helps to translate from country name to
     |      standard for specific databases. It's the first step
     |      before final translation.
     |      
     |      One can easily add some database support adding some new rules
     |      for specific databases
     |  
     |  get_list_db(self)
     |      return supported list of database name for translation of
     |      country names to standard.
     |  
     |  get_list_output(self)
     |      return supported list of output type. First one is default
     |      for the class
     |  
     |  get_list_standard(self)
     |      return the list of supported standard name of countries.
     |      First one is default for the class
     |  
     |  get_standard(self)
     |      return current standard use within the GeoManager class
     |  
     |  set_standard(self, standard)
     |      set the working standard type within the GeoManager class.
     |      The standard should meet the get_list_standard() requirement
     |  
     |  to_standard(self, w, **kwargs)
     |      Given a list of string of locations (countries), returns a
     |      normalised list according to the used standard (defined
     |      via the setStandard() or __init__ function. Current default is iso2.
     |      
     |      Arguments
     |      -----------------
     |      first arg        --  w, list of string of locations (or single string)
     |                           to convert to standard one
     |      
     |      output           -- 'list' (default), 'dict' or 'pandas'
     |      db               -- database name to help conversion.
     |                          Default : None, meaning best effort to convert.
     |                          Known database : jhu, wordometer
     |      interpret_region -- Boolean, default=False. If yes, the output should
     |                          be only 'list'.
     |  
     |  ----------------------------------------------------------------------
     |  Data descriptors defined here:
     |  
     |  __dict__
     |      dictionary for instance variables (if defined)
     |  
     |  __weakref__
     |      list of weak references to the object (if defined)
    


## Usage


```python
g=gm() # Create the instance of GeoManager 
```

### Suppported options


```python
g.get_list_db() # list of databases for which there is a translation support. First one is default.
```




    [None, 'jhu', 'worldometers', 'owid']




```python
g.get_list_output() 
```




    ['list', 'dict', 'pandas']




```python
g.get_list_standard() # get the list of supported standards. First one is default
```




    ['iso2', 'iso3', 'name', 'num']




```python
g.get_standard() # get the current output standard
```




    'iso2'



### Changing the default output standard


```python
g.set_standard('name')
```




    'name'




```python
g2=gm('iso3')
g2.get_standard()
```




    'iso3'



### Converting countries to standardized names


```python
g.to_standard('england') # single country
```




    ['United Kingdom']




```python
g.to_standard(['esp','it']) # list of countries
```




    ['Spain', 'Italy']




```python
from cocoa.error import * 
try:
    z=g.to_standard('European Union') # the name does not exist as a country
except CocoaError:
    print('The input name is unknown, try to interpret as a region')
    z=g.to_standard('European Union',interpret_region=True)
print(z)
```

    The input name is unknown, try to interpret as a region
    ['Austria', 'Belgium', 'Bulgaria', 'Cyprus', 'Czechia', 'Germany', 'Denmark', 'Spain', 'Estonia', 'Finland', 'France', 'Greece', 'Croatia', 'Hungary', 'Ireland', 'Italy', 'Lithuania', 'Luxembourg', 'Latvia', 'Malta', 'Netherlands', 'Poland', 'Portugal', 'Romania', 'Slovakia', 'Slovenia', 'Sweden']



```python
g.to_standard(['usa','South America','russia'],interpret_region=True) # mix between region and countries
```




    ['United States',
     'Argentina',
     'Bolivia, Plurinational State of',
     'Brazil',
     'Bouvet Island',
     'Chile',
     'Colombia',
     'Ecuador',
     'Falkland Islands (Malvinas)',
     'French Guiana',
     'Guyana',
     'Peru',
     'Paraguay',
     'South Georgia and the South Sandwich Islands',
     'Suriname',
     'Uruguay',
     'Venezuela, Bolivarian Republic of',
     'Russian Federation']




```python
g.to_standard('french') # difficult interpretation, getting first item, a warning appears
```

    ../cocoa/geo.py:174: UserWarning: Caution. More than one country match the key "French" : ['France, ', 'French Guiana, ', 'French Polynesia, ', 'French Southern Territories, ', 'Saint Martin (French part), '], using first one.
    
      warnings.warn('Caution. More than one country match the key "'+\





    ['France']



### Conversion for specific databases


```python
try:
    z=g.to_standard('Congo (Kinshasa)')
except CocoaError:
    print('Try to interpret within the JHU database country name usage')
    z=g.to_standard('Congo (Kinshasa)',db='jhu')
z
```

    Try to interpret within the JHU database country name usage





    ['Congo, The Democratic Republic of the']



### Other outputs


```python
g.to_standard(['fr','spain','england'],output='dict')
```




    {'Fr': 'France', 'Spain': 'Spain', 'England': 'United Kingdom'}




```python
g.to_standard(['fr','spain','england'],output='pandas')
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>inputname</th>
      <th>name</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Fr</td>
      <td>France</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Spain</td>
      <td>Spain</td>
    </tr>
    <tr>
      <th>2</th>
      <td>England</td>
      <td>United Kingdom</td>
    </tr>
  </tbody>
</table>
</div>



## Management of errors

As far as possible, errors are managed within the `cocoa.error` framework. `CocoaError` should be raised.


```python
g.set_standard('oups') # the standard is not in the standard list 
```


    ---------------------------------------------------------------------------

    CocoaKeyError                             Traceback (most recent call last)

    <ipython-input-26-55a54eace16a> in <module>
    ----> 1 g.set_standard('oups') # the standard is not in the standard list
    

    ~/Dropbox/Git/dev_versions/CoCoA/cocoa/geo.py in set_standard(self, standard)
         92                 ' must be a string')
         93         if standard not in self.get_list_standard():
    ---> 94             raise CocoaKeyError('GeoManager.set_standard error, "'+\
         95                                     standard+' not managed. Please see '\
         96                                     'get_list_standard() function')


    CocoaKeyError: 'GeoManager.set_standard error, "oups not managed. Please see get_list_standard() function'



```python
g3=gm('hi!') # idem
```


    ---------------------------------------------------------------------------

    CocoaKeyError                             Traceback (most recent call last)

    <ipython-input-27-cb78b4c897a2> in <module>
    ----> 1 g3=gm('hi!') # idem
    

    ~/Dropbox/Git/dev_versions/CoCoA/cocoa/geo.py in __init__(self, standard)
         58         """
         59         verb("Init of GeoManager()")
    ---> 60         self.set_standard(standard)
         61         self._gr=GeoRegion()
         62 


    ~/Dropbox/Git/dev_versions/CoCoA/cocoa/geo.py in set_standard(self, standard)
         92                 ' must be a string')
         93         if standard not in self.get_list_standard():
    ---> 94             raise CocoaKeyError('GeoManager.set_standard error, "'+\
         95                                     standard+' not managed. Please see '\
         96                                     'get_list_standard() function')


    CocoaKeyError: 'GeoManager.set_standard error, "hi! not managed. Please see get_list_standard() function'



```python
g.to_standard('Congo (Kinshasa)',db='another base') # unknown base
```


    ---------------------------------------------------------------------------

    CocoaDbError                              Traceback (most recent call last)

    <ipython-input-28-39775babb578> in <module>
    ----> 1 g.to_standard('Congo (Kinshasa)',db='another base') # unknown base
    

    ~/Dropbox/Git/dev_versions/CoCoA/cocoa/geo.py in to_standard(self, w, **kwargs)
        125         db=kwargs.get('db',self.get_list_db()[0])
        126         if db not in self.get_list_db():
    --> 127             raise CocoaDbError('Unknown database "'+db+'" for translation to '
        128                 'standardized location names. See get_list_db() or help.')
        129 


    CocoaDbError: Unknown database "another base" for translation to standardized location names. See get_list_db() or help.



```python
g.to_standard('aus',output='another output') # bad output type
```


    ---------------------------------------------------------------------------

    CocoaKeyError                             Traceback (most recent call last)

    <ipython-input-29-75657fc6e3ef> in <module>
    ----> 1 g.to_standard('aus',output='another output') # bad output type
    

    ~/Dropbox/Git/dev_versions/CoCoA/cocoa/geo.py in to_standard(self, w, **kwargs)
        120         output=kwargs.get('output',self.get_list_output()[0])
        121         if output not in self.get_list_output():
    --> 122             raise CocoaKeyError('Incorrect output type. See get_list_output()'
        123                 ' or help.')
        124 


    CocoaKeyError: 'Incorrect output type. See get_list_output() or help.'



```python
g.to_standard('Europe',interpret_region=1) # bad type (boolean required) for interpret_region option
```


    ---------------------------------------------------------------------------

    CocoaTypeError                            Traceback (most recent call last)

    <ipython-input-30-236321a486ee> in <module>
    ----> 1 g.to_standard('Europe',interpret_region=1) # bad type (boolean required) for interpret_region option
    

    ~/Dropbox/Git/dev_versions/CoCoA/cocoa/geo.py in to_standard(self, w, **kwargs)
        130         interpret_region=kwargs.get('interpret_region',False)
        131         if not isinstance(interpret_region,bool):
    --> 132             raise CocoaTypeError('The interpret_region argument is a boolean, '
        133                 'not a '+str(type(interpret_region)))
        134 


    CocoaTypeError: The interpret_region argument is a boolean, not a <class 'int'>



```python
g.to_standard('elsewhere') # unknown country
```


    ---------------------------------------------------------------------------

    LookupError                               Traceback (most recent call last)

    ~/Dropbox/Git/dev_versions/CoCoA/cocoa/geo.py in to_standard(self, w, **kwargs)
        168                     try:
    --> 169                         n0=pc.countries.lookup(c)
        170                     except LookupError:


    ~/.local/lib/python3.8/site-packages/pycountry/db.py in load_if_needed(self, *args, **kw)
         44                 self._load()
    ---> 45         return f(self, *args, **kw)
         46     return load_if_needed


    ~/.local/lib/python3.8/site-packages/pycountry/db.py in lookup(self, value)
        136                     return candidate
    --> 137         raise LookupError('Could not find a record for %r' % value)
    

    LookupError: Could not find a record for 'elsewhere'

    
    During handling of the above exception, another exception occurred:


    LookupError                               Traceback (most recent call last)

    ~/Dropbox/Git/dev_versions/CoCoA/cocoa/geo.py in to_standard(self, w, **kwargs)
        171                         try:
    --> 172                             nf=pc.countries.search_fuzzy(c)
        173                             if len(nf)>1:


    ~/.local/lib/python3.8/site-packages/pycountry/__init__.py in search_fuzzy(self, query)
         87         if not results:
    ---> 88             raise LookupError(query)
         89 


    LookupError: elsewhere

    
    During handling of the above exception, another exception occurred:


    CocoaLookupError                          Traceback (most recent call last)

    <ipython-input-31-487287483e0e> in <module>
    ----> 1 g.to_standard('elsewhere') # unknown country
    

    ~/Dropbox/Git/dev_versions/CoCoA/cocoa/geo.py in to_standard(self, w, **kwargs)
        177                             n0=nf[0]
        178                         except LookupError:
    --> 179                             raise CocoaLookupError('No country match the key "'+c+'". Error.')
        180                         except Exception as e1:
        181                             raise CocoaNotManagedError('Not managed error '+type(e1))


    CocoaLookupError: No country match the key "Elsewhere". Error.



```python
g.to_standard('European Union',output='dict',interpret_region=True) # cannont create dict or pandas output with interpret_region=True
```


    ---------------------------------------------------------------------------

    CocoaKeyError                             Traceback (most recent call last)

    <ipython-input-32-bbd30d86d8f7> in <module>
    ----> 1 g.to_standard('European Union',output='dict',interpret_region=True) # cannont create dict or pandas output with interpret_region=True
    

    ~/Dropbox/Git/dev_versions/CoCoA/cocoa/geo.py in to_standard(self, w, **kwargs)
        134 
        135         if interpret_region==True and output!='list':
    --> 136             raise CocoaKeyError('The interpret_region True argument is incompatible '
        137                 'with non list output option.')
        138 


    CocoaKeyError: 'The interpret_region True argument is incompatible with non list output option.'



```python

```
