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
from datetime import datetime as dt

from cocoa import covid19 as cc

import bokeh
from bokeh.io import show, output_notebook
from bokeh.models import ColumnDataSource, ColorBar, HoverTool, Legend
from bokeh.plotting import figure, output_file, show
from bokeh.palettes import brewer
from bokeh.layouts import row, column, gridplot
from bokeh.models import CustomJS, Slider, Select, Plot, \
    Button, LinearAxis, Range1d, DatetimeTickFormatter
from bokeh.models import CheckboxGroup, RadioGroup, Toggle, RadioGroup

from bokeh.models.widgets import Tabs, Panel
from bokeh.models import Label, LabelSet
from bokeh.models import ColumnDataSource, Grid, Line, LinearAxis, Plot
from bokeh.models import DataRange1d
import bokeh.palettes
import cocoa.geo as coge
#import plotly.express as px
#import plotly.graph_objects as go
#from branca.colormap import LinearColormap
import folium
import json
from geopy.geocoders import Nominatim
import altair as alt

class CocoDisplay():
    def __init__(self, database):
        self.colors =  bokeh.palettes.d3['Category20'][10]
        self.coco_circle = []
        self.coco_line = []
        self.database=database
        if self.database.get_db() != 'aphp':
            self.geo = coge.GeoManager('name')

    def DefFigStatic(self, **kwargs):
        if not isinstance(kwargs['location'], list):
            clist = [kwargs['location']]
        else:
            clist = kwargs['location']
        panels = []

        if self.database.get_db() != 'aphp':
            clist=self.geo.to_standard(clist,output='list',interpret_region=True)
        clist_cp = clist.copy()

        option = kwargs.get('option', None)

        if option == 'nonneg':
            babypandas = self.database.get_stats( which=kwargs['which'], type=kwargs['type'], location=clist_cp,
                                         output='pandas', option='nonneg')

        else:
            babypandas = self.database.get_stats( which=kwargs['which'], type=kwargs['type'], location=clist_cp,
                                         output='pandas')
        self.cocoa_pandas = babypandas

        for axis_type in ["linear", "log"]:
            self.hover_tool = HoverTool(tooltips=[
                        ('location',"@location"),
                        (kwargs['which'], '@'+kwargs['which']),
                        ('date', '@date{%F}')],
                        formatters={'@date': 'datetime'}
            )
            fig = figure(plot_width=600, plot_height=400, y_axis_type=axis_type, x_axis_type="datetime",
                         tools=[self.hover_tool, 'box_zoom,box_select,crosshair,reset'])
            fig.xaxis.formatter = DatetimeTickFormatter(
                days=["%d %B %Y"], months=["%d %B %Y"], years=["%d %B %Y"])

            i = 0
            for coun in sorted(clist):
                name=coun
                filter_data = babypandas.loc[babypandas['location']==coun]
                src=ColumnDataSource(filter_data)
                fig.line(x='date', y=kwargs['which'], source=src,line_color=self.colors[i%10], legend_label=coun, line_width=2,name=coun)
                i += 1
            fig.legend.location = "bottom_left"
            if kwargs['which'] == 'confirmed' and self.database == 'aphp':
                kwargs['which'] = 'Rea.'
            fig.legend.title = kwargs['which'].upper()
            fig.legend.title_text_font_style = "bold"
            fig.legend.title_text_font_size = "15px"
            panel = Panel(child=fig, title=axis_type)
            panels.append(panel)
        tabs = Tabs(tabs=panels)
        return tabs

    def DefFigInteractive(self, **kwargs):
        ''' Define interactive bokeh figure i.e with a window location selection'''
        if not isinstance(kwargs['location'], list):
            clist = [kwargs['location']]
        else:
            clist = kwargs['location']

        if self.database != 'aphp':
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
                     line_color='red', line_width=2, line_alpha=.2)

            fig.circle('date',kwargs['which'], size=3, color='blue', source=src2,name=name2)
            fig.line(x='date', y=kwargs['which'], source=src2,
                     line_color='blue', line_width=2, line_alpha=.2)

            if kwargs['which'] == 'confirmed' and self.database == 'aphp':
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
                    )], value[1][:crys.GetTotalDaysConsidered()], line_color='red', line_width=2)

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



