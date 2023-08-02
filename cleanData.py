import requests
import time
from datetime import timedelta
from ratelimit import limits, RateLimitException, sleep_and_retry

def cleanUp(data):
    temp = []
    temp2 = []
    master_data = data
    pointer = 0
 
    # While the pointer is valid/exists
    while pointer<len(master_data):

        # If the data at pointer is a string and not all characters in the data are numbers (If data is ticker)(DO WE NEED THE and not statement??)
        # If data is not string, then pointer gets incremented
        if((type(master_data[pointer]) ==str)and not master_data[pointer].strip('-').isnumeric()):
            temp2.append(master_data[pointer])

            # Loop through the next 2 pointers
            for pointer2 in range(pointer+1,pointer+3):

                # If pointer2 is valid/exists
                if(0<=pointer2<len(master_data)):

                    # If the data at pointer2 is a float or a number (check if the data is going in as string or int... does it really matter what it goes in as?)
                    if((isinstance(master_data[pointer2],float)) or ((master_data[pointer2].strip('-')).isnumeric())):
                        temp2.append(master_data[pointer2])

                    # If data at pointer2 is empty or Null, append 0 for remaining values and exit for loop
                    else:
                        while(len(temp2)!=3):
                            temp2.append(0)
                        break

                # If pointer2 doesn't exist, append 0 (It means it's empty or Null and got cut off from the end of the array)
                else:
                    while(len(temp2)!=3):
                            temp2.append(0)

            # Append temp2 to the larger temp array
            temp.append(temp2)
            temp2 = []
        pointer+=1

    # temp array can be moved to result now for returning  
    result = temp

    return result

def removeFromList(data,orgData):
    #print("orgData example element",orgData[0])
    #print("Data example element",data[0])
    #print('data original length', len(data))

    #Split data into sublists of 3 elements each
    data_sublists = [data[i:i+3] for i in range(0,len(data),3)]
    print(data_sublists)
    # Create a set of the tickers in org_data
    tickers_in_org_data = {arr[0] for arr in orgData}
    #print(tickers_in_org_data)

    # Filter data on set of tickers                     
    data_compiled = [arr for arr in data_sublists if arr[0] in tickers_in_org_data]
    #print(data_compiled)
    result = [item for arr in data_compiled for item in arr]
    #print(result)
    #print('data length', len(result))
    #print('orgData length', len(orgData))
    return result
                
