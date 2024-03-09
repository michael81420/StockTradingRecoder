import yfinance as yf
import xlsxwriter
import yaml
from enum import Enum, auto
import numpy as np

CONFIG_YAML_PATH = "./config.yaml"
DEFAULT_SUMMARY = [
    ("shortName",           "Name"),
    ("trailingPE",          "Trailing P/E"),
    ("forwardPE",           "Forward P/E"),
    ("pegRatio",    "PEG Ratio"),
]

class FINANICAL_GROUP_TYPE(Enum):
    INCOME_STATEMENT = auto()
    BALANCE_SHEET = auto()
    CASH_FLOW = auto()
    SOTCK_INFO = auto()

class POST_PROCESS_TYPE(Enum):
    NONE = auto()
    DIVDE_MILLION = auto()
    DIVDE_BILLION = auto()

    def do4int(cls, input : int) -> int:
        if np.isnan(input):
            return "Nan"
        
        if cls == POST_PROCESS_TYPE.DIVDE_MILLION:
            return input / 1000000
        elif cls == POST_PROCESS_TYPE.DIVDE_BILLION:
            return input / 1000000000
        elif cls == POST_PROCESS_TYPE.NONE:
            return input
        else:
            raise ValueError('Unexpected POST_PROCESS_TYPE enum')
    
    def do4str(cls, input : str) -> str:
        if cls == POST_PROCESS_TYPE.DIVDE_MILLION:
            return input + " (M)"
        elif cls == POST_PROCESS_TYPE.DIVDE_BILLION:
            return input + " (B)"
        elif cls == POST_PROCESS_TYPE.NONE:
            return input
        else:
            raise ValueError('Unexpected POST_PROCESS_TYPE enum')

class ReportMgr:
    def __init__(self, stocks) -> None:
        with open(CONFIG_YAML_PATH, 'r') as f:
            self.config = yaml.safe_load(f)
        self.tickers = yf.Tickers(" ".join(stocks))
        
        # parse config 
        for i, (key, finanical_group, post_proc) in enumerate(self.config['FINANICAL_KEY']):
            finanical_group_enum = FINANICAL_GROUP_TYPE[finanical_group]
            post_proc_enum = POST_PROCESS_TYPE[post_proc]
            self.config['FINANICAL_KEY'][i] = (key, finanical_group_enum, post_proc_enum)

    def write_report_to_excel(self) -> bool:
        workbook  = xlsxwriter.Workbook('report.xlsx')

        for stock_name in self.tickers.tickers.keys():
            tk = self.tickers.tickers[stock_name]
            
            stmt_history = tk.get_income_stmt(as_dict=True)
            balance_history = tk.get_balancesheet(as_dict=True)
            cash_flow_history = tk.get_cash_flow(as_dict=True)
            history_dates = stmt_history.keys()

            worksheet = workbook.add_worksheet(stock_name)

            worksheet.set_column(0, 0, 40)
            default_gap = len(DEFAULT_SUMMARY) + 2

            title_format = workbook.add_format({'bold': True, 'font_name': 'Calibri', 'bg_color': 'gray', 'align': 'center'})
            cell_format = workbook.add_format({'font_name': 'Calibri'})

            # default summary info
            worksheet.merge_range(0, 0, 0, 1, "Summary", title_format)
            for i, (key, sheet_name) in enumerate(DEFAULT_SUMMARY):
                worksheet.write(i + 1, 0, sheet_name, cell_format)
                worksheet.write(i + 1, 1, tk.info.get(key, "N/A"), cell_format)

            # user optional history info
            worksheet.merge_range(default_gap, 0, default_gap, 4, "Finanical History", title_format)
            for i, (key, _, post_proc) in enumerate(self.config['FINANICAL_KEY']):
                worksheet.write(i + 2 + default_gap, 0, post_proc.do4str(key), cell_format)

            for i, date in enumerate(history_dates):
                worksheet.set_column(i + 2 + default_gap, i + 1, 15)
                worksheet.write(1 + default_gap, i + 1, date.strftime("%Y-%m-%d"), cell_format)
                for j, (key, info_type, post_proc) in enumerate(self.config['FINANICAL_KEY']):
                    if info_type == FINANICAL_GROUP_TYPE.INCOME_STATEMENT:
                        worksheet.write(j + 2 + default_gap, i + 1, post_proc.do4int(stmt_history[date][key]), cell_format)
                    elif info_type == FINANICAL_GROUP_TYPE.BALANCE_SHEET:
                        worksheet.write(j + 2 + default_gap, i + 1, post_proc.do4int(balance_history[date][key]), cell_format)
                    elif info_type == FINANICAL_GROUP_TYPE.CASH_FLOW:
                        worksheet.write(j + 2 + default_gap, i + 1, post_proc.do4int(cash_flow_history[date][key]), cell_format)
                    

        workbook.close()
        return True