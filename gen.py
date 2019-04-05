'''
Generate byte code
'''
import marshal

data = None
with open("get_game_code.py", "r") as fh:
    data = fh.read()

obj = compile(data, "<string>", "exec", optimize=2)
with open("gen.dump", "wb") as fh:
    fh.write(marshal.dumps(obj))
