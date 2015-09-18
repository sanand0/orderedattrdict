orderedattrdict
===============

.. image:: https://img.shields.io/travis/sanand0/orderedattrdict.svg
        :target: https://travis-ci.org/sanand0/orderedattrdict

.. image:: https://img.shields.io/pypi/v/orderedattrdict.svg
        :target: https://pypi.python.org/pypi/orderedattrdict


An ordered dictionary with attribute-style access.

Usage
-----

``AttrDict`` behaves exactly like ``collections.OrderedDict``, but also allows
keys to be accessed as attributes::

    >>> from orderedattrdict import AttrDict
    >>> conf = AttrDict()
    >>> conf['z'] = 1
    >>> assert conf.z == 1
    >>> conf.y = 2
    >>> assert conf['y'] == 2
    >>> conf.x = 3
    >>> assert conf.keys() == ['z', 'y', 'x']

**NOTE**: If the key clashes with an ``OrderedDict`` attribute or starts with
``__`` (two underscores), you can't access it as an attribute. For example::

    >>> a = AttrDict(keys=1)
    >>> a.keys
    <bound method AttrDict.keys of AttrDict([('keys', 1)])>
    >>> a['keys']
    1

Load JSON preserving the order of keys::

    >>> import json
    >>> data = json.load(open('test.json'), object_pairs_hook=AttrDict)

Load YAML preserving the order of keys::

    >>> import yaml
    >>> from orderedattrdict.yamlutils import AttrDictYAMLLoader
    >>> data = yaml.load(open('test.yaml'), Loader=AttrDictYAMLLoader)

Make PyYAML *always* load all dictionaries as ``AttrDict``::

    >>> from orderedattrdict.yamlutils import from_yaml
    >>> yaml.add_constructor(u'tag:yaml.org,2002:map', from_yaml)
    >>> yaml.add_constructor(u'tag:yaml.org,2002:omap', from_yaml)

``json.dump``, ``yaml.dump`` and ``yaml.safe_dump`` convert ``AttrDict`` into
dictionaries, retaining the order::

    >>> json.dumps(data)
    >>> yaml.dump(data)

You can subclass ``AttrDict`` with mixins for more functionality. Set the
``__exclude_keys__`` to exclude certain keys from attribute access. For example,
to implement a ``Counter`` that uses ``AttrDict``, create this class::

    >>> from collections import Counter
    >>> class CounterAttrDict(AttrDict, Counter):
    >>>     def __init__(self, *args, **kwargs):
    >>>         AttrDict.__init__(self, *args, **kwargs)
    >>>         Counter.__init__(self)
    >>>         self.__exclude_keys__ |= {'most_common', 'elements', 'subtract'}

This ``CounterAttrDict`` acts like a counter but with ordered keys via attribute
access. However, ``.most_common``, ``.elements`` and ``.subtract`` will not be
used as keys::

    >>> c = CounterAttrDict()
    >>> c.x
    0
    >>> c.elements
    <bound method CounterAttrDict.elements of CounterAttrDict()>
    >>> c.x += 1
    >>> c.y += 2
    >>> c.most_common()
    [('y', 2), ('x', 1)]
    >>> list(c.elements())
    ['x', 'y', 'y']
    >>> c.subtract(y=1)
    >>> c
    CounterAttrDict([('x', 1), ('y', 1)])

To create a ``defaultdict`` that is ordered and has attribute access, subclass
from ``AttrDict`` and ``defaultdict``::

    >>> from collections import defaultdict
    >>> class DefaultAttrDict(AttrDict, defaultdict):
    >>>     def __init__(self, default_factory, *args, **kwargs):
    >>>         AttrDict.__init__(self, *args, **kwargs)
    >>>         defaultdict.__init__(self, default_factory)
    >>>         self.__exclude_keys__ |= {'default_factory', '_ipython_display_'}

This can be used with a list factory::

    >>> d.x
    []
    >>> d.y.append(10)
    >>> d
    DefaultAttrDict([('x', []), ('y', [10])])

You can create a tree structure where you can set attributes in any level of the
hierarchy::

    >>> tree = lambda: DefaultAttrDict(tree)
    >>> node = tree()
    >>> node.x.y.z = 1
    >>> node
    DefaultAttrDict([('x', DefaultAttrDict([('y', DefaultAttrDict([('z', 1)]))]))])


Installation
------------

This is a pure-Python package built for Python 2.7+ and Python 3.0+. To set up::

    pip install orderedattrdict

Changelog
---------

- ``1.0``: Basic implementation
- ``1.1``: Add utilities to load and save as YAML
- ``1.2``: Allow specific keys to be excluded from attribute access
