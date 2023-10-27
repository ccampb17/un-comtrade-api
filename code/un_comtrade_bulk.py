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

# set some variables

today = date.today()
yesterday = today - timedelta(days=1)
lastweek = today - timedelta(days=7)

# get cbam data
cbam_hs_df = pd.read_csv(f'{data_directory}/cbam_hs.csv')

# get hs codes
cbam_hs = ','.join(str(x) for x in cbam_hs_df['HS 6-digit (text)'])

# TODO work out why it doesn't work when putting cbam_hs in the cmdCode param

request_params = {
    'typeCode': 'C', # C commodities; S service
    'freqCode': 'M', # A annual; M monthly
    'clCode': 'HS', # HS; SITC; BEC; EBOPS
    'period': 2020, # year or month in form YYYY or YYYYMM respectively # will add that in loop later on
    'reporterCode': '36', # M49 code of countries, csv
    'cmdCode': cbam_hs, #'91', #your HS codes
    'flowCode': 'M', # rest of the params aren't listed on the param explanation page, lol
    'partnerCode': None,
    'partner2Code': None,
    'customsCode': None, 
    'motCode': None, 
    'maxRecords': None,
    'format_output': 'JSON',
    'aggregateBy': None, 
    'breakdownMode': 'classic', 
    'countOnly': None, 
    'includeDesc': True
}

start_year = 2018
end_year = 2023

cbam_data_years = dict()

for year in range(start_year, end_year+1):
    print(f'Starting request for year {year}')

    request_params_y = request_params.copy() # keep original params constant

    request_params_y['period'] = str(year)

    cbam_data_years[year] = comtradeapicall.previewFinalData(**request_params_y)

    sys.sleep(5)


#cbam_df = comtradeapicall.previewFinalData(**request_params)


##### EXAMPLES #####
# Call preview final data API to a data frame, max to 500 records, no subscription key required
# This example: Australia imports of commodity code 91 in classic mode in May 2022
mydf = comtradeapicall.previewFinalData(typeCode='C', 
                                        freqCode='M', 
                                        clCode='HS', 
                                        period='202205',
                                        reporterCode='36', 
                                        cmdCode='760110,760120,760120,760310,760320,760410,760410,760421,760429,760429,760511,760519,760521,760529',#cbam_hs,#'91,86',
                                        flowCode='M', 
                                        partnerCode=None,
                                        partner2Code=None,
                                        customsCode=None, 
                                        motCode=None, 
                                        maxRecords=500, 
                                        format_output='JSON',
                                        aggregateBy=None, 
                                        breakdownMode='classic', 
                                        countOnly=None, 
                                        includeDesc=True)
mydf.head(5)



# Call preview tariffline data API to a data frame, max to 500 records, no subscription key required
# This example: Australia imports of commodity code started with 90 and 91 from Indonesia in May 2022
mydf = comtradeapicall.previewTarifflineData(typeCode='C', freqCode='M', clCode='HS', period='202205',
                                             reporterCode='36', cmdCode='91,90', flowCode='M', partnerCode=36,
                                             partner2Code=None,
                                             customsCode=None, motCode=None, maxRecords=500, format_output='JSON',
                                             countOnly=None, includeDesc=True)
mydf.head(5)



# Call get final data API to a data frame, max to 250K records, subscription key required
# This example: Australia imports of commodity codes 90 and 91 from all partners in classic mode in May 2022
mydf = comtradeapicall.getFinalData(subscription_key, typeCode='C', freqCode='M', clCode='HS', period='202205',
                                    reporterCode='36', cmdCode='91,90', flowCode='M', partnerCode=None,
                                    partner2Code=None,
                                    customsCode=None, motCode=None, maxRecords=2500, format_output='JSON',
                                    aggregateBy=None, breakdownMode='classic', countOnly=None, includeDesc=True)
mydf.head(5)



# Call get tariffline data API to a data frame, max to 250K records, subscription key required
# This example: Australia imports of commodity code started with 90 and 91 from Indonesia in May 2022
mydf = comtradeapicall.getTarifflineData(subscription_key, typeCode='C', freqCode='M', clCode='HS', period='202205',
                                         reporterCode='36', cmdCode='91,90', flowCode='M', partnerCode=36,
                                         partner2Code=None,
                                         customsCode=None, motCode=None, maxRecords=2500, format_output='JSON',
                                         countOnly=None, includeDesc=True)
mydf.head(5)



# Call bulk download final file(s) API to output dir, (premium) subscription key required
# This example: Download monthly France final data of Jan-2000
comtradeapicall.bulkDownloadFinalFile(subscription_key, directory, typeCode='C', freqCode='M', clCode='HS',
                                      period='200001', reporterCode=251, decompress=True)



# Call bulk download tariff data file(s) to output dir, (premium) subscription key required
# This example: Download monthly France tariffline data of Jan-2000
comtradeapicall.bulkDownloadTarifflineFile(subscription_key, directory, typeCode='C', freqCode='M', clCode='HS',
                                           period='200001,200002,200003', reporterCode=504, decompress=True)



# Call bulk download tariff data file(s) to output dir, (premium) subscription key required
# This example: Download annual Morocco  data of 2010
comtradeapicall.bulkDownloadTarifflineFile(subscription_key, directory, typeCode='C', freqCode='A', clCode='HS',
                                           period='2010', reporterCode=504, decompress=True)



# Call data availability for annual HS in 2021
mydf = comtradeapicall.getFinalDataAvailability(subscription_key, typeCode='C', freqCode='A', clCode='HS',
                                                period='2021', reporterCode=None)
mydf.head(5)




# Call tariffline data availability for monthly HS in Jun-2022
mydf = comtradeapicall.getTarifflineDataAvailability(subscription_key, typeCode='C', freqCode='M', clCode='HS',
                                                     period='202206', reporterCode=None)
mydf.head(5)



