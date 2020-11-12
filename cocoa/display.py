# -*- coding: utf-8 -*-

"""
Project : CoCoA
Date :    april-june 2020
Authors : Olivier Dadoun, Julien Browaeys, Tristan Beau
Copyright ©CoCoa-team-17
License: See joint LICENSE file

Module : cocoaplot
About :

An interface module to easily plot cocoa data with bokeh

"""

import random
import math
import pandas as pd
import geopandas as gpd

from datetime import datetime as dt
from collections import defaultdict

import bokeh
from bokeh.io import show, output_notebook
from bokeh.models import ColumnDataSource, ColorBar, HoverTool, Legend
from bokeh.plotting import figure, output_file, show
from bokeh.palettes import brewer
from bokeh.layouts import row, column, gridplot
from bokeh.models import CustomJS, Slider, Select, Plot, \
    Button, LinearAxis, Range1d, DatetimeTickFormatter
from bokeh.models import CheckboxGroup, RadioGroup, Toggle, RadioGroup
from bokeh.palettes import Paired12
from bokeh.models.widgets import Tabs, Panel
from bokeh.models import Label, LabelSet
from bokeh.models import ColumnDataSource, Grid, Line, LinearAxis, Plot
from bokeh.models import DataRange1d
from bokeh.models import LogScale
import bokeh.palettes
import itertools
import sys

import cocoa.geo as coge
from cocoa.verb import info,verb

from pyproj import CRS
#import plotly.express as px
#import plotly.graph_objects as go
from branca.colormap import LinearColormap
import folium
import json
from geopy.geocoders import Nominatim
import altair as alt
import numpy as np
from shapely.ops import unary_union

