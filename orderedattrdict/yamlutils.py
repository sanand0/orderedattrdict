'YAML utilities for working with AttrDicts'

from . import AttrDict
from yaml import Loader, MappingNode
from yaml.constructor import ConstructorError
from yaml.representer import Representer, SafeRepresenter


def from_yaml(loader, node):
    'Load mapping as AttrDict, preserving order'
    # Based on yaml.constructor.SafeConstructor.construct_mapping()
    attrdict = AttrDict()
    yield attrdict
    if not isinstance(node, MappingNode):
        raise ConstructorError(
            None, None, 'expected a mapping node, but found %s' % node.id, node.start_mark)
    loader.flatten_mapping(node)
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=False)
        try:
            hash(key)
        except TypeError as exc:
            raise ConstructorError(
                'while constructing a mapping', node.start_mark,
                'found unacceptable key (%s)' % exc, key_node.start_mark)
        attrdict[key] = loader.construct_object(value_node, deep=False)


class AttrDictYAMLLoader(Loader):
    '''A YAML loader that loads mappings into ordered AttrDict.

    >>> attrdict = yaml.load('x: 1\ny: 2', Loader=AttrDictYAMLLoader)
    '''

    def __init__(self, *args, **kwargs):
        super(AttrDictYAMLLoader, self).__init__(*args, **kwargs)
        self.add_constructor(u'tag:yaml.org,2002:map', from_yaml)
        self.add_constructor(u'tag:yaml.org,2002:omap', from_yaml)


def to_yaml(dumper, data):
    'Convert AttrDict to dictionary, preserving order'
    # yaml.representer.BaseRepresenter.represent_mapping sorts keys if the
    # object has .items(). So instead, pass the items directly.
    return dumper.represent_mapping(u'tag:yaml.org,2002:map', data.items())


SafeRepresenter.add_representer(AttrDict, to_yaml)
SafeRepresenter.add_multi_representer(AttrDict, to_yaml)

Representer.add_representer(AttrDict, to_yaml)
Representer.add_multi_representer(AttrDict, to_yaml)
