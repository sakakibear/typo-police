# typo-police

## Introduction

A tool to detect typos in text files (eg. source code files) and give suggestions for correction.

Stemming and lemmatization supported.

eg. `looked` => `look`, `children` => `child`

Camel case word will be split into individual words.

eg. `mansurTheBear` => `mansur`, `the`, `bear`

## Requirements

Python 3.6 or above.

NLTK.

https://www.nltk.org/

## Usage

Input: text files by STDIN.

Output: Detected typos and suggestions for correction.

`python3 typo_police.py [DICT...]`

eg.

`cat foo.txt | python3 typo_police.py dict1.txt dict2.txt`

`cat foo.txt | python3 typo_police.py dict/`

### Options

`DICT...`

One or more dictionary file(s) or directory(s).

Words in dictionaries and conjugations of them will not be considered as typos.

----

Test SSH access.
Another line for test.
