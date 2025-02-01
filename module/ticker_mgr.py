import datetime
import logging
import yfinance as yf
from module.finance_key import FinanceKey, INFO_TYPE, POST_PROCESS
import statistics
DEFAULT_DISCOUNT_RATE = 0.1

class TickerMgr():
    def __init__(self, ticker : yf.Ticker) -> None:
        self._tk = ticker
        self._stmt_info = ticker.get_income_stmt(as_dict=True)
        self._balance_info = ticker.get_balancesheet(as_dict=True)
        self._cash_flow_info = ticker.get_cash_flow(as_dict=True)
        self._tk_info = ticker.get_info()
        self._dates = self._stmt_info.keys()

        dividends = self._tk.get_dividends()
        now_date = datetime.datetime.now()

        self._cur_year_dividend = 0
        self._past_1y_dividend = 0
        self._past_3y_dividend = 0
        self._past_5y_dividend = 0
        for date, dividend in dividends.items():
            if now_date - datetime.timedelta(days=365) <= date.to_pydatetime().replace(tzinfo=None):
                self._cur_year_dividend += dividend
            elif now_date - datetime.timedelta(days=730) < date.to_pydatetime().replace(tzinfo=None) and \
                 now_date - datetime.timedelta(days=365) > date.to_pydatetime().replace(tzinfo=None):
                self._past_1y_dividend += dividend
            elif now_date - datetime.timedelta(days=1461) < date.to_pydatetime().replace(tzinfo=None) and \
                 now_date - datetime.timedelta(days=1095) > date.to_pydatetime().replace(tzinfo=None):
                self._past_3y_dividend += dividend
            elif now_date - datetime.timedelta(days=2191) < date.to_pydatetime().replace(tzinfo=None) and \
                 now_date - datetime.timedelta(days=1826) > date.to_pydatetime().replace(tzinfo=None):
                self._past_5y_dividend += dividend
        
        self._estimate_grow_rate = statistics.mean([
            ((self._cur_year_dividend / self._past_1y_dividend) - 1) if self._past_1y_dividend != 0 else 0, \
            ((self._cur_year_dividend / self._past_3y_dividend) ** (1/3) - 1) if self._past_3y_dividend != 0 else 0, \
            ((self._cur_year_dividend / self._past_5y_dividend) ** (1/5) - 1) if self._past_5y_dividend != 0 else 0])
        self._estimate_discount_rate = DEFAULT_DISCOUNT_RATE
    
    @property
    def estimate_grow_rate(self):
        return self._estimate_grow_rate

    @property
    def estimate_discount_rate(self):
        return self._estimate_discount_rate
    
    @property
    def dates(self):
        return self._dates
    
    def do_post_proc(self, val : int, post_proc : POST_PROCESS) -> str:
        try:
            if post_proc == POST_PROCESS.DIVDE_BILLION:
                return str(val / 1000000000)
            elif post_proc == POST_PROCESS.DIVDE_MILLION:
                return str(val / 1000000)
            else:
                return str(val)
        except:
            logging.error(f"unexcept val({val})")
            return "N/A"

    def get_val(self, date: datetime, finance_key : FinanceKey):
        try:
            if finance_key.info_type == INFO_TYPE.INCOME_STATEMENT:
                return self.do_post_proc(self._stmt_info[date][finance_key.name], finance_key.post_proc)
            elif finance_key.info_type == INFO_TYPE.BALANCE_SHEET:
                return self.do_post_proc(self._balance_info[date][finance_key.name], finance_key.post_proc)
            elif finance_key.info_type == INFO_TYPE.CASH_FLOW:
                return self.do_post_proc(self._cash_flow_info[date][finance_key.name], finance_key.post_proc)
            elif finance_key.info_type == INFO_TYPE.SOTCK_INFO:
                return self.do_post_proc(self._tk_info[finance_key.name], finance_key.post_proc)
            else:
                logging.error(f"unexcept info_type({finance_key.info_type})")
                return "N/A"
        except:
            logging.error(f"unexcept finance_key({str(finance_key)})")
            return "N/A"

    def get_DDM_model_price(self) -> int:
        return self._cur_year_dividend * (1 + self._estimate_grow_rate) / (self._estimate_discount_rate - self._estimate_grow_rate)
