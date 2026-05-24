"""Template discovery and loading."""

from __future__ import annotations

from dataclasses import dataclass
from importlib.resources import files
from pathlib import Path


PACKAGE_NAME = "modelit"
TEMPLATES_DIR = "templates"


@dataclass(frozen=True)
class TemplateInfo:
    name: str


def _templates_root():
    return files(PACKAGE_NAME).joinpath(TEMPLATES_DIR)


def _template_dir(name: str):
    return _templates_root().joinpath(name)


def _get_template_file(name_or_dir):
    target_dir = _template_dir(name_or_dir) if isinstance(name_or_dir, str) else name_or_dir
    
    if not target_dir.is_dir():
        return None
        
    for child in target_dir.iterdir():
        if child.is_file() and child.name.startswith("template."):
            return child
            
    return None


def available_models() -> tuple[str, ...]:
    root = _templates_root()
    if not root.is_dir():
        return ()

    names: list[str] = []
    for child in root.iterdir():
        if child.is_dir() and _get_template_file(child) is not None:
            names.append(child.name)
    return tuple(sorted(names))


def load_metadata(name: str) -> TemplateInfo:
    return TemplateInfo(name=name)


def load_source_and_ext(name: str) -> tuple[str, str]:
    template_file = _get_template_file(name)
    if template_file is None:
        raise FileNotFoundError(f"Missing template source for {name!r}")
    
    ext = Path(template_file.name).suffix
    return template_file.read_text(encoding="utf-8"), ext


def load_source(name: str) -> str:
    source, _ = load_source_and_ext(name)
    return source


def build_template_callable(name: str):
    source, ext = load_source_and_ext(name)
    info = load_metadata(name)
    
    output_file = f"{name}{ext}"

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