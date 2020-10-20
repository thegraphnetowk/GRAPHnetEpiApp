#!/usr/bin/env python3
"""
Script for loading the CSVs into Postgre
"""
import pandas as pd
from pandas.errors import ParserError
from sqlalchemy import create_engine

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
]

def insert_into_db(pth):
    """
    Insert CSV files into database
    :param pth: Path to directory containing the CSVs
    :return:
    """
    csvs = glob.glob(os.path.join(pth,'*_clean.csv'))
    for csv in csvs:
        print (f'loading {os.path.split(csv)[-1]}')
        try:
            df = pd.read_csv(csv, encoding='utf8')
        except ParserError as e:
            print(f"Problem parsing {os.path.split(csv)[-1]}")
            print(e)
        except UnicodeDecodeError as ue:
            print(f"Encoding of {os.path.split(csv)[-1]} is not UTF-8")
            print(ue)





answers = inquirer.prompt(questions)

insert_into_db(answers['data_dir'])