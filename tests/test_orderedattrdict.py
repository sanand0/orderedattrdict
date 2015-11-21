import os
import json
import yaml
import random
import unittest
from collections import OrderedDict
from orderedattrdict import AttrDict, DefaultAttrDict, CounterAttrDict
from orderedattrdict.yamlutils import AttrDictYAMLLoader, from_yaml


# In Python 3, chr is unichr
try:
    unichr
except NameError:
    unichr = chr


class Generator(object):
    '''
    Generated random object hierarchies using AttrDict.
    https://github.com/maxtaco/python-random-json
    '''

    def __init__(self):
        random.seed()

    def byte(self):
        return random.randint(0, 0xff)

    def integer(self, signed):
        i = random.randint(0, 0xfffffff)
        if signed:
            i = 0x7ffffff - i
        return i

    def _small_float(self, signed=True):
        numerator = self.integer(signed=signed)
        denominator = self.integer(signed=False)
        return float(numerator) / float(1 + denominator)

    def float(self):
        while True:
            try:
                base = self._small_float(signed=False)
                exp = self._small_float()
                return base ** exp
            except OverflowError:
                pass

    def string(self, n=None):
        if not n:
            n = random.randint(32, 128)
        return u''.join([unichr(self.byte()) for i in range(n)]).strip()

    def array(self, n, d):
        if not n:
            n = random.randint(0, 10)
        return [self.json(d + 1) for i in range(n)]

    def obj(self, n, d=0):
        if not n:
            n = random.randint(0, 8)
        return AttrDict([(self.string(10), self.json(d+1)) for i in range(n)])

    def json(self, d=0):
        b = random.randint(0, 7)
        ret = None

        # Don't go more than 4 levels deep. Cut if off by
        # not allowing recursive structures at level 5.
        if d > 4 and b > 5:
            b = b % 5

        if False:
            pass
        elif b is 0:
            ret = False
        elif b is 1:
            ret = True
        elif b is 2:
            ret = None
        elif b is 3:
            ret = self.integer(True)
        elif b is 4:
            ret = self.float()
        elif b is 5:
            ret = self.string()
        elif b is 6:
            ret = self.array(None, d)
        elif b is 7:
            ret = self.obj(None, d)
        return ret


class TestAttrDict(unittest.TestCase):
    '''Test core orderedattrdict.AttrDict behaviour'''

    def setUp(self):
        self.gen = Generator()
        self.klass = AttrDict

    def test_attribute_access(self):
        'Items can be accessed as attributes'

        ad = self.klass()
        ad['x'] = 1
        self.assertEqual(ad.x, 1)
        self.assertTrue('x' in ad)

        ad._y = 2
        self.assertEqual(ad['_y'], 2)

        del ad['x']
        with self.assertRaises(AttributeError):
            ad.x
        del ad._y
        with self.assertRaises(KeyError):
            ad['_y']

    def test_ordereddict(self):
        'AttrDict inherits all OrderedDict behaviour'

        items = [('x', 1), ('_y', 2), (3, 3)]
        ad = self.klass(items)
        od = OrderedDict(items)
        self.assertEqual(ad, od)
        self.assertEqual(ad.keys(), od.keys())
        self.assertEqual(ad.items(), od.items())

        ad.pop(items[0][0])
        od.pop(items[0][0])
        self.assertEqual(ad, od)

        ad.pop(items[1][0])
        od.pop(items[1][0])
        self.assertEqual(ad, od)

        ad['x'] = od['x'] = 1
        self.assertEqual(ad, od)

        ad.setdefault('x', 10)
        od.setdefault('x', 10)
        ad.setdefault('new', 10)
        od.setdefault('new', 10)
        self.assertEqual(ad, od)

        new_ad = ad.copy()
        new_od = od.copy()
        self.assertEqual(new_ad, new_od)
        self.assertEqual(type(new_ad), type(ad))

        ad.popitem()
        od.popitem()
        self.assertEqual(ad, od)

        ad.clear()
        od.clear()
        self.assertEqual(ad, od)

        ad = self.klass.fromkeys(range(10), 1)
        od = OrderedDict.fromkeys(range(10), 1)
        self.assertEqual(ad, od)

        # Not tested:
        #   ad.iterkeys()
        #   ad.itervalues()
        #   ad.iteritems()
        #   ad.viewkeys()
        #   ad.viewvalues()
        #   ad.viewitems()

    def test_yaml(self):
        'Load YAML with ordered AttrDict instead of dict'''
        for iteration in range(10):
            ad = self.gen.obj(10)
            self.assertEqual(
                ad, yaml.load(yaml.dump(ad), Loader=AttrDictYAMLLoader))
            self.assertEqual(
                ad, yaml.load(yaml.safe_dump(ad), Loader=AttrDictYAMLLoader))

        yaml.add_constructor(u'tag:yaml.org,2002:map', from_yaml)
        yaml.add_constructor(u'tag:yaml.org,2002:omap', from_yaml)
        for iteration in range(10):
            ad = self.gen.obj(10)
            self.assertEqual(ad, yaml.load(yaml.dump(ad)))
            self.assertEqual(ad, yaml.load(yaml.safe_dump(ad)))

    def test_mergetag(self):
        'Check if YAML merge tag works'
        folder = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(folder, 'test.mergetag.yaml')) as handle:
            self.assertEqual(
                {'base': {'key': 'value'}, 'derived': {'key': 'value'}},
                yaml.load(handle, Loader=AttrDictYAMLLoader))

    def test_json(self):
        for iteration in range(10):
            ad = self.gen.obj(10)
            self.assertEqual(ad, json.loads(json.dumps(ad), object_pairs_hook=self.klass))

    def test_files(self):
        'Ensure that test JSON files have values in sorted order'
        folder = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(folder, 'test.json')) as handle:
            result = json.load(handle, object_pairs_hook=self.klass)
            self.assertEqual(list(result.values()), sorted(result.values()))
        with open(os.path.join(folder, 'test.yaml')) as handle:
            result = yaml.load(handle, Loader=AttrDictYAMLLoader)
            self.assertEqual(list(result.values()), sorted(result.values()))


