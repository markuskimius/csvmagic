# csvcut
A command line utility to select columns or values in a csv file.


## Motivation

csv files often needs to be filtered:

- you may want to see only certain column(s) in a csv file.
- you may want to see only certain value(s) in a csv file.

There already exists a UNIX utility, `cut`, for doing the former and `grep` for
doing the latter. But:

- `cut` and `grep` are difficult or impossible to use with [rfc4180] compliant
  csv file containing newlines and commas.
- `cut` cannot reorder columns.
- `cut` cannot select columns by name.

csvcut is a utilty to address these problems.


## The Basics

Given the following csv file,
```csv
ID,FIRST_NAME,LAST_NAME,EMAIL,TEL
1001,John,Doe,jdoe@email.com,111-111-1111
1002,Jane,Smith,jsmith@email.com,222-222-2222
```

csvcut can select just the 1st and 4th columns using column numbers:
```sh
$ csvcut -f1,4 users.csv
ID,EMAIL
1001,jdoe@email.com
1002,jsmith@email.com
```

or using column names:
```sh
$ csvcut -fID,EMAIL users.csv
ID,EMAIL
1001,jdoe@email.com
1002,jsmith@email.com
```

By default, a numeric selector is assumed to be a column number; to force it to
be interpreted as a column name, prefix it with `=`:
```sh
$ csvcut -f=ID,=EMAIL users.csv
ID,EMAIL
1001,jdoe@email.com
1002,jsmith@email.com
```


## Column Name by Regex

Column names may also be selected using regex. To show all columns with the word "NAME" in it:
```sh
$ csvcut -f/NAME/ users.csv
FIRST_NAME,LAST_NAME
John,Doe
Jane,Smith
```

The regex accepts modifiers. For case insensitive match, pass the `i` option:
```sh
$ csvcut -f/name/i users.csv
FIRST_NAME,LAST_NAME
John,Doe
Jane,Smith
```

At this time, the only accepted modifier is `i`.

The regex expression may not contain the comma (`,`) as it is used as the field
selector separator.


## Column Ranges

The `-f` option supports column ranges:
* `1-5`: Columns 1 through 5.
* `1-`: Column 1 to the end.


## Remaining Columns

The `-f` options supports displaying columns that have yet to be matched by any
previous `-f` expression.  These columns can be selected using `-`.  To select
columns 3, 2, followed by the remaining columns (1, 4, and 5):
```sh
$ csvcut -f3,2,- users.csv
LAST_NAME,FIRST_NAME,ID,EMAIL,TEL
Doe,John,1001,jdoe@email.com,111-111-1111
Smith,Jane,1002,jsmith@email.com,222-222-2222
```


## Selecting Values

To display a specific field value, use the `~` selector followed by a regex.
For example, to find all field values containing `@`:
```sh
$ csvcut -f~/@/ users.csv

jdoe@email.com
jsmith@email.com
```


## Alternate Delimiter

By default, csvcut guess the delimiter from the comma, tab, pipe, or the SOH
(ASCII 1) characters.  To use another delimiter or to force a delimiter, use
the `-d` option.

For example, if the file `users.rsv` were using the carrot (`^`) as the
delimiter, to select the columns 1 and 4:
```sh
$ csvcut -d^ -f1,4 users.rsv
ID^EMAIL
1001^jdoe@email.com
1002^jsmith@email.com
```

It is also possible to tell csvcut to use an alternate set of characters from
which the guess a file's delimiter by setting the environment variable
`CSV_DELIMS`.  For example, to tell csvcut to guess delimiters from a comma and
a carrot in BASH:

```sh
$ export CSV_DELIMS=,^
$ csvcut -f1,4 users.rsv
ID^EMAIL
1001^jdoe@email.com
1002^jsmith@email.com
```


[rfc4180]: https://tools.ietf.org/html/rfc4180

