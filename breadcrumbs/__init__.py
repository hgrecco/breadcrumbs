"""
    breadcrumbs
    ~~~~~~~~~~~

    A small library to record steps in a pipeline.

    :copyright: 2021 by breadcrumbs Authors, see AUTHORS for more details.
    :license: BSD, see LICENSE for more details.
"""

from __future__ import annotations

import contextlib
import contextvars
import copy
import dataclasses
import functools
import inspect

try:
    from importlib.metadata import version
except ImportError:
    # Backport for Python < 3.8
    from importlib_metadata import version

try:  # pragma: no cover
    __version__ = version("breadcrumbs")
except Exception:  # pragma: no cover
    # we seem to have a local copy not installed without setuptools
    # so the reported version will be unknown
    __version__ = "unknown"


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


REDACTED = NamedObject("REDACTED")


class TrailMixin:
    """Mixin class for annotated objects."""

    @property
    def trail(self):
        return getattr(self, "_trail", ())

    def put_crumb(self, cmb: Crumb):
        if hasattr(self, "_trail"):
            self._trail += (cmb,)
        else:
            self._trail = (cmb,)


@dataclasses.dataclass
class Crumb(TrailMixin):
    """A information piece that can contain others."""

    title: str
    info: dict[str, object] = dataclasses.field(default_factory=dict)
    extra: dict[str, object] = dataclasses.field(default_factory=dict)


RootCrumb = Crumb("RootEntry")

_crumb_ctx_var = contextvars.ContextVar("_crumb_ctx_var")
_token = _crumb_ctx_var.set(RootCrumb)


@contextlib.contextmanager
def context(nte: Crumb):
    """Set a given Crumb as current active one."""

    token = _crumb_ctx_var.set(nte)
    yield
    _crumb_ctx_var.reset(token)


def put(cmb: Crumb):
    """Add crumb to active crumb."""
    _cmb: Crumb = _crumb_ctx_var.get()
    _cmb.put_crumb(cmb)


def update_info(**kwargs):
    """Update the info attribute in the active crumb."""
    cmb: Crumb = _crumb_ctx_var.get()
    cmb.info.update(**kwargs)


def update_extra(**kwargs):
    """Update the extra attribute in the active crumb."""
    cmb: Crumb = _crumb_ctx_var.get()
    cmb.extra.update(**kwargs)


def aware(trail_param=None, redact_params=()):
    """Decorator to make a function or method aware of breadcrumbs.

    Parameters
    ----------
    trail_param : str or None
        Object to which the crumb will be added.
        If None, the root RootCrumb object will be used.
    redact_params : tuple of str
        Names of the parameters that will redacted replacing
        the actual values by Redacted.
    """

    def _wrapper(func):
        sig = inspect.signature(func)

        @functools.wraps(func)
        def _inner(*args, **kwargs):
            ba = sig.bind(*args, **kwargs)
            ba.apply_defaults()

            to_store = copy.deepcopy(ba.arguments)

            if trail_param is None:
                annotated_obj = _crumb_ctx_var.get()
            else:
                annotated_obj = ba.arguments[trail_param]
                to_store.pop(trail_param)

            if isinstance(redact_params, str):
                to_store[redact_params] = REDACTED
            else:
                for param in redact_params:
                    to_store[param] = REDACTED

            ann = Crumb(func.__qualname__, to_store)

            with context(ann):
                out = func(*ba.args, **ba.kwargs)

            annotated_obj.put_crumb(ann)

            return out

        return _inner

    return _wrapper


__all__ = [
    "RootCrumb",
    "TrailMixin",
    "Crumb",
    "context",
    "put",
    "update_info",
    "update_extra",
    "aware",
    "REDACTED",
]
