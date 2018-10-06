# csvread
A command line utility to display csv rows in a human-readable format.

This tool solves the problem with a csv file's readability:
- Csv files are hard to read because the columns don't align.
- Csv files with many columns are hard to read because the rows wrap around the screen.

This script addresses these readability problems.

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
