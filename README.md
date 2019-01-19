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

If the file uses an alternate delimiter (say, a tab):
```sh
$ csvread -d\\t names.csv
ID    : 1
NAME  : John
EMAIL : john@email.com
TEL   : 111-111-1111

ID    : 2
NAME  : Jane
EMAIL : jane@email.com
TEL   : 222-222-2222
```
The output can be piped to [cgrep] to filter records by its field value:
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
       csvread - print csv rows in a human-readable format

SYNOPSIS
       csvread [-h] [-s] [-n] [-d DELIM] [-l LIB] [-p PATH] [FILE [FILE ...]]

DESCRIPTION
       csvread  displays  a  comma-separated value (csv) file FILE in a more readable format.  It
       prints one value per line, prefixed by the header that corresponds to the value's  column,
       where  the  header  is  the first row of the file and is not printed separately.  An empty
       line is printed between the last value of each row and the first value of  the  next  row,
       serving as a record separator.

       This  purpose  of  this  layout is to make it clear which values in the file correspond to
       which headers.  The layout can also be used to grep for  a  specific  column  or  columns.
       Piping  its  output to cgrep(1), the layout can look for records containing certain values
       in certain columns.

   Options
       -h, --help
              Output a usage message and exit.

       -s, --strip-quotes
              Strip quotes from field values.

       -n, --no-header
              The file contains no header.  The values are numbered  by  their  column  positions
              instead.

       -d DELIM, --delim=DELIM
              Use DELIM as the value delimiter instead of a comma.

       -l LIB, --lib=LIB
              Use  the  plugin  library LIB to preprocess header(s) and/or values before display.
              Useful for enriching symbols in values or headers with a description of their mean‐
              ing.   LIB may be a full path to the library without the .py suffix, or it may just
              be the library name in which case the appropriate paths are searched.

       -p PATH, --path=PATH
              Search for the plugin library in PATH.

   Variables
       CSV_LIBRARY_PATH
              A colon-separated list of directories in which the plugin library is searched.

SEE ALSO
       cgrep(1)
```

## Library

Plugin libraries may be specified to preprocess a header or value before they
are printed. Such library can be used to translate symbols to better
descriptions.

For example, csvread comes with a plugin library to translate [FIX] messages.
FIX messages do not have headers, so use the `-n` option along with the `-l`
option to load the `fix` library in the `plugins` directory:
```sh
$ csvread -nlplugins/fix fixmessages.csv
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

[cgrep]: https://github.com/markuskimius/cgrep
[FIX]: http://fiximate.fixtrading.org/
