orderedattrdict
===============

An ordered dictionary with attribute-style access.

Usage
-----

`AttrDict` behaves exactly like `collections.OrderedDict`, but also allows keys
to be accessed as attributes.

    >>> from orderedattrdict import AttrDict
    >>> conf = AttrDict()
    >>> conf['z'] = 1
    >>> assert conf.z == 1
    >>> conf.y = 2
    >>> assert conf['y'] == 2
    >>> conf.x = 3
    >>> assert conf.keys() == ['z', 'y', 'x']

**NOTE**: If the key clashes with an AttrDict attribute, the key is not used.
This also applies if the key starts with `__` (two underscores). For example:

    >>> a = AttrDict(keys=1)
    >>> a.keys
    <bound method AttrDict.keys of AttrDict([('keys', 1)])>
    >>> a['keys']
    1

JSON files can be parsed using `AttrDict` as follows:

    >>> import json
    >>> data = json.load(open('file.json'), object_pairs_hook=AttrDict)

YAML files can be parsed using `AttrDict` as follows:

    >>> import yaml
    >>> from orderedattrdict import AttrDictYAMLLoader
    >>> data = yaml.load(open('file.yaml'), Loader=AttrDictYAMLLoader)

YAML files can be saved from AttrDict structures as follows:

    >>> from orderedattrdict import AttrDictYAMLDumper
    >>> yaml.dump(data, Dumper=AttrDictYAMLDumper)

Installation
------------

    pip install orderedattdict

This is a pure-Python package is build for Python 2.7+ and Python 3.0+.
