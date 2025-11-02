import threading
import pickle
import json
from typing import Dict, Any


def exec_and_return(code: str, 
                    variable_name: str):
    '''
# Exec and return
Execute code and return result of {variable name}.
### Args:

- {code}: str - full code.
- {variable_name}: str - name of vatiable to return.

### Uasge:
Code:
```
simple_code = """
x = 10
y = 34
res = x + y
"""
print('result:', exec_and_return(simple_code, 'res'))
```
Output:
```
result: 34
```
    '''
    local_namespace = {}
    try:
        exec(code, globals(), local_namespace)
        return local_namespace.get(variable_name)
    except Exception as e:
        print(f"Error in code running: {e}")
        return None


class FramerError(Exception):
    def __init__(self, *args):
        super().__init__(*args)
class FrameError(Exception):
    def __init__(self, *args):
        super().__init__(*args)


class Framer():
    '''
# Framer

Main context manager class: Framer.

For system.
    '''
    def __init__(self):
        self._code = []
        self._vars = {}
        self._aliases = {}
        self._lock = threading.RLock()
    
    def var(self, name:str, value):
        self._vars[name] = value
        return self

    def op(self, a, b, 
           operator: str = '+'):
        result_var = f'__tmp_{len(self._code)}'
        res = f'{a} {operator} {b}'
        code_line = f'{result_var} = {res}'
        self._code.append(code_line)
        return result_var
    
    def execute(self):
        final_code = "\n".join(self._code)
        local_scope = self._vars.copy()
        compiled = compile(final_code, '<string>', 'exec')
        exec(compiled, {}, local_scope)
        return local_scope.get(f"__tmp_{len(self._code)-1}") 
    
    def get_thread_safe(self, name):
        with self._lock:
            return self._vars.get(self._aliases[name])
    
    def _new_code_line(self, line: str): self._code.append(line)

    def __enter__(self):
        System.last_framer = System.framer
        System.framer = self
        return self
    def __exit__(self, *args, **kwargs): pass


class System:
    '''
# System

System context class: System.

Has main [{framer}: Framer], [{last_framer}: Framer] and [{framers}: dict] self parameters.

For system.'''
    framer: Framer = Framer()
    last_framer: Framer = framer
    framers: dict = {'basic': Framer(), 'temp': Framer()}
    def match(condition: str, 
              true_block: str, 
              false_block: str = None, 
              framer: Framer | None = None):
        framer = System.framer if framer == None else framer
        cache = len(framer._code)+len(System.framers)
        Var(f'__condition_temp{cache}', condition, with_eval=True, framer=framer)
        framer._new_code_line(f'if __condition_temp{cache}:')
        new_true_block = ''
        for i in true_block.split('\n'):
            if i.strip() != '': new_true_block += '\n    ' + i
        framer._new_code_line(f'    {new_true_block}')
        if false_block:
            framer._new_code_line('else:')
            new_false_block = ''
            for i in false_block.split('\n'):
                if i.strip() != '': new_false_block += '\n    ' + i
            framer._new_code_line(f'    {new_false_block}')
    def to_last():
        s = System.framer
        System.framer = System.last_framer
        System.last_framer = s
class Var:
    '''
# Variable

Abstraction api class for [Framer] and [System].

### Args:

- {name}: str - name of variable.
- {value}: Any - value of variable.
- {type}: str - type hint for debug in code.
- {to_repr}: bool - if true, value in variable will be repr(value).
- {with_eval}: bool - if true, value in variable will be ```f'eval({repr(value)})'```.
- {framer}: Framer | None - Framer object.


### Example: 
```
ctx = Framer() # creating context
Var('x', 10, framer = ctx) # setting variable
```
'''
    def __init__(self, 
                 name: str, 
                 value, 
                 type: str = 'int', 
                 to_repr: bool = True, 
                 with_eval: bool = False,
                 framer: Framer | None = None):
        framer = System.framer if framer == None else framer
        param_name = f'__tmp_{len(framer._code)}'
        self.name = param_name
        self.value = value
        to_repr = True if with_eval else to_repr
        val = repr(value) if to_repr else value
        val = f'eval({val})' if with_eval else val
        with framer._lock:
            framer.var(param_name, value)
            framer._new_code_line(f'{name}: {type} = {val}')
            framer._aliases[name] = param_name
