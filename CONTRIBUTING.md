# Mini contribution guide

The package uses `pyproject.toml` and [Poetry](https://python-poetry.org/). To install the dependencies:

```console
$ poetry install --extras "docs"
```

## Tests

To run tests with the current Python version:

```console
$ poetry run pytest
```

To run tests with all supported Python versions:

```console
$ poetry run tox
```

## Docs

To build the docs, use [Sphinx](https://www.sphinx-doc.org/en/):

```console
$ poetry run sphinx-build docs docs/_build
```

Then, browse from `docs/_build/index.html`.
