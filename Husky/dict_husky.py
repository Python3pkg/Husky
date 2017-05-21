import pickle as pickle

from . import wrap


def dumps(variable, gen_globals=True):
    return pickle.dumps({wrap.dumps(k, gen_globals): wrap.dumps(v, gen_globals) for k, v in variable.items()})


def loads(bytes, use_globals=False):
    return {wrap.loads(k, use_globals): wrap.loads(v, use_globals) for k, v in pickle.loads(bytes).items()}
