orderedattrdict
===============

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

**NOTE**: If the key clashes with an AttrDict attribute, the key is not used.
This also applies if the key starts with ``__`` (two underscores). For example::

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

Installation
------------

This is a pure-Python package is build for Python 2.7+ and Python 3.0+. Set it
up using::

    pip install orderedattdict
