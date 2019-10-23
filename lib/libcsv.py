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
    def __init__(self, file, delim=None, has_header=True):
        self.__file = file
        self.__rownum = 0
        self.__colnames = None
        self.__memoized_delim = delim
        self.__memoized_row_re = None
        self.__memoized_field_re = None

        if has_header:
            self.__colnames = self.__read_row()

    def __iter__(self):
        while True:
            row = self.__read_row()
            if row is None: break

            yield row

    def __read_row(self):
        rownum = self.__rownum
        line = ''

        # A row may consist of multiple lines, so this loop reads them all.
        # In most cases it will break after reading one line.
        while True:
            next = self.__file.readline()
            if next == '': break        # Break on EOF

            row_re = self.__row_re(next)
            line += next

            # Break on a valid row
            if row_re.match(line): break

        if line == '':
            row = None
        else:
            line = line.rstrip('\r\n')
            values = self.__split_line(line)
            delim = self.__delim(line)
            self.__rownum += 1

            row = Row(rownum, self.__colnames, values, delim)

        return row

    def __split_line(self, line):
        delim = self.__delim(line)
        field_re = self.__field_re(line)

        rawfields = line.split(delim)
        fields = []
        last = ''

        # Join fields containing delimiters
        for f in rawfields:
            if len(last):
                last += delim + f

                if(field_re.match(last)):
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

    def __delim(self, line):
        '''
        Return the delimiter with which the class was instantiated, if any,
        otherwise guess one from the list of possible delimiters DELIM and the
        last read line.  The guess is memoized for future calls.
        '''
        if self.__memoized_delim is None:
            guesses = DELIMS.encode().decode('unicode_escape')
            delim = guesses[0]   # Default to the first guess
            count = 0

            for g in guesses:
                if line.count(g) > count:
                    count = line.count(g)
                    delim = g

            self.__memoized_delim = delim

        return self.__memoized_delim

    def __row_re(self, line):
        '''
        Return the regular expression that matches a row.  The `line` parameter
        is required to guess the delimiter for the file.
        '''
        if not self.__memoized_row_re:
            delim = self.__delim(line)

            unquoted_field_re = r'[^%s"]*' % delim
            quoted_field_re = r'"(?:[^"]|"")*"'
            field_re = r'(?:%s)|(?:%s)' % (unquoted_field_re, quoted_field_re)
            row_re = r'(?:%s)(?:%s(?:%s))*' % (field_re, re.escape(delim), field_re)

            self.__memoized_row_re = re.compile(r'^(%s)$' % row_re)

        return self.__memoized_row_re

    def __field_re(self, line):
        '''
        Return the regular expression that matches a field.  The `line`
        parameter is required to guess the delimiter for the file.
        '''
        if not self.__memoized_field_re:
            delim = self.__delim(line)

            unquoted_field_re = r'[^%s"]*' % delim
            quoted_field_re = r'"(?:[^"]|"")*"'
            field_re = r'(?:%s)|(?:%s)' % (unquoted_field_re, quoted_field_re)

            self.__memoized_field_re = re.compile(r'^(%s)$' % field_re)

        return self.__memoized_field_re


##############################################################################
# CSV ROW

class Row(object):
    def __init__(self, rownum, colnames, values, delim):
        self.__rownum = rownum
        self.__colnames = colnames
        self.__values = values
        self.__delim = delim

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

        if num < len(values):
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