class WorldMapDisplay():
    def __init__(self, countries, cumul_or_diff, which_data):
        self.geolocator = Nominatim(
            user_agent="Worldmap for Covid-19 studing case")
        # ,tiles="cartodbpositron")#,"CartoDB dark_matter")
        self.world_map = folium.Map(width=600, height=400, location=[
                                    48.52, 2.19], zoom_start=3)
        self.countries = sorted(countries)
        self.which_data = which_data
        p = cc.Parser()
        babypandas = (p.get_stats(location=self.countries,type=cumul_or_diff,
                                 which=which_data, output='pandas'))
        babypandascumul = babypandas
        babypandascumul['cumul'] = babypandas.groupby(
            ['location'])['cases'].apply(lambda x: x.cumsum())

        mask_date_max = babypandas.groupby(['location'])['date'].max()
        babypandascumulmasked_date = babypandascumul['date'].isin(
            mask_date_max)
        self.data = pd.pivot_table(
            babypandas, index='date', columns='location', values='cases').reset_index()
        if cumul_or_diff == 'cumul':
            self.data = pd.pivot_table(
                babypandascumul, index='date', columns='location', values='cumul').reset_index()

        map_data = pd.DataFrame({
            'location': self.countries,
            'totcases': babypandascumul[babypandascumulmasked_date]['cumul'].to_list()
        })
        self.totalsallcountries = sum(
            babypandascumul[babypandascumulmasked_date]['cumul'])
        self.maxdeaths = max(
            babypandascumul[babypandascumulmasked_date]['cumul'])
        self.map_dict = map_data.set_index('location')['totcases'].to_dict()

    def LatLong(self, location):
        if location != None:
            location = self.geolocator.geocode(location)
            if location != None:
                Lat = location.latitude  # , location.longitude)
                Long = location.longitude
            else:
                Lat = float("Nan")  # , location.longitude)
                Long = float("Nan")
        return (Lat, Long)

    def DrawPopUpCircle(self):
        for coun in self.countries:
            filter_data = self.data[['date', coun]].rename(
                columns={coun: 'cases'})
            tot = self.map_dict[coun]
            latlong = self.LatLong(coun)
            start_coords = [latlong[0], latlong[1]]
            source = pd.DataFrame(
                {
                    'date':  filter_data['date'],
                    'cases':  filter_data['cases'],
                })
            if sum(filter_data['cases']) != 0:
                chart = alt.Chart(source).mark_line().encode(
                    alt.X('date', axis=alt.Axis(title='Date')),
                    alt.Y('cases', axis=alt.Axis(title='Cases'))).properties(title=coun.upper())
                vis1 = chart.to_json()
                vega = folium.features.VegaLite(
                    vis1, width='100%', height='100%')

                #
                maxrad = 50
                circ_mkr = folium.CircleMarker(
                    location=start_coords,
                    radius=maxrad*tot/self.totalsallcountries,
                    color='blue',
                    fill=True,
                    fill_color='red',
                    fillOpacity=1.0,
                    opacity=1.0,
                    tooltip=coun,
                    popup=folium.Popup(max_width=300).add_child(vega))
                circ_mkr.add_to(self.world_map)

    def drawLocation(self):
        folium.GeoJson(
            data='https://raw.githubusercontent.com/johan/world.geo.json/master/countries.geo.json',
            style_function=lambda feature: {
                'fillColor': self.getColor(feature),
                'caption': 'Total deaths',
                'fillOpacity': 0.5,
                'weight': 0.5
            }).add_to(self.world_map)

    def getColor(self, feature):
        value = self.map_dict.get(feature['properties']['name'])
        self.color_scale = LinearColormap(['yellow', 'red'],
                                          vmin=min(self.map_dict.values()), vmax=max(self.map_dict.values()))
        # vmin = 0, vmax = 150)

        if value is None:
            return '#8c8c8c'  # MISSING -> gray
        else:
            return self.color_scale(value)

    def returnMap(self):
        self.drawLocation()
        self.DrawPopUpCircle()
        colormap = self.color_scale.to_step(len(self.countries))
        colormap.caption = self.which_data.upper()
        self.world_map.add_child(colormap)
        return self.world_map
