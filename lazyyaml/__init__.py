import yaml
import jinja2
import jinja2.meta

try:
    from collections import abc as collections_abc
except ImportError:
    import collections as collections_abc


demo_doc = """
---
things:
    - thing2
    - thing3

cheese:
    - eggs
    - "{{ things }}"

things2:
    banana:
      - "{{ things }}"

otherthings: "{{ things }}"

otherotherthings: "{{ otherthings + cheese }}"

things3: "{{ things2 }}"
"""


class LazyBase(object):

    def __init__(self, data):
        self.data = data
        self._env = jinja2.Environment(undefined=jinja2.StrictUndefined)
        self.vars = self

    def __getitem__(self, key):
        thing = self.data[key]
        if type(thing) == str:
            template = self._env.from_string(thing)
            context = template.new_context(self.vars, shared=True)
            thing = yaml.load(''.join(template.root_render_func(context)),
                              Loader=LazyLoader)

        if type(thing) == LazyMapping or type(thing) == LazySequence:
            thing.vars = self.vars
        return thing

    def __len__(self):
        return len(self.data)

    def __setitem__(self, index, value):
        return self.data.__setitem__(index, value)

    def __delitem__(self, index):
        return self.data.__delitem__(index)


class LazyMapping(LazyBase, collections_abc.MutableMapping):

    def __iter__(self):
        for i in self.data.keys():
            yield i

    def __repr__(self):
        return ("{" + ", ".join(["%r: %r" % (k, v) for k, v in self.items()])
                + "}")

    def to_native(self):
        result = {}
        for k, v in self.items():
            if type(v) == LazyMapping or type(v) == LazySequence:
                v = v.to_native()
            result[k] = v
        return result


class LazySequence(LazyBase, collections_abc.MutableSequence):

    def __repr__(self):
        return "[" + ", ".join(["%r" % i for i in self]) + "]"

    def insert(self, index, value):
        return self.data.insert(index, value)

    def __add__(self, other):
        if type(other) == LazySequence:
            added = LazySequence(self.data + other.data)
        elif type(other) == list:
            added = LazySequence(self.data + other)
        added.vars = self.vars
        return added

    def to_native(self):
        result = []
        for v in self:
            if type(v) == LazyMapping or type(v) == LazySequence:
                v = v.to_native()
            result.append(v)
        return result


def map_constructor(loader, node):
    return LazyMapping(loader.construct_mapping(node))


def seq_constructor(loader, node):
    return LazySequence(loader.construct_sequence(node))


class LazyLoader(yaml.Loader):
    pass


LazyLoader.add_constructor('tag:yaml.org,2002:map', map_constructor)
LazyLoader.add_constructor('tag:yaml.org,2002:seq', seq_constructor)


def load(yaml_doc):
    return yaml.load(yaml_doc, Loader=LazyLoader)


def load_demo_doc():
    return load(demo_doc)


if __name__ == "__main__":
    print(load_demo_doc())
