"""A csv library for Python.

https://github.com/markuskimius/csvutils
"""

import os
import re
import sys

__copyright__ = 'Copyright 2019 Mark Kim'
__license__ = 'Apache 2.0'


##############################################################################
# GLOBALS

# Delimiters tested when autodetecting the file's delimiter
DELIMS = os.environ.get('CSV_DELIMS', ',\\t|\\u0001')


##############################################################################
# CSV READER

class Reader(object):
    def __init__(self, file, delim=None, has_header=False):
        self.__file = file
        self.__rownum = 0
        self.__firstrow = None
        self.__memoized_delim = None
        self.__memoized_row_re = None
        self.__memoized_field_re = None
        self.__has_header = has_header

        if delim is not None:
            self.__memoize(delim)

        if has_header:
            self.__read_row()

    def header(self):
        return self.__firstrow

    def next(self):
        return self.__read_row()

    def __next__(self):
        return self.__read_row()

    def __iter__(self):
        while True:
            row = self.__read_row()
            if row is None: break

            yield row

    def __read_row(self):
        line = ''

        # A row may consist of multiple lines, so this loop reads them all.
        # In most cases it should break after reading one line.
        while True:
            next = self.__file.readline()
            line += next

            if next == '': break                          # Break on EOF
            if self.__is_row(line.rstrip('\r\n')): break  # Break on valid row

        if line == '':
            row = None
        else:
            values = self.__split_line(line.rstrip('\r\n'))
            cols = self.__firstrow

            row = Row(self.__rownum, cols, values, self.__memoized_delim)
            self.__rownum += 1

        # Save the first row with possible column names
        if self.__has_header and not self.__firstrow and row is not None:
            # Recreate the row with column names
            row = Row(self.__rownum, row, values, self.__memoized_delim)
            self.__firstrow = row

        return row

    def __is_row(self, line):
        is_row = False

        # Use the memoized regex, if any
        if self.__memoized_row_re:
            is_row = self.__memoized_row_re.match(line)

        # Otherwise determine the regex and memoize it
        else:
            delims = DELIMS.encode().decode('unicode_escape')
            best_delim = None
            best_count = 0

            for d in delims:
                count = line.count(d)

                if count > best_count:
                    best_delim = d
                    best_count = count

            if best_delim is not None:
                regex = self.__mk_regex(best_delim)

                if regex['row_re'].match(line):
                    is_row = True

            if is_row:
                self.__memoize(best_delim)
            else:
                sys.stderr.write('Unable to guess delimiter, please specify one with --delim\n')
                sys.exit(1)

        return is_row
        
    def __mk_regex(self, delim):
        unquoted_field_r = r'[^%s"]*' % delim
        quoted_field_r = r'"(?:[^"]|"")*"'
        field_r = r'(?:%s)|(?:%s)' % (unquoted_field_r, quoted_field_r)
        row_r = r'(?:%s)(?:%s(?:%s))*' % (field_r, re.escape(delim), field_r)

        regexes = dict(
            row_re = re.compile(r'^(%s)$' % row_r),
            field_re = re.compile(r'^(%s)$' % field_r)
        )

        return regexes

    def __memoize(self, delim):
        regex = self.__mk_regex(delim)

        self.__memoized_delim = delim
        self.__memoized_row_re = regex['row_re']
        self.__memoized_field_re = regex['field_re']

    def __split_line(self, line):
        delim = self.__memoized_delim
        field_re = self.__memoized_field_re

        rawfields = line.split(delim)
        fields = []
        last = ''

        # Join fields containing delimiters
        for f in rawfields:
            if len(last):
                last += delim + f

                if field_re.match(last):
                    fields.append(last)
                    last = ''
            elif field_re.match(f):
                fields.append(f)
            else:
                last = f

        # Clean up
        if len(last):
            fields.append(last)

        return fields


##############################################################################
# CSV ROW

class Row(object):
    def __init__(self, rownum, colnames, values, delim):
        self.__rownum = rownum
        self.__colnames = colnames
        self.__values = values
        self.__delim = delim

    def header(self):
        return self.__colnames

    def delim(self):
        return self.__delim

    def rownum(self):
        return self.__rownum

    def as_list(self):
        return self.__values

    def as_dict(self):
        mydict = dict()
        values = self.__values
        colnames = self.__colnames
        colcount = max(len(values), len(colnames or []))

        for num in range(colcount):
            key = colnames[num] if colnames else None
            val = values[num] if num < len(values) else None

            mydict[key] = val

        return mydict

    def index(self, val):
        return self.__values.index(val)

    def __len__(self):
        return len(self.__values)

    def __getitem__(self, key):
        colnames = self.__colnames
        values = self.__values
        cell = None

        if isinstance(key, slice):
            raise Exception('Slice is not supported')
        elif isinstance(key, str):
            num = colnames.index(key)
        else:
            num = key

        if num < 0:
            num += len(colnames)

        if 0 <= num and num < len(values):
            name = colnames[num].value() if colnames else None
            val = values[num] if num < len(values) else None
            cell = Cell(self.__rownum, name, num, val)

        return cell

    def __iter__(self):
        colnames = self.__colnames

        for num, val in enumerate(self.__values):
            name = colnames[num].value() if colnames and num < len(colnames) else None

            yield Cell(self.__rownum, name, num, val)

    def __str__(self):
        return self.__delim.join(self.__values)


##############################################################################
# CSV CELL

class Cell(object):
    __quoted_field_re = re.compile(r'^"(.*)"$')

    def __init__(self, rownum, colname, colnum, value):
        self.__rownum = rownum
        self.__colname = colname
        self.__colnum = colnum
        self.__value = value

    def stripped(self):
        return self.__quoted_field_re.sub(r'\1', self.__value)

    def colname(self):
        return self.__colname

    def colnum(self):
        return self.__colnum

    def rownum(self):
        return self.__rownum

    def value(self):
        return self.__value

    def __str__(self):
        return self.__value

