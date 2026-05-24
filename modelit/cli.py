"""Command-line entry point for ModelIt."""

from __future__ import annotations

import argparse

from .registry import available_models, build_template_callable


def _create(args: argparse.Namespace) -> None:
    build_template_callable(args.name)(output=args.output)


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(prog="modelit", description="Print or save ML template code.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    create_parser = subparsers.add_parser("create", help="Print or save a template")
    create_parser.add_argument("name", choices=available_models(), help="Template name")
    create_parser.add_argument("-o", "--output", help="Write to a file for single-file templates or a directory for multi-file templates")
    create_parser.set_defaults(func=_create)

    args = parser.parse_args(argv)
    args.func(args)
