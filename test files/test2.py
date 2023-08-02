import requests
import csv
#Total shareholderequity, add up all debts for total debt
print("LOADING DATA")
url = 'https://www.alphavantage.co/query?function=BALANCE_SHEET&symbol=IBM&apikey=demo'
r = requests.get(url)
print("DATA HAS BEEN DOWNLOADED")
data = r.json()
print(data)
