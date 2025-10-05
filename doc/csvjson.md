# csvjson
A command line utility to convert csv to json.


## Motivation

Many present-day applications use json.

csvjson is a utility for converting csv data to json.


## Basic Usage

To display the csv file in json, simply pass the filename to csvjson:
```sh
$ csvjson users.csv
[
 {"ID": 1001, "FIRST_NAME": "John", "LAST_NAME": "Doe", "EMAIL": "jdoe@email.com", "TEL": "111-111-1111"},
 {"ID": 1002, "FIRST_NAME": "Jane", "LAST_NAME": "Smith", "EMAIL": "jsmith@email.com", "TEL": "222-222-2222"}
]
```


## Man Page
```
NAME
       csvjson - convert csv to json

SYNOPSIS
       csvjson [-d DELIM] [-f] [-g] [-m] [-n] [-s] [-t LIB] [FILE [FILE ...]]

DESCRIPTION
       csvjson  converts  a comma-separated value (csv) file FILE to json for-
       mat.

   Options
       -d DELIM, --delim=DELIM
              Use DELIM as the value delimiter, where DELIM may be 'p' for the
              pipe (|), 't' for the tab (\t), 'a' for the SOH  (ASCII  1),  or
              other string literal of one or more characters and Python string
              escape  sequences.  DELIM may include escape characters.  By de-
              fault the delimiter  is  guessed  from  the  characters  in  the
              CSV_DELIMS environment variable.

       -m, --multitable
              The  file  may  contain  more  than one csv table, divided by an
              empty line.  The second set of table is  treated  as  though  it
              were the start of a new csv file.

       -n, --no-header
              The  file  contains no header.  The values are numbered by their
              column positions instead.

       -S, --all-string
              Treat all fields as string.

       -s, --strip-quotes
              Strip quotes from field values.

       -t LIB, --translator=LIB
              Use the plugin library LIB to preprocess the values before  dis-
              play.   LIB  may be the full path to the library without the .py
              suffix, or it may  just  be  the  library  name  in  which  case
              CSV_PLUGINS_PATH is searched for the library.

       -e ENCODING, --encoding=ENCODING
              Use ENCODING encoding to read FILE.

       -V, --version
              Display the version and exit.

   Environment Variables
       CSV_DELIMS
              A  set  of characters used to guess the delimiter of a csv file.
              The guesswork happens when reading the first line of  the  first
              FILE,  by  testing  each character present in CSV_DELIMS for the
              character with the most occurrence in the line.  If any  of  the
              characters  occur the same number of times (including zero), the
              earlier character in the variable is chosen.  If the environment
              variable is not set, it defaults  to  ',\t|\u0001'.   CSV_DELIMS
              may include escape characters.

       CSV_PLUGINS_PATH
              A  colon-separated  list  of directories in which the plugin li-
              brary is searched.

SEE ALSO
       csvalign(1), csvcut(1),  csvgrep(1),  cgrep(1),  csvsql(1),  csvcsv(1),
       csvread(1)
```


[cgrep]: https://github.com/markuskimius/cgrep
[FIX]: http://fiximate.fixtrading.org/
