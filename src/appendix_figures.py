#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly as py
import plotly.express as px
import plotly.graph_objs as go
import plotly.io as pio
import plotly.tools as tls
import seaborn as sns
from plotly.graph_objs import graph_objs
from plotly.offline import init_notebook_mode, iplot

import cufflinks as cf

"""
Author: Ahmed Tidiane BALDE
"""

sns.set()

COVID_19_DATA_PATH = '../../COVID-19/'
DAILY_REPORTS_PATH = COVID_19_DATA_PATH + \
    'csse_covid_19_data/csse_covid_19_daily_reports/'
GUINEA_COVID_19_START_DATE = '03-13-2020'


def evolution_bars_cumul_plot(df):
    x = df['Date'].values

    fig = go.Figure(data=[
        go.Bar(
            name='Décès',
            x=x,
            y=df['Décès'].values,
            marker_color='red'),
        go.Bar(
            name='Guéris',
            x=x,
            y=df['Guéris'].values,
            marker_color='darkgreen'),
        go.Bar(
            name='Cas hospitalisés',
            x=x,
            y=df['Cas hospitalisés'],
            marker_color='gold')
    ])
    fig.add_trace({'x': df['Date'],
                   'y': df['Cas confirmés'],
                   'name': 'Cas confirmés'})

    # Change the bar mode
    fig.update_layout(template='plotly_dark',
                      barmode='stack', hovermode='x',
                      xaxis_tickangle=-60,
                      legend_orientation="h",
                      legend=dict(x=0, y=-0.3),
                      margin=dict(t=40, b=0, l=25, r=3),
                      title='Évolution du Covid-19 en Guinée : données cumulées')
    fig.update_yaxes(automargin=True)

    return fig
