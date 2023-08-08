import requests
import time
from datetime import timedelta
from ratelimit import limits, RateLimitException, sleep_and_retry
import pickle

ONE_MINUTE = 60
MAX_CALLS_PER_MINUTE = 70

@sleep_and_retry
@limits(calls=MAX_CALLS_PER_MINUTE, period=ONE_MINUTE)
def call_api(url):
    #This function performs an API call using the given URL as long as the call does not fail
    req = requests.get(url)
    while req.status_code!=200:    
        time.sleep(5)
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
        
        # Perform clean up for organizational data
        if c=="Organizational Data":
            if obj['Symbol']:
                temp.append(obj['Symbol'])
            else:
                continue
            if obj["Name"]:
                temp.append(obj["Name"])
            else:
                temp.append("NA")
            if obj["Industry"]:
                temp.append(obj["Industry"])
            else:
                temp.append("NA")
            if obj["PERatio"]:
                temp.append(obj["PERatio"])
            else:
                temp.append("NA")
            

        # Perform clean up for balance sheet data
        elif c=="Balance Sheet Data":
            if obj['symbol']:
                temp.append(obj['symbol'])
            else:
                continue
                
            if obj["quarterlyReports"]==[]:
                temp.append("NA")
                temp.append("NA")
            else:
                if obj["quarterlyReports"][0]['totalShareholderEquity']=='None':
                    temp.append("NA")
                else:
                    temp.append(obj["quarterlyReports"][0]['totalShareholderEquity'])
                if (obj["quarterlyReports"][0]['currentDebt']=='None'):
                    obj["quarterlyReports"][0]['currentDebt'] = 0
                if (obj["quarterlyReports"][0]['shortTermDebt']=='None'):
                    obj["quarterlyReports"][0]['shortTermDebt'] = 0
                if (obj["quarterlyReports"][0]['longTermDebt']=='None'):
                    obj["quarterlyReports"][0]['longTermDebt'] = 0
                if (obj["quarterlyReports"][0]['currentLongTermDebt']=='None'):
                    obj["quarterlyReports"][0]['currentLongTermDebt'] = 0
                if (obj["quarterlyReports"][0]['longTermDebtNoncurrent']=='None'):
                    obj["quarterlyReports"][0]['longTermDebtNoncurrent'] = 0
                if (obj["quarterlyReports"][0]['shortLongTermDebtTotal']=='None'):
                    obj["quarterlyReports"][0]['shortLongTermDebtTotal'] = 0
                temp.append(float(obj["quarterlyReports"][0]['currentDebt']) + float(obj['quarterlyReports'][0]['shortTermDebt']) + float(obj['quarterlyReports'][0]['longTermDebt']) + float(obj['quarterlyReports'][0]['currentLongTermDebt']) + float(obj['quarterlyReports'][0]['longTermDebtNoncurrent']) + float(obj['quarterlyReports'][0]['shortLongTermDebtTotal']))
                
            
        # Perform clean up for income statement data
        elif c=="Income Statement Data":
            if obj['symbol']:
                temp.append(obj['symbol'])
            else:
                continue
            if(obj["quarterlyReports"]==[]):
                temp.append("NA")
                temp.append("NA")
            else:
                if(obj["quarterlyReports"][0]['netInterestIncome']=='None'):
                    temp.append("NA")
                else:
                    temp.append(obj["quarterlyReports"][0]['netInterestIncome'])
                if(obj["quarterlyReports"][0]['netIncome']=='None'):
                    temp.append("NA")
                else:
                    temp.append(obj["quarterlyReports"][0]['netIncome'])

        # Add all data to final master list
        final_master_list.append(temp)

    temp = []
        
    print(c," SUCCESSFULLY DOWNLOADED")
    return final_master_list
                
            
    
    
