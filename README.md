# Across

Across is the fastest, cheapest and most secure cross-chain bridge. It is a system that uses UMA contracts to quickly move tokens across chains. This contains various utilities to support applications on across.

## How to use

Use across official API to get suggested fees.
```py
>>> import across
>>> a = across.AcrossAPI()
>>> a.suggested_fees("0x7f5c764cbc14f9669b88837ca1490cca17c31607", 10, 1000000000)
{'slowFeePct': '43038790000000000', 'instantFeePct': '5197246000000000'}
```

## How to build and test

Install poetry and install the dependencies:

```shell
pip3 install poetry

poetry install

# test
python -m unittest

# local install and test
pip3 install twine
python3 -m twine upload --repository testpypi dist/*
pip3 install --index-url https://test.pypi.org/simple/ --no-deps across
```
