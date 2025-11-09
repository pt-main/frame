from frame import *

with Framer() as f: # creating new framer
    fVar('y', 23)
    res = fVar('x', 10 + fGet('y'))
    fReturn(res)
print(fExec())
# framer is *GLOBAL*



x = fGet('name', fSys.framers['basic'])
print(x)


# example

cntx = Framer()
def test():
    result = (10 + 28 + 64 ** 2) << 2
    fVar('res', result, framer=cntx)
test()
print(fGet('res', cntx)) # 16536

@framing(return_frame=True)
def test():
    print('test')
    return 10
res_frame = fGet('frame', fSys.framers['temp'])
print(test(), res_frame)
print(fGet('res', res_frame))



# production example
cntx = Framer() # context
fVar('data', 10, framer=cntx)
@framing(cntx, 'tmp')
def test(k: int):
    return fGet('data', cntx) << k
print(framing_result(cntx, test, 'tmp', 3))



# ========== else example ==========


import frame as f




cntx = f.Framer() # context
f.fVar('inp', int(input('Input start number: ')), framer=cntx)
f.fVar('k', 156, framer=cntx)

sgc = f.Framer() # superglobal context
f.fVar('inp', f.fGet('inp', cntx), framer=sgc)
f.fVar('k', f.fGet('k', cntx), framer=sgc)

def bytest0():
    return abs(f.fGet('tmp_k', sgc) + f.fGet('inp', sgc))

@f.framing(sgc)
def bytest1(k: int):
    f.fVar('tmp_k', k, framer=sgc)
    return f.fGet('inp', sgc) << bytest0()
res = f.framing_result(sgc, bytest1, 'res', f.fGet('k', sgc))
print(res)



# or just
sgc = f.Frame()
sgc.Var('inp', f.fGet('inp', cntx))

def bytest0():
    return abs(sgc.Get('tmp_k') + sgc.Get('inp'))

@f.framing(sgc())
def bytest1(k: int):
    sgc.Var('tmp_k', k)
    return sgc.Get('inp') << bytest0()
res = f.framing_result(sgc, bytest1, 'res', f.fGet('k', cntx))
print(res)

# <- so clean!



# vanila python ->

inp = f.fGet('inp', cntx)
tmp_k = 0
k = f.fGet('k', cntx)
def bytest0():
    return tmp_k + inp
def bytest1(k: int):
    global tmp_k
    tmp_k = k
    return inp << bytest0()
# looks bad & not incrasement
print(bytest1(k))

print('some =========')

with Frame(safemode=False, save_while_exit=True, save_args=['ctx.json', 'json']) as f:
    m = PluginRegistry.get_plugin('math', f).include()
    f.Var('x', 3)
    f.Var('y', 56)
    true = '''
print("x bigger")
print(f'x = {x}')
print(f'y = {y}')
'''
    false = '''
print("y bigger")
print(f'x = {x}')
print(f'y = {y}')
'''
    f.Sys().match('x > y', true, false)
    f.Var('test', f.Get('x') * f.Get('y')) 
    fVar('z', 3.14)
    fVar('k', 0.4567897086543678965)
    fVar('test3', '(k + (test / z)) ** k', with_eval=True)
    fVar('test2', 'test3 + (((test ** z) - (y << x)) ** k)', with_eval=True)
    fCode('print("====")')
    m.sqrt('test2').relu('res').parabola('res').discriminant(2, 89, 6, 'res4').discriminant(2, 64, 15, 'res5')
    fCode('print("====")')
    code = '''
try: result = (x + y + test + z + k + test3 + test2 + sum(res4)) ** (res5[0] * res5[1])
except Exception as e: raise ValueError(f'1-{x}, 2-{y}, 3-{test}, 4-{z}, 5-{k}, 6-{test2}, 7-{test2}, 8-{sum(res4)}, 9-{sum(res5)} 10-{res4}, 11-{res5}, Err: {e}')
'''
    f.Code(code)
    fCode('print("====")')
    fVar('res', 'result ** k + res', with_eval=True)
    fCode('print(res)')
    fVar('test', 10, 'const')
with Frame().load('ctx.json', 'json') as f:
    code = f.compile()
    res = exec_and_return(code, 'res', locals(), globals())
    print('result:', res)
    save_code_to_bin()
    fVar('test', 10, 'const')


'''
33
frame
16536
test
10 <frame.frame_core.frames.Framer object at 0x110a916d0>
10
80
Input start number: 5
14615016373309029182036848327162830196559325429760
14615016373309029182036848327162830196559325429760
14615016373309029182036848327162830196559325429760
some =========
1
y bigger
x = 3
y = 56
====
====
====
44369621299267.914
result: 44369621299267.914
1
2
Traceback (most recent call last):
  File "/Users/macbook/Desktop/Frame/tests/test_arch.py", line 147, in <module>
  File "/Users/macbook/Desktop/Frame/frame/frame_core/frames.py", line 178, in __init__
    raise VariableTypeError(f'Variable already declared with type [{type}]. It cannot be overwritten.')
frame.frame_core.exceptions.VariableTypeError: Variable already declared with type [const]. It cannot be overwritten.
'''
