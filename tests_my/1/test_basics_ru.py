from frame import *

if __name__ == '__main__':
    filename = 'fc'
    format = 'json'
    filepath = f'{filename}.{format}'
    with FramesComposer(safemode=False) as fc:
        fc['test1'] = Frame(safemode=False)
        fc['test2'] = Frame(safemode=False)
        @fc['test2'].register()
        def test():
            return 'compleate'
        with fc['test2'] as f:
            f.Var('x', 10)
            f.Var('y', 50)
            fOp.match('x > y', 'print("x bigger")', 'print("y bigger")')
            f.Var('test', f.Get('x') * f.Get('y')) 
            @f.register()
            def test(): 
                print('testing')
            @f.register()
            class Test():
                hello = 'World'
                pass
        @fc['test1'].register()
        def test():
            return 'compleate'
        mfc = MathPlugin(fc['test1']).include()
        mfc.discriminant(10, 20, 30)
        mfc.discriminant(20, 20, 80)
        fc.sync('test1', '$')
        fc.sync('test2', '$')
        fc.save(filepath, format)
    with FramesComposer.from_file(filepath, format) as fc:
        fc.deploy('test.py', filepath, format)