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


def cumul_plot(df):
    """FIXME! briefly describe function

    :param df:
    :returns:
    :rtype:

    """
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
                      title=dict(text='Évolution du Covid-19 en Guinée : données cumulées',
                                 x=0.5, y=0.94))
    fig.update_yaxes(automargin=True)

    return fig


def daily_plot(df):
    """FIXME! briefly describe function

    :param df:
    :returns:
    :rtype:

    """
    x = df['Date'].values

    fig = go.Figure(data=[
        go.Bar(
            name='Nouveaux décès',
            x=x,
            y=df['Nouveaux décès'].values,
            marker_color='red'),
        go.Bar(
            name='Nouveaux guéris',
            x=x,
            y=df['Nouveaux guéris'].values,
            marker_color='darkgreen'),
        go.Bar(
            name='Nouveaux cas',
            x=x,
            y=df['Nouveaux cas'],
            marker_color='gold')
    ])

    # Change the bar mode
    fig.update_layout(template='plotly_dark',
                      barmode='stack', hovermode='x',
                      xaxis_tickangle=-60,
                      legend_orientation="h",
                      legend=dict(x=0, y=-0.3),
                      margin=dict(t=40, b=0, l=25, r=3),
                      title=dict(text='Suivi journalier du Covid-19 en Guinée',
                                 x=0.5, y=0.94))
    fig.update_yaxes(automargin=True)

    return fig


def evolution_bars_plot(df):
    """FIXME! briefly describe function

    :param df:
    :returns:
    :rtype:

    """
    x = df['Date'].values

    fig = go.Figure()

    config = {'displayModeBar': True}

    fig.add_traces(data=[
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

    fig.add_traces(data=[
        go.Bar(name='Nouveaux décès', x=x, y=df['Nouveaux décès'].values, marker_color='red',
               visible=False),
        go.Bar(name='Nouveaux guéris', x=x, y=df['Nouveaux guéris'].values, marker_color='darkgreen',
               visible=False),
        go.Bar(name='Nouveaux cas', x=x, y=df['Nouveaux cas'], marker_color='gold',
               visible=False)
    ])

    fig.update_yaxes(automargin=True)

    # Add dropdown
    fig.update_layout(
        updatemenus=[
            dict(
                type='dropdown',
                active=0,
                buttons=list([
                    dict(
                        label="Cumul",
                        method="update",
                        args=[
                            {"visible": [True, True, True, True, False, False, False]}],
                    ),
                    dict(
                        label="Par jour",
                        method="update",
                        args=[{"visible": [False, False, False, False, True, True, True]},
                              {"title": 'Suivi journalier du Covid-19 en Guinée',
                               }],
                    )
                ]),
                direction="down",
                showactive=True,
                x=0.01,
                xanchor="center",
                y=1.02,
                yanchor='middle',
                bgcolor='darkred',
                font=dict(color='gray', size=14)
            ),
        ],
        template='plotly_dark',
        barmode='stack', hovermode='x',
        xaxis_tickangle=-60,
        legend_orientation="h",
        legend=dict(x=0, y=-0.3),
        margin=dict(t=40, b=0, l=25, r=3),
        title=dict(
            text='Évolution du Covid-19 en Guinée : données cumulées', x=0.5, y=0.1,
            font=dict(size=12.5)),
    )

    return fig
