#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import datetime
import glob

import git
import numpy as np
import pandas as pd
import requests

from bs4 import BeautifulSoup

PATH_OF_GIT_REPO = '../.git'
COMMIT_MESSAGE = 'automatic update of data and graphs'
ANSS_URL = 'https://anss-guinee.org'
INDEX_HTML_PATH = '../index.html'
"""
Author: Ahmed Tidiane BALDE
"""


def scraping_anss():
    """FIXME! briefly describe function

    :returns:
    :rtype:

    """

    source_code = requests.get(ANSS_URL)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, 'html.parser')
    data = soup.findAll('span', attrs={'class': 'count-text'})
    confirmed = int(data[0].attrs['data-stop'])
    death = int(data[1].attrs['data-stop'])
    healed = int(data[2].attrs['data-stop'])
    new_line = [confirmed, death, healed]

    return new_line


def create_index_html(figs=[]):
    """FIXME! briefly describe function

    :param figs: List of figs
    :returns:
    :rtype:

    """

    with open(INDEX_HTML_PATH, 'w') as f:
        f.write(figs[0].to_html(full_html=False, include_plotlyjs='cdn'))

    if len(figs) > 1:
        with open(INDEX_HTML_PATH, 'a') as f:
            for fig in figs[1:]:
                f.write(fig.to_html(full_html=False, include_plotlyjs='cdn'))


def git_push():
    """Git push covid-19-guinea repo

    :returns: None
    :rtype: Void

    """
    try:
        repo = git.Repo(PATH_OF_GIT_REPO)
        repo.git.add(update=True)
        repo.index.commit(COMMIT_MESSAGE)
        origin = repo.remote(name='origin')
        origin.push()
    except BaseException:
        print('Pushing did not succeed')
