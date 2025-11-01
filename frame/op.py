import threading

__version__ = '0.2.5'



class FramerError(Exception):
    def __init__(self, *args):
        super().__init__(*args)


class Framer():
    def __init__(self):
        self._code = []
        self._vars = {}
        self._aliases = {}
    
    def var(self, name:str, value):
        self._vars[name] = value
        return self

    def op(self, a, b, operator: str = '+'):
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
    
    def _new_code_line(self, line: str): self._code.append(line)

    def __enter__(self):
        System.last_framer = System.framer
        System.framer = self
        return self
    def __exit__(self, *args, **kwargs): pass


class System:
    framer: Framer = Framer()
    last_framer: Framer = framer
    framers: dict = {'basic': Framer(), 'temp': Framer()}
    lock = threading.Lock()
    def match(condition: str, true_block: str, false_block: str = None, framer = None):
        framer = System.framer if framer == None else framer
        framer._new_code_line(f'if {condition}:')
        framer._new_code_line(f'    {true_block.replace("\n", "; ")}')
        if false_block:
            framer._new_code_line('else:')
            framer._new_code_line(f'    {false_block.replace("\n", "; ")}')
    def to_last():
        s = System.framer
        System.framer = System.last_framer
        System.last_framer = s
class Var:
    def __init__(self, name, value, type: str = 'int', to_repr: bool = True, framer = None):
        framer = System.framer if framer == None else framer
        param_name = f'__tmp_{len(framer._code)}'
        self.name = param_name
        self.value = value
        with System.lock:
            framer.var(param_name, value)
            framer._new_code_line(f'{name}: {type} = {repr(value) if to_repr else value}')
            framer._aliases[name] = param_name
def Get(name: str, framer = None):
    with System.lock:
        framer: Framer = System.framer if framer == None else framer
        return framer._vars.get(framer._aliases[name])
class Return:
    def __init__(self, value: Var, framer = None):
        framer = System.framer if framer == None else framer
        try: framer.var(f'__tmp_{len(framer._code) - 1}', f'{framer._vars.get(value.name)}')
        except AttributeError:
            raise FramerError(f'Exception in atribute parsing. \nObject [{value}, {type(value)}] has no atribute .name to create return. \nPlease, use [value] declaration like [`res = Var(...); Return(res, ...)`].')
class Code:
    def __init__(self, code: str, framer = None):
        framer = System.framer if framer == None else framer
        framer._new_code_line(code)
def Exec(framer = None):
    with System.lock:
        framer = System.framer if framer == None else framer
        return framer.execute()
    
class Frame:
    def __init__(self, framer: str | Framer = 'new', name: str = 'f1'):
        self.framer = Framer() if framer == 'new' else framer
        System.framers[name] = self.framer
    def Sys(self): 
        return System
    def Var(self, name, value, type: str = 'int', to_repr:bool = True):
        return Var(name, value, type, to_repr, self.framer)
    def Get(self, name: str): 
        return Get(name, self.framer)
    def Return(self, name: Var): 
        return Return(name, self.framer)
    def Code(self, code: str):
        return Code(code, self.framer)
    def Exec(self): 
        return Exec(self.framer)
    def __enter__(self): 
        self.framer.__enter__()
        return self
    def __exit__(self, *args, **kwargs): pass



Var('ver', __version__, framer=System.framers['basic'])

if __name__ == '__main__':
    with Frame() as f:
        x = Var('x', 10)
        y = Var('y', 50)
        System.match('x > y', 'print("x bigger")', 'print("y bigger")')
        res = Var('test', Get('x') * Get('y')) 
        Return(res)  
    print(Exec())  # → 500
