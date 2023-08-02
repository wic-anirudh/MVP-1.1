import requests
import csv
from openpyxl import Workbook

# Using Alpha Vantage API Premium Version ($49.99/month)
# 75 calls per minute
# API KEY: W23N28A5DES6ZKCP

master_data = []

# Extract List Method
def extract_list(active_stocks):
    count = 0
    ticker_list = []
    for stock in active_stocks:
        if count>0:
            ticker_list.append(stock[0])
        count+=1
    return ticker_list
    
# Get list of all active stocks
#CSV_URL = 'https://www.alphavantage.co/query?function=LISTING_STATUS&apikey=W23N28A5DES6ZKCP'

#print("CP1")
print("WELCOME")
print("GATHERING ACTIVE STOCKS")

list_of_active_stocks = []
with requests.Session() as s:
    download = s.get('https://www.alphavantage.co/query?function=LISTING_STATUS&apikey=W23N28A5DES6ZKCP')
    decoded_content = download.content.decode('utf-8')
    cr = csv.reader(decoded_content.splitlines(), delimiter=',')
    my_list = list(cr)
list_of_active_stocks = extract_list(my_list)
#print(list_of_active_stocks)

print("ALL ACTIVE STOCKS GATHERED")
print("OBTAINING URLS")

# Generate all URLs for each stock (organizational data, balance sheet data, income statement data)
# Restricted call count for testing purposes
stock_urls = []
balance_sheet_urls = []
income_statement_urls = []
call_count = 0
for stock in list_of_active_stocks:
    if call_count<1:
        stock_urls.append('https://www.alphavantage.co/query?function=OVERVIEW&symbol={}&apikey=W23N28A5DES6ZKCP'.format(stock))
        balance_sheet_urls.append('https://www.alphavantage.co/query?function=BALANCE_SHEET&symbol={}&apikey=W23N28A5DES6ZKCP'.format(stock))
        income_statement_urls.append('https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol={}&apikey=W23N28A5DES6ZKCP'.format(stock))
        call_count+=1
    else:
        break
#print(stock_urls)

print("ALL URLS GENERATED")
#print("CP2")

# ***********************
# ***********************
# ORGANIZATIONAL DATA
# ***********************
# ***********************

print("OBTAINING ORG DATA")

#Get organizational data for all active stocks
stock_url = None
m_list = []
f_o_list = []
for url in stock_urls:
    #print("x")
    stock_url = url
    r = requests.get(stock_url)
    data = r.json()
    m_list.append(data)

#print("CP3")
# Clean up master list
new_m_list = []
for i in m_list:
    if i:
        new_m_list.append(i)
#print(new_m_list)
m_list = new_m_list
#print(m_list)

to_list = []
for i in m_list:
    if i["Symbol"]:
        to_list.append(i["Symbol"])
    if i["Name"]:
        to_list.append(i["Name"])
    if i["Industry"]:
        to_list.append(i["Industry"])
    if i["PERatio"]:
        to_list.append(i["PERatio"])
    f_o_list.append(to_list)
    
#print(f_o_list)

print("ORG DATA SUCCESSFULLY DOWNLOADED")


# ***********************
# ***********************
# BALANCE SHEET DATA
# ***********************
# ***********************

print("OBTAINING BALANCE SHEET DATA")

# Get balance sheet data for all active stocks
bs_url = None
m_bs_list = []
f_m_bs_list = []
for url in balance_sheet_urls:
    bs_url = url
    r_bs = requests.get(bs_url)
    data_bs = r_bs.json()
    m_bs_list.append(data_bs)

# Clean up balance sheet data
new_m_list = []
for i in m_bs_list:
    if i:
        new_m_list.append(i)
m_bs_list = new_m_list
#print(m_bs_list)

tb_list = []
for i in m_bs_list:
    #print(i["annualReports"])
    if i["symbol"]:
        tb_list.append(i["symbol"])
    if i["annualReports"]:
        tb_list.append(i["annualReports"][0]['totalShareholderEquity'])
        if (i["annualReports"][0]['currentDebt']=="None"):
            i["annualReports"][0]['currentDebt'] = 0
        if (i["annualReports"][0]['shortTermDebt']=="None"):
            i["annualReports"][0]['shortTermDebt'] = 0
        if (i["annualReports"][0]['longTermDebt']=="None"):
            i["annualReports"][0]['longTermDebt'] = 0
        if (i["annualReports"][0]['currentLongTermDebt']=="None"):
            i["annualReports"][0]['currentLongTermDebt'] = 0
        if (i["annualReports"][0]['longTermDebtNoncurrent']=="None"):
            i["annualReports"][0]['longTermDebtNoncurrent'] = 0
        if (i["annualReports"][0]['shortLongTermDebtTotal']=="None"):
            i["annualReports"][0]['shortLongTermDebtTotal'] = 0
            
        tb_list.append(int(i["annualReports"][0]['currentDebt']) + int(i['annualReports'][0]['shortTermDebt']) + int(i['annualReports'][0]['longTermDebt']) + int(i['annualReports'][0]['currentLongTermDebt']) + int(i['annualReports'][0]['longTermDebtNoncurrent']) + int(i['annualReports'][0]['shortLongTermDebtTotal']))
    f_m_bs_list.append(tb_list)
    
#print(f_m_bs_list)

print("BALANCE SHEET DATA SUCCESSFULLY DOWNLOADED")

# ***********************
# ***********************
# INCOME STATEMENT DATA
# ***********************
# ***********************

print("OBTAINING INCOME STATEMENT DATA")

# Get income statement data for all active stocks
is_url = None
m_is_list = []
f_m_is_list = []
for url in income_statement_urls:
    is_url = url
    r_is = requests.get(is_url)
    data_is = r_is.json()
    m_is_list.append(data_is)

# Clean up income statement data
new_m_list = []
for i in m_is_list:
    if i:
        new_m_list.append(i)
m_is_list = new_m_list

t_list = []
for i in m_is_list:
    if i["symbol"]:
        t_list.append(i["symbol"])
    if i["annualReports"]:
        t_list.append(i["annualReports"][0]['netInterestIncome'])
        t_list.append(i["annualReports"][0]['netIncome'])
    f_m_is_list.append(t_list)
         
#print(f_m_is_list)

print("INCOME STATEMENT DATA SUCCESSFULLY DOWNLOADED")

# ***********************
# ***********************
# DATA COMPILATION
# ***********************
# ***********************

print("COMPILING DATA TO ONE ARRAY")

# Compile data to one array
for i in f_o_list:
    master_data.append(i)

for i in range(len(f_o_list)):
    if(f_m_bs_list[i][0]==master_data[i][0]):
        for j in range(len(f_m_bs_list[i])):
            if(j!=0):
                master_data[i].append(f_m_bs_list[i][j])
    if(f_m_is_list[i][0]==master_data[i][0]):
        for j in range(len(f_m_is_list[i])):
            if(j!=0):
                master_data[i].append(f_m_is_list[i][j])

#print(master_data)

print("PUTTING DATA INTO SPREADSHEET")
# Put data in excel spreadsheet
wb = Workbook()
ws = wb.active

headings = ['Ticker', 'Company Name','Industry','PE Ratio','Total Debt','Total Equity','Interest Income','Total Income']
ws.append(headings)

for stock in master_data:
    #print(stock)
    ws.append(stock)
wb.save("clean_stock_data.xlsx")

print("SPREADSHEET UPDATED")


print("Goodbye")
