import yfinance as yf
import logging
import json
import argparse

PARSE_KEY = [
    "TotalRevenue",
    "CostOfRevenue",
    "GrossProfit",
    "OperatingExpense",
    "OperatingIncome",
    "NetNonOperatingInterestIncomeExpense",
    "OtherIncomeExpense",
    "PretaxIncome",
    "TaxProvision",
    "NetIncome",
    "BasicEPS",
    "EBITDA"
]

PARSE_KEY_2 = [
    "ShareIssued",
]

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("-stock", "-s", nargs='+', help="stocks list")
    parser.add_argument("-debug", help="debug mode", action="store_true")
    args = parser.parse_args()

    if args.debug:
        logging.basicConfig(level=logging.DEBUG, format='%(relativeCreated)6d %(threadName)s %(message)s')
    else:
        logging.basicConfig(level=logging.INFO, format='%(relativeCreated)6d %(threadName)s %(message)s')


    print(args.stock)

    apple = yf.Ticker("AAPL")
    # print("apple", )
    
    stmt_list = apple.get_income_stmt(as_dict=True)
    balance_list = apple.get_balancesheet(as_dict=True)

    for date in stmt_list:
        stmt = stmt_list[date]
        balance = balance_list[date]
        
        print([(key, stmt[key] / 1000000) for key in PARSE_KEY])
        print([(key, balance[key]) for key in PARSE_KEY_2])



    # with open("sample.json", "w") as outfile: 
    #     json.dump(apple.get_info(), outfile, indent = 4)
    
    return 

if __name__ == '__main__':
    main()