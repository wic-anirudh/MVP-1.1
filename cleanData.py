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
                else:
                    temp2.append(master_data[pointer2])
            pointer+=4

        # For balance sheet data and income statement data
        if(c==2):
            # Loop through the next 2 pointers
            for pointer2 in range(pointer+1,pointer+3):

                # If pointer2 is valid/exists
                if(0<=pointer2<len(master_data)):

                    # If the data at pointer2 is a float or a number (check if the data is going in as string or int... does it really matter what it goes in as?)
                    if((isinstance(master_data[pointer2],float)) or ((master_data[pointer2].strip('-')).isnumeric())):
                        temp2.append(master_data[pointer2])

                    # If data at pointer2 is empty or Null, append 0 for remaining values and exit for loop
                    elif(master_data[pointer2]=='NA'):
                         temp2.append(0)
                         counter+=1

                         # If both values are NA
                         if(counter==2):
                             temp2 = []
                             counter = 0
                             pointer+=3
                             break                     

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
        

    # Remove empty arrays left over from dead stocks
    for stock in temp:
        if stock==[]:
            temp.remove(stock)
            
    return temp

def removeFromList(data,orgData):
    #Split data into sublists of 3 elements each
    data_sublists = [data[i:i+3] for i in range(0,len(data),3)]
    
    # Create a set of the tickers in org_data
    tickers_in_org_data = {arr[0] for arr in orgData}

    # Filter data on set of tickers                     
    data_compiled = [arr for arr in data_sublists if arr[0] in tickers_in_org_data]
    
    result = [item for arr in data_compiled for item in arr]
    
    return result
                
