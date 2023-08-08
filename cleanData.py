import requests
import time
from datetime import timedelta
from ratelimit import limits, RateLimitException, sleep_and_retry

def cleanUp(data,c):
    temp = []
    temp2 = []
    master_data = data
    pointer = 0
    counter = 0
    exit_checker = 0
    result = []

    if c==1:
        for i in range(0,len(data),4):
            for j in range(i,i+4):
                # We don't consider blank check corps/Shell corps
                if(master_data[j]=='BLANK CHECKS'):
                    exit_checker = 1
                    break
                
                # If no PE Ratio, we don't want it
                elif(master_data[j]=='None'):
                    exit_checker = 1
                    break

                else:
                    temp2.append(master_data[j])
            # Append temp2 to the larger temp array
            if exit_checker!=1:
                temp.append(temp2)

            exit_checker = 0
            temp2 = []

    if c==2:
        for i in range(0,len(data),3):
            for j in range(i,i+3):
                if 0<=j<=len(data):
                    # If data at pointer2 is empty or Null, append 0 for remaining values and exit for loop
                    if(master_data[j]=='NA'):
                         temp2.append(0)
                         counter+=1

                         # If both values are NA
                         if(counter==2):
                             temp2 = []
                             counter = 0
                             break
                            
                    # Else it's a number
                    else:
                        temp2.append(master_data[j])
                else:
                    temp2.append(0)
            temp.append(temp2)
            temp2 = []
            counter = 0

            
    '''                

    #print(data[10830:10840])
    # While the pointer is valid/exists
    while pointer<len(master_data):

        temp2.append(master_data[pointer])

        # For organizational data:
        if(c==1):
            for pointer2 in range(pointer+1,pointer+4):
                # We don't consider blank check corps/Shell corps
                if(master_data[pointer2]=='BLANK CHECKS'):
                    exit_checker = 1
                    break
                
                # If no PE Ratio, we don't want it
                elif(master_data[pointer2]=='None'):
                   exit_checker = 1
                   break
                     
                else:
                    temp2.append(master_data[pointer2])
            pointer+=4

        # For balance sheet data and income statement data
        if(c==2):
            # Loop through the next 2 pointers
            for pointer2 in range(pointer+1,pointer+3):
                
                # If pointer2 is valid/exists
                if(0<=pointer2<len(master_data)):

                    # If data at pointer2 is empty or Null, append 0 for remaining values and exit for loop
                    if(master_data[pointer2]=='NA'):
                         temp2.append(0)
                         counter+=1

                         # If both values are NA
                         if(counter==2):
                             temp2 = []
                             counter = 0
                             pointer+=3
                             break
                            
                    # Else it's a number
                    else:
                        temp2.append(master_data[pointer2])
                        
                # If pointer2 doesn't exist, append 0 (It means it's empty or Null and got cut off from the end of the array)
                else:
                    while(len(temp2)!=3):
                            temp2.append(0)

            counter = 0
            pointer+=3

        # Append temp2 to the larger temp array
        if exit_checker!=1:
            temp.append(temp2)
        exit_checker = 0
        temp2 = []

    #print(temp[3000:3400])
'''
        
    # Remove empty arrays left over from dead stocks
    for stock in temp:
        if stock!=[]:
            result.append(stock)
    #print(result[3000:3400])
    return result

def removeFromList(bsData,isData,orgData):
    result = []
    tickers_orgData = []
    tickers_bsData = []
    tickers_isData = []

    # Get tickers from BS data
    for arr in bsData:
        tickers_bsData.append(arr[0])

    # Get tickers from IS data
    for arr in isData:
        tickers_isData.append(arr[0])

    # Get tickers from org data
    for arr in orgData:
        tickers_orgData.append(arr[0])

    # Find common tickers
    common_tickers = set(tickers_orgData) & set(tickers_bsData) & set(tickers_isData)

    # Remove all uncommon tickers
    filtered_orgData = [arr for arr in orgData if arr[0] in common_tickers]
    filtered_bsData = [arr for arr in bsData if arr[0] in common_tickers]
    filtered_isData = [arr for arr in isData if arr[0] in common_tickers]
    
    return filtered_orgData,filtered_bsData,filtered_isData
                
