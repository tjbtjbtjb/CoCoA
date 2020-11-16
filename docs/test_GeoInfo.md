# Testing cocoa.geo.GeoInfo (cocoa release 1.0)

Within the `cocoa.geo`, the `GeoInfo` provide data for all countries, using various databases.

## Making  CoCoA available
If executed locally


```python
import sys
sys.path.insert(1, '..')
```

If executed on a jupyter server (e.g. [Google Colab](https://colab.research.google.com/) ), you should install cocoa via `pip3`


```python
!pip3 install -q git+https://github.com/tjbtjbtjb/CoCoA.git
```


```python
from cocoa.geo import GeoInfo as gi
```

## Getting some help


```python
help(gi)
```

    Help on class GeoInfo in module cocoa.geo:
    
    class GeoInfo(builtins.object)
     |  GeoInfo(gm=0)
     |  
     |  GeoInfo class definition. No inheritance from any other class.
     |  
     |  It should raise only CocoaError and derived exceptions in case
     |  of errors (see cocoa.error)
     |  
     |  Methods defined here:
     |  
     |  __init__(self, gm=0)
     |      __init__ member function.
     |  
     |  add_field(self, **kwargs)
     |      this is the main function of the GeoInfo class. It adds to
     |      the input pandas dataframe some fields according to
     |      the geofield field of input.
     |      The return value is the pandas dataframe.
     |      
     |      Arguments :
     |      field    -- should be given as a string of list of strings and
     |                  should be valid fields (see get_list_field() )
     |                  Mandatory.
     |      input    -- provide the input pandas dataframe. Mandatory.
     |      geofield -- provide the field name in the pandas where the
     |                  location is stored. Default : 'location'
     |      overload -- Allow to overload a field. Boolean value.
     |                  Default : False
     |  
     |  get_list_field(self)
     |      return the list of supported additionnal fields available
     |  
     |  get_source(self, field=None)
     |      return the source of the information provided for a given
     |      field.
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
g=gi() # Create the instance of GeoManager 
```

### Currently known fields from countries


```python
g.get_list_field()
```




    ['area',
     'capital',
     'continent_code',
     'continent_name',
     'country_name',
     'fertility',
     'geometry',
     'median_age',
     'population',
     'region_code_list',
     'region_name_list',
     'urban_rate']




```python
g.get_source() # for all available fields
```




    {'continent_code': 'pycountry_convert (https://pypi.org/project/pycountry-convert/)',
     'continent_name': 'pycountry_convert (https://pypi.org/project/pycountry-convert/)',
     'country_name': 'pycountry_convert (https://pypi.org/project/pycountry-convert/)',
     'population': 'https://www.worldometers.info/world-population/population-by-country/',
     'area': 'https://www.worldometers.info/world-population/population-by-country/',
     'fertility': 'https://www.worldometers.info/world-population/population-by-country/',
     'median_age': 'https://www.worldometers.info/world-population/population-by-country/',
     'urban_rate': 'https://www.worldometers.info/world-population/population-by-country/',
     'geometry': 'https://github.com/johan/world.geo.json/',
     'region_code_list': 'https://en.wikipedia.org/wiki/List_of_countries_by_United_Nations_geoscheme',
     'region_name_list': 'https://en.wikipedia.org/wiki/List_of_countries_by_United_Nations_geoscheme',
     'capital': 'https://en.wikipedia.org/wiki/List_of_countries_by_United_Nations_geoscheme'}




```python
g.get_source('geometry') # for a specific field
```




    'geometry : https://github.com/johan/world.geo.json/'



### Adding info to a pandas

The pandas may come from `cocoa` or may be created within another framework


```python
import pandas as pd
country=['France','Italy','Germany','Tunisia','Egypt']
value=[1,2,3,4,5]
pf=pd.DataFrame({'location':country,'value':value})
pf
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
      <th>location</th>
      <th>value</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>France</td>
      <td>1</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Italy</td>
      <td>2</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Germany</td>
      <td>3</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Tunisia</td>
      <td>4</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Egypt</td>
      <td>5</td>
    </tr>
  </tbody>
</table>
</div>




```python
g.add_field(input=pf,field='population') # adding one field
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
      <th>location</th>
      <th>value</th>
      <th>population</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>France</td>
      <td>1</td>
      <td>65273511</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Italy</td>
      <td>2</td>
      <td>60461826</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Germany</td>
      <td>3</td>
      <td>83783942</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Tunisia</td>
      <td>4</td>
      <td>11818619</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Egypt</td>
      <td>5</td>
      <td>102334404</td>
    </tr>
  </tbody>
</table>
</div>




```python
g.add_field(input=pf,field=['capital','region_name_list','population','region_code_list']) # adding list of fields
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
      <th>location</th>
      <th>value</th>
      <th>capital</th>
      <th>region_name_list</th>
      <th>population</th>
      <th>region_code_list</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>France</td>
      <td>1</td>
      <td>Paris</td>
      <td>[Western Europe, Europe, World]</td>
      <td>65273511</td>
      <td>[155, 150, 1]</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Italy</td>
      <td>2</td>
      <td>Rome</td>
      <td>[Northern Africa, Africa, World]</td>
      <td>60461826</td>
      <td>[15, 2, 1]</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Germany</td>
      <td>3</td>
      <td>Berlin</td>
      <td>[Western Europe, Europe, World]</td>
      <td>83783942</td>
      <td>[155, 150, 1]</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Tunisia</td>
      <td>4</td>
      <td>Tunis</td>
      <td>[Southern Europe, Europe, World]</td>
      <td>11818619</td>
      <td>[39, 150, 1]</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Egypt</td>
      <td>5</td>
      <td>Cairo</td>
      <td>[Northern Africa, Africa, World]</td>
      <td>102334404</td>
      <td>[15, 2, 1]</td>
    </tr>
  </tbody>
</table>
</div>




```python
pf2=pf.copy() 
pf2['capital']=['a','b','c','d','e']
print(pf2)
g.add_field(input=pf2,field='capital',overload=True) # overload an existing field
```

      location  value capital
    0   France      1       a
    1    Italy      2       b
    2  Germany      3       c
    3  Tunisia      4       d
    4    Egypt      5       e





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
      <th>location</th>
      <th>value</th>
      <th>capital</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>France</td>
      <td>1</td>
      <td>Paris</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Italy</td>
      <td>2</td>
      <td>Rome</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Germany</td>
      <td>3</td>
      <td>Berlin</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Tunisia</td>
      <td>4</td>
      <td>Tunis</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Egypt</td>
      <td>5</td>
      <td>Cairo</td>
    </tr>
  </tbody>
</table>
</div>




```python
pf2=pf2.rename(columns={'location':'here'})
print(pf2)
g.add_field(input=pf2,field='area',geofield='here')
```

          here  value capital
    0   France      1       a
    1    Italy      2       b
    2  Germany      3       c
    3  Tunisia      4       d
    4    Egypt      5       e





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
      <th>here</th>
      <th>value</th>
      <th>capital</th>
      <th>area</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>France</td>
      <td>1</td>
      <td>a</td>
      <td>547557</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Italy</td>
      <td>2</td>
      <td>b</td>
      <td>294140</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Germany</td>
      <td>3</td>
      <td>c</td>
      <td>348560</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Tunisia</td>
      <td>4</td>
      <td>d</td>
      <td>155360</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Egypt</td>
      <td>5</td>
      <td>e</td>
      <td>995450</td>
    </tr>
  </tbody>
</table>
</div>



## Management of errors

As far as possible, errors are managed within the `cocoa.error` framework. `CocoaError` should be raised.


```python
g.get_source('myfield') # source for an unknonw field
```


    ---------------------------------------------------------------------------

    CocoaKeyError                             Traceback (most recent call last)

    <ipython-input-15-64cac9fb5649> in <module>
    ----> 1 g.get_source('myfield') # source for an unknonw field
    

    ~/Dropbox/Git/dev_versions/CoCoA/cocoa/geo.py in get_source(self, field)
        313             return self._list_field
        314         elif field not in self.get_list_field():
    --> 315             raise CocoaKeyError('The field "'+str(field)+'" is not '
        316                 'a supported field of GeoInfo(). Please see help or '
        317                 'the get_list_field() output.')


    CocoaKeyError: 'The field "myfield" is not a supported field of GeoInfo(). Please see help or the get_list_field() output.'



```python
g.add_field() # no input
```


    ---------------------------------------------------------------------------

    CocoaTypeError                            Traceback (most recent call last)

    <ipython-input-16-1246f580b67c> in <module>
    ----> 1 g.add_field() # no input
    

    ~/Dropbox/Git/dev_versions/CoCoA/cocoa/geo.py in add_field(self, **kwargs)
        342         p=kwargs.get('input',None) # the panda
        343         if not isinstance(p,pd.DataFrame):
    --> 344             raise CocoaTypeError('You should provide a valid input pandas'
        345                 ' DataFrame as input. See help.')
        346         p=p.copy()


    CocoaTypeError: You should provide a valid input pandas DataFrame as input. See help.



```python
g.add_field(input='nothing') # bad input
```


    ---------------------------------------------------------------------------

    CocoaTypeError                            Traceback (most recent call last)

    <ipython-input-17-f3ac1ef21a24> in <module>
    ----> 1 g.add_field(input='nothing') # bad input
    

    ~/Dropbox/Git/dev_versions/CoCoA/cocoa/geo.py in add_field(self, **kwargs)
        342         p=kwargs.get('input',None) # the panda
        343         if not isinstance(p,pd.DataFrame):
    --> 344             raise CocoaTypeError('You should provide a valid input pandas'
        345                 ' DataFrame as input. See help.')
        346         p=p.copy()


    CocoaTypeError: You should provide a valid input pandas DataFrame as input. See help.



```python
g.add_field(input=pf) # no field given
```


    ---------------------------------------------------------------------------

    CocoaKeyError                             Traceback (most recent call last)

    <ipython-input-18-6d1015d71b30> in <module>
    ----> 1 g.add_field(input=pf) # no field given
    

    ~/Dropbox/Git/dev_versions/CoCoA/cocoa/geo.py in add_field(self, **kwargs)
        352         fl=kwargs.get('field',None) # field list
        353         if fl == None:
    --> 354             raise CocoaKeyError('No field given. See help.')
        355         if not isinstance(fl,list):
        356             fl=[fl]


    CocoaKeyError: 'No field given. See help.'



```python
g.add_field(input=pf,field='myfield') # unknown field
```


    ---------------------------------------------------------------------------

    CocoaKeyError                             Traceback (most recent call last)

    <ipython-input-19-141ccb2c83fe> in <module>
    ----> 1 g.add_field(input=pf,field='myfield') # unknown field
    

    ~/Dropbox/Git/dev_versions/CoCoA/cocoa/geo.py in add_field(self, **kwargs)
        356             fl=[fl]
        357         if not all(f in self.get_list_field() for f in fl):
    --> 358             raise CocoaKeyError('All fields are not valid or supported '
        359                 'ones. Please see help of get_list_field()')
        360 


    CocoaKeyError: 'All fields are not valid or supported ones. Please see help of get_list_field()'



```python
g.add_field(input=pf2,field='population') # no geofield given whereas 'location' is not available to localize the country
```


    ---------------------------------------------------------------------------

    CocoaKeyError                             Traceback (most recent call last)

    <ipython-input-21-eb9022e58f74> in <module>
    ----> 1 g.add_field(input=pf2,field='population') # no geofield given whereas 'location' is not available to localize the country
    

    ~/Dropbox/Git/dev_versions/CoCoA/cocoa/geo.py in add_field(self, **kwargs)
        369                 'string.')
        370         if geofield not in p.columns.tolist():
    --> 371             raise CocoaKeyError('The geofield "'+geofield+'" given is '
        372                 'not a valid column name of the input pandas dataframe.')
        373 


    CocoaKeyError: 'The geofield "location" given is not a valid column name of the input pandas dataframe.'



```python
g.add_field(input=pf2,field='capital',geofield='here') # try to overload a column which exists already, without the overload option
```


    ---------------------------------------------------------------------------

    CocoaKeyError                             Traceback (most recent call last)

    <ipython-input-23-0abf74d02479> in <module>
    ----> 1 g.add_field(input=pf2,field='capital',geofield='here') # try to overload a column which exists already, without the overload option
    

    ~/Dropbox/Git/dev_versions/CoCoA/cocoa/geo.py in add_field(self, **kwargs)
        360 
        361         if not overload and not all(f not in p.columns.tolist() for f in fl):
    --> 362             raise CocoaKeyError('Some fields already exist in you panda '
        363                 'dataframe columns. You may set overload to True.')
        364 


    CocoaKeyError: 'Some fields already exist in you panda dataframe columns. You may set overload to True.'



```python

```
