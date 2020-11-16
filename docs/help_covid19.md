# Help on cocoa.covid19 (cocoa release 1.0)

## Making CoCoA available
If executed locally


```python
import sys
sys.path.insert(1, '..')
```

If executed on a server (e.g. Google Colab ), you should install cocoa via pip3


```python
!pip3 install -q git+https://github.com/tjbtjbtjb/CoCoA.git
```


```python
import cocoa.covid19 as cc
help(cc)
```

    Help on module cocoa.covid19 in cocoa:
    
    NAME
        cocoa.covid19
    
    DESCRIPTION
        Project : CoCoA
        Date :    april-november 2020
        Authors : Olivier Dadoun, Julien Browaeys, Tristan Beau
        Copyright © CoCoa-team-17
        License: See joint LICENSE file
        
        Module : cocoa.covid19
        About :
        
        Main class definitions for covid19 dataset access. Currently, we are only using the JHU CSSE data.
        The parser class gives a simplier access through an already filled dict of data
    
    CLASSES
        builtins.object
            DataBase
        
        class DataBase(builtins.object)
         |  DataBase(db_name)
         |  
         |  Parse the chosen database and a return a pandas
         |  
         |  Methods defined here:
         |  
         |  __init__(self, db_name)
         |      Initialize self.  See help(type(self)) for accurate signature.
         |  
         |  csv_to_pandas_index_location_date(self, url, **kwargs)
         |      Parse and convert CSV file to a pandas with location+date as an index
         |  
         |  fill_cocoa_field(self)
         |      Fill CoCoA variables with database data
         |  
         |  flat_list(self, matrix)
         |  
         |  get_available_database(self)
         |      Return available COVID database
         |  
         |  get_available_keys_words(self)
         |      Return available keys words for the database selected
         |  
         |  get_cumul_days(self)
         |  
         |  get_current_days(self)
         |  
         |  get_database_url(self)
         |      Return the url associated with chosen database
         |  
         |  get_dates(self)
         |      Return all dates available in the current database
         |  
         |  get_db(self)
         |      Return database name
         |  
         |  get_diff_days(self)
         |  
         |  get_locations(self)
         |      Return available location countries / regions in the current database
         |  
         |  get_more_db_info(self, country)
         |  
         |  get_posteriors(self, sr, window=7, min_periods=1)
         |  
         |  get_rawdata(self)
         |      Return raw data associated with chosen database
         |  
         |  get_stats(self, **kwargs)
         |  
         |  pandas_index_location_date_to_jhu_format(self, mypandas, **kwargs)
         |      Return a pandas in CoCoa Structure
         |  
         |  parse_convert_jhu(self)
         |      For center for Systems Science and Engineering (CSSE) at Johns Hopkins University
         |      COVID-19 Data Repository by the see homepage: https://github.com/CSSEGISandData/COVID-19
         |  
         |  set_more_db_info(self, country, val)
         |  
         |  smooth_cases(self, cases)
         |      ## https://www.kaggle.com/freealf/estimation-of-rt-from-cases
         |  
         |  ----------------------------------------------------------------------
         |  Data descriptors defined here:
         |  
         |  __dict__
         |      dictionary for instance variables (if defined)
         |  
         |  __weakref__
         |      list of weak references to the object (if defined)
    
    FILE
        /home/beau/Dropbox/Git/dev_versions/CoCoA/cocoa/covid19.py
    
    



```python

```
