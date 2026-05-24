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

def available_models() -> tuple[str, ...]:
    root = _templates_root()
    if not root.is_dir():
        return ()

    names: list[str] = []
    for child in root.iterdir():
        if child.is_dir() and not child.name.startswith("__"):
            if any(child.iterdir()):
                names.append(child.name)
    return tuple(sorted(names))

def load_metadata(name: str) -> TemplateInfo:
    return TemplateInfo(name=name)

def load_template_files(name: str) -> dict[str, str]:
    target_dir = _template_dir(name)
    if not target_dir.is_dir():
        raise FileNotFoundError(f"Missing template directory for {name!r}")
        
    file_contents = {}
    for child in target_dir.iterdir():
        if child.is_file() and not child.name.startswith("__"):
            file_contents[child.name] = child.read_text(encoding="utf-8")
    return file_contents

def build_template_callable(name: str):
    files_dict = load_template_files(name)
    info = load_metadata(name)

    is_single_file = len(files_dict) == 1
    default_filename = list(files_dict.keys())[0] if is_single_file else name

    def runner(output: str | None = None) -> None:
        if output:
            out_path = Path(output)

            if is_single_file:
                if out_path.exists():
                    raise FileExistsError(f"Output path already exists: {out_path}")
                out_path.parent.mkdir(parents=True, exist_ok=True)
                out_path.write_text(list(files_dict.values())[0], encoding="utf-8")
                print(f"Generated {out_path}")
            else:
                if out_path.suffix:
                    raise ValueError("Multi-file templates require a directory output path")
                if out_path.exists() and not out_path.is_dir():
                    raise FileExistsError(f"Output path already exists and is not a directory: {out_path}")
                out_path.mkdir(parents=True, exist_ok=True)
                for fname, content in files_dict.items():
                    file_path = out_path / fname
                    if file_path.exists():
                        print(f"Skipping {file_path} (already exists)")
                        continue
                    file_path.write_text(content, encoding="utf-8")
                    print(f"Generated {file_path}")
            return None

        # If no output is specified, print to terminal
        for fname, content in files_dict.items():
            if not is_single_file:
                print(f"\n{'='*40}\nFile: {fname}\n{'='*40}")
            print(content, end="\n\n" if not is_single_file else "")

    runner.__name__ = name
    runner.__qualname__ = name
    runner.__module__ = "modelit"
    runner.__doc__ = f"Print or save the {name} template."
    runner.output_file = default_filename  # type: ignore[attr-defined]
    runner.template_info = info  # type: ignore[attr-defined]
    return runner
