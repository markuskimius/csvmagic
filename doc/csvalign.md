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

