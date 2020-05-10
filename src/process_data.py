#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import datetime
import glob
import os

import numpy as np
import pandas as pd

COVID_19_DATA_PATH = '../../COVID-19/'
DAILY_REPORTS_PATH = COVID_19_DATA_PATH + \
    'csse_covid_19_data/csse_covid_19_daily_reports/'
GUINEA_COVID_19_START_DATE = '03-13-2020'

"""
Author: Ahmed Tidiane BALDE
"""


def update_data(df, new_line):
    """FIXME! briefly describe function

    :param df:
    :param new_line:
    :returns:
    :rtype:

    """
    ch = new_line[0] - new_line[1] - new_line[2]
    nc = new_line[0] - df.iloc[-1, 1]
    nd = new_line[1] - df.iloc[-1, 2]
    ng = new_line[2] - df.iloc[-1, 3]
    new_line.extend([ch, nc, nd, ng])
    new_line.insert(0, datetime.datetime.today().strftime('%d-%m-%Y'))

    # Inserting the new preprocessed data to the dataframe we have
    df = df.append(pd.DataFrame(new_line, index=df.columns).T)

    # Dropping duplicates lines
    df.iloc[-2:, :] = df.iloc[-2:,
                              :].drop_duplicates(subset=['Cas confirmés', 'Décès', 'Guéris'])

    df = df.dropna(how='all')
    df[list(df.columns)[1:]] = df.iloc[:, 1:].applymap(int)

    return df


def get_historic_data_from_CSSE_gh_repo():
    """FIXME! briefly describe function

    :returns:
    :rtype:

    """

    repo = git.Repo(COVID_19_DATA_PATH)
    repo.remotes.origin.pull()

    files = glob.glob(DAILY_REPORTS_PATH + '*.csv')
    files.sort(key=os.path.getmtime)
    index_start = files.index(
        DAILY_REPORTS_PATH +
        GUINEA_COVID_19_START_DATE +
        '.csv')

    files = files[index_start:]
    columns = ['Date', 'Cas confirmés', 'Décès', 'Guéris']
    df = pd.DataFrame(columns=columns)

    for f in files:
        df_file = pd.read_csv(f)
        date = f.split('/')[-1].split('.')[0]
        date = datetime.datetime.strptime(
            date, '%m-%d-%Y').strftime("%d-%m-%Y")
        try:
            cases = df_file[df_file['Country_Region']
                            == 'Guinea'].values[0][7:10]
        except BaseException:
            cases = df_file[df_file['Country/Region']
                            == 'Guinea'].values[0][3:6]

        line = list(cases)
        line.insert(0, date)
        df = df.append(pd.DataFrame(line, index=columns).T)

    df.index = range(len(df))

    df['Cas hospitalisés'] = df['Cas confirmés'] - df['Décès'] - df['Guéris']
    df['Nouveaux cas'] = 0
    df['Nouveaux décès'] = 0
    df['Nouveaux guéris'] = 0
    df.iloc[:, 1:] = df.iloc[:, 1:].apply(pd.to_numeric)
    df.iloc[0, 5] = df.iloc[0, 1]
    df.iloc[1:, 5] = df.iloc[1:, 1] - df.iloc[0:-1, 1].values
    df.iloc[1:, 6] = df.iloc[1:, 2] - df.iloc[0:-1, 2].values
    df.iloc[1:, 7] = df.iloc[1:, 3] - df.iloc[0:-1, 3].values

    return df
