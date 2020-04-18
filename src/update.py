#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse

import pandas as pd

from appendix_figures import evolution_bars_cumul_plot
from process_data import get_historic_data_from_CSSE_gh_repo, update_data
from utils import create_index_html, git_push, scraping_anss

DATA_CSV_PATH = '../data/guinea.csv'


def main(args):

    print("Updating data ...")
    if args.source == 'csse':
        print("    from csse github repo...")
        df = get_historic_data_from_CSSE_gh_repo()
        df.to_csv(DATA_CSV_PATH, index=False)

    elif args.source == 'anss':
        print("    from anss website")
        df = pd.read_csv(DATA_CSV_PATH)
        new_line_of_data = scraping_anss()
        df = update_data(df, new_line_of_data)
        df.to_csv(DATA_CSV_PATH, index=False)

    else:
        raise('This parameter can only take "anss", or "csse"')

    print("    file saved to ".format(DATA_CSV_PATH))

    print("Creating Cumulated evolution bars plot...")
    evol_bars_fig = evolution_bars_cumul_plot(df)

    figs = [evol_bars_fig]

    print("Creating index.html file... ")
    create_index_html(figs)

    print("Pushing updates to github...")
    git_push()

    print("Done.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', metavar='[A-Za-z]*', type=str, default='anss',
                        help='Either from "csse" or "anss"')
    args = parser.parse_args()
    main(args)
