#!/usr/bin/env python
# coding: utf-8

# In[9]:


import geopandas as gpd
import numpy as np
import pandas as pd

shapefile='https://datanova.laposte.fr/explore/dataset/geoflar-departements-2015/download/?format=shp&timezone=Europe/Berlin&lang=fr'

gdf = gpd.read_file(shapefile)[['nom_dept','code_dept','geometry',]]

gdf.head()


# In[10]:


depnum=pd.to_numeric(gdf["code_dept"],errors='coerce').replace(np.nan,0,regex=True).astype(int)
gdf2=gdf[((depnum>0) & (depnum<100)) | (gdf["code_dept"]=="2A") | (gdf["code_dept"]=="2B")]
gdf2.head()


# In[11]:


# cas des tests
# Source https://www.data.gouv.fr/fr/datasets/donnees-relatives-aux-resultats-des-tests-virologiques-covid-19/

import urllib.request, json 
import pandas as pd
from io import StringIO

url_covid_france='https://www.data.gouv.fr/fr/datasets/r/406c6a23-e283-4300-9484-54e78c8ae675'

with urllib.request.urlopen(url_covid_france) as url:
    data=pd.read_table(StringIO(url.read().decode()),sep=",")
data.tail()


# In[12]:


import datetime as dt
ftime="%Y-%m-%d"
maxdata=max(data["jour"])


# In[13]:


from bokeh.io import curdoc, output_notebook, show
from bokeh.models import Slider, HoverTool, GeoJSONDataSource, LinearColorMapper, ColorBar
from bokeh.layouts import widgetbox, row, column
from bokeh.palettes import brewer
from bokeh.plotting import figure
from bokeh.palettes import brewer

#Define function that returns json_data for year selected by user.
    
def fjson_data(t):
    when=dt.datetime.strptime(maxdata,ftime)+dt.timedelta(days=t)
    whens=when.strftime(ftime)
    d=data[(data["jour"]==whens) & (data["cl_age90"]==0) ]
    v=d["p"]
    dd=pd.DataFrame({"dep":d["dep"],"val":v})
    merged=gdf2.merge(dd, left_on = 'code_dept', right_on = 'dep', how = 'left')
    return merged.to_json(),whens

#Input GeoJSON source that contains features for plotting.
geojson,when = fjson_data(0)
geosource = GeoJSONDataSource( geojson=geojson )

#Define a sequential multi-hue color palette.
palette = brewer['YlGnBu'][8]

#Reverse color order so that dark blue is highest obesity.
palette = palette[::-1]

#Instantiate LinearColorMapper that linearly maps numbers in a range, into a sequence of colors. Input nan_color.
color_mapper = LinearColorMapper(palette = palette, low = 0, high = 100, nan_color = '#d9d9d9')

#Define custom tick labels for color bar.
#tick_labels = {'0': '0%', '5': '5%', '10':'10%', '15':'15%', '20':'20%', '25':'25%', '30':'30%','35':'35%', '40': '>40%'}

#Add hover tool
hover = HoverTool(tooltips = [ ('Département','@nom_dept (@dep)'),('Nombre de cas', '@val')])

#Create color bar. 
color_bar = ColorBar(color_mapper=color_mapper, label_standoff=8,width = 500, height = 20,
                     border_line_color=None,location = (0,0), orientation = 'horizontal')#, major_label_overrides = tick_labels)


#Create figure object.
p = figure(title = 'Nombre de nouveaux cas positifs quotidiens le '+when, plot_height = 900 , plot_width = 950, tools = [hover]) # toolbar_location = None,
p.xgrid.grid_line_color = None
p.ygrid.grid_line_color = None

#Add patch renderer to figure. 
p.patches('xs','ys', source = geosource,fill_color = {'field' :'val', 'transform' : color_mapper}, line_color = 'black', line_width = 0.25, fill_alpha = 1)

p.add_layout(color_bar, 'below')

# Define the callback function: update_plot
def update_plot(attr, old, new):
    t = slider.value
    new_data,when = fjson_data(t)
    geosource.geojson = new_data
    p.title.text = 'Nombre de nouveaux cas positifs quotidiens le'+when
    
# Make a slider object: slider 
slider = Slider(title = 'Jour',start = -30, end = 0, step = 1, value = 0)
slider.on_change('value', update_plot)

# Make a column layout of widgetbox(slider) and plot, and add it to the current document
layout = column(p,widgetbox(slider))
curdoc().add_root(layout)

#Display plot inline in Jupyter notebook
output_notebook()

#Display plot
show(layout)


# In[ ]:




