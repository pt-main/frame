'''
# Frame
The Frame - multitool module for programming.
Functions: 
    Framer functions -
        Framer, fExec, fGet, fVar, fSys, fReturn, fCode, @frmaing, framing_result
        FramerError, FramingError
'''
from frame.op import __version__

from frame.op import (Framer, Exec as fExec, Get as fGet, Var as fVar, System as fSys, Return as fReturn, Code as fCode)



def framing(
    framer: str | Framer = 'new',
    name_of_result_variable: str = 'res',
    return_frame: bool = False
    ):
    '''
## Frame decorator
### Args: 
arg {framer}:  object[Frame] | str = 'new' -

- Frame to load {name_of_result_variable}. 
- If == 'new', will be created new frame.
    
arg {name_of_result_variable}:  str = 'res' -
- Variable that will be created in {framer}.
    
arg {return_frame}:  bool = False -
- Args for choise create 'frame' variable (Frame object) in System.frames['temp'] .
### Example:
```
@frame_dec(return_frame=True)
def test():
    print('test')
    return 10
# geting frame object from decorator
res_frame = fGet('frame', fSys.framers['temp']) 
print(test(), res_frame)
# geting result variable from decorator
print(fGet('res', res_frame))
```
- Output:
```
10 <frame.op.Framer object at 0x10ddf3d10>
10
```
    '''
    if framer == 'new': framer_obj = Framer()
    else: framer_obj = framer
    def decorator(func):
        def wrapper(*args, **kwargs):
            res = func(*args, **kwargs)
            fVar(name_of_result_variable, res, framer=framer_obj)
            return res
        return wrapper
    if return_frame:
        fVar('frame', framer_obj, to_repr=False, framer=fSys.framers['temp'])
        return decorator
    else:
        return decorator
    



from frame.op import FramerError
class FramingError(Exception):
    def __init__(self, *args):
        super().__init__(*args)
    
def framing_result(framer: Framer, func: object, name_of_result_variable: str = 'res', *func_args, **func_kwargs):
    '''
    ## Getting result from [@framing def ...] function
    ### Args:
    - '''
    resf = func(*func_args, **func_kwargs)
    resg = fGet(name_of_result_variable, framer)
    if resf != resg: raise FramingError(f'Variable [{name_of_result_variable}] is not found in Frame[{framer}].')
    return resg