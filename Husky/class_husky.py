import types

from . import module_husky
from . import wrap

ignores = ["__weakref__", "__dict__"]

TYPE_NON_USERDEFINED = 0
TYPE_USERDEFINED = 1


def dumps(C):
    m = module_husky.loads(C.__module__)
    if not module_husky.is_userdefined(m):
        return wrap.dumps((TYPE_NON_USERDEFINED, C.__name__, m))
    else:
        dicts = {k: v for k, v in vars(C).items() if k not in ignores}
        return wrap.dumps((TYPE_USERDEFINED, C.__name__, C.__bases__, dicts))


def loads(bytes):
    s = wrap.loads(bytes)
    if s[0] == TYPE_NON_USERDEFINED:
        return vars(s[2])[s[1]]
    elif s[0] == TYPE_USERDEFINED:
        return types.TypeType(*s[1:])
