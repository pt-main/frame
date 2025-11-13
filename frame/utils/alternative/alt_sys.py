'''
# Alternative system methods.\n
Custom methods:
    __version__() 
        - get python version.
    __has_module__(module) 
        - check module instalation.
    __ch[mode](args)
        - cache function. Modes: get/set. In 'get' args is empty, 
          in 'set' args is [data] - data for cache.
Custom params:
    __has_cython__ - check for cython available.
Edited:
    sys.version - to custom version name.
'''


# imports and configs
import builtins, sys

CYTHON_AVAILABLE = 1
try: import Cython
except ImportError: CYTHON_AVAILABLE = 0

builtins._cache_alternativemodule_env_ = 'NONE'



# our methods
def get_ver():
    ver = sys.version.split('.')[:3]
    ver = ver[:2] + [ver[2].split(' ')[0]]
    return '.'.join(ver) + '.E#Pt' # Edited # (by) Pt

def ver(): return sys.version

def has_module(module_name: str): 
    try: __import__(module_name); return True
    except ImportError: return False

def set_cache(data):
    global builtins
    builtins._cache_alternativemodule_env_ = data

def get_cache(): return builtins._cache_alternativemodule_env_



# ===================================================================
# editing builtins to replace standart (to) and add ours functions
# while user use that module - our modules was imported like defaults
# ===================================================================

builtins.__version__ = ver
sys.version = f'{get_ver()} - edited python by pt'
builtins.__has_cython__ = bool(CYTHON_AVAILABLE)
builtins.__has_module__ = has_module
builtins.__ch = {'get': get_cache, 'set': set_cache}
