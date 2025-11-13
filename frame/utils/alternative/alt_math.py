'''
# Alternative math. 
'''


# imports and settings for int and float
import ctypes, sys, builtins, abc
from decimal import Decimal, getcontext

getcontext().prec = 500000
sys.set_int_max_str_digits(500000)



# our methods
def superlarge(x):
    '''creating large integrer from [x]'''
    res = x
    for i in range(x): res **= (i if i != 0 else 1) 
    return res

def supersmall(x):
    '''creating small float from [x]'''
    res = x
    for i in range(x+x): res *= eval(f'0.{i}' if i != 0 else '1')
    return res

def re_pow(x):
    '''creating alternative 'power' operations to create float from [x]. like 'normalization'.'''
    res = x
    for i in range(x+x): 
        evaled = eval(f'0.{i}' if i != 0 else '0')
        res -= evaled if res - evaled >= 0 else -evaled
    return res





# ===================================================================
# editing builtins to replace standart (to) and add ours functions
# while user use that module - our modules was imported like defaults
# ===================================================================

FLOAT = float

class nw_float(Decimal): # new float
    @classmethod
    def fromhex(cls, string: str) -> Decimal: 
        float_num = FLOAT.fromhex(string)
        return cls(float_num)
    @classmethod
    def hex(cls, float: FLOAT) -> str:
        return FLOAT.hex(FLOAT(float))
    @classmethod
    def is_integer(cls, number) -> bool:
        return FLOAT.is_integer(FLOAT(number))
        
builtins.float = nw_float

class cl_float(float):... # classic float
builtins.cl_float = cl_float

dFLOAT = float

def set_default_float(): 
    global builtins
    builtins.float = FLOAT

def set_decimal_float(): 
    global builtins
    builtins.float = dFLOAT

def set_alt_funcs():
    global builtins
    builtins.superlarge = superlarge
    builtins.supersmall = supersmall
    builtins.repow = re_pow

    builtins.dfl_float = set_default_float
    builtins.new_float = set_default_float

def replace_alt_funcs():
    import builtins as nbins
    global builtins
    builtins = bin

class alt_math(abc.ABC):
    @staticmethod
    def __enter__():
        set_decimal_float()
        set_alt_funcs()
    @staticmethod
    def __exit__(*args):
        set_default_float()
        replace_alt_funcs()

