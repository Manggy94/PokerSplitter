# Poker Splitter

A package to split poker history files

[![Documentation Status](https://readthedocs.org/projects/pkrsplitter/badge/?version=latest)](https://pkrsplitter.readthedocs.io/en/latest/?badge=latest)
[![PyPI version](https://badge.fury.io/py/pkrsplitter.svg)](https://badge.fury.io/py/pkrsplitter)

## Table of Contents

- [Description](#description)
- [Setup](#setup)
- [Usage](#usage)
- [License](#license)
- [Documentation](#documentation)

## Description
A package to split poker history files
Currently only supports Winamax history files

## Setup

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
DATA_DIR=path/to/data/dir
BUCKET_NAME=your_bucket_name on s3
```

You can also directly set the environment variable in your system.


## Usage

Basic Usage from the command line:

```bash
# Split all files in the directory to local split directory
python -m pkrsplitter.runs.local.split_files

# split only the files that have not been split yet from S3 raw histories to S3 split histories
python -m pkrsplitter.runs.s3.split_new_files
```

Usage in a script:

```python
from pkrsplitter.splitters.local import LocalFileSplitter

splitter = LocalFileSplitter(data_dir='path/to/data/dir')
splitter.split_files()
```

You can choose to split all the files in the directory or only the files that have not been split yet.:

```python
from pkrsplitter.splitters.local import LocalFileSplitter

splitter = LocalFileSplitter(data_dir='path/to/data/dir')
splitter.split_new_files()
```
This will result in overwriting the files if they already exist in the split directory.
The same can be done considering splitting only raw histories that have never been split before:

```python
from pkrsplitter.splitters.local import LocalFileSplitter

splitter = LocalFileSplitter(data_dir='path/to/data/dir')
splitter.split_new_histories()

```
We can also replace the LocalFileSplitter with the S3FileSplitter to split files from an S3 bucket:


## License

This project is licensed under the MIT License -
You can check out the full license [here](LICENSE.txt)

## Documentation

The documentation can be found [here](https://pkrsplitter.readthedocs.io/en/latest/)


