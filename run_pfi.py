
"""

==========================================
Deploy file [run_pfi.py] for fcomp by [None]
Version: None
Metadata:
    1  | deploy_time = 1763059908.745156
    2  | arch - dict 
    3  | by pt 
    4  | lines: 71

==========================================

"""

# fcirf - frames composotion iso runtime file
_fcirf_version_ = None
_fcirf_name_ = 'run_pfi.py'
_fcirf_author_ = None
_fcirf_dir_ = '/Users/macbook/Desktop/Frame'
_fcirf_deps_ = ['time']
_fcirf_fcomp_info_ = ['pfi.json', 'json']

# imports
from frame import *
import time

fcomp = FramesComposer.from_file(_fcirf_fcomp_info_[0], _fcirf_fcomp_info_[1])
sgc = fcomp.superglobal

string = "===== Welcome to PFI ====="
print(string); print('python frame idle, by pt.'); print('based by frame-fwl and using composer.'); print('=' * len(string))
time.sleep(1); exec_and_return(fcomp.superglobal().compile(), '', locals(), globals())
        