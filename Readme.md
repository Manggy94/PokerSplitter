# Poker Splitter

A package to split poker history files

[![Documentation Status](https://readthedocs.org/projects/pkrsplitter/badge/?version=latest)](https://pkrsplitter.readthedocs.io/en/latest/?badge=latest)
[![PyPI version](https://badge.fury.io/py/pkrsplitter.svg)](https://badge.fury.io/py/pkrsplitter)
## Table of Contents

- [Description](#description)
- [Installation](#installation)
- [Usage](#usage)
- [License](#license)
- [Documentation](#documentation)

## Description
A package to split poker history files
Currently only supports Winamax history files

## Installation

From PyPi:

```bash
pip install pkrsplitter
```

From source:

```bash
git clone https://github.com/manggy94/PokerSplitter.git
cd PokerSplitter
```

Add a .env file in the root directory with the following content:

```.env
SOURCE_DIR=path/to/source/dir
```

You can also directly set the environment variable in your system.


## Usage

Basic Usage from the command line:

```bash
python -m pkrsplitter.main
```

Usage in a script:

```python
from pkrsplitter.splitter import FileSplitter

splitter = FileSplitter(raw_histories_directory='path/to/raw/dir', split_histories_directory='path/to/split/dir')
splitter.split_files()
```

You can use the check_exists parameter to check if the files have already been split:

```python
from pkrsplitter.splitter import FileSplitter

splitter = FileSplitter(raw_histories_directory='path/to/raw/dir', split_histories_directory='path/to/split/dir')
splitter.split_files(check_exists=True)
```
This will result in overwriting the files if they already exist in the split directory.

## License

This project is licensed under the MIT License -
You can check out the full license [here](LICENSE.txt)

##Documentation

The documentation can be found [here](https://pkrsplitter.readthedocs.io/en/latest/)


