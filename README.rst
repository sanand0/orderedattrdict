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

CounterAttrDict
---------------

``CounterAttrDict`` provides a Counter with ordered keys and attribute-style
access::

    >>> from orderedattrdict import CounterAttrDict
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

DefaultAttrDict
---------------

``DefaultAttrDict`` provides a defaultdict with ordered keys and attribute-style
access. This can be used with a list factory to collect items::

    >>> from orderedattrdict import DefaultDict
    >>> d = DefaultAttrDict(list)
    >>> d.x.append(10)  # Append item without needing to initialise list
    >>> d.x.append(20)
    >>> sum(d.x)
    30

or with a set to collect unique items::

    >>> d = DefaultAttrDict(set)
    >>> d.x.add(5)
    >>> d.x.add(2)
    >>> d.x.add(5)      # Duplicate item is ignored
    >>> sum(d.x)
    7

Tree
----

``Tree`` lets you can set attributes in any level of the hierarchy::

    >>> node = Tree()
    >>> node
    Tree()
    >>> node.x.y = 1
    >>> node
    Tree([('x', Tree([('y', 1)]))])
    >>> node.x.z = 2
    >>> node
    Tree([('x', Tree([('y', 1), ('z', 2)]))])
    >>> node.y.a.b = 3
    >>> node
    Tree([('x', Tree([('y', 1), ('z', 2)])), ('y', Tree([('a', Tree([('b', 3)]))]))])

Installation
------------

This is a pure-Python package built for Python 2.7+ and Python 3.0+. To set up::

    pip install orderedattrdict

Updating
--------

Test locally::

    rm -rf build dist
    flake8 .
    python setup.py test

Update version in ``setup.py`` and Changelog below. Then commit. Then::

    git tag -a v1.x.x           # Annotate with a one-line summary of features
    git push --follow-tags
    # Ensure that travis builds pass
    python setup.py sdist bdist_wheel --universal
    twine upload dist/*

Changelog
---------

- ``1.0``: Basic implementation
- ``1.1``: Add utilities to load and save as YAML
- ``1.2``: Allow specific keys to be excluded from attribute access
- ``1.3``: Restore ``<<`` merge tags for YAML
- ``1.4.1``: Add ``CounterAttrDict`` and ``DefaultAttrDict``
- ``1.4.2``: Add Python 3.5 support
- ``1.4.3``: Fix bdist installation issues for Python 2.7
- ``1.5``: Add ``Tree`` data structure
