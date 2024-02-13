import yfinance as yf
import logging
import json
import argparse
import xlsxwriter
from enum import Enum, auto

class INFO_TYPE(Enum):
    INCOME_STATEMENT = auto()
    BALANCE_SHEET = auto()
    SOTCK_INFO = auto()

class POST_PROCESS(Enum):
    NONE = auto()
    DIVDE_MILLION = auto()
    DIVDE_BILLION = auto()

CHECK_RULE = [
    
]

PARSE_KEY = [
    ("TotalRevenue", INFO_TYPE.INCOME_STATEMENT, POST_PROCESS.DIVDE_BILLION),
    ("OperatingIncome", INFO_TYPE.INCOME_STATEMENT, POST_PROCESS.DIVDE_BILLION),
    ("NetIncome", INFO_TYPE.INCOME_STATEMENT, POST_PROCESS.DIVDE_BILLION),
    ("ShareIssued", INFO_TYPE.BALANCE_SHEET, POST_PROCESS.DIVDE_BILLION),
    # ("CostOfRevenue", INFO_TYPE.INCOME_STATEMENT, POST_PROCESS.DIVDE_BILLION),
    # ("GrossProfit", INFO_TYPE.INCOME_STATEMENT, POST_PROCESS.DIVDE_BILLION),
    # ("OperatingExpense", INFO_TYPE.INCOME_STATEMENT, POST_PROCESS.DIVDE_BILLION),
    # ("NetNonOperatingInterestIncomeExpense", INFO_TYPE.INCOME_STATEMENT, POST_PROCESS.DIVDE_BILLION),
    # ("OtherIncomeExpense", INFO_TYPE.INCOME_STATEMENT, POST_PROCESS.DIVDE_BILLION),
    # ("PretaxIncome", INFO_TYPE.INCOME_STATEMENT, POST_PROCESS.DIVDE_BILLION),
    # ("TaxProvision", INFO_TYPE.INCOME_STATEMENT, POST_PROCESS.DIVDE_BILLION),
    ("BasicEPS", INFO_TYPE.INCOME_STATEMENT, POST_PROCESS.NONE),
    ("EBITDA", INFO_TYPE.INCOME_STATEMENT, POST_PROCESS.DIVDE_BILLION),
    # ("trailingPE", INFO_TYPE.SOTCK_INFO, POST_PROCESS.NONE),
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

    workbook  = xlsxwriter.Workbook('report.xlsx')

    for stock_name in args.stock:
        tk = yf.Ticker(stock_name)
        stmt_list = tk.get_income_stmt(as_dict=True)
        balance_list = tk.get_balancesheet(as_dict=True)
        # tk_info = tk.get_info()

        dates = stmt_list.keys()

        worksheet = workbook.add_worksheet(stock_name)

        worksheet.set_column(0, 0, 40)
        for i, (key, _, post_proc) in enumerate(PARSE_KEY):
            if post_proc == POST_PROCESS.DIVDE_MILLION:
                worksheet.write(i + 1, 0, key + " (M)")
            elif post_proc == POST_PROCESS.DIVDE_BILLION:
                worksheet.write(i + 1, 0, key + " (B)")
            elif post_proc == POST_PROCESS.NONE:
                worksheet.write(i + 1, 0, key)

        for i, date in enumerate(dates):
            worksheet.set_column(i + 1, i + 1, 15)
            worksheet.write(0, i + 1, date.strftime("%Y-%m-%d"))
            for j, (key, info_type, post_proc) in enumerate(PARSE_KEY):
                if info_type == INFO_TYPE.INCOME_STATEMENT:
                    if post_proc == POST_PROCESS.DIVDE_MILLION:
                        worksheet.write(j + 1, i + 1, stmt_list[date][key] / 1000000)
                    elif post_proc == POST_PROCESS.DIVDE_BILLION:
                        worksheet.write(j + 1, i + 1, stmt_list[date][key] / 1000000000)
                    elif post_proc == POST_PROCESS.NONE:
                        worksheet.write(j + 1, i + 1, stmt_list[date][key])
                elif info_type == INFO_TYPE.BALANCE_SHEET:
                    if post_proc == POST_PROCESS.DIVDE_MILLION:
                        worksheet.write(j + 1, i + 1, balance_list[date][key] / 1000000)
                    elif post_proc == POST_PROCESS.DIVDE_BILLION:
                        worksheet.write(j + 1, i + 1, balance_list[date][key] / 1000000000)
                    elif post_proc == POST_PROCESS.NONE:
                        worksheet.write(j + 1, i + 1, balance_list[date][key])
                # elif info_type == INFO_TYPE.SOTCK_INFO:
                #     if post_proc == POST_PROCESS.DIVDE_MILLION:
                #         worksheet.write(j + 1, i + 1, balance_list[date][key] / 1000000)
                #     elif post_proc == POST_PROCESS.DIVDE_BILLION:
                #         worksheet.write(j + 1, i + 1, balance_list[date][key] / 1000000000)
                #     elif post_proc == POST_PROCESS.NONE:
                #         worksheet.write(j + 1, i + 1, balance_list[date][key])




        # print(stock_name, stmt_list, balance_list)

        # for date in stmt_list:
        #     stmt = stmt_list[date]
        #     balance = balance_list[date]
            
        #     print([(key, stmt[key] / 1000000) for key in PARSE_KEY])
        #     print([(key, balance[key]) for key in PARSE_KEY_2])


            # print([(key, stmt[key] / 1000000) for key in PARSE_KEY])
            # print([(key, balance[key]) for key in PARSE_KEY_2])


    # print("apple", )
    

    
    # worksheet.write(0, 0, 'Hello Excel')
    workbook.close()

    # with open("sample.json", "w") as outfile: 
    #     json.dump(apple.get_info(), outfile, indent = 4)
    
    return 

if __name__ == '__main__':
    main()