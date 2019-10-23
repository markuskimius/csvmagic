# csvread
A command line utility to display csv rows in a more human-readable format.

## Statement of Problem

This utility solves these problems:

- csv files are hard to read because the columns don't align.
- csv files with many columns are hard to read because the rows wrap around the
  screen.

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
ID    : 1
NAME  : John
EMAIL : john@email.com
TEL   : 111-111-1111

ID    : 2
NAME  : Jane
EMAIL : jane@email.com
TEL   : 222-222-2222
```

By default, csvread tries to guess the delimiter from the comma, tab, pipe, or
the SOH (ASCII 1) characters.  To use another delimiter or to force a
delimiter, `-d` option along with the delimiter may be passed to csvread.

For example, to force csvread to use the carrot (`^`) as the delimiter:
```sh
$ csvread -d^ names.csv
ID    : 1
NAME  : John
EMAIL : john@email.com
TEL   : 111-111-1111

ID    : 2
NAME  : Jane
EMAIL : jane@email.com
TEL   : 222-222-2222
```

csvread's output can be piped to [cgrep] to filter records by its field value:
```sh
$ csvread names.csv | cgrep "^NAME *: John$"
ID    : 1
NAME  : John
EMAIL : john@email.com
TEL   : 111-111-1111
```

## Usage
```
NAME
       csvread - print csv rows in a more human-readable format

SYNOPSIS
       csvread [-h] [-n] [-s] [-d DELIM] [-t LIB] [FILE [FILE ...]]

DESCRIPTION
       csvread  displays  a  comma-separated value (csv) file FILE in a more readable format.  It
       prints one value per line, prefixed by the column name.  An empty line is printed  between
       the records to serve as the record separator.

       This  purpose of this layout is to make it easier to associate each value with its column.
       The layout can also be used to grep for a specific column or columns.  Its output  can  be
       piped to cgrep(1) to look for records containing a value in a specific column.

   Options
       -h, --help
              Output a usage message and exit.

       -n, --no-header
              The  file  contains  no  header.  The values are numbered by their column positions
              instead.

       -s, --strip-quotes
              Strip quotes from field values.

       -d DELIM, --delim=DELIM
              Use DELIM as the value delimiter, where DELIM may be 'p' for the pipe (|), 't'  for
              the  tab  (\t),  'a'  for the SOH (ASCII 1), or other string literal of one or more
              characters and Python string escape sequences.  DELIM may  include  escape  charac-
              ters.   By  default  the delimiter is guessed from the characters in the CSV_DELIMS
              environment variable.

       -t LIB, --translator=LIB
              Use the plugin library LIB to preprocess the values before display.  LIB may be the
              full path to the library without the .py suffix, or it may just be the library name
              in which case CSV_PLUGINS_PATH is searched for the library.

   Environment Variables
       CSV_DELIMS
              A set of characters used to guess the delimiter of a csv file.  The guesswork  hap-
              pens  when  reading  the  first  line  of the first FILE, by testing each character
              present in CSV_DELIMS for the character with the most occurrence in the  line.   If
              any  of the characters occur the same number of times (including zero), the earlier
              character in the variable is chosen.  If the environment variable is  not  set,  it
              defaults to ',\t|\x0001'.  CSV_DELIMS may include escape characters.

       CSV_PLUGINS_PATH
              A colon-separated list of directories in which the plugin library is searched.

SEE ALSO
       cgrep(1)
```

## Translation Library

A plugin library may be specified to translate the values before they are
output.

As an example, csvread provides a plugin to translate [FIX] messages.  FIX
messages do not have headers, so use the `-n` option along with the `-t` option
to load the `fix` library in the `plugins` directory:
```sh
$ csvread -ntplugins/fix fixmessages.csv
```
... which takes the following content in fixmessages.csv:
```
8=FIX.4.2,35=D,49=CLIENT,56=BROKER,54=1,38=7000,55=AMZN,40=1
```
... to produces the following output:
```
8    BeginString  : FIX.4.2
35   MsgType      : D .. NewOrderSingle
49   SenderCompID : CLIENT
56   TargetCompID : BROKER
54   Side         : 1 .. Buy
38   OrderQty     : 7000
55   Symbol       : AMZN
40   OrdType      : 1 .. Market
```
To specify the library by its base name (without qualifying it by its path) set
the `CSV_PLUGINS_PATH` environment variable to the directory containing the
plugins.

[cgrep]: https://github.com/markuskimius/cgrep
[FIX]: http://fiximate.fixtrading.org/
