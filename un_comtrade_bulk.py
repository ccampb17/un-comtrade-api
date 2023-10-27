### ADAPTED FROM
# https://github.com/uncomtrade/comtradeapicall/blob/main/tests/example%20calling%20functions%20-%20notebook.ipynb

import os
from dotenv import dotenv




# Install a pip comtradeapicall package in the current Jupyter kernel
import sys
!{sys.executable} -m pip install --upgrade comtradeapicall

# Install a pip pandas package in the current Jupyter kernel
import sys
!{sys.executable} -m pip install pandas


import pandas
import requests
import comtradeapicall

# sub key should be stored properly in the .env file
print('make sure your subscription key is stored in the .env file AND that file is gitignored!')

subscription_key = f'{comtrade_user_subscription_key}' # comtrade api subscription key (from comtradedeveloper.un.org)
directory = './data'  # output directory for downloaded files
#set some variables
from datetime import date
from datetime import timedelta
today = date.today()
yesterday = today - timedelta(days=1)
lastweek = today - timedelta(days=7)
# Call preview final data API to a data frame, max to 500 records, no subscription key required
# This example: Australia imports of commodity code 91 in classic mode in May 2022
mydf = comtradeapicall.previewFinalData(typeCode='C', freqCode='M', clCode='HS', period='202205',
                                        reporterCode='36', cmdCode='91', flowCode='M', partnerCode=None,
                                        partner2Code=None,
                                        customsCode=None, motCode=None, maxRecords=500, format_output='JSON',
                                        aggregateBy=None, breakdownMode='classic', countOnly=None, includeDesc=True)
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



