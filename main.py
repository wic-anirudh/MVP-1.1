import requests
import csv
from openpyxl import Workbook
from getActiveStocks import *
from generateMasterDataArray import *
from getData import *
from xlsxFuncs import *
import pickle
#import sqlite3
#from generateMasterTable import *

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

# CREATE DB CONNECTION
#connection = sqlite3.connect("stock_data.db")
#cursor = connection.cursor()

# CREATE TABLE FOR ACTIVE STOCKS
#cursor.execute("CREATE TABLE IF NOT EXISTS active_stocks (ticker TEXT PRIMARY KEY, company_name TEXT)")

# LIST OF ACTIVE STOCKS
#cursor.execute("SELECT * FROM active_stocks")
#active_stocks = cursor.fetchall()
'''
if len(active_stocks) == 0:
    active_stocks = get_active_stocks()
    #cursor.executemany("INSERT INTO active_stocks VALUES (?, ?)", active_stocks)
    cursor.executemany("INSERT INTO active_stocks VALUES (?, ?)", active_stocks)

    conn.commit()
    print("ACTIVE STOCKS SAVED")
else:
    print("ACTIVE STOCKS LOADED")
    
'''
#USING PICKLE
try:
    with open("active_stocks.pkl", "rb") as file:
        active_stocks = pickle.load(file)
        #print(active_stocks[0])
        print("ACTIVE STOCKS LOADED")
except FileNotFoundError:
    active_stocks = get_active_stocks()
    with open("active_stocks.pkl", "wb") as file:
        pickle.dump(active_stocks, file)
    print("ACTIVE STOCKS SAVED")

# GENERATE ALL URLS     
print("OBTAINING STOCK URLS")
stock_urls, balance_sheet_urls, income_statement_urls = generate_URLs(active_stocks)

print("OBTAINING ALL INDIVIDUAL STOCK DATA")
'''
# ORG DATA
cursor.execute("CREATE TABLE IF NOT EXISTS org_data (ticker TEXT PRIMARY KEY, company_name TEXT, industry TEXT)")
cursor.execute("SELECT * FROM org_data")
org_data = cursor.fetchall()

if len(org_data) == 0:
    org_data = get_org_data(stock_urls)
    cursor.executemany("INSERT INTO org_data VALUES (?, ?, ?)", org_data)
    conn.commit()
    print("ORGANIZATIONAL DATA SAVED")
else:
    print("INDIVIDUAL STOCK DATA LOADED")

'''
# USING PICKLE
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


# BALANCE SHEET DATA
'''
cursor.execute("CREATE TABLE IF NOT EXISTS bs_data (ticker TEXT PRIMARY KEY, total_shareholder_equity REAL, total_debt REAL)")
cursor.execute("SELECT * FROM bs_data")
balance_sheet_data = cursor.fetchall()

if len(balance_sheet_data) == 0:
    balance_sheet_data = get_bs_data(balance_sheet_urls)
    cursor.executemany("INSERT INTO bs_data VALUES (?, ?, ?)", balance_sheet_data)
    conn.commit()
    print("BALANCE SHEET DATA SAVED")
else:
    print("BALANCE SHEET DATA LOADED")
    
'''
#USING PICKLE
try:
    with open("bs_data.pkl", "rb") as file:
        balance_sheet_data = pickle.load(file)
        balance_sheet_data = balance_sheet_data[0]
        #print(balance_sheet_data)
        print("BALANCE SHEET DATA LOADED")
except FileNotFoundError:
    balance_sheet_data = get_data(balance_sheet_urls,"Balance Sheet Data")
    with open("bs_data.pkl", "wb") as file:
        pickle.dump(balance_sheet_data, file)
        print("BALANCE SHEET DATA SAVED")


# INCOME STATEMENT DATA
'''
cursor.execute("CREATE TABLE IF NOT EXISTS is_data (ticker TEXT PRIMARY KEY, interest_income REAL, total_income REAL)")
cursor.execute("SELECT * FROM is_data")
income_statement_data = cursor.fetchall()

if len(income_statement_data) == 0:
    income_statement_data = get_is_data(income_statement_urls)
    cursor.executemany("INSERT INTO is_data VALUES (?, ?, ?)", income_statement_data)
    conn.commit()
    print("INCOME STATEMENT DATA SAVED")
else:
    print("INCOME STATEMENT DATA LOADED")
'''
#USING PICKLE
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

        
print("COMPILING ALL DATA TO ONE ARRAY")
master_data = compile_data(org_data,balance_sheet_data,income_statement_data)
#print(master_data)

print("CREATING MASTER SPREADSHEET")
createSpreadsheet(master_data)

#print("CREATING SHARIAH SPREADSHEET")
#createShariahSpreadsheet()

#generate_master_table()

print("GOODBYE")
