#!/usr/bin/env python3
"""
Script for loading the CSVs into Postgre
"""
import pandas as pd
from pandas.errors import ParserError
from sqlalchemy import create_engine, Table, MetaData

import inquirer
import os
import glob
from dotenv import load_dotenv

load_dotenv('../.env_db')
PGUSER = os.getenv('POSTGRES_USER')
PGPASS = os.getenv('POSTGRES_PASSWORD')
PGHOST = 'localhost'
PGDB = os.getenv('POSTGRES_DB')

# Create connection
pg_con = create_engine(f"postgresql://{PGUSER}:{PGPASS}@{PGHOST}/{PGDB}")

questions = [
    inquirer.Path('data_dir',
                  message="Enter directory where the clean CSVs located(don't forget the trailing '/')",
                  path_type=inquirer.Path.DIRECTORY,
                  ),
    inquirer.Text('table_name',
                  message="Type the name of the table in which to insert the data",
                  default='line_list'
                  )
]


def get_table_info(table_name):
    """
    :return table information from database
    :param table_name:
    :return:
    """
    metadata = MetaData()
    table = Table(table_name, metadata, autoload=True, autoload_with=pg_con)
    return table


def load_csvs(pth):
    """
    Generator that loads CSV files with pandas reporting any parsing error
    :param pth: Path to directory containing the CSVs
    :return: DataFrame with the contents of the CSVs
    """
    csvs = glob.glob(os.path.join(pth, '*_clean.csv'))
    for csv in csvs:
        cname = os.path.split(csv)[-1]
        print(f'loading {cname}')
        try:
            df = pd.read_csv(csv, encoding='utf8')
            yield df
        except ParserError as e:
            print(f"Problem parsing {cname}")
            print(e)
            continue
        except UnicodeDecodeError as ue:
            print(f"Encoding of {cname} is not UTF-8")
            print(ue)
            continue
        except Exception as oe:
            print(f"Unclassified error when reading {cname}")
            print(oe)
            continue


def insert_into_db(csvg, table_name):
    '''
    Pulls dataframes from the load_csvs generator and attempts to insert
    it into the database
    :param csvg: Generator yieldind dataframes
    :return:
    '''
    table = get_table_info(table_name)
    for df in csvg:
        df.columns = [c.lower() for c in df.columns]  # make sure all column names are lowercase
        for c in df.columns:
            if c not in list(table.columns):
                print(f"Missing column: {c}")
        # df.to_sql('line_list', con=pg_con, if_exists='append', index=False, method=None)#'multi')


answers = inquirer.prompt(questions)
csvgen = load_csvs(answers['data_dir'])
insert_into_db(csvgen, answers['table_name'])
