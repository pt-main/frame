from abc import ABC
from .op import Frame, exec_and_return
import math, cmath, random

class PluginIsNotWorkingError(Exception):
    def __init__(self, *args):
        super().__init__(*args)

class PluginError(Exception):
    def __init__(self, *args):
        super().__init__(*args)


class PluginBase(ABC):
    def __init__(self, frame: Frame | None = None):
        self.frame = frame
        self._has_frame = isinstance(frame, Frame)
        super().__init__()
    def work(self):
        '''Main plugin method.'''
        raise PluginIsNotWorkingError
    def __call__(self, *args, **kwds):
        return self.frame


class MathPlugin(PluginBase):
    '''
    # Math Plugin
    Oficial math plugin for Frame's. 
    
    You have to run `include` method before using Plugin.
    
    Argument {framer}: Framer | None - frame context to using lib (only without safemode)'''
    def __init__(self, frame = None):
        super().__init__(frame)
        self._state = {'included': False, 'safemode': self.frame._get_safemode()}
        self._version = 'v0.1.1'
        self._counter = 0
    
    def include(self):
        if not self._state['included']:
            self.frame.Code(f'import math, cmath \n_math_plugin_ver = {repr(self._version)}')
            self._state['included'] = True
        return self
    
    def parabola(self, x: int | float, 
                 name_of_result_variable: str = 'res', 
                 returning: str = 'frame'): 
        '{returning} - frame / Code'
        return self._operand(x, name_of_result_variable, returning, op='$ ** 2')
    
    def sqrt(self, x: int | float, 
             name_of_result_variable: str = 'res', 
             returning: str = 'frame'): 
        '{returning} - frame / Code'
        return self._operand(x, name_of_result_variable, returning, op='math.sqrt($)')
    
    def relu(self, x: int | float, 
             name_of_result_variable: str = 'res', 
             returning: str = 'frame'):
        '{returning} - frame / Code'
        return self._operand(x, name_of_result_variable, returning, op='1 if abs($) != $ else $')
    
    def discriminant(self, a: int | float, b: int | float, c: int | float, 
                     name_of_result_variable: str = 'res', 
                     returning: str = 'frame') -> 'Frame.Code' | MathPlugin:
        '{returning} - frame / Code. \n\nValue of {name_of_result_variable} in code will be list[x1, x2, discriminant].'
        cache = self._cache()
        self.frame.Var(f'__temp_a_math{cache}', a)
        self.frame.Var(f'__temp_b_math{cache}', b)
        self.frame.Var(f'__temp_c_math{cache}', c)
        code = f'''
if __temp_a_math{cache} == 0: raise ValueError
__temp_D_math{cache} = (__temp_b_math{cache} ** 2) - (4 * __temp_a_math{cache} * __temp_c_math{cache})
if __temp_D_math{cache} >= 0: __temp_sqrt_D_math{cache} = math.sqrt(__temp_D_math{cache})
else: __temp_sqrt_D_math{cache} = cmath.sqrt(__temp_D_math{cache})
__temp_x1_math{cache} = (-__temp_b_math{cache} + __temp_sqrt_D_math{cache}) / (2 * __temp_a_math{cache})
__temp_x2_math{cache} = (-__temp_b_math{cache} - __temp_sqrt_D_math{cache}) / (2 * __temp_a_math{cache})
{name_of_result_variable} = [__temp_x1_math{cache}, __temp_x2_math{cache}, __temp_D_math{cache}]
'''
        code = self.frame.Code(code)
        if returning == 'code': return code
        return self

    def _check(self):
        if not self._state['included']: raise PluginError("Use include method before using operations. \nUse 'plugin.include()'' (example) for include lib.")
        if self._state['safemode']: raise PluginError('Your frame in safemode. \nMath operations works only without safemode: code execution must be available.')
    
    def _cache(self): self._counter += 1; return self._counter

    def _operand(self, x: int | float, 
                 name_of_result_variable: str = 'res', 
                 returning: str = 'frame', 
                 op: str = '$') -> 'Frame.Code' | MathPlugin:
        self._check()
        cache = self._cache()
        temp_name = f'__x_temp_{name_of_result_variable}_math{cache}'
        self.frame.Var(temp_name, f'{x}', with_eval=True)
        code = self.frame.Code(f'{name_of_result_variable} = {op.replace("$", f"({temp_name})")}')
        if returning.lower() == 'code':
            return code
        return self
    
    def work(self):
        return f'mathplugin <{self._version}>'


if __name__ == '__main__':
    with Frame(safemode=False) as test:
        m = MathPlugin(test).include()
        m.sqrt(3.14).parabola(3.14, 'res1').relu(10, 'res2').relu(-10, 'res3').discriminant(2, 89, 6, 'res4')
        m().Var('result', 'res + res1 + res2 + res3 + res4[-1]', with_eval=True)
        code = test.compile()
        print(code)
        print(exec_and_return(code, 'result'))
