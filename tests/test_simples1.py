import frame.simple as s
import frame as f

with s.Frame() as test:
    code = test.compile()
    print(code)