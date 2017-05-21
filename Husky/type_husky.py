import types

from . import class_husky
from . import wrap

type_list = [
    type(None),
    type,
    bool,
    int,
    int,
    float,
    complex,
    bytes,
    str,
    tuple,
    list,
    dict,
    dict,
    types.FunctionType,
    types.LambdaType,
    types.GeneratorType,
    types.CodeType,
    type,
    types.InstanceType,
    types.MethodType,
    types.UnboundMethodType,
    types.BuiltinFunctionType,
    types.BuiltinMethodType,
    types.ModuleType,
    types.FileType,
    range,
    slice,
    type(Ellipsis),
    types.TracebackType,
    types.FrameType,
    memoryview,
    types.DictProxyType,
    type(NotImplemented),
    types.GetSetDescriptorType,
    types.MemberDescriptorType,
    str,
]


def dumps(t):
    if t in type_list:
        return wrap.dumps(type_list.index(t))
    else:
        return class_husky.dumps(t)


def loads(i):
    b = wrap.loads(i)
    if isinstance(b, int):
        return type_list[b]
    else:
        return class_husky.loads(i)
