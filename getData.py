import requests
import time
from datetime import timedelta
from ratelimit import limits, RateLimitException, sleep_and_retry
from cleanData import *
import pickle

ONE_MINUTE = 60
MAX_CALLS_PER_MINUTE = 65

@sleep_and_retry
@limits(calls=MAX_CALLS_PER_MINUTE, period=ONE_MINUTE)
def call_api(url):
    #This function performs an API call using the given URL as long as the call does not fail
    req = requests.get(url)
    while req.status_code!=200:    
        time.sleep(10)
        req = requests.get(url)
    return req

def get_master_list(urls):
    # This function takes urls and performs API calls to get the required data pertaining
    # to Organizational Data, Balance Sheet Data, and Income Statement Data.
    
    master_list = []
    
    # Call the API and input the data into the master list
    for url in urls:
        req = call_api(url)
        info = req.json()
        if info!={}:
            master_list.append(info)
            
    return master_list
    
def get_data(urls,c):
    print("OBTAINING ",c)

    final_master_list = []
    temp = []

    # Get master list
    master_list = get_master_list(urls)
    
    # Clean up data to remove all error messages 
    for obj in master_list:
        if obj and ('Error Message' not in obj.keys()):
            temp.append(obj)
    master_list = temp
    temp = []  # Empty temp for later use

    # Loop through the master list (Each object is a dictionary - Master list is a list of dictionaries)
    for obj in master_list:
        # Add symbol as it is required irrespective of the type of data
        if obj['symbol']:
            temp.append(obj['symbol'])

        # Perform clean up for organizational data
        if c=="Organizational Data":
            if obj["Name"]:
                temp.append(obj["Name"])
            if obj["Industry"]:
                temp.append(obj["Industry"])
            if obj["PERatio"]:
                temp.append(obj["PERatio"])

        # Perform clean up for balance sheet data
        elif obj["quarterlyReports"]:
            if c=="Balance Sheet Data":
                temp.append(obj["quarterlyReports"][0]['totalShareholderEquity'])
                if (obj["quarterlyReports"][0]['currentDebt']=="None"):
                    obj["quarterlyReports"][0]['currentDebt'] = 0
                if (obj["quarterlyReports"][0]['shortTermDebt']=="None"):
                    obj["quarterlyReports"][0]['shortTermDebt'] = 0
                if (obj["quarterlyReports"][0]['longTermDebt']=="None"):
                    obj["quarterlyReports"][0]['longTermDebt'] = 0
                if (obj["quarterlyReports"][0]['currentLongTermDebt']=="None"):
                    obj["quarterlyReports"][0]['currentLongTermDebt'] = 0
                if (obj["quarterlyReports"][0]['longTermDebtNoncurrent']=="None"):
                    obj["quarterlyReports"][0]['longTermDebtNoncurrent'] = 0
                if (obj["quarterlyReports"][0]['shortLongTermDebtTotal']=="None"):
                    obj["quarterlyReports"][0]['shortLongTermDebtTotal'] = 0
                temp.append(float(obj["quarterlyReports"][0]['currentDebt']) + float(obj['quarterlyReports'][0]['shortTermDebt']) + float(obj['quarterlyReports'][0]['longTermDebt']) + float(obj['quarterlyReports'][0]['currentLongTermDebt']) + float(obj['quarterlyReports'][0]['longTermDebtNoncurrent']) + float(obj['quarterlyReports'][0]['shortLongTermDebtTotal']))

            # Perform clean up for income statement data
            elif c=="Income Statement Data":
                temp.append(obj["quarterlyReports"][0]['netInterestIncome'])
                temp.append(obj["quarterlyReports"][0]['netIncome'])

        # Add all data to final master list
        final_master_list.append(temp)

    temp = []  # Empty temp for later use
    if c=="Balance Sheet Data" or c=="Income Statement Data":
        cleanUp(final_master_list)
        
    print(c," SUCCESSFULLY DOWNLOADED")

    return final_master_list
                
            
    
    
