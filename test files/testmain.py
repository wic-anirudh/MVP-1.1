import requests
import csv
from openpyxl import Workbook
from getActiveStocks import *
from generateMasterDataArray import *
from getBSData import *
from getISData import *
from getOrgData import *
from xlsxFuncs import *
#import pickle
import sqlite3
from generateMasterTable import *

# Using Alpha Vantage API Premium Version ($49.99/month)
# 75 calls per minute
# API KEY: W23N28A5DES6ZKCP

print("WELCOME")
print("OBTAINING LIST OF ACTIVE STOCKS")

# CREATE DB CONNECTION
conn = sqlite3.connect("stock_data.db")
cursor = conn.cursor()

# CREATE TABLE FOR ACTIVE STOCKS
cursor.execute("CREATE TABLE IF NOT EXISTS active_stocks (ticker TEXT PRIMARY KEY, company_name TEXT)")

# LIST OF ACTIVE STOCKS
cursor.execute("SELECT * FROM active_stocks")
active_stocks = cursor.fetchall()

if len(active_stocks) == 0:
    active_stocks = get_active_stocks()
    print("Number of active stocks:", len(active_stocks))
    print("Structure of active stocks:", active_stocks[0])
    cursor.executemany("INSERT INTO active_stocks (ticker, company_name) VALUES (?, ?)", active_stocks)
    conn.commit()
    print("ACTIVE STOCKS SAVED")
else:
    print("ACTIVE STOCKS LOADED")

# Print active_stocks for verification
print("Active Stocks:", active_stocks)

# GENERATE ALL URLS     
print("OBTAINING STOCK URLS")
stock_urls, balance_sheet_urls, income_statement_urls = generate_URLs(active_stocks)

print("OBTAINING ALL INDIVIDUAL STOCK DATA")

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

# BALANCE SHEET DATA
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

# INCOME STATEMENT DATA
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

generate_master_table()

print("GOODBYE")
