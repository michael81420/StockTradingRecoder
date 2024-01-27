import yfinance as yf
import logging
import json

def main() -> int:
    apple = yf.Ticker("AAPL")
    print("apple currentPrice", apple.get_info()['currentPrice'])




    # with open("sample.json", "w") as outfile: 
    #     json.dump(apple.get_info(), outfile, indent = 4)
    
    return 

if __name__ == '__main__':
    main()