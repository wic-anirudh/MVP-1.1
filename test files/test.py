import pandas as pd
from polygon import WebSocketClient
from polygon.websocket.models import WebSocketMessage
from typing import List

client = WebSocketClient(subscriptions=["T.*"])

def handle_msg(msgs: List[WebSocketMessage]):
    POLYGON_API_KEY = "jkfq7GKspSgL52UGHXp73Ij3BXNAvj34"
    for m in msgs:
        print(m)

client.run(handle_msg)

def shariah_analysis(stock):
    """
    A basic Shariah analysis on a stock.
   
    Parameters:
    stock (str): The ticker symbol for the stock

    Possible Additions:
    Dividend purification

       Resources: The intelligent investor
       
    Returns:
    dict: A dictionary containing the results of the Shariah analysis
    """
    # Get the financial data for the stock   -- Need all listings of companies (financial data): Industry, level of debt, income, interest, etc.
    # ticker,industry,pe_ratio,total_debt,total_equity,interest_income,total_income
    stock_data = pd.read_csv('stock.csv')

    for i in stock_data:
        if i=='ticker':
            for j in i:
                if (j==stock):
                    stock_d = j
   
    # Initialize a dictionary to store the results of the Shariah analysis
    results = {}
   
    # Check if the stock is involved in any prohibited industries (e.g. gambling, alcohol, tobacco)  -- Could be more
    prohibited_industries = ['gambling', 'alcohol', 'tobacco']
    results['prohibited_industries'] = any(industry in stock_data['industry'] for industry in prohibited_industries)
   
    # Check if the stock has a high level of debt
    debt_to_equity_ratio = stock_data['total_debt'].sum() / stock_data['total_equity'].sum()
    results['high_debt'] = debt_to_equity_ratio > 0.5
   
    # Check if the stock has a high level of interest-based income
    interest_income = stock_data['interest_income'].sum() / stock_data['total_income'].sum()
    results['high_interest_income'] = interest_income > 0.1
   
    # Return the results of the Shariah analysis
    return results

# Example usage
stock = 'AAPL'
results = shariah_analysis(stock)
print(results)
