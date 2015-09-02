'An ordered dictionary with attribute-style access.'

from collections import OrderedDict

try:
    from yaml import Loader, Dumper, MappingNode
    from yaml.constructor import ConstructorError
except:
    pass


class AttrDict(OrderedDict):
    '''
    AttrDict extends OrderedDict to provide attribute-style access.

    Note: Items starting with __ or _OrderedDict__ can't be accessed as
    attributes.
    '''
    def __getattr__(self, name):
        'Getting ad.x gets ad["x"]'
        if name.startswith('__') or name.startswith('_OrderedDict__'):
            return super(AttrDict, self).__getattr__(name)
        else:
            try:
                return self[name]
            except KeyError:
                raise AttributeError(name)

    def __setattr__(self, name, value):
        'Setting ad.x sets ad["x"]'
        if name.startswith('__') or name.startswith('_OrderedDict__'):
            return super(AttrDict, self).__setattr__(name, value)
        self[name] = value

    def __delattr__(self, name):
        'Deleting ad.x deletes ad["x"]'
        if name.startswith('__') or name.startswith('_OrderedDict__'):
            return super(AttrDict, self).__delattr__(name)
        del self[name]


class AttrDictYAMLLoader(Loader):
    '''A YAML loader that loads mappings into ordered AttrDict.

    >>> attrdict = yaml.load('x: 1\ny: 2', Loader=AttrDictYAMLLoader)
    '''

    def __init__(self, *args, **kwargs):
        super(AttrDictYAMLLoader, self).__init__(*args, **kwargs)
        self.add_constructor(u'tag:yaml.org,2002:map', type(self).construct_yaml_attrdict)
        self.add_constructor(u'tag:yaml.org,2002:omap', type(self).construct_yaml_attrdict)

    def construct_yaml_attrdict(self, node):
        # Based on yaml.constructor.BaseConstructor.constructor_mapping()
        attrdict = AttrDict()
        yield attrdict
        if not isinstance(node, MappingNode):
            raise ConstructorError(
                None, None, 'expected a mapping node, but found %s' % node.id, node.start_mark)
        for key_node, value_node in node.value:
            key = self.construct_object(key_node, deep=False)
            try:
                hash(key)
            except TypeError as exc:
                raise ConstructorError(
                    'while constructing a mapping', node.start_mark,
                    'found unacceptable key (%s)' % exc, key_node.start_mark)
            attrdict[key] = self.construct_object(value_node, deep=False)


class AttrDictYAMLDumper(Dumper):
    '''
    A YAML dumper that dumps AttrDicts as dictionaries, preserving order

    >>> yaml.dump(AttrDict((('x', 1), ('y', 2))), Dumper=AttrDictYAMLDumper)
    '''

    def __init__(self, *args, **kwargs):
        super(AttrDictYAMLDumper, self).__init__(*args, **kwargs)
        self.add_representer(AttrDict, type(self).represent_attrdict)

    def represent_attrdict(self, data):
        # yaml.representer.BaseRepresenter.represent_mapping sorts keys if the
        # object has .items(). So instead, pass the items directly.
        return self.represent_mapping(u'tag:yaml.org,2002:map', data.items())
