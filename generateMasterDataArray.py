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

    # Set master data to be same as organizational data
    master_data = f_o_list

    # REMOVE STOCKS FROM BS/IS LIST NOT IN ORG LIST
    master_data,f_m_bs_list,f_m_is_list = removeFromList(f_m_bs_list,f_m_is_list,master_data)

    # ASSEMBLY
    for i in range(len(f_m_bs_list)):
        for j in range(1,3):
            if(f_m_bs_list[i][0]==master_data[i][0]):
                if(j!=0):
                    master_data[i].append(f_m_bs_list[i][j])
        for j in range(1,3):
            if(f_m_is_list[i][0]==master_data[i][0]):
                if(j!=0):
                    master_data[i].append(f_m_is_list[i][j])
                    
    print("COMPILATION COMPLETED")
    
    return master_data
