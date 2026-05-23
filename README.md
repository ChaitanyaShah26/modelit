# ModelIt

Tiny local-first ML template printer.

## Install

```bash
pip install modelit
```

For development from a clone, use:

```bash
pip install -e .
```

## Run

```python
from modelit import perceptron

perceptron()
```

Or from CLI:

```bash
modelit create perceptron
```

## Save to file

```python
from modelit import perceptron

perceptron(output="code1.py")
```

Or:

```bash
modelit create perceptron --output code1.py
```

Then run:

```bash
python3 code1.py
```

## Publish

This project is set up for PyPI publishing with GitHub Actions.

1. Push a tag like `v0.1.0`
2. GitHub Actions builds and publishes to PyPI
3. Users install with `pip install modelit`

To update later, change the version, add your new templates, and publish a new tag.

## Add a new code

Create:

```text
modelit/templates/<name>/template.py
modelit/templates/<name>/metadata.json
```

Then the new name is exposed automatically as:

```python
from modelit import <name>
```
