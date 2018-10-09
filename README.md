# csvread
A command line utility to display csv rows in a human-readable format.

This tool solves the problem with a csv file's readability:
- Csv files are hard to read because the columns don't align.
- Csv files with many columns are hard to read because the rows wrap around the screen.

This script addresses these readability problems.

## Usage

```
usage: csvread [-h] [-x] [-d DELIM] [-l LIB] [-p PATH] [FILE [FILE ...]]

Display csv rows in a more readable format.

positional arguments:
  FILE                  csv file(s) to read.

optional arguments:
  -h, --help            show this help message and exit
  -x, --no-header       csv file with no header
  -d DELIM, --delim DELIM
                        Delimiter [default=,]
  -l LIB, --lib LIB     Translation plugin to use [default=none]
  -p PATH, --path PATH  Path to the translation plugin
```

## Example

Given the following csv file,
```csv
ID,NAME,EMAIL,TEL
1,John,john@email.com,111-111-1111
2,Jane,jane@email.com,222-222-2222
```
Running csvread on it gives the following output:
```sh
$ csvread names.csv
ID    = 1
NAME  = John
EMAIL = john@email.com
TEL   = 111-111-1111

ID    = 2
NAME  = Jane
EMAIL = jane@email.com
TEL   = 222-222-2222
```
