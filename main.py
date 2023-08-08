import requests
import csv
from openpyxl import Workbook
from getActiveStocks import *
from generateMasterDataArray import *
from getData import *
from xlsxFuncs import *
import pickle
from cleanData import *

# Using Alpha Vantage API Premium Version ($49.99/month)
# 75 calls per minute
# API KEY: W23N28A5DES6ZKCP

'''
Pickle is great for small use cases or testing because in most case the memory
consumption doesn't matter a lot.

For intensive work where you have to dump and load a lot of files and/or big
files you should consider using another way to store your data (ex.: hdf,
wrote your own serialize/deserialize methods for your object)
'''

print("WELCOME")
print("OBTAINING LIST OF ACTIVE STOCKS")

# LIST OF ACTIVE STOCKS
try:
    with open("active_stocks.pkl", "rb") as file:
        active_stocks = pickle.load(file)
        print("ACTIVE STOCKS LOADED")
except FileNotFoundError:
    active_stocks = get_active_stocks()
    with open("active_stocks.pkl", "wb") as file:
        pickle.dump(active_stocks, file)
    print("ACTIVE STOCKS SAVED")

# GENERATE ALL URLS     
print("OBTAINING STOCK URLS")
stock_urls, balance_sheet_urls, income_statement_urls = generate_URLs(active_stocks)

# ORGANIZATIONAL DATA
print("OBTAINING ALL INDIVIDUAL STOCK DATA")
try:
    with open("org_data.pkl", "rb") as file:
        org_data = pickle.load(file)
        org_data = org_data[0]
        print("INDIVIDUAL STOCK DATA LOADED")
except FileNotFoundError:
    org_data = get_data(stock_urls,"Organizational Data")
    with open("org_data.pkl", "wb") as file:
        pickle.dump(org_data, file)
    print("ORGANIZATIONAL DATA SAVED")

org_data = cleanUp(org_data,1)

# BALANCE SHEET DATA
print("OBTAINING BALANCE SHEET DATA")
try:
    with open("bs_data.pkl", "rb") as file:
        balance_sheet_data = pickle.load(file)
        balance_sheet_data = balance_sheet_data[0]
        print("BALANCE SHEET DATA LOADED")
except FileNotFoundError:
    balance_sheet_data = get_data(balance_sheet_urls,"Balance Sheet Data")
    with open("bs_data.pkl", "wb") as file:
        pickle.dump(balance_sheet_data, file)
        print("BALANCE SHEET DATA SAVED")

balance_sheet_data = cleanUp(balance_sheet_data,2)

# INCOME STATEMENT DATA
try:
    with open("is_data.pkl", "rb") as file:
        income_statement_data = pickle.load(file)
        income_statement_data = income_statement_data[0]
        print("INCOME STATEMENT DATA LOADED")
except FileNotFoundError:
    income_statement_data = get_data(income_statement_urls,"Income Statement Data")
    with open("is_data.pkl", "wb") as file:
        pickle.dump(income_statement_data, file)
        print("INCOME STATEMENT DATA SAVED")

income_statement_data = cleanUp(income_statement_data,2)

print("COMPILING ALL DATA TO ONE ARRAY")
master_data = compile_data(org_data,balance_sheet_data,income_statement_data)

print("CREATING MASTER SPREADSHEET")
createSpreadsheet(master_data)

#print("CREATING SHARIAH SPREADSHEET")
#createShariahSpreadsheet()

#generate_master_table()

print("GOODBYE")
