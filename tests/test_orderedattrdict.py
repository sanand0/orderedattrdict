import yaml
import random
import unittest
from collections import OrderedDict
from orderedattrdict import AttrDict, AttrDictYAMLLoader, AttrDictYAMLDumper


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

    def _small_float(self, pos=True):
        n = self.integer(not pos)
        d = self.integer(False)
        d = 1 if d is 0 else d
        return float(d) / float(n)

    def float(self):
        base = self._small_float(True)
        exp = self._small_float()
        return base ** exp

    def string(self, n=None):
        if not n:
            n = random.randint(32, 128)
        return ''.join([chr(self.byte()) for i in range(n)]).strip()

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

    def test_attribute_access(self):
        'Items can be accessed as attributes'

        ad = AttrDict()
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
        ad = AttrDict(items)
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

        ad = AttrDict.fromkeys(range(10), 1)
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
        gen = Generator()
        for iteration in range(10):
            ad = gen.obj(10)
            result = yaml.dump(ad, Dumper=AttrDictYAMLDumper)
            self.assertEqual(yaml.load(result, Loader=AttrDictYAMLLoader), ad)
