import ctypes
import marshal
import types

from . import wrap

cellnew = ctypes.pythonapi.PyCell_New
cellnew.restype = ctypes.py_object
cellnew.argtypes = (ctypes.py_object,)


def dumps(f, gen_globals=True):
    code = marshal.dumps(f.__code__)
    if f.__closure__:
        closure = [c.cell_contents for c in f.__closure__]
    else:
        closure = None
    if gen_globals:
        g = find_requires(f)
    else:
        g = {}
    return wrap.dumps((code, g, closure, f.__defaults__), False)


def loads(bytes, use_globals=False):
    code, g, closure, defaults = wrap.loads(bytes, True)
    g["__builtins__"] = __import__("__builtin__")
    if defaults:
        defaults = tuple(defaults)
    func_code = marshal.loads(code)
    if closure:
        closure = tuple(cellnew(c) for c in closure)
    f = types.FunctionType(func_code, g, closure=closure, argdefs=defaults)
    if not use_globals:
        for n, f0 in f.__globals__.items():
            if isinstance(f0, types.FunctionType):
                f.__globals__[n] = replace_globals(f0, f.__globals__)
        g[f.__name__] = f
    return f


def replace_globals(f, g):
    return types.FunctionType(f.__code__, g, f.__closure__, f.__defaults__)


def find_requires(f, ignores=None):
    if ignores is None:
        ignores = ["__builtins__", "__file__"]
    g = dict(f.__globals__)
    rs = find_requires_code(f.__code__, g, ignores)
    return {x: g[x] for x in rs if x in g}


def find_requires_code(code, g, ignores):
    requires = [name for name in code.co_names if name not in ignores and name != code.co_name]
    for item in code.co_consts:
        if isinstance(item, types.CodeType) and item not in ignores:
            requires += find_requires_code(item, g, ignores + requires + [code.co_name])
    i = 0
    while i < len(requires):
        item = requires[i]
        if item in g and isinstance(g[item], types.FunctionType):
            g.update(g[item].__globals__)
            for j in find_requires(g[item], list(ignores) + requires):
                if j not in requires:
                    requires.append(j)
        i += 1
    return requires
