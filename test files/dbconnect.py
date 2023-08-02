import sqlite3

def generate_master_table():
    conn = sqlite3.connect("stock_data.db")
    cursor = conn.cursor()

    # Drop the existing master table if it already exists
    cursor.execute("DROP TABLE IF EXISTS master")

    # Create the master table with STOCK as the primary key and compile the data
    cursor.execute("CREATE TABLE master AS SELECT active_stocks.ticker AS STOCK, active_stocks.company_name, org_data.industry, bs_data.total_shareholder_equity, bs_data.total_debt, is_data.interest_income, is_data.total_income FROM active_stocks LEFT JOIN org_data ON active_stocks.ticker = org_data.ticker LEFT JOIN bs_data ON active_stocks.ticker = bs_data.ticker LEFT JOIN is_data ON active_stocks.ticker = is_data.ticker")

    conn.commit()
    conn.close()