def Get(name: str, 
        framer: Framer | None = None):
    '''Get variable by {name} from {framer} method.'''
    framer: Framer = System.framer if framer == None else framer
    return framer.get_thread_safe(name)
class Return:
    '''
# Return
 
Method to set variable to return with Exec() method.

### Args: 
- {value}: Var - Variable for return (object).
- {framer}: Framer | None - Framer object.

### Example: 
Code:
```
with Frame() as f: # creating context
    # setting variables
    x = Var('x', 10)
    y = Var('y', 50)
    res = Var('test', Get('x') * Get('y')) 
    Return(res) # setting variable to return
print('result:', Exec()) # executing code
```
Output:
```
result: 500
```'''
    def __init__(self, 
                 value: Var, 
                 framer: Framer | None = None):
        framer = System.framer if framer == None else framer
        try: framer.var(f'__tmp_{len(framer._code) - 1}', f'{framer._vars.get(value.name)}')
        except AttributeError:
            raise FramerError(f'Exception in atribute parsing. \nObject [{value}, {type(value)}] has no atribute .name to create return. \nPlease, use [value] declaration like [`res = Var(...); Return(res, ...)`].')
class Code:
    '''
# Code append

Method to append code in Framer.

### Args:
- {code}: str - code for paste to framer.
- {framer}: Framer | None - framer object.

### Example:
Code:
```
with Frame() as f:
    x = Var('x', 10)
    y = Var('y', 50)
    Code('result = x + y')
    Var('test', Get('x') * Get('y')) 
    Var('res', 'test + result', with_eval=True)
print('result:', exec_and_return(f.compile(), 'res'))
```
Output:
```
result: 560
```'''
    def __init__(self, 
                 code: str, 
                 framer: Framer | None = None):
        framer = System.framer if framer == None else framer
        framer._new_code_line(code)
        self._code = code
def Exec(framer = None):
    '''
Execution of [Frame] method.
    '''
    framer = System.framer if framer == None else framer
    with framer._lock:
        return framer.execute()
    
