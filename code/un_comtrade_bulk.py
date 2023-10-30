### ADAPTED FROM
# https://github.com/uncomtrade/comtradeapicall/blob/main/tests/example%20calling%20functions%20-%20notebook.ipynb

##### IMPORTS #####
import os
import sys
from dotenv import load_dotenv

import pandas as pd
import requests
import comtradeapicall

from datetime import date
from datetime import timedelta

# load environment vars, e.g. subscription key
load_dotenv()

# sub key should be stored properly in the .env file
print('make sure your subscription key is stored in the .env file AND that file is gitignored!')
subscription_key = os.getenv("comtrade_user_subscription_key")
# comtrade api subscription key (from comtradedeveloper.un.org)

data_directory = './data'  # output directory for downloaded files

# set some time-related variables, if needed
today = date.today()
yesterday = today - timedelta(days=1)
lastweek = today - timedelta(days=7)

# get cbam data
cbam_hs_df = pd.read_csv(f'{data_directory}/cbam_hs.csv')



### SET UP HS CODES
cbam_hs = ','.join(str(x) for x in cbam_hs_df['HS 6-digit (text)'])

cbam_hs_df.columns

cbam_sectors = cbam_hs_df['CBAM Sector'].unique()

cbam_sectors_hs = dict()

for s in cbam_sectors:
    cbam_sectors_hs[s] = ','.join(str(x) for x in cbam_hs_df['HS 6-digit (text)'][cbam_hs_df['CBAM Sector'] == s])


### SET UP TIMEFRAME

start_year = 2015
end_year = 2023

years_desired = ','.join("%d"%i for i in range(start_year, end_year+1))


### SET UP DESIRED JURS
un_country = pd.read_csv(f'{data_directory}/UNSD_Methodology.csv',sep=';')

un_country_m49_all = ','.join(str(x) for x in un_country['M49 Code'])

un_country_m49_chunks = dict()

chunk_size = 50

for chk in range(0, un_country.shape[0]+1, 50):

    chunk_upper_lim = chk+50

    if chunk_upper_lim>(un_country.shape[0]+1):
        chunk_upper_lim  = un_country.shape[0] + 1

    print(chk)

    un_country_m49_chunks[chk] = ','.join(str(x) for x in un_country['M49 Code'][chk:chunk_upper_lim])



request_params = {
    'subscription_key': subscription_key,
    'typeCode': 'C', # C commodities; S service
    'freqCode': 'A', # A annual; M monthly
    'clCode': 'HS', # HS; SITC; BEC; EBOPS
    'period': 2020, # year or month in form YYYY or YYYYMM respectively # will add that in loop later on
    'reporterCode': '36', # M49 code of countries, csv
    #'cmdCode': cbam_hs, #'91', #your HS codes
    'flowCode': 'M', # rest of the params aren't listed on the param explanation page, lol
    'partnerCode': None,
    'partner2Code': None,
    'customsCode': None, 
    'motCode': None, 
    'maxRecords': None,
    'format_output': 'JSON',
#    'aggregateBy': None,
#    'breakdownMode': 'classic',
    'countOnly': None, 
    'includeDesc': True
}

# basic example of api call
#cbam_df = comtradeapicall.previewFinalData(**request_params)

##### ITERATING OVER JURISDICTION CHUNKS #####


### ITERATING OVER COMMODITY GROUPS ####
cbam_data_by_commodity = dict()

cbam_data_all = pd.DataFrame()
failed_requests = dict()

for cmdty in cbam_sectors_hs.keys():

    cmdty = 'Iron and Steel' # DBG DBG DBG
    print(f'Starting request for {cmdty}')

    # have to do nested loop as the requests fail when they're too large
    # so need to break them up in this stupid way

    _request_params = request_params.copy() # keep original params constant

    #_request_params['reporterCode'] = un_country_m49_all
    _request_params['period'] = years_desired

    _request_params['cmdCode'] = cbam_sectors_hs[cmdty]
    #_request_params['cmdCode'] = '760110'
    cbam_data_m49_chunks = dict()
#    for chk in un_country_m49_chunks.keys():

        chk = 100 # DBG DBG DBG

        print(f'Starting request for {chk}')

        _request_params['reporterCode'] = un_country_m49_chunks[chk]

        ##### EXECUTE API CALL #####
        try:
            request_df = comtradeapicall.getTarifflineData(**_request_params)
        except Exception as e:
            print('Request failed successfully! (ie it didn\'t work)')
            print(e)
            request_df = pd.DataFrame()
            failed_requests[cmdty] = chk

        cbam_data_m49_chunks[chk] = request_df

        cbam_data_all = pd.concat([cbam_data_all, request_df])
        cbam_data_all.to_csv(f'{data_directory}/cbam_data_all.csv')

    cbam_data_by_commodity[cmdty] = cbam_data_m49_chunks

    # cbam_data_by_commodity[cmdty] = comtradeapicall.getTarifflineData(**_request_params)

    # attempt to cheat the rate limiter


#
# # example loop for years
# cbam_data_years = dict()
#
# for year in range(start_year, end_year+1):
#     print(f'Starting request for year {year}')
#
#     request_params_y = request_params.copy() # keep original params constant
#
#     request_params_y['period'] = str(year)
#
#     cbam_data_years[year] = comtradeapicall.previewFinalData(**request_params_y)
#
#     sys.sleep(5)







