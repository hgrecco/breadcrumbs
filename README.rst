.. image:: https://img.shields.io/pypi/v/use-breadcrumbs.svg
    :target: https://pypi.python.org/pypi/use-breadcrumbs
    :alt: Latest Version

.. image:: https://img.shields.io/pypi/l/use-breadcrumbs.svg
    :target: https://pypi.python.org/pypi/use-breadcrumbs
    :alt: License

.. image:: https://img.shields.io/pypi/pyversions/use-breadcrumbs.svg
    :target: https://pypi.python.org/pypi/use-breadcrumbs
    :alt: Python Versions

.. image:: https://github.com/hgrecco/breadcrumbs/workflows/CI/badge.svg?branch=main
    :target: https://github.com/hgrecco/breadcrumbs/actions?query=workflow%3ACI

.. image:: https://github.com/hgrecco/breadcrumbs/workflows/Lint/badge.svg?branch=main
    :target: https://github.com/hgrecco/breadcrumbs/actions?query=workflow%3ALint

.. image:: https://coveralls.io/repos/github/hgrecco/breadcrumbs/badge.svg?branch=main
    :target: https://coveralls.io/github/hgrecco/breadcrumbs?branch=main


breadcrumbs: keep track of what is going on
===========================================

This library started with a rather simple objective in mind:
keep track of a sequence of transforming steps.

It is extremely easy to use:

.. code-block:: python

    >>> import breadcrumbs as bc
    >>> crumb = bc.Crumb("start")
    >>> crumb.info.update(value=35)
    >>> crumb.info.update(other_value=70)
    >>> print(crumb.info)
    {'value': 35, 'other_value': 70}

A Crumb can has three attributes: a name (here `Start`), and two dicts (`info` and `extra`)
to store additional information. You can also store dependent crumbs using the `put_crumb`
method.

'What is the big deal?' you might ask, 'You are just writing a dict!'
True, but the cool thing is that it works a little bit like logging and
therefore you use it decoupled across you code:

.. code-block:: python

    >>> def func1():
    ...     bc.info.update(value=35)
    >>> def func2():
    ...     bc.extra.update(other_value=70)
    >>> crumb = bc.Crumb("start")
    >>> with bc.context(crumb):
    ...     func2()
    ...     func1()
    >>> print(crumb.info)
    {'value': 35}
    >>> print(crumb.extra)
    {'other_value': 70}


`func1` and `func2` now nothing about `crumb` but it just works.

You can also decorate a function to do some things for you automatically.

.. code-block:: python

    >>> @bc.aware()
    ... def func1(x, y):
    ...     return x + y
    >>> crumb = bc.Crumb("start")
    >>> with bc.context(crumb):
    ...     func1(1, 2)
    >>> print(crumb.trail)
    (Crumb('func1', info={'x': 1, y: '2'}, extra={}))

So in trail you can see that `func1` has been called with certain parameters. You
can redact some parameters that might be memory intensive or pointless to store.

.. code-block:: python

    >>> @bc.aware(redact_params='y')
    ... def func1(x, y):
    ...     return x + y
    >>> crumb = bc.Crumb("start")
    >>> with bc.context(crumb):
    ...     func1(1, 2)
    >>> print(crumb.trail)
    (Crumb('func1', info={'x': 1}, extra={}))

To redact more parameters, just pass an iterable.

A useful feature is that a `TrailMixin` allows you to add object
specific notes and teach this to functions.

.. code-block:: python

    >>> class MyCoolClass(bc.TrailMixin):
    ...     # Here goes your cool class
    ...     internal = 10
    >>> @bc.aware(trail_param="obj")
    ... def func1(obj, x, y):
    ...     return (x + y) * obj.internal
    >>> myobj = MyCoolClass()
    >>> func1(myobj, 1, 2)
    >>> print(myobj.trail)
    (Crumb('func1', info={'x': 1, 'y': 2}, extra={}))


Quick Installation
------------------

To install breadcrumbs, simply:

.. code-block:: bash

    $ pip install use-breadcrumbs

and then simply enjoy it!

It runs in Python 3.7+ with no other dependency. It is licensed under
BSD.

----

breadcrumbs is maintained by a community. See AUTHORS_ for a complete list.

To review an ordered list of notable changes for each version of a project,
see CHANGES_


.. _`AUTHORS`: https://github.com/hgrecco/breadcrumbs/blob/master/AUTHORS
.. _`CHANGES`: https://github.com/hgrecco/breadcrumbs/blob/master/CHANGES
