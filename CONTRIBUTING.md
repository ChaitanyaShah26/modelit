# Contributing to ModelIt

Thanks for helping improve ModelIt.

## Add a new template

1. Fork this repo.
2. Create a new folder:

```text
modelit/templates/<name>/
```

3. Add your code in:

```text
modelit/templates/<name>/template.py
```

For multi-file templates, add more files in the same folder.

4. Make sure the folder name is the function name.
5. Test it locally:

```python
from modelit import <name>

<name>()
```

or:

```bash
modelit create <name>
```

You can list all available templates with:

```bash
modelit list
```

## Rules

- Keep templates simple and runnable.
- Avoid internet-only dependencies.
- Do not add `metadata.json`.
- Keep file names lowercase.
- Prefer clean, beginner-friendly code.
- If a template has multiple files, `--output` should be treated as a directory.

## Pull request flow

1. Fork the repo.
2. Create a branch.
3. Add your template.
4. Commit and push.
5. Open a pull request.

## Maintainer notes

I will review templates for clarity, correctness, and portability before merging.
