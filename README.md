# ModelIt

ModelIt is a tiny Python package for storing your ML/DL boilerplate templates.

## What it does

- `from modelit import perceptron`
- `perceptron()` prints the full code
- `perceptron(output="code1.py")` saves it to a file
- `modelit create perceptron` works from the terminal

## Install

```bash
pip install modelit
```

For local development:

```bash
pip install -e .
```

## Use it

### Simple Python Run which prints the code.

```python
from modelit import perceptron

perceptron()
```

### Save to file And then Run so the file is created with code in it.

```python
from modelit import perceptron

perceptron(output="code1.py")
```

Then run:

```bash
python3 code1.py
```

### CLI

```bash
modelit create perceptron
modelit create perceptron --output code1.py
```

## Add a new code

1. Create a folder:

```text
modelit/templates/mycode/
```

2. Add your code file:

```text
modelit/templates/mycode/template.py
```

3. Done. The folder name becomes the function name.

That means this will work automatically:

```python
from modelit import mycode

mycode()
```

And this too:

```bash
modelit create mycode
modelit create mycode --output mycode.py
```

## Publish flow

1. Add a new template folder.
2. `git add .`
3. `git commit -m "..."`
4. `git push`
5. `git tag v0.x.y`
6. `git push origin v0.x.y`

The version is taken from the git tag, so you do not edit `pyproject.toml` for releases.
