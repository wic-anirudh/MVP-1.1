import requests
import csv
from openpyxl import Workbook

def get_active_stocks():
    # Get list of all active stocks
    #CSV_URL = 'https://www.alphavantage.co/query?function=LISTING_STATUS&apikey=W23N28A5DES6ZKCP'

    print("WELCOME")
    print("GATHERING ACTIVE STOCKS")

    list_of_active_stocks = []
    with requests.Session() as s:
        download = s.get('https://www.alphavantage.co/query?function=LISTING_STATUS&apikey=W23N28A5DES6ZKCP')
        decoded_content = download.content.decode('utf-8')
        cr = csv.reader(decoded_content.splitlines(), delimiter=',')
        my_list = list(cr)

    count = 0
    for stock in my_list:
        if count>0:
            #print(stock[0])
            list_of_active_stocks.append(stock[0])
        count+=1
    #print(list_of_active_stocks)
    print("ALL ACTIVE STOCKS GATHERED")

    return list_of_active_stocks

def generate_URLs(list_of_active_stocks):
    # Generate all URLs for each stock (organizational data, balance sheet data, income statement data)
    
    print("OBTAINING URLS")

    stock_urls = []
    balance_sheet_urls = []
    income_statement_urls = []

    for stock in list_of_active_stocks:
        stock_urls.append('https://www.alphavantage.co/query?function=OVERVIEW&symbol={}&apikey=W23N28A5DES6ZKCP'.format(stock))
        balance_sheet_urls.append('https://www.alphavantage.co/query?function=BALANCE_SHEET&symbol={}&apikey=W23N28A5DES6ZKCP'.format(stock))
        income_statement_urls.append('https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol={}&apikey=W23N28A5DES6ZKCP'.format(stock))
    
    print("ALL URLS GENERATED")
    
    return stock_urls, balance_sheet_urls, income_statement_urls
