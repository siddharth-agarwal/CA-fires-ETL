"""CAL FIRE Data Ingest

This script retrieves data from the 'Incidents' page maintained by the California Dept of Forestry and Fire Protection (CAL FIRE) : fire.ca.gov/incidents/ 

Yearly data is available from 2013-onwards.

This file contains the following functions:
    * main - retrieves the webpage as raw html, peforms ETL on the raw html to create a DataFrame, then writes the output as a CSV
"""

import pandas as pd
import numpy as np

import os
import requests
import json
import re

# specify year to request data for
select_year = 2019

ca_fire_base_url = "https://fire.ca.gov/incidents/{:d}/"

# csv_out_path = "../data/{:d}_new.csv"

drop_colnames = [
  'CanonicalUrl',
  'ConditionStatement',
  'ControlStatement',
  'CountyIds',
  'Location',
  'SearchDescription',
  'SearchKeywords'
]

def main():
  ca_fire_url = ca_fire_base_url.format(select_year)
  data_raw = requests.get(ca_fire_url).text

  # regex to find/extract the JSON data we want
  pattern = re.compile('incidentListTableInitialData = (.+)')
  finder = re.findall(pattern, data_raw)

  json_list = []
  splitlist=finder[0].split("{")

  for i in range(1,len(splitlist)-1):
    tmp_json = json.loads("{"+splitlist[i][:-1])
    json_list.append(tmp_json)    
  df_transform = pd.DataFrame(json_list)

  df_transform['Started'] = pd.to_datetime(df_transform['Started'], infer_datetime_format=True)
  df_transform['Updated'] = pd.to_datetime(df_transform['Updated'], infer_datetime_format=True)
  df_transform['Extinguished'] = pd.to_datetime(df_transform['Extinguished'], infer_datetime_format=True)

  # drop unnecessary/verbose columns
  df_transform=df_transform.drop(columns=drop_colnames)

  # for the 'Counties' column, replace occurrences of '[]' with NaNs 
  df_transform['Counties']=df_transform.Counties.apply(lambda y: np.nan if len(y)==0 else y)

  # write out the result DataFrame to a CSV
  script_dir = os.path.abspath('.')
  csv_out_path = os.path.join(script_dir, 'fire-incidents/data/{:d}_new.csv'.format(select_year))
  df_transform.to_csv(path_or_buf=csv_out_path.format(select_year),index=False,date_format='%Y-%m-%d %H:%M:%S')

if __name__ == '__main__':
    main()