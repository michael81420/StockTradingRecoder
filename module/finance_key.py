from enum import Enum, auto

class INFO_TYPE(Enum):
    INCOME_STATEMENT = auto()
    BALANCE_SHEET = auto()
    CASH_FLOW = auto()
    SOTCK_INFO = auto()

class POST_PROCESS(Enum):
    NONE = auto()
    DIVDE_MILLION = auto()
    DIVDE_BILLION = auto()

class FinanceKey():
    def __init__(self, name : str, info_type : INFO_TYPE, post_proc : POST_PROCESS = POST_PROCESS.NONE) -> None:
        self._name = name
        self._info_type = info_type
        self._post_proc = post_proc
    
    def __str__(self) -> str:
        return f"name: {self._name}, info_type: {self._info_type.value}, post_proc: {self._post_proc.value}"
    
    @property
    def info_type(self) -> INFO_TYPE:
        return self._info_type
        
    @property
    def post_proc(self) -> POST_PROCESS:
        return self._post_proc

    @property
    def name(self) -> str:
        return self._name
    
    def name_with_unit(self) -> str:
        if self._post_proc == POST_PROCESS.DIVDE_MILLION:
            return self._name + " (M)"
        elif self._post_proc == POST_PROCESS.DIVDE_BILLION:
            return self._name + " (B)"
        else:
            return self._name
    
    