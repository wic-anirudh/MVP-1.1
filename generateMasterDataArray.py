import requests
import csv
from cleanData import *
from openpyxl import Workbook

def compile_data(f_o_list, f_m_bs_list, f_m_is_list):
    # Compile data to one array
    
    print("COMPILING DATA TO ONE ARRAY")

    master_data = []
    temp_arr = []
    count = 1

    #print("#1", f_o_list)
    #print((master_data[0]))
    print((f_m_bs_list[0:20]))
    print(f_m_is_list[0:20])
    
    for i in range(len(f_o_list)):
        if(f_o_list[i] == 'None'):
            f_o_list[i] = 0
        if(count<4):
            temp_arr.append(f_o_list[i])
            count+=1
        else:
            temp_arr.append(f_o_list[i])
            count=1
            master_data.append(temp_arr)
            temp_arr = []

    #print("#2", f_o_list)
    print((master_data[0]))
    print((f_m_bs_list[0:20]))
    print(f_m_is_list[0:20])
    # REMOVE STOCKS FROM BS LIST NOT IN ORG LIST
    f_m_bs_list = removeFromList(f_m_bs_list,master_data)

    # REMOVE STOCKS FROM IS LIST NOT IN ORG LIST
    f_m_is_list = removeFromList(f_m_is_list,master_data)

    print(len(master_data))
    print(len(f_m_bs_list))
    print(len(f_m_is_list))
    checker = 0
    loop_argument = 0
    iterator = 0

    # ASSEMBLE
    # Use linked list to speed up deletions
    z = 1
    while loop_argument<len(master_data):
        print("Iter# ",z)
        print("Loop arg ",loop_argument)
        if(f_m_bs_list[loop_argument][0]==master_data[loop_argument][0]):
            for j in range(len(f_m_bs_list[loop_argument])):
                if(j!=0):
                    master_data[loop_argument].append(f_m_bs_list[loop_argument][j])
        if(f_m_is_list[loop_argument][0]==master_data[loop_argument][0]):
            for j in range(len(f_m_is_list[loop_argument])):
                if(j!=0):
                    master_data[loop_argument].append(f_m_is_list[loop_argument][j])
        for j in range(len(master_data[loop_argument])):
            if j>2:
                if master_data[loop_argument][j]==0:
                    checker+=1
            if j==7:
                if(checker==5):
                    master_data.pop(loop_argument)
                    f_m_bs_list.pop(loop_argument)
                    f_m_is_list.pop(loop_argument)
                    checker = 0
                else:
                    loop_argument+=1
                    checker = 0
        z+=1
                       

    print("COMPILATION COMPLETED")
    
    return master_data
