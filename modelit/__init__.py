"""ModelIt exports local ML boilerplate templates."""

from __future__ import annotations

from .registry import available_models, build_template_callable

__all__ = list(available_models())


def __getattr__(name: str):
    if name in available_models():
        fn = build_template_callable(name)
        globals()[name] = fn
        return fn
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def __dir__():
    return sorted(set(globals()) | set(available_models()))
