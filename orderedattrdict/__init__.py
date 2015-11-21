'An ordered dictionary with attribute-style access.'

from collections import OrderedDict, Counter, defaultdict


class AttrDict(OrderedDict):
    '''
    AttrDict extends OrderedDict to provide attribute-style access.

    Items starting with __ or _OrderedDict__ can't be accessed as attributes.
    '''
    __exclude_keys__ = set()

    def __getattr__(self, name):
        'Getting ad.x gets ad["x"]'
        if (name.startswith('__') or name.startswith('_OrderedDict__') or
                name in self.__exclude_keys__):
            return super(AttrDict, self).__getattr__(name)
        else:
            try:
                return self[name]
            except KeyError:
                raise AttributeError(name)

    def __setattr__(self, name, value):
        'Setting ad.x sets ad["x"]'
        if (name.startswith('__') or name.startswith('_OrderedDict__') or
                name in self.__exclude_keys__):
            return super(AttrDict, self).__setattr__(name, value)
        self[name] = value

    def __delattr__(self, name):
        'Deleting ad.x deletes ad["x"]'
        if (name.startswith('__') or name.startswith('_OrderedDict__') or
                name in self.__exclude_keys__):
            return super(AttrDict, self).__delattr__(name)
        del self[name]


class CounterAttrDict(AttrDict, Counter):
    '''
    A Counter with ordered keys and attribute-style access
    '''
    def __init__(self, *args, **kwargs):
        AttrDict.__init__(self, *args, **kwargs)
        Counter.__init__(self)
        self.__exclude_keys__ |= {'most_common', 'elements', 'subtract'}


class DefaultAttrDict(AttrDict, defaultdict):
    '''
    A defaultdict with ordered keys and attribute-style access.
    '''
    def __init__(self, default_factory, *args, **kwargs):
        AttrDict.__init__(self, *args, **kwargs)
        defaultdict.__init__(self, default_factory)
        self.__exclude_keys__ |= {'default_factory', '_ipython_display_'}
