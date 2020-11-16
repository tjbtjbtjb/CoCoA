# Help on cocoa.display (cocoa release 1.0)

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
import cocoa.display as cd
help(cd)
```

    Help on module cocoa.display in cocoa:
    
    NAME
        cocoa.display
    
    DESCRIPTION
        Project : CoCoA
        Date :    april-november 2020
        Authors : Olivier Dadoun, Julien Browaeys, Tristan Beau
        Copyright ©CoCoa-team-17
        License: See joint LICENSE file
        
        Module : display
        About :
        
        An interface module to easily plot cocoa data with bokeh
    
    CLASSES
        builtins.object
            CocoDisplay
        
        class CocoDisplay(builtins.object)
         |  CocoDisplay(db=None)
         |  
         |  Methods defined here:
         |  
         |  CrystalFig(self, crys, err_y)
         |  
         |  DefFigInteractive(self, **kwargs)
         |      Define interactive bokeh figure i.e with a window location selection
         |  
         |  __delete__(self, instance)
         |  
         |  __init__(self, db=None)
         |      Initialize self.  See help(type(self)) for accurate signature.
         |  
         |  get_pandas(self)
         |      Retrieve the pandas when CoCoDisplay is called
         |  
         |  return_map(self, mypandas, which_data=None, width_height=None, date='last')
         |      Create a Folium map from a pandas input
         |      
         |      Keyword arguments
         |      -----------------
         |      babepandas : pandas consided
         |      which_data: variable from pandas data. If pandas is produced from cocoa get_stat method
         |      then 'diff' and 'cumul' can be also used
         |      width_height : as a list of width and height of the histo, default [500,400]
         |      date : - default 'last'
         |             Value at the last date (from database point of view) and for all the location defined in
         |             the pandas will be computed
         |             - date
         |             Value at date (from database point of view) and for all the location defined in the pandas
         |             will be computed
         |  
         |  standardfig(self, title=None, axis_type='linear', x_axis_type='datetime')
         |  
         |  ----------------------------------------------------------------------
         |  Static methods defined here:
         |  
         |  cocoa_basic_plot(babepandas, input_names_data=None, title=None, width_height=None)
         |      Create a Bokeh plot with a date axis from pandas input
         |      
         |      Keyword arguments
         |      -----------------
         |      babepandas : pandas where the data is considered
         |      input_names_data : variable from pandas data . If pandas is produced from cocoas get_stat method
         |      the 'diff' or 'cumul' are available
         |      A list of names_data can be given
         |      title: title for the figure , no title by default
         |      width_height : width and height of the figure,  default [400,300]
         |      
         |      
         |      Note
         |      -----------------
         |      HoverTool is available it returns location, date and value
         |  
         |  cocoa_histo(babepandas, input_names_data=None, bins=None, title=None, width_height=None, date='last')
         |      Create a Bokeh histogram from a pandas input
         |      
         |      Keyword arguments
         |      -----------------
         |      babepandas : pandas consided
         |      input_names_data : variable from pandas data. If pandas is produced from cocoa get_stat method
         |      then 'diff' and 'cumul' can be also used
         |      title: title for the figure , no title by default
         |      width_height : as a list of width and height of the histo, default [500,400]
         |      bins : number of bins of the hitogram default 50
         |      date : - default 'last'
         |             Value at the last date (from database point of view) and for all the location defined in
         |             the pandas will be computed
         |             - date
         |             Value at date (from database point of view) and for all the location defined in the pandas
         |             will be computed
         |             - 'all'
         |             Value for all the date and for all the location will be computed
         |      Note
         |      -----------------
         |      HoverTool is available it returns position of the middle of the bin and the value. In the case where
         |      date='all' i.e all the date for all the location then location name is provided
         |  
         |  min_max_range(a_min, a_max)
         |      Return a cleverly rounded min and max giving raw min and raw max of data.
         |      Usefull for hist range and colormap
         |  
         |  ----------------------------------------------------------------------
         |  Data descriptors defined here:
         |  
         |  __dict__
         |      dictionary for instance variables (if defined)
         |  
         |  __weakref__
         |      list of weak references to the object (if defined)
    
    FUNCTIONS
        resume_pandas(self, pd)
    
    DATA
        Paired12 = ('#a6cee3', '#1f78b4', '#b2df8a', '#33a02c', '#fb9a99', '#e...
        brewer = {'Accent': {3: ('#7fc97f', '#beaed4', '#fdc086'), 4: ('#7fc97...
        width_height_default = [500, 400]
    
    FILE
        /home/beau/Dropbox/Git/dev_versions/CoCoA/cocoa/display.py
    
    



```python

```
