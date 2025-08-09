# Mini contribution guide

The requires [`uv`](https://docs.astral.sh/uv/).

## Tests

To run tests with the current Python version:

```console
$ uv run pytest
```

To run tests with all supported Python versions:

```console
$ uv run tox
```

## Linter, format & type check

```console
$ uv run ruff check . --fix
$ uv run ruff format .
$ uv run mypy .
```

## Docs

To build the docs, use [Sphinx](https://www.sphinx-doc.org/en/):

```console
$ uv run --group docs sphinx-build docs docs/_build
```

Then, browse from `docs/_build/index.html`.
