# csvgrep
A command line utility to grep csv rows by a field value.


## Motivation

Although `grep` typically works fine for finding a row in a csv file, it is not easy to:

* Retain the header in the output.
* Match only in a specific column(s).
* Display the entirety of the matching row that spans more than one line.

`csvgrep` solves these issues.


## Basic Usage

Given the following csv file,

```csv
ID,NAME,EMAIL,TEL
1001,"Doe, John","jdoe@email.com","111-111-1111"
1002,"Smith, Jane","jsmith@email.com","222-222-2222"
```

`csvgrep` can grep only the row with 1 in the TEL column:

```sh
$ csvgrep -fTEL 1 users.csv
ID,FIRST_NAME,LAST_NAME,EMAIL,TEL
1001,"John","Doe","jdoe@email.com","111-111-1111"
$
```

## Man Page

```
CSVGREP(1)                  General Commands Manual                 CSVGREP(1)

NAME
       csvgrep - find matching rows in a comma-separated value (csv) file.

SYNOPSIS
       csvgrep [-d DELIM] [-f FIELDS] [-i] [-k] [-m] [-n] [-v] PATTERN [FILE]

DESCRIPTION
       csvcut extract columns and values from a comma-separated value (csv)
       file FILE.

   Options
       -d DELIM, --delim=DELIM
              Use DELIM as the value delimiter, where DELIM may be 'p' for the
              pipe (|), 't' for the tab (\t), 'a' for the SOH (ASCII 1), or
              other string literal of one or more characters and Python string
              escape sequences.  DELIM may include escape characters.  By
              default the delimiter is guessed from the characters in the
              CSV_DELIMS environment variable.

       -f FIELDS, --fields=FIELDS
              FIELDS is a comma-separated list of columns in the csv file in
              which to match PATTERN.  The default is to look in all columns.
              See Selector Format below on how to select column(s).

       -i, --ignore-case
              Ignore case when matching the field.

       -k, --keep-quotes
              Keep any quotes surrounding the field value when testing
              PATTERN.  The default is to discard them.

       -m, --multitable
              The file may contain more than one csv table, divided by an
              empty line.  The second set of table is treated as though it
              were the start of a new csv file.

       -n, --no-header
              The file contains no header.  Otherwise the first line is always
              matched.

       -v, --inverse
              Extract non-matching fields only.

   Selector Format
       INT    An integer select the column by its number.  The leftmost column
              is 1.

       INT1-[INT2]
              Select all columns between INT1 and INT2, inclusive.  If INT2 is
              omitted all columns from INT1 to the last column are selected.

       [=]STRING
              Select the column by its name.  The string may be prefixed by
              the equal sign (=) to avoid other interpretations.

       /REGEX/[i]
              Select all columns whose name matches the regular expression
              REGEX.  The i modifier forces case-insensitive match.

       -      Select all fields that have not already been selected.

       No selector may include the comma character.

   Environment Variables
       CSV_DELIMS
              A set of characters used to guess the delimiter of a csv file.
              The guesswork happens when reading the first line of the first
              FILE, by testing each character present in CSV_DELIMS for the
              character with the most occurrence in the line.  If any of the
              characters occur the same number of times (including zero), the
              earlier character in the variable is chosen.  If the environment
              variable is not set, it defaults to ',\t|\u0001'.  CSV_DELIMS
              may include escape characters.

SEE ALSO
       csvcut(1), csvread(1), csvalign(1), csvsql(1), csvcsv(1)

                                 03 July 2022                       CSVGREP(1)
```
