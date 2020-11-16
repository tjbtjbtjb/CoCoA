# Testing cocoa.geo.GeoRegion (cocoa release 1.0)

Within the cocoa.geo, the GeoRegion provides method interpret region name as list of country names.

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
from cocoa.geo import GeoRegion as gr
```

## Getting some help


```python
help(gr)
```

    Help on class GeoRegion in module cocoa.geo:
    
    class GeoRegion(builtins.object)
     |  GeoRegion class definition. Does not inheritate from any other
     |  class.
     |  
     |  It should raise only CocoaError and derived exceptions in case
     |  of errors (see cocoa.error)
     |  
     |  Methods defined here:
     |  
     |  __init__(self)
     |      __init__ member function.
     |  
     |  get_countries_from_region(self, region)
     |      it returns a list of countries for the given region name.
     |      The standard used is iso3. To convert to another standard,
     |      use the GeoManager class.
     |  
     |  get_pandas(self)
     |  
     |  get_region_list(self)
     |  
     |  get_source(self)
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
g=gr() # Create the instance of GeoManager 
```

### Known regions (United Nation M49 geoscheme)
and some usefull additionnal regions.


```python
g.get_region_list() # The list of known regions
```




    ['World',
     'Africa',
     'Northern Africa',
     'Sub-Saharan Africa',
     'Eastern Africa',
     'Middle Africa',
     'Southern Africa',
     'Western Africa',
     'Americas',
     'Latin America and the Caribbean',
     'Caribbean',
     'Central America',
     'South America',
     'North America',
     'Northern America',
     'Asia',
     'Central Asia',
     'Eastern Asia',
     'South-eastern Asia',
     'Southern Asia',
     'Western Asia',
     'Europe',
     'Eastern Europe',
     'Northern Europe',
     'Southern Europe',
     'Western Europe',
     'Oceania',
     'Australia and New Zealand',
     'Melanesia',
     'Micronesia',
     'Polynesia',
     'European Union',
     'G7',
     'G8',
     'G20',
     'Oecd',
     'G77']




```python
g.get_source()
```




    {'UN_M49': 'https://en.wikipedia.org/wiki/UN_M49',
     'GeoScheme': 'https://en.wikipedia.org/wiki/List_of_countries_by_United_Nations_geoscheme',
     'European Union': 'https://europa.eu/european-union/about-eu/countries/member-countries_en',
     'G7': 'https://en.wikipedia.org/wiki/Group_of_Seven',
     'G8': 'https://en.wikipedia.org/wiki/Group_of_Eight',
     'G20': 'https://en.wikipedia.org/wiki/G20',
     'G77': 'https://www.g77.org/doc/members.html',
     'OECD': 'https://en.wikipedia.org/wiki/OECD'}



### Getting countries from a given region


```python
g.get_countries_from_region('South America')
```




    ['ARG',
     'BOL',
     'BRA',
     'BVT',
     'CHL',
     'COL',
     'ECU',
     'FLK',
     'GUF',
     'GUY',
     'PER',
     'PRY',
     'SGS',
     'SUR',
     'URY',
     'VEN']



### Getting the whole pandas from the used database


```python
g.get_pandas()
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
      <th>iso3</th>
      <th>capital</th>
      <th>region</th>
      <th>region_name</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>DZA</td>
      <td>Algiers</td>
      <td>15</td>
      <td>Northern Africa</td>
    </tr>
    <tr>
      <th>1</th>
      <td>DZA</td>
      <td>Algiers</td>
      <td>2</td>
      <td>Africa</td>
    </tr>
    <tr>
      <th>2</th>
      <td>DZA</td>
      <td>Algiers</td>
      <td>1</td>
      <td>World</td>
    </tr>
    <tr>
      <th>3</th>
      <td>EGY</td>
      <td>Cairo</td>
      <td>15</td>
      <td>Northern Africa</td>
    </tr>
    <tr>
      <th>4</th>
      <td>EGY</td>
      <td>Cairo</td>
      <td>2</td>
      <td>Africa</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>885</th>
      <td>TUV</td>
      <td>Funafuti</td>
      <td>9</td>
      <td>Oceania</td>
    </tr>
    <tr>
      <th>886</th>
      <td>TUV</td>
      <td>Funafuti</td>
      <td>1</td>
      <td>World</td>
    </tr>
    <tr>
      <th>887</th>
      <td>WLF</td>
      <td>Mata-Utu</td>
      <td>61</td>
      <td>Polynesia</td>
    </tr>
    <tr>
      <th>888</th>
      <td>WLF</td>
      <td>Mata-Utu</td>
      <td>9</td>
      <td>Oceania</td>
    </tr>
    <tr>
      <th>889</th>
      <td>WLF</td>
      <td>Mata-Utu</td>
      <td>1</td>
      <td>World</td>
    </tr>
  </tbody>
</table>
<p>890 rows × 4 columns</p>
</div>



## Management of errors

As far as possible, errors are managed within the `cocoa.error` framework. `CocoaError` should be raised.


```python
g.get_countries_from_region('somewhere') # unknown region
```


    ---------------------------------------------------------------------------

    CocoaKeyError                             Traceback (most recent call last)

    <ipython-input-10-1ab44cb1dcbb> in <module>
    ----> 1 g.get_countries_from_region('somewhere') # unknown region
    

    ~/Dropbox/Git/dev_versions/CoCoA/cocoa/geo.py in get_countries_from_region(self, region)
        566 
        567         if region not in self.get_region_list():
    --> 568             raise CocoaKeyError('The given region "'+str(region)+'" is unknown.')
        569 
        570         clist=[]


    CocoaKeyError: 'The given region "Somewhere" is unknown.'



```python
g.get_countries_from_region(['Europe','Americas']) # Bad type, expecting only string
```


    ---------------------------------------------------------------------------

    CocoaKeyError                             Traceback (most recent call last)

    <ipython-input-11-409ae1e0b531> in <module>
    ----> 1 g.get_countries_from_region(['Europe','Americas']) # Bad type, expecting only string
    

    ~/Dropbox/Git/dev_versions/CoCoA/cocoa/geo.py in get_countries_from_region(self, region)
        561 
        562         if type(region) != str:
    --> 563             raise CocoaKeyError("The given region is not a str type.")
        564 
        565         region=region.title()  # if not properly capitalized


    CocoaKeyError: 'The given region is not a str type.'



```python

```
