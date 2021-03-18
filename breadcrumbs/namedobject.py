"""
    breadcrumbs.namedobject
    ~~~~~~~~~~~~~~~~~~~~~~~

    Sentinels with good representation.

    :copyright: 2021 by breadcrumbs Authors, see AUTHORS for more details.
    :license: BSD, see LICENSE for more details.
"""


class NamedObject(object):
    """A class to construct named sentinels."""

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name

    def __hash__(self):
        return id(self)

    def __deepcopy__(self, memo):
        return self