class CocoDisplay():
    def __init__(self,db=None):
        verb("Init of CocoDisplay()")
        self.colors = itertools.cycle(Paired12)
        self.coco_circle = []
        self.coco_line = []
        self.base_fig = None
        self.hover_tool = None
        self.increment = 1
        if db == None:
            self.info = coge.GeoInfo()
        else:
            self.info = coge.GeoInfo(db.geo)


    def standardfig(self,title=None, axis_type='linear',x_axis_type='datetime'):
         return figure(title=title,plot_width=400, plot_height=300,y_axis_type=axis_type,x_axis_type=x_axis_type,
         tools=['save','box_zoom,box_select,crosshair,reset'])

    @staticmethod
    def cocoa_basic_plot(babepandas, input_names_data = None,title = None, width_height = None):
        """Create a Bokeh plot with a date axis from pandas input

        Keyword arguments
        -----------------
        babepandas : pandas where the data is considered
        input_names_data : variable from pandas data . If pandas is produced from cocoas get_stat method
        the 'diff' or 'cumul' are available
        A list of names_data can be given
        title: title for the figure , no title by default
        width_height : width and height of the figure,  default [400,300]


        Note
        -----------------
        HoverTool is available it returns location, date and value
        """

        dict_filter_data = defaultdict(list)
        tooltips='Date: @date{%F} <br>  $name: @$name'

        if type(input_names_data) is None.__class__:
            print("Need variable to plot", file=sys.stderr)

        if not isinstance(input_names_data, list):
           input_names_data=[input_names_data]

        if 'location' in babepandas.columns:
            tooltips='Location: @location <br> Date: @date{%F} <br>  $name: @$name'
            loc = babepandas['location'].unique()
            shorten_loc = [ i if len(i)<15 else i.replace('-',' ').split()[0]+'...'+i.replace('-',' ').split()[-1] for i in loc]
            for i in input_names_data:
                dict_filter_data[i] =  \
                    dict(babepandas.loc[babepandas['location'].isin(loc)].groupby('location').__iter__())
                for j in range(len(loc)):
                    dict_filter_data[i][shorten_loc[j]] = dict_filter_data[i].pop(loc[j])

        else:
            for i in input_names_data:
                dict_filter_data[i] = {i:babepandas}

        hover_tool = HoverTool(tooltips=tooltips,formatters={'@date': 'datetime'})

        panels = []
        for axis_type in ["linear", "log"]:
            if width_height:
                plot_width  = width_height[0]
                plot_height = width_height[1]
            else :
                plot_width  = 400
                plot_height = 300
            standardfig = figure(plot_width=plot_width, plot_height=plot_height,y_axis_type=axis_type, x_axis_type='datetime',
            tools=['save','box_zoom,box_select,crosshair,reset'],toolbar_location="below")
            if title:
                standardfig.title.text = title
            standardfig.add_tools(hover_tool)
            colors = itertools.cycle(Paired12)
            for i in input_names_data:
                p = [standardfig.line(x='date', y=i, source=ColumnDataSource(value),
                color=next(colors), line_width=3, legend_label=key,
                name=i,hover_line_width=4) for key,value in dict_filter_data[i].items()]

            standardfig.legend.label_text_font_size = "12px"
            panel = Panel(child=standardfig , title=axis_type)
            panels.append(panel)
            standardfig.legend.background_fill_alpha = 0.6

            standardfig.legend.location = "bottom_left"

        standardfig.xaxis.formatter = DatetimeTickFormatter(
        days=["%d %B %Y"], months=["%d %B %Y"], years=["%d %B %Y"])
        tabs = Tabs(tabs=panels)
        return tabs

    @staticmethod
    def cocoa_histo(babepandas, input_names_data = None, bins=None,title = None, width_height = None ,  date = 'last'):
        """Create a Bokeh histogram from a pandas input

        Keyword arguments
        -----------------
        babepandas : pandas consided
        input_names_data : variable from pandas data. If pandas is produced from cocoa get_stat method
        then 'diff' and 'cumul' can be also used
        title: title for the figure , no title by default
        width_height : width and height of the figure,  default [400,300]
        bins : number of bins of the hitogram default 50
        date : - default 'last'
               Value at the last date (from database point of view) and for all the location defined in
               the pandas will be computed
               - date
               Value at date (from database point of view) and for all the location defined in the pandas
               will be computed
               - 'all'
               Value for all the date and for all the location will be computed
        Note
        -----------------
        HoverTool is available it returns position of the middle of the bin and the value. In the case where
        date='all' i.e all the date for all the location then location name is provided
        """

        dict_histo = defaultdict(list)
        if bins:
            bins = bins
        else:
            bins = 50

        if type(input_names_data) is None.__class__:
            print("Need variable to plot", file=sys.stderr)

        if 'location' in babepandas.columns:
            tooltips='Value at around @middle_bin : @val'
            loc = babepandas['location'].unique()
            shorten_loc = [ i if len(i)<15 else i.replace('-',' ').split()[0]+'...'+i.replace('-',' ').split()[-1] for i in loc]

            if date == 'all':
                tooltips='Location: @location <br> Value at around @middle_bin : @val'
                for w in loc:
                    histo,edges = np.histogram((babepandas.loc[babepandas['location'] == w][input_names_data]),density=False, bins=bins)
                    dict_histo[w] = pd.DataFrame({'location':w,'val': histo,
                       'left': edges[:-1],
                       'right': edges[1:],
                       'middle_bin':np.floor(edges[:-1]+(edges[1:]-edges[:-1])/2)})
                for j in range(len(loc)):
                    dict_histo[shorten_loc[j]] = dict_histo.pop(loc[j])

            else:
               if date == "last" :
                   when = babepandas['date'].max()
               else:
                   when = date
               val_per_country=[]
               for w in loc:
                   val_per_country.append(babepandas.loc[(babepandas['location'] == w) & (babepandas['date'] == when)][input_names_data].values)
               histo,edges = np.histogram(val_per_country,density=False, bins=bins)
               frame_histo = pd.DataFrame({'val': histo,'left': edges[:-1],'right': edges[1:],'middle_bin':np.floor(edges[:-1]+(edges[1:]-edges[:-1])/2)})

        hover_tool = HoverTool(tooltips=tooltips)
        panels = []
        bottom=0
        for axis_type in ["linear", "log"]:
            if width_height:
                plot_width  = width_height[0]
                plot_height = width_height[1]
            else :
                plot_width  = 400
                plot_height = 300
            standardfig = figure(plot_width=plot_width, plot_height=plot_height,y_axis_type=axis_type,
            tools=['save','box_zoom,box_select,crosshair,reset'],toolbar_location="below")
            if title:
                standardfig.title.text = title
            standardfig.add_tools(hover_tool)
            colors = itertools.cycle(Paired12)

            if axis_type=="log":
                bottom=1

            if date == 'all' :
                [standardfig.quad(source=ColumnDataSource(value),top='val', bottom=bottom, left='left', right='right',name=key,
                    fill_color=next(colors),legend_label=key) for key,value in dict_histo.items()]
            else:
                standardfig.quad(source=ColumnDataSource(frame_histo),top='val', bottom=bottom, left='left', right='right',
                fill_color=next(colors),legend_label=input_names_data + ' @ ' +when)
            standardfig.legend.label_text_font_size = "12px"

            panel = Panel(child=standardfig , title=axis_type)
            panels.append(panel)
        tabs = Tabs(tabs=panels)
        return tabs


    def DefFigInteractive(self, **kwargs):
        ''' Define interactive bokeh figure i.e with a window location selection'''
        if not isinstance(kwargs['location'], list):
            clist = [kwargs['location']]
        else:
            clist = kwargs['location']

        if self.database != 'spf':
            clist=self.geo.to_standard(clist,output='list',interpret_region=True)
        clist_cp = clist.copy()

        panels = []
        option = kwargs.get('option', None)
        if option == 'nonneg':
            babypandas = self.database.get_stats( which=kwargs['which'], type=kwargs['type'], location=clist_cp,
                                             output='pandas', option='nonneg')
        else:
            babypandas = self.database.get_stats( which=kwargs['which'], type=kwargs['type'], location=clist_cp,
                                         output='pandas')

        self.cocoa_pandas = babypandas

        data = pd.pivot_table(babypandas, index='date',columns='location', values=kwargs['which']).reset_index()
        filter_data1 = data[['date', clist[0]]].rename(
            columns={clist[0]: kwargs['which']})
        name1=clist[0]
        filter_data1['location']=[name1]*len(data[['date',clist[0]]])
        src1 = ColumnDataSource(filter_data1)

        filter_data2 = data[['date', clist[1]]].rename(
            columns={clist[1]: kwargs['which']})
        name2=clist[1]
        filter_data2['location']=[name2]*len(data[['date',clist[1]]])
        src2 = ColumnDataSource(filter_data2)

        self.hover_tool = HoverTool(tooltips=[
                        ('location',"@location"),
                        (kwargs['which'], '@'+kwargs['which']),
                        ('date', '@date{%F}')],
                        formatters={'@date': 'datetime'}
            )
        for axis_type in ["linear", "log"]:
            fig = figure(plot_width=600, plot_height=400, y_axis_type=axis_type, x_axis_type="datetime",
                         tools=[self.hover_tool, 'box_zoom,box_select,crosshair,reset'])

            fig.xaxis.formatter = DatetimeTickFormatter(
                days=["%d %B %Y"], months=["%d %B %Y"], years=["%d %B %Y"])

            fig.circle('date',kwargs['which'], size=3, color='red', source=src1,name=name1)
            fig.line(x='date', y=kwargs['which'], source=src1,
                     line_color='red', line_width=4, line_alpha=.2)

            fig.circle('date',kwargs['which'], size=3, color='blue', source=src2,name=name2)
            fig.line(x='date', y=kwargs['which'], source=src2,
                     line_color='blue', line_width=4, line_alpha=.2)

            if kwargs['which'] == 'confirmed' and self.database == 'spf':
                kwargs['which'] = 'Rea.'
            label = Label(x=70, y=350, x_units='screen', y_units='screen',
                          text=kwargs['which'], render_mode='css',
                          border_line_color='black', border_line_alpha=1.0,
                          background_fill_color='white', background_fill_alpha=1.0)

            fig.add_layout(label)

            panel = Panel(child=fig, title=axis_type)
            panels.append(panel)

        code="""
      var c = cb_obj.value;
      var y = s0.data[c];
      for (var i = 0; i < y.length; i++) {
        s1.data['location'][i]=c
        }
      s1.data[val] = y;
      s1.change.emit();
      ax=p1.yaxis[0]
      """

        source = ColumnDataSource(data)
        callback1 = CustomJS(args=dict(s0=source, s1=src1,val=kwargs['which']), code=code)
        callback2 = CustomJS(args=dict(s0=source, s1=src2,val=kwargs['which']), code=code)

        select_countries1 = Select(title="RED CURVE:", value=clist[0], options=clist)
        select_countries1.js_on_change('value', callback1)

        select_countries2 = Select(title="BLUE CURVE", value=clist[1], options=clist)
        select_countries2.js_on_change('value', callback2)
        tabs = Tabs(tabs=panels)
        layout = row(column(row(select_countries1, select_countries2), row(tabs)))
        return layout

    def CrystalFig(self, crys, err_y):
        sline = []
        scolumn = []
        i = 1
        list_fits_fig = crys.GetListFits()
        for dct in list_fits_fig:
            for key, value in dct.items():
                location = key
                if math.nan not in value[0] and math.nan not in value[1]:
                    maxy = crys.GetFitsParameters()[location][1]
                    if math.isnan(maxy) == False:
                        maxy = int(maxy)
                    leg = 'From fit : tmax:' + \
                        str(crys.GetFitsParameters()[location][0])
                    leg += '   Tot deaths:' + str(maxy)
                    fig = figure(plot_width=300, plot_height=200,
                                 tools=['box_zoom,box_select,crosshair,reset'], title=leg, x_axis_type="datetime")

                    date = [datetime.strptime(i, '%m/%d/%y')
                            for i in self.p.getDates()]
                    if err_y:
                        fig.circle(
                            date, value[0], color=self.colors[i % 10], legend_label=location)
                        y_err_x = []
                        y_err_y = []
                        for px, py in zip(date, value[0]):
                            err = np.sqrt(np.abs(py))
                            y_err_x.append((px, px))
                            y_err_y.append((py - err, py + err))
                        fig.multi_line(y_err_x, y_err_y,
                                       color=self.colors[i % 10])
                    else:
                        fig.line(
                            date, value[0], line_color=self.colors[i % 10], legend_label=location)

                    fig.line(date[:crys.GetTotalDaysConsidered(
                    )], value[1][:crys.GetTotalDaysConsidered()], line_color='red', line_width=4)

                    fig.xaxis.formatter = DatetimeTickFormatter(
                        days=["%d %b %y"], months=["%d %b %y"], years=["%d %b %y"])
                    fig.xaxis.major_label_orientation = math.pi/4
                    fig.xaxis.ticker.desired_num_ticks = 10

                    # tot_type_country=self.p.get_stats(country=country,type='Cumul',which='deaths')[-1]

                    fig.legend.location = "bottom_left"
                    fig.legend.title_text_font_style = "bold"
                    fig.legend.title_text_font_size = "5px"

                    scolumn.append(fig)
                    if i % 2 == 0:
                        sline.append(scolumn)
                        scolumn = []
                    i += 1
        fig = gridplot(sline)
        return fig

    def get_pandas(self):
        ''' Retrieve the pandas when CoCoDisplay is called '''
        return self.cocoa_pandas

    def __delete__(self, instance):
        print("deleted in descriptor object")
        del self.value

    #@staticmethod
    def return_map(self,mypandas):
        which_data = mypandas.columns[2]
        jhu_stuff = mypandas.loc[(mypandas.date == mypandas.date.max())]

        pandas_data = pd.DataFrame({
            'location': jhu_stuff.location,
            'totcases': jhu_stuff.iloc[:, 2]
        })
        #geo = coge.GeoManager('name')
        #info = coge.GeoInfo()

        a = self.info.add_field(field=['geometry'],input=jhu_stuff ,geofield='location')


        data=gpd.GeoDataFrame(self.info.add_field(input=a,geofield='location',\
                                  field=['country_name']),crs="EPSG:4326")
        data = data.loc[data.geometry != None]
        data['geoid'] = data.index.astype(str)
        data=data[['geoid','location','deaths','geometry']]
        #centroid=data.geometry.centroid
        centroid=unary_union(data.geometry).centroid
        mapa = folium.Map(width=600, height=400, location=[centroid.y, centroid.x], zoom_start=2)
        folium.Choropleth(
        geo_data=data,
        name='Covid19cases',
        data=data,
        columns=['geoid', 'deaths'],
        key_on='feature.id',
        fill_color='YlOrRd',
        fill_opacity=0.7,
        line_opacity=0.2,
        line_color='white',
        line_weight=0,
        highlight=False,
        smooth_factor=1.0,
        legend_name= 'Covid19 cases').add_to(mapa)

        folium.GeoJson(data,
               name="Cases",
               style_function=lambda x: {'color':'transparent','fillColor':'transparent','weight':0},
               highlight_function=lambda x: {'weight':3, 'color':'blue'},
               tooltip=folium.GeoJsonTooltip(fields=['location','deaths'],
                                             aliases = ['country','totcases'],
                                             labels=False)
                      ).add_to(mapa)
        folium.LayerControl(autoZIndex=False, collapsed=False).add_to(mapa)

        return mapa


