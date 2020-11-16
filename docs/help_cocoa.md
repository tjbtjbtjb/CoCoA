# Help on cocoa.cocoa (cocoa release 1.0)

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
import cocoa.cocoa as coco
help(coco)
```



    JHU aka Johns Hopkins database selected ...
    Few information concernant the selected database :  jhu
    Available which key-words for:  ['deaths', 'confirmed', 'recovered']
    Example of location :  Indonesia, Chad, Dominica, France, Spain  ...
    Last date data  11/15/20
    Help on module cocoa.cocoa in cocoa:
    
    NAME
        cocoa.cocoa
    
    DESCRIPTION
        Project : CoCoA - Copyright © CoCoa-team-17
        Date :    april-november 2020
        Authors : Olivier Dadoun, Julien Browaeys, Tristan Beau
        License: See joint LICENSE file
        About
        -----
        This is the CoCoA front end functions. It provides easy access and
        use of the whole CoCoA framework in a simplified way.
        The use can change the database, the type of data, the output format
        with keywords (see help of functions below).
        Basic usage
        -----------
        ** plotting covid deaths (default value) vs. time **
            import cocoa.cocoa as cc
            cc.plot(where='France')  # where keyword is mandatory
        ** getting recovered data for some countries **
        
            cc.get(where=['Spain','Italy'],which='recovered')
        ** listing available database and which data can be used **
            cc.listwhom()
            cc.setwhom('JHU') # return available keywords (aka 'which' data)
            cc.listwhich()   # idem
            cc.listwhat()    # return available time serie type (total,
                             # daily...)
    
    FUNCTIONS
        get(**kwargs)
            Return covid19 data in specified format output (default, by list)
            for specified locations ('where' keyword).
            The used database is set by the setbase() function but can be
            changed on the fly ('whom' keyword)
            Keyword arguments
            -----------------
            
            where  --   a single string of location, or list of (mandatory,
                        no default value)
            which  --   what sort of data to deliver ( 'death','confirmed',
                        'recovered' …). See listwhat() function for full
                        list according to the used database.
            what   --   which data are computed, either in cumulative mode
                        ( 'cumul', default value) or 'daily' or other. See
                        listwhich() for fullist of available
                        Full list of which keyword with the listwhich() function.
            whom   --   Database specification (overload the setbase()
                        function). See listwhom() for supported list
                        function). See listwhom() for supported list
            
            output --   output format returned ( list (default), dict or pandas)
        
        hist(**kwargs)
            Create histogram according to arguments (same as the get
            function) and options.
            
            Keyword arguments
            -----------------
            
            where (mandatory), what, which, whom : (see help(get))
            input  --   input data to plot within the cocoa framework (e.g.
                        after some analysis or filtering). Default is None which
                        means that we use the basic raw data through the get
                        function.
                        When the 'input' keyword is set, where, what, which,
                        whom keywords are ignored.
        
        listwhat()
            Return the list of currently avalailable type of series available.
            The first one is the default one.
        
        listwhich(dbname=None)
            Get which are the available fields for the current or specified
            base. Output is a list of string.
            By default, the listwhich()[0] is the default which field in other
            functions.
        
        listwhom()
            Return the list of currently avalailable databases for covid19
            data in CoCoA.
            The first one is the default one.
        
        map(**kwargs)
            Create a map according to arguments and options.
            See help(hist).
        
        plot(**kwargs)
            Plot data according to arguments (same as the get function)
            and options.
            
            Keyword arguments
            -----------------
            
            where (mandatory), what, which, whom : (see help(get))
            
            input  --   input data to plot within the cocoa framework (e.g.
                        after some analysis or filtering). Default is None which
                        means that we use the basic raw data through the get
                        function.
                        When the 'input' keyword is set, where, what, which,
                        whom keywords are ignored.
                        input should be given as valid cocoa pandas dataframe.
        
        setwhom(base)
            Set the covid19 database used, given as a string.
            Please see cocoa.listbase() for the available current list.
            
            By default, the listbase()[0] is the default base used in other
            functions.
    
    DATA
        __warningregistry__ = {'version': 22}
        brewer = {'Accent': {3: ('#7fc97f', '#beaed4', '#fdc086'), 4: ('#7fc97...
    
    FILE
        /home/beau/Dropbox/Git/dev_versions/CoCoA/cocoa/cocoa.py
    
    



```python

```
