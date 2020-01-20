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
    def __init__(self, file, delim=None, has_header=False, is_multitable=False):
        self.__init_delim = delim
        self.__has_header = has_header
        self.__is_multitable = is_multitable
        self.__file = file

        self.__reset()

    def __reset(self):
        self.__rownum = 0
        self.__firstrow = None
        self.__is_sot = False

        if self.__init_delim is None:
            self.__delim = None
            self.__row_re = None
            self.__field_re = None
        else:
            self.__setdelim(self.__init_delim)

        if self.__has_header:
            self.__readrow()

    def header(self):
        if self.__has_header and self.__is_sot:
            self.__readrow()

        return self.__firstrow

    def next(self):
        return self.__readrow()

    def __next__(self):
        return self.__readrow()

    def __iter__(self):
        while True:
            row = self.__readrow()
            if row is None: break

            yield row

    def __readrow(self):
        gotline = False
        row = None
        buf = ''

        # reset at the start of a new table
        if self.__is_sot:
            self.__reset()

        while True:
            line = self.__readline()
            if line is None: break

            if gotline: buf += '\n'
            buf += line

            gotline = True

            if self.__is_validrow(buf): break

        if gotline:
            values = self.__split(buf) if len(buf) else []
            header = self.__firstrow

            # empty line starts a new table on next reading
            if len(values) == 0 and self.__is_multitable:
                self.__is_sot = True

            # current row becomes the header if header not already set
            if header is None and self.__has_header:
                header = Row(self.__rownum, header, values, self.__delim)

            row = Row(self.__rownum, header, values, self.__delim)
            self.__rownum += 1

            if self.__firstrow is None and self.__has_header:
                self.__firstrow = row

        return row

    def __readline(self):
        line = self.__file.readline()

        if line == '':
            line = None
        else:
            line = line.rstrip('\n')

        if self.__delim is None and line is not None:
            self.__guessdelim(line)

        return line

    def __guessdelim(self, buf):
        delims = DELIMS.encode().decode('unicode_escape')
        best_delim = None
        best_count = 0
        
        for d in delims:
            count = buf.count(d)

            if count > best_count:
                best_delim = d
                best_count = count

        if best_delim is None:
            sys.stderr.write('Unable to guess the delimiter, please specify one with --delim\n')
            sys.exit(1)
        else:
            self.__setdelim(best_delim)

    def __setdelim(self, delim):
        unquoted_field_r = r'[^%s"]*' % delim
        quoted_field_r = r'"(?:[^"]|"")*"'
        field_r = r'(?:%s)|(?:%s)' % (unquoted_field_r, quoted_field_r)
        row_r = r'(?:%s)(?:%s(?:%s))*' % (field_r, re.escape(delim), field_r)
        row_re = re.compile(r'^(%s)$' % row_r)
        field_re = re.compile(r'^(%s)$' % field_r)

        self.__delim = delim
        self.__row_re = row_re
        self.__field_re = field_re

    def __is_validrow(self, buf):
        return self.__row_re.match(buf)

    def __split(self, buf):
        rawfields = buf.split(self.__delim)
        fields = []
        last = ''

        for f in rawfields:
            if len(last):
                last += self.__delim + f

                if self.__field_re.match(last):
                    fields.append(last)
                    last = ''
            elif self.__field_re.match(f):
                fields.append(f)
            else:
                last = f

        if len(last):
            fields.append(last)

        return fields


##############################################################################
# CSV ROW

class Row(object):
    def __init__(self, rownum, header, values, delim):
        self.__rownum = rownum
        self.__header = header
        self.__values = values
        self.__delim = delim

    def header(self):
        return self.__header

    def delim(self):
        return self.__delim

    def rownum(self):
        return self.__rownum

    def as_list(self):
        return self.__values

    def as_dict(self):
        mydict = dict()
        values = self.__values
        header = self.__header.as_list() if self.__header else []
        colcount = max(len(values), len(header))

        for num in range(colcount):
            key = header[num] if header else num
            val = values[num] if num < len(values) else None

            mydict[key] = val

        return mydict

    def index(self, val):
        return self.__values.index(val)

    def __len__(self):
        return len(self.__values)

    def __getitem__(self, key):
        header = self.__header
        values = self.__values
        cell = None

        if isinstance(key, slice):
            raise Exception('Slice is not supported')
        elif isinstance(key, str):
            num = header.index(key)
        else:
            num = key

        if num < 0:
            num += len(header)

        if 0 <= num and num < len(values):
            name = header[num].value() if header and header[num] else None
            val = values[num] if num < len(values) else None
            cell = Cell(self.__rownum, name, num, val)

        return cell

    def __iter__(self):
        header = self.__header

        for num, val in enumerate(self.__values):
            name = header[num].value() if header and num < len(header) else None

            yield Cell(self.__rownum, name, num, val)

    def __str__(self):
        return self.__delim.join(self.__values)


##############################################################################
# CSV CELL

class Cell(object):
    __quoted_field_re = re.compile(r'^"((.|\s)*)"$')

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

