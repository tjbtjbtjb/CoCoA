# Help on cocoa.geo (cocoa release 1.0)

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
import cocoa.geo as cg
help(cg)
```

    Help on module cocoa.geo in cocoa:
    
    NAME
        cocoa.geo
    
    DESCRIPTION
        Project : CoCoA
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
    
    CLASSES
        builtins.object
            GeoInfo
            GeoManager
            GeoRegion
        
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
    
    FILE
        /home/beau/Dropbox/Git/dev_versions/CoCoA/cocoa/geo.py
    
    



```python

```
