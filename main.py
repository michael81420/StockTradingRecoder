import yfinance as yf
import logging
import json
import argparse
import xlsxwriter
from module.finance_key import FinanceKey, INFO_TYPE, POST_PROCESS
from module.ticker_mgr import TickerMgr

PARSE_KEY = [
    FinanceKey("TotalRevenue", INFO_TYPE.INCOME_STATEMENT, POST_PROCESS.DIVDE_BILLION),
    FinanceKey("OperatingIncome", INFO_TYPE.INCOME_STATEMENT, POST_PROCESS.DIVDE_BILLION),
    FinanceKey("NetIncome", INFO_TYPE.INCOME_STATEMENT, POST_PROCESS.DIVDE_BILLION),
    FinanceKey("ShareIssued", INFO_TYPE.BALANCE_SHEET, POST_PROCESS.DIVDE_BILLION),
    FinanceKey("CostOfRevenue", INFO_TYPE.INCOME_STATEMENT, POST_PROCESS.DIVDE_BILLION),
    FinanceKey("GrossProfit", INFO_TYPE.INCOME_STATEMENT, POST_PROCESS.DIVDE_BILLION),
    FinanceKey("OperatingExpense", INFO_TYPE.INCOME_STATEMENT, POST_PROCESS.DIVDE_BILLION),
    FinanceKey("NetNonOperatingInterestIncomeExpense", INFO_TYPE.INCOME_STATEMENT, POST_PROCESS.DIVDE_BILLION),
    FinanceKey("OtherIncomeExpense", INFO_TYPE.INCOME_STATEMENT, POST_PROCESS.DIVDE_BILLION),
    FinanceKey("PretaxIncome", INFO_TYPE.INCOME_STATEMENT, POST_PROCESS.DIVDE_BILLION),
    FinanceKey("TaxProvision", INFO_TYPE.INCOME_STATEMENT, POST_PROCESS.DIVDE_BILLION),
    FinanceKey("BasicEPS", INFO_TYPE.INCOME_STATEMENT, POST_PROCESS.NONE),
    FinanceKey("EBITDA", INFO_TYPE.INCOME_STATEMENT, POST_PROCESS.DIVDE_BILLION),
    FinanceKey("trailingPE", INFO_TYPE.SOTCK_INFO, POST_PROCESS.NONE),
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

    workbook  = xlsxwriter.Workbook("report.xlsx")
    title_format = workbook.add_format({'bg_color': '#ADADAD', 'bold': True, 'align': 'center'})
    percent_format = workbook.add_format({'num_format': '0.00%'})
    float_format = workbook.add_format({'num_format': '0.00'})
    
    tks = yf.Tickers(' '.join(args.stock))

    for stock_name, tk in tks.tickers.items():        
        ticker_mgr = TickerMgr(tk)

        worksheet = workbook.add_worksheet(stock_name)
        worksheet.set_column(0, 0, 40)
        for i, finance_key in enumerate(PARSE_KEY):
            worksheet.write(i + 1, 0, finance_key.name_with_unit())

        for i, date in enumerate(ticker_mgr.dates):
            worksheet.set_column(i + 1, i + 1, 15)
            worksheet.write(0, i + 1, date.strftime("%Y-%m-%d"))

            for j, finance_key in enumerate(PARSE_KEY):
                worksheet.write(j + 1, i + 1, ticker_mgr.get_val(date, finance_key), float_format)
        
        worksheet.set_column(8, 10, 15)
        worksheet.write(0, 8, "Est. grow rate", title_format)
        worksheet.write(0, 9, "Est. discount rate", title_format)
        worksheet.write(0, 10, "DDM Price", title_format)
        worksheet.write(1, 8, ticker_mgr.estimate_grow_rate, percent_format)
        worksheet.write(1, 9, ticker_mgr.estimate_discount_rate, percent_format)
        worksheet.write(1, 10, ticker_mgr.get_DDM_model_price(), float_format)

        

    workbook.close()
    
    return 

if __name__ == '__main__':
    main()