def resume_pandas(self,pd):
    pd['New cases (last 30 days)'] = pd['deaths'].apply(self.sparkline)

'''
    babypandas_diff=self.p.getStats(country=self.countries,type='Diff',which='deaths',output='pandas')
    babypandas_diff=babypandas_diff.set_index('date')
    babypandas_cumul=self.p.getStats(country=self.countries,type='Cumul',which='deaths',output='pandas')
    babypandas_cumul=babypandas_cumul.set_index('date')

    n=self.SetTotalDaysConsidered(self.p.getDates()[0],self.stop_date_fit)
    [self.returnFits(i) for i in self.countries]

    pop_pd=w.getData()[w.getData()['Country'].isin(self.countries)]
        pop=pop_pd.sort_values(by=['Country'])['Population']

    Pourcentage=[[100*(self.GetTodayProjNdeaths()[i]-\
                      (babypandas_cumul.loc[babypandas_cumul['country']==i]).loc[self.stop_date_fit]['cases'])\
                  /(babypandas_cumul.loc[babypandas_cumul['country']==i]).loc[self.stop_date_fit]['cases'],0]\
                 [self.GetTodayProjNdeaths()[i] == -1]\
                 for i in self.countries]

    print(Pourcentage)

    resume =  pd.DataFrame({
                  'Country':self.countries,'Population':pop,
                  'Totaldeaths':babypandas_cumul.loc[self.stop_date_fit]['cases'].to_list(),
                  'TotaldeathsProj':[self.GetTodayProjNdeaths()[i] for i in self.countries],
                  'Diff%': Pourcentage,
                  'Total Forecast': [crys.GetFitsParameters()[i][1] for i in self.countries],
                  'Estimated pick': [crys.GetFitsParameters()[i][0] for i in self.countries],
                  'Last deaths': babypandas_diff.loc[self.stop_date_fit]['cases'].to_list(),
                  'Caseslist':(babypandas_diff.sort_values('date').groupby('country').apply(lambda x: x['cases'].tail(30)).values[:]).tolist()
    })
    resume['New cases (last 30 days)'] = resume['Caseslist'].apply(self.sparkline)
    last_date=self.stop_date_fit
    title='Resume and forcast for COVID-19 pandemy @ ' + str(last_date)
    resume=resume.loc[:, resume.columns != 'Caseslist']
    resume=resume.set_index('Country')
    resume=resume.sort_values(by=['Country'])
'''
