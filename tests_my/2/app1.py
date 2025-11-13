from frame import *
FILENAME = 'pfi.json'
deps = ['time']
with FramesComposer() as fc:
    @fc.superglobal().register()
    def calculate(expr: str): 
        res = eval(expr)
        print('Formula:', expr); print(f'Result: {res}'); print(expr, '=', res, '\n')
    for i in '''def main(): \n    try: \n        choise = input('IDLE or calc: ').lower(); print('\\n'*2) \n        if choise == 'calc': \n            while True: calculate(input('>>> ')) \n        else: \n            local_scope = locals(); global_scope = globals() \n            while True: exec(input('>>> '), global_scope, local_scope) \n    except KeyboardInterrupt: print('\\n>>> Exiting...'); time.sleep(1); return \nmain()'''.split('\n'): fc.superglobal().Code(i, False)
    fc.save(FILENAME).deploy('run_pfi.py', FILENAME, dependencies=deps, metadata=f'arch - dict \nby pt \nlines: {34+37}', main_code='''string = "===== Welcome to PFI ====="\nprint(string); print('python frame idle, by pt.'); print('based by frame-fwl and using composer.'); print('=' * len(string))\ntime.sleep(1); exec_and_return(fcomp.superglobal().compile(), '', locals(), globals())''')