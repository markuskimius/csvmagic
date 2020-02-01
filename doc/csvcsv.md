# csvcsv
A command line utility to convert a csv file from one variant to another.


## Motivation

Although there exists a [formal csv standard], in practice there are many
variations of csv formats.  This utility converts csv files between some of the
common variants so utilities written for one variant can be used with csv
file in another variant format.


## Basic Usage

Given the following csv file,

```csv
ID,NAME,EMAIL,TEL
1001,"Doe, John","jdoe@email.com","111-111-1111"
1002,"Smith, Jane","jsmith@email.com","222-222-2222"
```

csvcsv can strip quotes from all values using the *strip* option, `-s`:

```sh
$ csvcsv -s users.csv
ID,NAME,EMAIL,TEL
1001,Doe, John,jdoe@email.com,111-111-1111
1002,Smith, Jane,jsmith@email.com,222-222-2222
```

But stripping quotes from all values can cause a loss of information if the
value contains a special character such as the comma or newline, as can be seen
above in the `NAME` column.  To strip quotes from all values except where it
can cause loss of information, use the *minimally quote* option, `-m`:

```sh
$ csvcsv -m users.csv
ID,NAME,EMAIL,TEL
1001,"Doe, John",jdoe@email.com,111-111-1111
1002,"Smith, Jane",jsmith@email.com,222-222-2222
```

csvcsv can also add quotes to all values using the quote option `-q`, or quote
only non-numeric values using the autoquote option `-a`:

```sh
$ csvcsv -q users.csv
"ID","NAME","EMAIL","TEL"
"1001","Doe, John","jdoe@email.com","111-111-1111"
"1002","Smith, Jane","jsmith@email.com","222-222-2222"
```

```sh
$ csvcsv -a users.csv
"ID","NAME","EMAIL","TEL"
1001,"Doe, John","jdoe@email.com","111-111-1111"
1002,"Smith, Jane","jsmith@email.com","222-222-2222"
```

See the man page for more options and information.


[formal csv standard]: https://tools.ietf.org/html/rfc4180
