import pickle as pickle
import struct
import types

from . import dict_husky
from . import function_husky
from . import instance_husky
from . import iterable_husky
from . import module_husky
from . import type_husky

dispatches = [
    (type(None), pickle),
    (bool, pickle),
    (int, pickle),
    (int, pickle),
    (float, pickle),
    (bytes, pickle),
    (complex, pickle),
    (str, pickle),
    (types.BuiltinFunctionType, pickle),
    (range, pickle),
    (tuple, iterable_husky),
    (list, iterable_husky),
    (types.GeneratorType, instance_husky),
    (dict, dict_husky),
    (dict, dict_husky),
    (types.FunctionType, function_husky),
    (types.LambdaType, function_husky),
    (types.ModuleType, module_husky),
    (type, type_husky),
    (object, pickle)
    # (object,                    instance_husky)
]

containers = [function_husky, dict_husky, iterable_husky]


def tag(s, t):
    return struct.pack(">c", chr(dispatches.index(t))) + s


def untag(s):
    return ord(struct.unpack(">c", s)[0])


def dumps(d, gen_globals=True):
    for item in dispatches:
        if isinstance(d, item[0]):
            if item[1] in containers:
                return tag(item[1].dumps(d, gen_globals), item)
            else:
                return tag(item[1].dumps(d), item)
    return None


def loads(s, use_globals=False):
    t, m = dispatches[untag(s[0])]
    if m in containers:
        f = m.loads(s[1:], use_globals)
    else:
        f = m.loads(s[1:])
    if not isinstance(f, t):
        f = t(f)
    return f


if __name__ == '__main__':
    v = {1: [1, 2, 3], "v": None}
    b = dumps(v)
    print(repr(b))
    v1 = loads(b)
    print(v1)
