'''
# Frame
The Frame - multitool module for programming.

Functions: 
    Framer functions -
        Framer, fExec, fGet, fVar, fSys, fReturn, fCode, @frmaing, framing_result
        FramerError, FramingError
'''

from .op import __version__
from .op import (Framer, Frame, Exec as fExec, Get as fGet, Var as fVar, 
                System as fSys, Return as fReturn, Code as fCode,
                FramerError)


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
    if return_frame: fVar('frame', framer_obj, to_repr=False, framer=fSys.framers['temp'])
    return decorator



class FramingError(Exception):
    def __init__(self, *args):
        super().__init__(*args)
    
def framing_result(framer: Framer, func: object, name_of_result_variable: str = 'res', *func_args, **func_kwargs):
    '''
## Getting result from [@framing def ...] function
### Args:
- framer: object[Frame] -  framer to run.
- func: object - function for runing.
- name_of_result_variable: str - name_of_result_variable from decorator @framing.
- *args & **kwargs - arguments for [func] running.
### Example:
change 
```
# geting frame object from decorator
res_frame = fGet('frame', fSys.framers['temp'])
# runing 
print(test(), res_frame)
# geting result variable from decorator
print(fGet('res', res_frame))
```
to just
```
print(framing_result(fGet('frame', fSys.framers['temp']), test, 'res'))
```
    '''
    if isinstance(framer, Frame): framer = framer.framer
    resf = func(*func_args, **func_kwargs)
    resg = fGet(name_of_result_variable, framer)
    if resf != resg: raise FramingError(f'Variable [{name_of_result_variable}] is not found in Frame[{framer}].')
    return resg
