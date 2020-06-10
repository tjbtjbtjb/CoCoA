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

# output_notebook(hide_banner=True)

class CocoDisplay():
    def __init__(self, d=0):
        self.colors = bokeh.palettes.d3['Category10'][10]
        self.hover_tool = HoverTool(tooltips=[
            ('cases', '@cases'),
            ('date', '@date{%F}')],
            formatters={'date': 'datetime'}
        )
        self.coco_circle = []
        self.coco_line = []
        self.database = ''
        self.p = cc.Parser()

    def DefFigStatic(self, **kwargs):
        if not isinstance(kwargs['country'], list):
            clist = [kwargs['country']]
        else:
            clist = kwargs['country']
        panels = []
        option = kwargs.get('option', None)
        if option == 'nonneg':
            babypandas = self.p.getStats(country=clist, type=kwargs['type'], which=kwargs['which'],
                                         output='pandas', option='nonneg')
        else:
            babypandas = self.p.getStats(
                country=clist, type=kwargs['type'], which=kwargs['which'], output='pandas')

        data = pd.pivot_table(babypandas, index='date',
                              columns='country', values='cases').reset_index()
        for axis_type in ["linear", "log"]:
            fig = figure(plot_width=600, plot_height=400, y_axis_type=axis_type,
                         tools=[self.hover_tool, 'box_zoom,box_select,crosshair,reset'])
            fig.xaxis.formatter = DatetimeTickFormatter(
                days=["%d %B %Y"], months=["%d %B %Y"], years=["%d %B %Y"])

            i = 0
            for coun in sorted(clist):
                filter_data = data[['date', coun]].rename(
                    columns={coun: 'cases'})
                src = ColumnDataSource(filter_data)
                fig.line(x='date', y='cases', source=src,
                         line_color=self.colors[i], legend_label=coun, line_width=2)
                i += 1
            fig.legend.location = "top_left"
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
        if not isinstance(kwargs['country'], list):
            clist = [kwargs['country']]
        else:
            clist = kwargs['country']

        panels = []
        curvos = []
        option = kwargs.get('option', None)
        if option == 'nonneg':
            babypandas = self.p.getStats(country=clist, type=kwargs['type'], which=kwargs['which'],
                                         output='pandas', option='nonneg')
        else:
            babypandas = self.p.getStats(
                country=clist, type=kwargs['type'], which=kwargs['which'], output='pandas')

        data = pd.pivot_table(babypandas, index='date',
                              columns='country', values='cases').reset_index()
        filter_data1 = data[['date', clist[0]]].rename(
            columns={clist[0]: 'cases'})
        src1 = ColumnDataSource(filter_data1)

        filter_data2 = data[['date', clist[1]]].rename(
            columns={clist[1]: 'cases'})
        src2 = ColumnDataSource(filter_data2)

        for axis_type in ["linear", "log"]:
            fig = figure(plot_width=600, plot_height=400, y_axis_type=axis_type,
                         tools=[self.hover_tool, 'box_zoom,box_select,crosshair,reset'])

            fig.xaxis.formatter = DatetimeTickFormatter(
                days=["%d %B %Y"], months=["%d %B %Y"], years=["%d %B %Y"])

            fig.circle('date', 'cases', size=7, color='red', source=src1)
            fig.line(x='date', y='cases', source=src1,
                     line_color='red', line_width=3, line_alpha=.8)

            fig.circle('date', 'cases', size=7, color='blue', source=src2)
            fig.line(x='date', y='cases', source=src2,
                     line_color='blue', line_width=3, line_alpha=.8)

            if kwargs['which'] == 'confirmed' and self.database == 'aphp':
                kwargs['which'] = 'Rea.'
            label = Label(x=70, y=350, x_units='screen', y_units='screen',
                          text=kwargs['which'], render_mode='css',
                          border_line_color='black', border_line_alpha=1.0,
                          background_fill_color='white', background_fill_alpha=1.0)

            fig.add_layout(label)

            panel = Panel(child=fig, title=axis_type)
            panels.append(panel)

        code = """
      var c = cb_obj.value;
      var y = s0.data[c];
      s1.data['cases'] = y;
      s1.change.emit();
      ax=p1.yaxis[0]
      """
        source = ColumnDataSource(data)
        callback1 = CustomJS(args=dict(s0=source, s1=src1), code=code)
        callback2 = CustomJS(args=dict(s0=source, s1=src2), code=code)

        select_countries1 = Select(
            title="RED CURVE:", value=clist[0], options=clist)

        select_countries1.js_on_change('value', callback1)

        select_countries2 = Select(
            title="BLUE CURVE", value=clist[1], options=clist)
        select_countries2.js_on_change('value', callback2)

        tabs = Tabs(tabs=panels)

        layout = row(
            column(row(select_countries1, select_countries2), row(tabs)))
        return layout

    def CrystalFig(self, crys, err_y):
        sline = []
        scolumn = []
        i = 1
        list_fits_fig = crys.GetListFits()
        for dct in list_fits_fig:
            for key, value in dct.items():
                country = key
                if math.nan not in value[0] and math.nan not in value[1]:
                    maxy = crys.GetFitsParameters()[country][1]
                    if math.isnan(maxy) == False:
                        maxy = int(maxy)
                    leg = 'From fit : tmax:' + \
                        str(crys.GetFitsParameters()[country][0])
                    leg += '   Tot deaths:' + str(maxy)
                    fig = figure(plot_width=300, plot_height=200,
                                 tools=['box_zoom,box_select,crosshair,reset'], title=leg, x_axis_type="datetime")

                    date = [datetime.strptime(i, '%m/%d/%y')
                            for i in self.p.getDates()]
                    if err_y:
                        fig.circle(
                            date, value[0], color=self.colors[i % 10], legend_label=country)
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
                            date, value[0], line_color=self.colors[i % 10], legend_label=country)

                    fig.line(date[:crys.GetTotalDaysConsidered(
                    )], value[1][:crys.GetTotalDaysConsidered()], line_color='red', line_width=2)

                    fig.xaxis.formatter = DatetimeTickFormatter(
                        days=["%d %b %y"], months=["%d %b %y"], years=["%d %b %y"])
                    fig.xaxis.major_label_orientation = math.pi/4
                    fig.xaxis.ticker.desired_num_ticks = 10

                    # tot_type_country=self.p.getStats(country=country,type='Cumul',which='deaths')[-1]

                    fig.legend.location = "top_left"
                    fig.legend.title_text_font_style = "bold"
                    fig.legend.title_text_font_size = "5px"

                    scolumn.append(fig)
                    if i % 2 == 0:
                        sline.append(scolumn)
                        scolumn = []
                    i += 1
        fig = gridplot(sline)
        return fig

    def __delete__(self, instance):
        print("deleted in descriptor object")
        del self.value
