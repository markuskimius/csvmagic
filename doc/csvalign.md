# csvalign
A command line utility to display csv file with its columns aligned.


## Motivation

csv files often have these readability problems:

- csv files are hard to read because the columns don't always align.

One way to solve such problem is to display the csv file with its columns
aligned.  csvalign is such utility.


## Basic Usage

Given the following csv file,
```csv
ID,FIRST_NAME,LAST_NAME,EMAIL,TEL
1001,John,Doe,jdoe@email.com,111-111-1111
1002,Jane,Smith,jsmith@email.com,222-222-2222
```

Running csvalign gives the following output:
```sh
$ csvalign users.csv
ID    FIRST_NAME  LAST_NAME  EMAIL             TEL
1001  John        Doe        jdoe@email.com    111-111-1111
1002  Jane        Smith      jsmith@email.com  222-222-2222
```


## Adjusting Spacing

By default, csvalign pads spacing between column with 2 spaces.  To change the
padding, pass the `-p` option. For example, to space columns with a single space instead:

```sh
$ csvalign -p ' ' users.csv
ID   FIRST_NAME LAST_NAME EMAIL            TEL
1001 John       Doe       jdoe@email.com   111-111-1111
1002 Jane       Smith     jsmith@email.com 222-222-2222
```

or to pad them with the vertical bar `|`:

```sh
$ csvalign -p '|' users.csv
ID  |FIRST_NAME|LAST_NAME|EMAIL           |TEL
1001|John      |Doe      |jdoe@email.com  |111-111-1111
1002|Jane      |Smith    |jsmith@email.com|222-222-2222
```


## Alternate Delimiter

By default, csvalign guess the delimiter from the comma, tab, pipe, or the SOH
(ASCII 1) characters.  To use another delimiter or to force a delimiter, use
the `-d` option.

For example, if the file `users.rsv` were using the carrot (`^`) as the
delimiter:
```sh
$ csvalign -d^ users.rsv
ID    FIRST_NAME  LAST_NAME  EMAIL             TEL
1001  John        Doe        jdoe@email.com    111-111-1111
1002  Jane        Smith      jsmith@email.com  222-222-2222
```

It is also possible to tell csvalign to use an alternate set of characters from
which the guess a file's delimiter by setting the environment variable
`CSV_DELIMS`.  For example, to tell csvalign to guess delimiters from a comma and
a carrot in BASH:

```sh
$ export CSV_DELIMS=,^
$ csvalign users.rsv
ID    FIRST_NAME  LAST_NAME  EMAIL             TEL
1001  John        Doe        jdoe@email.com    111-111-1111
1002  Jane        Smith      jsmith@email.com  222-222-2222
```

## Man Page
```
NAME
       csvalign - print csv rows with its columns aligned

SYNOPSIS
       csvalign [-h] [-p PADDING] [-w WIDTHS] [-d DELIM] [FILE [FILE ...]]

DESCRIPTION
       csvalign displays a comma-separated value (csv) file FILE with its columns aligned.

       This  purpose of this layout is to make it easier to associate each value with its col-
       umn.

   Options
       -h, --help
              Output a usage message and exit.

       -p PADDING, --padding=PADDING
              Use PADDING as the padding between the columns.  The default is two spaces.

       -w WIDTHS, --width=WIDTHS
              By default, csvalign reads the entire csv file  into  memory  to  calculate  the
              width  of each column before outputting the file.  To avoid reading the contents
              of the file into memory first, the widths of the columsn may be manually  speci-
              fied using this option.

              WIDTHS  is  a  comma-separated list of integers.  A negative integer denotes the
              width that is left aligned.  A positive  intger  is  the  width  that  is  right
              aligned.  The last integer in the list is the default width of columns after the
              columns with the width specified.

   Environment Variables
       CSV_DELIMS
              A set of characters used to guess the delimiter of a csv  file.   The  guesswork
              happens when reading the first line of the first FILE, by testing each character
              present in CSV_DELIMS for the character with the most occurrence  in  the  line.
              If  any  of  the characters occur the same number of times (including zero), the
              earlier character in the variable is chosen.  If the environment variable is not
              set, it defaults to ',\t|\x0001'.  CSV_DELIMS may include escape characters.

SEE ALSO
       csvread(1), csvcut(1)
```

