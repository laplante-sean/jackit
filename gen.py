'''
Generate byte code
'''
import marshal

data = None
with open("submit_score.py", "r") as fh:
    data = fh.read()

obj = compile(data, "<string>", "exec", optimize=2)
with open("gen.dump", "wb") as fh:
    fh.write(marshal.dumps(obj))

data = None
with open("level_complete.py", "r") as fh:
    data = fh.read()

obj = compile(data, "<string>", "exec", optimize=2)
with open("gen2.dump", "wb") as fh:
    fh.write(marshal.dumps(obj))

data = None
with open("validate.py", "r") as fh:
    data = fh.read()

obj = compile(data, "<string>", "exec", optimize=2)
with open("gen3.dump", "wb") as fh:
    fh.write(marshal.dumps(obj))