class NoneDefaultAttrDict(DefaultAttrDict):
    'A DefaultAttrDict that mimics an AttrDict'
    def __init__(self, *args, **kwargs):
        super(NoneDefaultAttrDict, self).__init__(None, *args, **kwargs)

    def __copy__(self):
        return type(self)(self)


class TestDefaultAttrDict(TestAttrDict):
    'DefaultAttrDict with None constructor inherits all AttrDict behaviour'

    def setUp(self):
        super(TestDefaultAttrDict, self).setUp()
        self.klass = NoneDefaultAttrDict

    def test_defaultdict_counter(self):
        'DefaultAttrDict as a list generator'
        ad = DefaultAttrDict(int)
        self.assertEqual(ad['x'], 0)
        ad.x += 1
        ad.y += 2
        ad.z = ad.z + 3
        self.assertEqual(ad, {'x': 1, 'y': 2, 'z': 3})

    def test_defaultdict_with_list(self):
        'DefaultAttrDict as a list generator'
        ad = DefaultAttrDict(list)
        self.assertEqual(ad['x'], [])
        self.assertEqual(ad['y'], [])
        self.assertEqual(ad, {'x': [], 'y': []})
        self.assertFalse('z' in ad)

        ad = DefaultAttrDict(list)
        self.assertEqual(ad.x, [])
        self.assertEqual(ad.y, [])
        self.assertEqual(ad, {'x': [], 'y': []})
        self.assertFalse('z' in ad)

    def test_defaultdict_with_set(self):
        'DefaultAttrDict as a set generator'
        ad = DefaultAttrDict(set)
        self.assertEqual(ad['x'], set())
        self.assertEqual(ad['y'], set())
        self.assertEqual(ad, {'x': set(), 'y': set()})
        self.assertFalse('z' in ad)

        ad = DefaultAttrDict(set)
        self.assertEqual(ad.x, set())
        self.assertEqual(ad.y, set())
        self.assertEqual(ad, {'x': set(), 'y': set()})
        self.assertFalse('z' in ad)

    def test_defaultdict_tree(self):
        'DefaultAttrDict can be used as a tree'
        def tree():
            return DefaultAttrDict(tree)

        ad = tree()
        self.assertEqual(ad['x'], {})
        self.assertEqual(ad['y'], {})
        self.assertEqual(ad['x']['1'], {})
        self.assertEqual(ad, {'x': {'1': {}}, 'y': {}})
        self.assertFalse('z' in ad)

        ad = tree()
        ad.a.b.c = 1
        self.assertEqual(ad, {'a': {'b': {'c': 1}}})


class TestCounterAttrDict(unittest.TestCase):
    def test_counterattrdict(self):
        ad = CounterAttrDict()
        self.assertEqual(ad.x, 0)
        self.assertEqual(ad.y, 0)
        self.assertEqual(ad, {})
        ad.x += 1
        ad.y += 2
        ad.z += 3
        self.assertEqual(ad, {'x': 1, 'y': 2, 'z': 3})

        ad = CounterAttrDict()
        self.assertEqual(ad['x'], 0)
        self.assertEqual(ad['y'], 0)
        self.assertEqual(ad, {})
        ad['x'] += 1
        ad['y'] += 2
        ad['z'] += 3
        self.assertEqual(ad, {'x': 1, 'y': 2, 'z': 3})
