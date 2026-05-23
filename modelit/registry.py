"""Template discovery and loading."""

from __future__ import annotations

from dataclasses import dataclass
from importlib.resources import files
from pathlib import Path
import json
import sys


PACKAGE_NAME = "modelit"
TEMPLATES_DIR = "templates"
TEMPLATE_FILENAME = "template.py"
METADATA_FILENAME = "metadata.json"


@dataclass(frozen=True)
class TemplateInfo:
    name: str
    output_file: str


def _templates_root():
    return files(PACKAGE_NAME).joinpath(TEMPLATES_DIR)


def _template_dir(name: str):
    return _templates_root().joinpath(name)


def available_models() -> tuple[str, ...]:
    root = _templates_root()
    if not root.is_dir():
        return ()

    names: list[str] = []
    for child in root.iterdir():
        if child.is_dir() and child.joinpath(TEMPLATE_FILENAME).is_file():
            names.append(child.name)
    return tuple(sorted(names))


def load_metadata(name: str) -> TemplateInfo:
    metadata_path = _template_dir(name).joinpath(METADATA_FILENAME)
    data: dict[str, str] = {}
    if metadata_path.is_file():
        data = json.loads(metadata_path.read_text(encoding="utf-8"))

    output_file = data.get("output_file") or f"{name}.py"

    return TemplateInfo(
        name=name,
        output_file=output_file,
    )


def load_source(name: str) -> str:
    source_path = _template_dir(name).joinpath(TEMPLATE_FILENAME)
    if not source_path.is_file():
        raise FileNotFoundError(f"Missing template source for {name!r}")
    return source_path.read_text(encoding="utf-8")


def build_template_callable(name: str):
    info = load_metadata(name)
    source = load_source(name)
    output_file = info.output_file

    def runner(output: str | None = None) -> None:
        if output:
            path = Path(output)
            if path.exists():
                raise FileExistsError(f"{path} already exists")
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(source, encoding="utf-8")
            print(f"Generated {path}")
            return None

        print(source, end="")

    runner.__name__ = name
    runner.__qualname__ = name
    runner.__module__ = "modelit"
    runner.__doc__ = f"Print or save the {name} template."
    runner.output_file = output_file  # type: ignore[attr-defined]
    runner.template_info = info  # type: ignore[attr-defined]
    return runner