class Frame:
    '''
# Frame
Abstraction api for all [Framer] and [System] methods.

(framer in functions is Frame.framer)

You can use with to create context, and call [Frame] object like `ctx()` to get framer.

### Args of initialization:
- {framer}: str | Framer = 'new' - framer context object for frame.
- {safemode}: bool - if safemode true, Exec method will be is not available.
- {name}: str - framer name in [System.framers]
- {save_while_exit}: bool - if true, while will be called [__exit__], context will be automaticly saved.
- {save_args}: list - list of args [name, format] for method save.

### Example usage:
Code:
```
with Frame(safemode=False) as f:
    f.Var('x', 10)
    f.Var('y', 50)
    System.match('x > y', 'print("x bigger")', 'print("y bigger")')
    f.Var('test', Get('x') * Get('y')) 
code = f.compile()
print('result:', exec_and_return(code, 'test'))
```
Output:
```
y bigger
result: 500
```'''
    def __init__(self, 
                 framer: str | Framer = 'new', 
                 safemode: bool = True, 
                 name: str = 'f1',
                 save_while_exit: bool = False,
                 save_args: list = ['ctx', 'pickle']):
        self.__saving = [save_while_exit, save_args]
        self.framer = Framer() if framer == 'new' else framer
        self.__safemode = safemode
        self._name = name
        System.framers[name] = self.framer
    def Sys(self) -> System: 
        '''Return [System] class.'''
        return System
    def Var(self, 
            name: str, 
            value, 
            type: str = 'int', 
            to_repr: bool = True,
            with_eval: bool = False) -> Var:
        '''Creating variable.'''
        return Var(name, value, type, to_repr, with_eval, self.framer)
    def Get(self, name: str) -> Any: 
        '''Get variable by name.'''
        return Get(name, self.framer)
    def Return(self, name: Var) -> Return: 
        '''Set of variable to return.'''
        return Return(name, self.framer)
    def Code(self, code: str) -> Code:
        '''Append code to frame.'''
        return Code(code, self.framer)
    def Exec(self) -> Any:
        '''Executing code of frame.'''
        if not self.__safemode: return Exec(self.framer)
        else: raise FrameError('Exec is not avialable in safemode.')
    def compile(self) -> str: 
        '''Get full code of frame.'''
        return '\n'.join(self.framer._code)
    def reset(self) -> Frame: 
        '''Recreate framer.'''
        self.framer = Framer()
        return self
    def save(self, filename: str, format: str = 'pickle') -> Frame:
        '''
        ## Saving frame to file.
        ### Args:
            {filename}: str - file name
            {format}: str - saving format ('pickle' or 'json')
        '''
        data = {
            'framer': {
                '_code': self.framer._code,
                '_vars': self.framer._vars,
                '_aliases': self.framer._aliases
            },
            'saving': self.__saving,
            'safemode': self.__safemode,
            'name': self._name
        }
        try:
            if format == 'pickle':
                with open(filename, 'wb') as f: pickle.dump(data, f)
            elif format == 'json':
                json_data = {
                    'framer': {
                        '_code': data['framer']['_code'],
                        '_vars': {k: str(v) for k, v in data['framer']['_vars'].items()},  # Приводим к строке для JSON
                        '_aliases': data['framer']['_aliases']
                    },
                    'safemode': data['safemode'],
                    'saving': data['saving'],
                    'name': data['name']
                }
                with open(filename, 'w', encoding='utf-8') as f: 
                    json.dump(json_data, f, indent=2, ensure_ascii=False)
            else: raise FrameError(f"Unsupported format: {format}")
            return self
        except Exception as e:
            raise FrameError(f"Save failed: {e}")

    def load(self, filename: str = 'ctx', format: str = 'pickle') -> Frame:
        '''
        ## Loading frame from file.
        ### Args:
            {filename}: str - file name
            {format}: str - loading format ('pickle' or 'json')
        '''
        try:
            if format == 'pickle':
                with open(filename, 'rb') as f: data = pickle.load(f)
            elif format == 'json':
                with open(filename, 'r', encoding='utf-8') as f: data = json.load(f)
                restored_vars = {}
                for k, v in data['framer']['_vars'].items():
                    try: restored_vars[k] = eval(v)
                    except: restored_vars[k] = v
                data['framer']['_vars'] = restored_vars
            else: raise FrameError(f"Unsupported format: {format}")
            self.framer._code = data['framer']['_code']
            self.framer._vars = data['framer']['_vars'] 
            self.framer._aliases = data['framer']['_aliases']
            self.__safemode = data['safemode']
            self.__saving = data['saving']
            self._name = data['name']
            return self
        except Exception as e:
            raise FrameError(f"Load failed: {e}")
    def _get_safemode(self): return self.__safemode
    def __enter__(self): 
        self.framer.__enter__()
        return self
    def __exit__(self, *args, **kwargs): 
        if self.__saving[0]: self.save(*self.__saving[1])
    def __call__(self, *args, **kwds):
        return self.framer



Var('name', 'frame', framer=System.framers['basic'])

if __name__ == '__main__':
    with Frame() as f:
        x = Var('x', 10)
        y = Var('y', 50)
        System.match('x > y', 'print("x bigger")', 'print("y bigger")')
        res = Var('test', Get('x') * Get('y')) 
        Return(res)  
    print(Exec())  # → 500
    with Frame() as f:
        x = Var('x', 10)
        y = Var('y', 50)
        res = Var('res', 'x + y', with_eval=True)
        Return(res)
    print(Exec())
    code = f.compile()
    print(exec_and_return(code, 'res')) # 60
    with Frame() as f:
        x = Var('x', 10)
        y = Var('y', 50)
        Code('result = x + y')
        Var('test', Get('x') * Get('y')) 
        Var('res', 'test + result', with_eval=True)
    print(exec_and_return(f.compile(), 'res')) # 560

    with Frame(save_while_exit=True, save_args=['ctx.json', 'json']) as f:
        f.Var('x', 10)
        f.Var('y', 50)
        System.match('x > y', 'print("x bigger")', 'print("y bigger")')
        f.Var('test', Get('x') * Get('y')) 
    with Frame().load('ctx.json', format='json') as f:
        code = f.compile()
        print('result:', exec_and_return(code, 'test'))
    '''
    y bigger
    500
    x + y
    60
    560
    y bigger
    result: 500
    '''
