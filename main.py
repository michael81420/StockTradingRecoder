import yfinance as yf
import logging
import json
import argparse
import xlsxwriter
from report_mgr import ReportMgr

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("-stock", "-s", nargs='+', help="stocks list")
    parser.add_argument("-debug", help="debug mode", action="store_true")
    args = parser.parse_args()

    if args.debug:
        logging.basicConfig(level=logging.DEBUG, format='%(relativeCreated)6d %(threadName)s %(message)s')
    else:
        logging.basicConfig(level=logging.INFO, format='%(relativeCreated)6d %(threadName)s %(message)s')

    report_mgr = ReportMgr(args.stock)
    report_mgr.write_report_to_excel()
    
    return 

if __name__ == '__main__':
    main()