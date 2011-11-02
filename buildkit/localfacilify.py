# -*- encoding: utf8 -*-

"""\
We want to build two versions of this script:

* This one
* One with all comments, docstrings, log statements etc removed

Ideas:

* You can put pdb anywhere, including doctests to debug
* You can override the entire way command help works with a function that
  takes the command too
"""

import os
try:
    rows, columns = os.popen('stty size', 'r').read().split()
    default_wrap_width = int(columns)
except:
    default_wrap_width = 78

import warnings 
if 'set' not in __builtins__.keys():
    from sets import Set as set
else:
    set = __builtins__['set']

# Used in the doctests
from pprint import pprint
import logging
import StringIO
log = logging.getLogger('facilify')

def pretty(var):
    stream = StringIO.StringIO()
    if isinstance(var, OrderedDict):
        pprint(var.items(), stream)
        return u'OrderedDict(%s)'%stream.getvalue()
    else:
        pprint(var, stream)
        return stream.getvalue()

#############################################################################
#
# Reserved words
# (originally from recordconvert.reserved)
#

"""\
A set of words which should not be used as record keys in case they conflict
with keywords in SQL, Python or JavaScript.
"""

#
# Reserved Words (Generated in such a way that words should be easy to update)
#

# http://www.python.org/doc/2.5.2/ref/keywords.html
_python_reserved_words = [x.strip('\n ') for x in """
    and       del       from      not       while
    as        elif      global    or        with
    assert    else      if        pass      yield
    break     except    import    print
    class     exec      in        raise
    continue  finally   is        return
    def       for       lambda    try
""".replace('\n', ' ').split(' ')]

# http://dev.mysql.com/doc/mysqld-version-reference/en/mysqld-version-reference-reservedwords-5-0.html
_mysql_reserved_words = [x.strip() for x in """\
ADD ALL ALTER ANALYZE AND AS ASC ASENSITIVE BEFORE BETWEEN BIGINT BINARY BLOB
BOTH BY CALL CASCADE CASE CHANGE CHAR CHARACTER CHECK COLLATE COLUMN COLUMNS
CONDITION CONNECTION CONSTRAINT CONTINUE CONVERT CREATE CROSS CURRENT_DATE
CURRENT_TIME CURRENT_TIMESTAMP CURRENT_USER CURSOR DATABASE DATABASES DAY_HOUR
DAY_MICROSECOND DAY_MINUTE DAY_SECOND DEC DECIMAL DECLARE DEFAULT DELAYED
DELETE DESC DESCRIBE DETERMINISTIC DISTINCT DISTINCTROW DIV DOUBLE DROP DUAL
EACH ELSE ELSEIF ENCLOSED ESCAPED EXISTS EXIT EXPLAIN FALSE FETCH FIELDS FLOAT
FLOAT4 FLOAT8 FOR FORCE FOREIGN FROM FULLTEXT GOTO GRANT GROUP HAVING
HIGH_PRIORITY HOUR_MICROSECOND HOUR_MINUTE HOUR_SECOND IF IGNORE IN INDEX
INFILE INNER INOUT INSENSITIVE INSERT INT INT1 INT2 INT3 INT4 INT8 INTEGER
INTERVAL INTO IS ITERATE JOIN KEY KEYS KILL LABEL LEADING LEAVE LEFT LIKE LIMIT
LINES LOAD LOCALTIME LOCALTIMESTAMP LOCK LONG LONGBLOB LONGTEXT LOOP
LOW_PRIORITY MATCH MEDIUMBLOB MEDIUMINT MEDIUMTEXT MIDDLEINT MINUTE_MICROSECOND
MINUTE_SECOND MOD MODIFIES NATURAL NOT NO_WRITE_TO_BINLOG NULL NUMERIC ON
OPTIMIZE OPTION OPTIONALLY OR ORDER OUT OUTER OUTFILE PRECISION PRIMARY
PRIVILEGES PROCEDURE PURGE READ READS REAL REFERENCES REGEXP RELEASE RENAME
REPEAT REPLACE REQUIRE RESTRICT RETURN REVOKE RIGHT RLIKE SCHEMA SCHEMAS
SECOND_MICROSECOND SELECT SENSITIVE SEPARATOR SET SHOW SMALLINT SONAME SPATIAL
SPECIFIC SQL SQLEXCEPTION SQLSTATE SQLWARNING SQL_BIG_RESULT
SQL_CALC_FOUND_ROWS SQL_SMALL_RESULT SSL STARTING STRAIGHT_JOIN TABLE TABLES
TERMINATED THEN TINYBLOB TINYINT TINYTEXT TO TRAILING TRIGGER TRUE UNDO UNION
UNIQUE UNLOCK UNSIGNED UPDATE UPGRADE USAGE USE USING UTC_DATE UTC_TIME
UTC_TIMESTAMP VALUES VARBINARY VARCHAR VARCHARACTER VARYING WHEN WHERE WHILE
WITH WRITE XOR YEAR_MONTH ZEROFILL""".split(' ')]

# All keywords, reserved or not from PostgreSQL 8.3, SQL92, SQL99 and SQL2003
# http://www.postgresql.org/docs/8.3/static/sql-keywords-appendix.html
_postgresql_keywords = [x.strip() for x in """\
A ABORT ABS ABSOLUTE ACCESS ACTION ADA ADD ADMIN AFTER AGGREGATE ALIAS ALL
ALLOCATE ALSO ALTER ALWAYS ANALYSE ANALYZE AND ANY ARE ARRAY AS ASC ASENSITIVE
ASSERTION ASSIGNMENT ASYMMETRIC AT ATOMIC ATTRIBUTE ATTRIBUTES AUTHORIZATION
AVG BACKWARD BASE64 BEFORE BEGIN BERNOULLI BETWEEN BIGINT BINARY BIT BITVAR
BIT_LENGTH BLOB BOOLEAN BOTH BREADTH BY C CACHE CALL CALLED CARDINALITY CASCADE
CASCADED CASE CAST CATALOG CATALOG_NAME CEIL CEILING CHAIN CHAR CHARACTER
CHARACTERISTICS CHARACTERS CHARACTER_LENGTH CHARACTER_SET_CATALOG
CHARACTER_SET_NAME CHARACTER_SET_SCHEMA CHAR_LENGTH CHECK CHECKED CHECKPOINT
CLASS CLASS_ORIGIN CLOB CLOSE CLUSTER COALESCE COBOL COLLATE COLLATION
COLLATION_CATALOG COLLATION_NAME COLLATION_SCHEMA COLLECT COLUMN COLUMN_NAME
COMMAND_FUNCTION COMMAND_FUNCTION_CODE COMMENT COMMIT COMMITTED COMPLETION
CONCURRENTLY CONDITION CONDITION_NUMBER CONFIGURATION CONNECT CONNECTION
CONNECTION_NAME CONSTRAINT CONSTRAINTS CONSTRAINT_CATALOG CONSTRAINT_NAME
CONSTRAINT_SCHEMA CONSTRUCTOR CONTAINS CONTENT CONTINUE CONVERSION CONVERT COPY
CORR CORRESPONDING COST COUNT COVAR_POP COVAR_SAMP CREATE CREATEDB CREATEROLE
CREATEUSER CROSS CSV CUBE CUME_DIST CURRENT CURRENT_DATE
CURRENT_DEFAULT_TRANSFORM_GROUP CURRENT_PATH CURRENT_ROLE CURRENT_TIME
CURRENT_TIMESTAMP CURRENT_TRANSFORM_GROUP_FOR_TYPE CURRENT_USER CURSOR
CURSOR_NAME CYCLE DATA DATABASE DATE DATETIME_INTERVAL_CODE
DATETIME_INTERVAL_PRECISION DAY DEALLOCATE DEC DECIMAL DECLARE DEFAULT DEFAULTS
DEFERRABLE DEFERRED DEFINED DEFINER DEGREE DELETE DELIMITER DELIMITERS
DENSE_RANK DEPTH DEREF DERIVED DESC DESCRIBE DESCRIPTOR DESTROY DESTRUCTOR
DETERMINISTIC DIAGNOSTICS DICTIONARY DISABLE DISCARD DISCONNECT DISPATCH
DISTINCT DO DOCUMENT DOMAIN DOUBLE DROP DYNAMIC DYNAMIC_FUNCTION
DYNAMIC_FUNCTION_CODE EACH ELEMENT ELSE ENABLE ENCODING ENCRYPTED END END-EXEC
ENUM EQUALS ESCAPE EVERY EXCEPT EXCEPTION EXCLUDE EXCLUDING EXCLUSIVE EXEC
EXECUTE EXISTING EXISTS EXP EXPLAIN EXTERNAL EXTRACT FALSE FAMILY FETCH FILTER
FINAL FIRST FLOAT FLOOR FOLLOWING FOR FORCE FOREIGN FORTRAN FORWARD FOUND FREE
FREEZE FROM FULL FUNCTION FUSION G GENERAL GENERATED GET GLOBAL GO GOTO GRANT
GRANTED GREATEST GROUP GROUPING HANDLER HAVING HEADER HEX HIERARCHY HOLD HOST
HOUR IDENTITY IF IGNORE ILIKE IMMEDIATE IMMUTABLE IMPLEMENTATION IMPLICIT IN
INCLUDING INCREMENT INDEX INDEXES INDICATOR INFIX INHERIT INHERITS INITIALIZE
INITIALLY INNER INOUT INPUT INSENSITIVE INSERT INSTANCE INSTANTIABLE INSTEAD
INT INTEGER INTERSECT INTERSECTION INTERVAL INTO INVOKER IS ISNULL ISOLATION
ITERATE JOIN K KEY KEY_MEMBER KEY_TYPE LANCOMPILER LANGUAGE LARGE LAST LATERAL
LEADING LEAST LEFT LENGTH LESS LEVEL LIKE LIMIT LISTEN LN LOAD LOCAL LOCALTIME
LOCALTIMESTAMP LOCATION LOCATOR LOCK LOGIN LOWER M MAP MAPPING MATCH MATCHED
MAX MAXVALUE MEMBER MERGE MESSAGE_LENGTH MESSAGE_OCTET_LENGTH MESSAGE_TEXT
METHOD MIN MINUTE MINVALUE MOD MODE MODIFIES MODIFY MODULE MONTH MORE MOVE
MULTISET MUMPS NAME NAMES NATIONAL NATURAL NCHAR NCLOB NESTING NEW NEXT NO
NOCREATEDB NOCREATEROLE NOCREATEUSER NOINHERIT NOLOGIN NONE NORMALIZE
NORMALIZED NOSUPERUSER NOT NOTHING NOTIFY NOTNULL NOWAIT NULL NULLABLE NULLIF
NULLS NUMBER NUMERIC OBJECT OCTETS OCTET_LENGTH OF OFF OFFSET OIDS OLD ON ONLY
OPEN OPERATION OPERATOR OPTION OPTIONS OR ORDER ORDERING ORDINALITY OTHERS OUT
OUTER OUTPUT OVER OVERLAPS OVERLAY OVERRIDING OWNED OWNER PAD PARAMETER
PARAMETERS PARAMETER_MODE PARAMETER_NAME PARAMETER_ORDINAL_POSITION
PARAMETER_SPECIFIC_CATALOG PARAMETER_SPECIFIC_NAME PARAMETER_SPECIFIC_SCHEMA
PARSER PARTIAL PARTITION PASCAL PASSWORD PATH PERCENTILE_CONT PERCENTILE_DISC
PERCENT_RANK PLACING PLANS PLI POSITION POSTFIX POWER PRECEDING PRECISION
PREFIX PREORDER PREPARE PREPARED PRESERVE PRIMARY PRIOR PRIVILEGES PROCEDURAL
PROCEDURE PUBLIC QUOTE RANGE RANK READ READS REAL REASSIGN RECHECK RECURSIVE
REF REFERENCES REFERENCING REGR_AVGX REGR_AVGY REGR_COUNT REGR_INTERCEPT
REGR_R2 REGR_SLOPE REGR_SXX REGR_SXY REGR_SYY REINDEX RELATIVE RELEASE RENAME
REPEATABLE REPLACE REPLICA RESET RESTART RESTRICT RESULT RETURN
RETURNED_CARDINALITY RETURNED_LENGTH RETURNED_OCTET_LENGTH RETURNED_SQLSTATE
RETURNING RETURNS REVOKE RIGHT ROLE ROLLBACK ROLLUP ROUTINE ROUTINE_CATALOG
ROUTINE_NAME ROUTINE_SCHEMA ROW ROWS ROW_COUNT ROW_NUMBER RULE SAVEPOINT SCALE
SCHEMA SCHEMA_NAME SCOPE SCOPE_CATALOG SCOPE_NAME SCOPE_SCHEMA SCROLL SEARCH
SECOND SECTION SECURITY SELECT SELF SENSITIVE SEQUENCE SERIALIZABLE SERVER_NAME
SESSION SESSION_USER SET SETOF SETS SHARE SHOW SIMILAR SIMPLE SIZE SMALLINT
SOME SOURCE SPACE SPECIFIC SPECIFICTYPE SPECIFIC_NAME SQL SQLCODE SQLERROR
SQLEXCEPTION SQLSTATE SQLWARNING SQRT STABLE STANDALONE START STATE STATEMENT
STATIC STATISTICS STDDEV_POP STDDEV_SAMP STDIN STDOUT STORAGE STRICT STRIP
STRUCTURE STYLE SUBCLASS_ORIGIN SUBLIST SUBMULTISET SUBSTRING SUM SUPERUSER
SYMMETRIC SYSID SYSTEM SYSTEM_USER TABLE TABLESAMPLE TABLESPACE TABLE_NAME TEMP
TEMPLATE TEMPORARY TERMINATE TEXT THAN THEN TIES TIME TIMESTAMP TIMEZONE_HOUR
TIMEZONE_MINUTE TO TOP_LEVEL_COUNT TRAILING TRANSACTION TRANSACTIONS_COMMITTED
TRANSACTIONS_ROLLED_BACK TRANSACTION_ACTIVE TRANSFORM TRANSFORMS TRANSLATE
TRANSLATION TREAT TRIGGER TRIGGER_CATALOG TRIGGER_NAME TRIGGER_SCHEMA TRIM TRUE
TRUNCATE TRUSTED TYPE UESCAPE UNBOUNDED UNCOMMITTED UNDER UNENCRYPTED UNION
UNIQUE UNKNOWN UNLISTEN UNNAMED UNNEST UNTIL UPDATE UPPER USAGE USER
USER_DEFINED_TYPE_CATALOG USER_DEFINED_TYPE_CODE USER_DEFINED_TYPE_NAME
USER_DEFINED_TYPE_SCHEMA USING VACUUM VALID VALIDATOR VALUE VALUES VARCHAR
VARIABLE VARYING VAR_POP VAR_SAMP VERBOSE VERSION VIEW VOLATILE WHEN WHENEVER
WHERE WHITESPACE WIDTH_BUCKET WINDOW WITH WITHIN WITHOUT WORK WRITE XML XMLAGG
XMLATTRIBUTES XMLBINARY XMLCOMMENT XMLCONCAT XMLELEMENT XMLFOREST XMLNAMESPACES
XMLPARSE XMLPI XMLROOT XMLSERIALIZE YEAR YES ZONE""".split(' ')]

# https://developer.mozilla.org/en/Core_JavaScript_1.5_Reference/Reserved_Words
_javascript_reserved_words = """\
break case catch continue default delete do else finally for function if in
instanceof new return switch this throw try typeof var void while with abstract
boolean byte char class const debugger double enum export extends final float
goto implements import int interface long native package private protected
public short static super synchronized throws transient volatile const export
import null true false""".split(' ')

case_insensitive_reserved_words = _python_reserved_words + _javascript_reserved_words
case_sensitive_reserved_words = _mysql_reserved_words + _postgresql_keywords

#############################################################################
#
# OrderedDict
#

try:
    from collections import OrderedDict
except ImportError:
    # From http://code.activestate.com/recipes/576693/
    from UserDict import DictMixin
    class OrderedDict(dict, DictMixin):
        def __init__(self, *args, **kwds):
            if len(args) > 1:
                raise TypeError('expected at most 1 arguments, got %d' % len(args))
            try:
                self.__end
            except AttributeError:
                self.clear()
            self.update(*args, **kwds)

        def clear(self):
            self.__end = end = []
            end += [None, end, end]         # sentinel node for doubly linked list
            self.__map = {}                 # key --> [key, prev, next]
            dict.clear(self)

        def __setitem__(self, key, value):
            if key not in self:
                end = self.__end
                curr = end[1]
                curr[2] = end[1] = self.__map[key] = [key, curr, end]
            dict.__setitem__(self, key, value)

        def __delitem__(self, key):
            dict.__delitem__(self, key)
            key, prev, next = self.__map.pop(key)
            prev[2] = next
            next[1] = prev

        def __iter__(self):
            end = self.__end
            curr = end[2]
            while curr is not end:
                yield curr[0]
                curr = curr[2]

        def __reversed__(self):
            end = self.__end
            curr = end[1]
            while curr is not end:
                yield curr[0]
                curr = curr[1]

        def popitem(self, last=True):
            if not self:
                raise KeyError('dictionary is empty')
            if last:
                key = reversed(self).next()
            else:
                key = iter(self).next()
            value = self.pop(key)
            return key, value

        def __reduce__(self):
            items = [[k, self[k]] for k in self]
            tmp = self.__map, self.__end
            del self.__map, self.__end
            inst_dict = vars(self).copy()
            self.__map, self.__end = tmp
            if inst_dict:
                return (self.__class__, (items,), inst_dict)
            return self.__class__, (items,)

        def keys(self):
            return list(self)

        setdefault = DictMixin.setdefault
        update = DictMixin.update
        pop = DictMixin.pop
        values = DictMixin.values
        items = DictMixin.items
        iterkeys = DictMixin.iterkeys
        itervalues = DictMixin.itervalues
        iteritems = DictMixin.iteritems

        def __repr__(self):
            if not self:
                return '%s()' % (self.__class__.__name__,)
            return '%s(%r)' % (self.__class__.__name__, self.iteritems())

        def copy(self):
            return self.__class__(self)

        @classmethod
        def fromkeys(cls, iterable, value=None):
            d = cls()
            for key in iterable:
                d[key] = value
            return d

        def __eq__(self, other):
            if isinstance(other, OrderedDict):
                return len(self)==len(other) and self.items() == other.items()
            return dict.__eq__(self, other)

        def __ne__(self, other):
            return not self == other

#############################################################################
#
# Advanced Wrap
#

"""\
http://code.activestate.com/recipes/267662/
Published on a recipe site under MIT license
"""

import cStringIO,operator

def indent(rows, hasHeader=False, headerChar='-', delim=' | ', justify='left',
           separateRows=False, prefix='', postfix='', wrapfunc=lambda x:x):
    """Indents a table by column.
       - rows: A sequence of sequences of items, one sequence per row.
       - hasHeader: True if the first row consists of the columns' names.
       - headerChar: Character to be used for the row separator line
         (if hasHeader==True or separateRows==True).
       - delim: The column delimiter.
       - justify: Determines how are data justified in their column.
         Valid values are 'left','right' and 'center'.
       - separateRows: True if rows are to be separated by a line
         of 'headerChar's.
       - prefix: A string prepended to each printed row.
       - postfix: A string appended to each printed row.
       - wrapfunc: A function f(text) for wrapping text; each element in
         the table is first wrapped by this function."""
    # closure for breaking logical rows to physical, using wrapfunc
    def rowWrapper(row):
        newRows = [wrapfunc(item).split('\n') for item in row]
        return [[substr or '' for substr in item] for item in map(None,*newRows)]
    # break each logical row into one or more physical ones
    logicalRows = [rowWrapper(row) for row in rows]
    # columns of physical rows
    columns = map(None,*reduce(operator.add,logicalRows))
    # get the maximum of each column by the string length of its items
    maxWidths = [max([len(str(item)) for item in column]) for column in columns]
    rowSeparator = headerChar * (len(prefix) + len(postfix) + sum(maxWidths) + \
                                 len(delim)*(len(maxWidths)-1))
    # select the appropriate justify method
    justify = {'center':str.center, 'right':str.rjust, 'left':str.ljust}[justify.lower()]
    output=cStringIO.StringIO()
    if separateRows: print >> output, rowSeparator
    for physicalRows in logicalRows:
        for row in physicalRows:
            print >> output, \
                prefix \
                + delim.join([justify(str(item),width) for (item,width) in zip(row,maxWidths)]) \
                + postfix
        if separateRows or hasHeader: print >> output, rowSeparator; hasHeader=False
    return output.getvalue()

# written by Mike Brown
# http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/148061
def wrap_onspace(text, width):
    """
    A word-wrap function that preserves existing line breaks
    and most spaces in the text. Expects that existing line
    breaks are posix newlines (\n).
    """
    return reduce(lambda line, word, width=width: '%s%s%s' %
                  (line,
                   ' \n  '[(len(line[line.rfind('\n')+1:])
                         + len(word.split('\n',1)[0]
                              ) >= width)],
                   word),
                  text.split(' ')
                 )

import re
def wrap_onspace_strict(text, width):
    """Similar to wrap_onspace, but enforces the width constraint:
       words longer than width are split."""
    wordRegex = re.compile(r'\S{'+str(width)+r',}')
    return wrap_onspace(wordRegex.sub(lambda m: wrap_always(m.group(),width),text),width)

import math
def wrap_always(text, width):
    """A simple word-wrap function that wraps text on exactly width characters.
       It doesn't split the text in words."""
    return '\n'.join([ text[width*i:width*(i+1)] \
                       for i in xrange(int(math.ceil(1.*len(text)/width))) ])

# Wrap helper from CommandTool

def two_cols(rows):
    i = [0]
    def wrapper(x):
        if len(x) < 20:
            x += (20-len(x))*' '
        i[0] += 1
        if i[0]%2:
            return wrap_onspace_strict(x, (default_wrap_width*0.4)-5)
        else:
            return wrap_onspace_strict(x, (default_wrap_width*0.6)-1)
    return indent(
        rows,
        hasHeader=False,
        prefix='  ',
        postfix='',
        headerChar='',
        delim='  ',
        separateRows=False,
        wrapfunc=wrapper
    )

def __wrap(text, width=None, pad=None):
    """\
    Helper function to wrap text used in logging
    """
    if width is None:
        return [text]
    indent = ''
    if pad is not None:
        indent = ' ' * pad
    return textwrap.wrap(
        text,
        width,
        initial_indent=indent,
        subsequent_indent=indent,
    )

def _wrap(text, args=None, width=None, pad=None):
    '''\
    Wrap a block of text, respecting existing indentation where possible

    Here's an example:

    ::

        >>> input = """
        ... Oneeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee
        ...     Twoooooooooooooooooooooooooooooooooooooooooooo
        ...         Threeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee"""
        >>> print _wrap(input, None, 40, 10)[1:]
        Oneeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee
        eeeeeeeeee
            Twoooooooooooooooooooooooooooooooooo
            oooooooooo
                Threeeeeeeeeeeeeeeeeeeeeeeeeeeee
                eeeeeeeeee

    '''
    if args:
        text = text%args
    text = text.replace('\t', '    ')
    result = []
    for line in text.split('\n'):
        if not line.strip():
            result.append('')
        else:
            pad = 0
            while line and line.startswith(' '):
                line = line[1:]
                pad += 1
            result += __wrap(line, width, pad)
    return '\n'.join(result)


#############################################################################
#
# Converters
# (based on ideas from Navl by David Raznick
# https://bitbucket.org/kindly/navl/changeset/b52af1370abc and ConversionKit)
#

import copy
import inspect
import logging

try:
    import formencode
except ImportError:
    formencode_present=False
    class Invalid(Exception):
        def __init__(self, error, key=None):
            self.error = error
    def _stdtrans(arg):
        return arg
else:
    formencode_present=True
    class Invalid(formencode.Invalid):
        def __init__(self, error, key=None):
            self.error = error
    from formencode.api import _stdtrans

class obj(dict):
    """\
    Like a normal Python dictionary, but allows keys to be accessed as
    attributes. For example:

    ::

        >>> person = obj(firstname='James')
        >>> person.firstname
        'James'
        >>> person['surname'] = 'Jones'
        >>> person.surname
        'Jones'

    """
    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError('No such attribute %r'%name)

    def __setattr__(self, name, value):
        raise AttributeError(
            'You cannot set attributes of this object directly'
        )

class ordered_obj(obj, OrderedDict):
    def __setattr__(self, name, value):
        return OrderedDict.__setattr__(self, name, value)
        #raise AttributeError(
        #    'You cannot set attributes of this object directly'
        #)

class Unusable(object):
    """\
    A class that raises an exception any time you try to access one
    of its instances attributes. The error message it raises is the set when you
    create an instance as the ``error_msg`` argument.
   
    It is useful when you want to have an object as a placeholder to represent
    some particular internal state, but where you don't expect a user of your
    API to actually access that placeholder. 

    In facilify, this class is used to create the ``missing``, ``empty_list``
    and ``extra_keys`` that are used as part of the ``validate()`` funcitons
    processing.

    Here's a simple example of how you might use it:

    ::

        >>> no_such_key = Unusable('No such key', 'yourmodule.no_such_key')
        >>> no_such_key.key
        Traceback (most recent call last):
          File ...
        Exception: No such key


    """
    # This is a bit naughty but we all want all instances with the same name
    # to be treated as equal, regardless of their id.
    def __eq__(self, other):
        if other.__class__.__name__ == self.__class__.__name__ and \
           other.__dict__['name'] == self.__dict__['name']:
            return True
        return False

    def __init__(self, error_msg, name):
        self.error_msg = error_msg
        self.name = name

    def __getattr__(self, name):
        raise Exception(self.__dict__['error_msg'])

    def __repr__(self):
        return '<%s object at 0x%s>'%(self.__dict__['name'], id(self))

Missing = ExtraKeys = EmptyList = Unusable

missing = Missing('Missing value', 'facilify.missing')
empty_list = EmptyList('Empty list', 'facilify.empty_list')
extra_keys = ExtraKeys('Extra keys', 'facilify.extra_keys')

class StopOnError(Exception):
    '''error to stop validations for a particualar key'''
    pass

def flatten_schema(schema):
    """\
    Flatten a dictionary. For example:

    ::

        >>> print pretty(flatten_schema({'one': {'two': {'three': []}}})),
        OrderedDict([(('one', 'two', 'three'), [])]
        )
    """
    log.debug('Flattening %r', schema)
    flattened = []
    for key, value in schema.iteritems():
        log.debug('Working on key %r value %r', key, value)
        if isinstance(value, dict):
            for k, v in flatten_schema(value).iteritems():
                flattened.append((tuple([key]+list(k)), v))
        else:
            flattened.append(((key,), value))
    return OrderedDict(flattened)

def flatten_list(key, list_data, schema):
    """\
    Flatten a list of dictionaries. For example:

    ::

        >>> schema = {
        ...     'one': {
        ...         'two': []
        ...     },
        ... }
        >>> flatten_list('zero', [
        ...     {'one': [{'two': 1}]},
        ...     {'one': [{'two': 2}]},
        ... ], schema)
        ((('zero', 0, 'one', 0, 'two'), 1), (('zero', 1, 'one', 0, 'two'), 2))

    """
    flattened = []
    counter = 0
    for dict_data in list_data:
        for k, v in flatten_dict(dict_data, schema):
            if isinstance(k, (str, unicode)):
                k = [k]
            else:
                k = list(k)
            flattened.append((tuple([key, counter]+k), v))
        counter += 1
    return tuple(flattened)


def flatten_dict(augmented_data, schema):
    """\
    Flatten a dictionary according to a schema.

    This function takes data that has already been augmented.

    ::

        >>> schema = {'one': {'two': []}}
        >>> flatten_dict({"one": [{"two": '2a'}, {"two": '2b'}]}, schema)
        [(('one', 0, 'two'), '2a'), (('one', 1, 'two'), '2b')]

    Flatten tries to pass through unexpected data. This allows you to use lists
    and dicts as key values as you can see in these examples.

    ::

        >>> flatten_dict(OrderedDict({"one": 1, "two":[], "three": {}, "four": empty_list}), schema)
        [(('four',), <facilify.empty_list object at 0x...>), (('three',), {}), (('two',), []), (('one',), 1)]
        >>> flatten_dict({"one": [{"two": {'data': 'dict'}}]}, schema)
        [(('one', 0, 'two'), {'data': 'dict'})]

    """
    log.debug('Flattening %r', augmented_data)
    flattened = []
    schema_counter = 0
    for key, value in augmented_data.iteritems():
        log.debug('Working on key %r value %r', key, value)
        if key == extra_keys or not schema.has_key(key) or isinstance(value, dict):
            flattened.append(((key,), value))
        elif isinstance(value, (list, tuple)):
            if isinstance(schema.get(key), dict):
                log.debug('This is a list so flattening each dictionary it contains')
                for item in flatten_list(key, value, schema[key]):
                    flattened.append(item)
            else:
                flattened.append(((key,), value))
        else:
            flattened.append(((key,), value))
    return flattened

def augment(dict_data, schema):
    """\
    Change the data structure of ``data`` *in place*. This function modifies
    the original, rather than returning a modified copy.

    ::

        >>> schema = {'one': {'two': {'three': []}}}
        >>> data = {'one': [{'two': [{'four': 3}]}, {'two': []}]}
        >>> # returns None, instead the original data is modified
        >>> augment(data, schema) is None
        True
        >>> data['one'][0]['two'][0]['three'] == missing
        True
        >>> data['one'][1]['two'] == empty_list
        True
        >>> data['one'][0]['two'][0][extra_keys] == {'four': 3}
        True
        >>> print pretty(flatten_dict(data, schema)),
        [(('one', 0, 'two', 0, <facilify.extra_keys object at 0x...>),
          {'four': 3}),
         (('one', 0, 'two', 0, 'three'), 
         <facilify.missing object at 0x...>),
         (('one', 1, 'two'), <facilify.empty_list object at 0x...>)]

    """
    log.debug('Augmenting %r according to %r', dict_data, schema)
    schema_keys = schema.keys()
    data_keys = dict_data.keys()
    log.debug(
        'Augmenting data. Schema keys: %r; Data keys: %r',
        schema_keys,
        data_keys,
    )
    # Add any missing keys
    for schema_key in schema_keys:
        if schema_key in data_keys:
            # Remove the key from the list of things we are tracking
            log.debug(
                'Found schema key %r in the dict data with value %r',
                schema_key,
                dict_data[schema_key],
            )
            data_keys.pop(data_keys.index(schema_key))
            if isinstance(schema[schema_key], dict):
                if not isinstance(dict_data[schema_key], list):
                    raise Exception(
                        'Expected %r value %r to be a list of dictionaries'%(
                            schema_key,
                            dict_data[schema_key],
                        )
                    )
                if dict_data[schema_key] == []:
                     dict_data[schema_key] = empty_list
                else:
                    for new_data_dict in dict_data[schema_key]:
                        if not isinstance(new_data_dict, dict):
                            raise Exception(
                                'Expected %r to be a dictionary'%(
                                    new_data_dict,
                                )
                            )
                        augment(new_data_dict, schema[schema_key])
        else:
            log.debug(
                'Adding missing object to dict data using schema key %r',
                schema_key
            )
            if schema_key != extra_keys:
                dict_data[schema_key] = missing
    # Move any extra keys to extra
    if data_keys:
        log.debug('These data keys were not found in the schema: %r', data_keys)
        if not dict_data.has_key(extra_keys):
            dict_data[extra_keys] = {}
        for extra_data_key in data_keys:
            dict_data[extra_keys][extra_data_key] = dict_data[extra_data_key]
            del dict_data[extra_data_key]
    else:
        log.debug('All schema keys were found.')

def unaugment(dict_data, schema):
    """\
    This function operates on a flattened data structure to remove any
    ``extra_keys`` keys and keys where the value is ``missing``. It then
    replaces any ``empty_list`` values with ``[]``.

    Here's the whole process:

    ::

        >>> schema = {'two': {'three': []}}
        >>> data = {'two': empty_list}
        >>> result = unaugment(data, schema)
        >>> result
        {'two': []}
        >>> schema = {
        ...     "one": {
        ...         "two": {
        ...             "three": [],
        ...         },
        ...     },
        ... }
        >>> data = {
        ...     "one": [
        ...         {
        ...             "two": [
        ...                 {"three": 3}
        ...             ]
        ...         },
        ...         {
        ...             "two": [
        ...             ]
        ...         },
        ...         {
        ...             "four": 4
        ...         }
        ...     ]
        ... }
        >>> augment(data, schema)
        >>> print pretty(data),
        {'one': [{'two': [{'three': 3}]},
                 {'two': <facilify.empty_list object at 0x...>},
                 {<facilify.extra_keys object at 0x...>: {'four': 4},
                  'two': <facilify.missing object at 0x...>}]}
        >>> result = unaugment(data, schema)
        >>> result == {
        ...     'one': [
        ...         {
        ...             'two': [
        ...                 {'three': 3}
        ...             ]
        ...         },
        ...         {
        ...             'two': [
        ...             ]
        ...         },
        ...         {}
        ...     ]
        ... }
        True

    Now a more complex example:

        >>> schema = {
        ...     "one": {
        ...         "two": {
        ...             "three": [],
        ...         },
        ...     },
        ... }
        >>> data = {
        ...     "one": [
        ...         {
        ...             "two": [
        ...                 {"three": ['random', 'list', 1, {'dict': 'data'}]}
        ...             ]
        ...         },
        ...         {
        ...             "two": [
        ...                 {"three": {'dict': 'data'}}
        ...             ]
        ...         },
        ...         {
        ...             "two": [
        ...                 {"three": 3}
        ...             ]
        ...         },
        ...         {
        ...             "two": [
        ...             ]
        ...         },
        ...         {
        ...             "four": 4
        ...         }
        ...     ]
        ... }
        >>> augment(data, schema)
        >>> print pretty(data),
        {'one': [{'two': [{'three': ['random', 'list', 1, {'dict': 'data'}]}]},
                 {'two': [{'three': {'dict': 'data'}}]},
                 {'two': [{'three': 3}]},
                 {'two': <facilify.empty_list object at 0x...>},
                 {<facilify.extra_keys object at 0x...>: {'four': 4},
                  'two': <facilify.missing object at 0x...>}]}
        >>> flat = flatten_dict(data, schema)
        >>> print pretty(flat),
        [(('one', 0, 'two', 0, 'three'), ['random', 'list', 1, {'dict': 'data'}]),
         (('one', 1, 'two', 0, 'three'), {'dict': 'data'}),
         (('one', 2, 'two', 0, 'three'), 3),
         (('one', 3, 'two'), <facilify.empty_list object at 0x...>),
         (('one', 4, <facilify.extra_keys object at 0x...>), {'four': 4}),
         (('one', 4, 'two'), <facilify.missing object at 0x...>)]
        >>> result = unaugment(data, schema)
        >>> result == {
        ...     'one': [
        ...         {
        ...             'two': [
        ...                 {"three": ['random', 'list', 1, {'dict': 'data'}]}
        ...             ]
        ...         },
        ...         {
        ...             'two': [
        ...                 {'three': {'dict': 'data'}}
        ...             ]
        ...         },
        ...         {
        ...             'two': [
        ...                 {'three': 3}
        ...             ]
        ...         },
        ...         {
        ...             'two': [
        ...             ]
        ...         },
        ...         {}
        ...     ]
        ... }
        True
    """
    log.debug('Unaugmenting %r according to %r', dict_data, schema)
    result = type(schema)()
    for k, v in dict_data.items():
        if k == extra_keys or isinstance(k, (list, tuple)) \
           and k[-1] == extra_keys:
            continue
        if v == missing:
            continue
        if v == empty_list:
            result[k] = []
        elif isinstance(v, list) and isinstance(schema.get(k, None), dict):
            unaugmented_list = []
            for new_data in v:
                unaugmented_list.append(unaugment(new_data, schema[k]))
            result[k] = unaugmented_list
        else:
            result[k] = v
    return result

def validate(data, schema, context=None):
    """\
    Here's an example of how to use ``validate()``:

    ::

        >>> def upper(key, data, errors, context):
        ...     data[key] = data[key].upper()
        ...
        >>> schema = {
        ...    "commands": {
        ...         "definition": {
        ...             "run": [not_missing, upper],
        ...         }
        ...     }
        ... }
        >>> data = {
        ...     "commands": [
        ...         {
        ...             "definition": [
        ...                 {
        ...                     "run": "12a3a",
        ...                 },
        ...                 {
        ...                     "run": "12a3b",
        ...                 },
        ...             ]
        ...         },
        ...         {
        ...             "definition": [
        ...                 {
        ...                     "run": "12b3a",
        ...                 },
        ...                 {
        ...                     "runner": "12b3b",
        ...                 },
        ...             ]
        ...         },
        ...         {
        ...             "definition": [],
        ...         },
        ...     ],
        ... }
        >>> result, errors = validate(data, schema)
        >>> print pretty(result),
        {'commands': [{'definition': [{'run': '12A3A'}, {'run': '12A3B'}]},
                      {'definition': [{'run': '12B3A'}, {}]},
                      {'definition': []}]}
        >>> print pretty(errors),
        [(('commands', 1, 'definition', 1, 'run'), [u'Missing value'])]

    Also note that if you want the schema keys to be run in the correct order make the schame an OrderedDict.

    You can also have nested schema within lists if you need to. This is useful for setting defaults for example:

    ::

        >>> schema1 = {
        ...     'one': [
        ...         default([]),
        ...         {
        ...             'two': [],
        ...         }
        ...     ]
        ... }
        >>> data1 = {}
        >>> result1, error1 = validate(data1, schema1)
        >>> result1
        {'one': []}
        >>> error1
        []
        >>> schema2 = {
        ...     'one': [
        ...         default([]),
        ...         {
        ...             'two': [not_missing],
        ...         }
        ...     ]
        ... }
        >>> data2 = {'one': [{}]}
        >>> result2, error2 = validate(data2, schema2)
        >>> result2
        {'one': [{}]}
        >>> error2
        [(('one', 0, 'two'), [u'Missing value'])]

    You can also use different dict types. By default, the same dictionary type
    used for the schema, is applied to the result. So if you want you result to be
    ordered, use an ``OrderedDict()`` for the schema, if you want the keys of the
    result to be accessible as attributes use ``obj()`` in your schema.

    Here are some examples:

    ::

        >>> schema = {
        ...     'dict': {
        ...         'key': [],
        ...     },
        ...     'obj': obj({
        ...         'key': [],
        ...     }),
        ...     'OrderedDict': OrderedDict({
        ...         'c': [],
        ...         'a': [],
        ...         'b': [],
        ...     })
        ... }
        >>> data1 = {}
        >>> result1, error1 = validate(data1, schema1)
    """
    if not isinstance(data, dict):
        raise Exception(
            'Expected data %r to be a dictionary'%(data,)
        )
    # Take a copy of the data to work with, we don't want to mess up the
    # original. We have to do this all in one go so that Python can catch
    # circular dependencies etc
    data = copy.deepcopy(data)
    log.debug('Copied data: %r', data)
    # Augment the data with a value of ``missing`` for any keys in the
    # schema which aren't present and move any extra keys to ``extra_keys``
    # Note: data is augmented *in place* so no value is returned
    augment(data, schema)
    log.debug('Augmented data: %r', data)
    # Flatten the data dictionary
    flattened_data = flatten_dict(data, schema)
    log.debug('Flattened data: %r', flattened_data)
    # Flatten the schema
    flattened_schema = flatten_schema(schema)
    log.debug('Flattened schema: %r', flattened_schema)
    # Create an error dictionary mirroring the schema
    errors = OrderedDict([(key, []) for key, value in flattened_data])
    result = OrderedDict(flattened_data)
    # Main run including extras
    for key, value in flattened_data:
        if flattened_schema.has_key(key[::2]):
            for converter in flattened_schema[key[::2]]:
                if isinstance(converter, dict):
                    # Apply the schema to the result:
                    sub_schema = {key[-1]:converter}
                    sub_data = {key[-1]: result[key]}
                    sub_result, sub_errors = validate(sub_data, sub_schema)
                    counter = 0
                    for k, v in flatten_dict(sub_result, sub_schema):
                        result[tuple(list(key)+[counter, k])] = v
                        counter += 1
                    counter = 0
                    for k, v in sub_errors:
                        errors[k] = v
                        counter += 1
                else:
                    try:
                        convert(converter, key, result, errors, context)
                    except StopOnError, e:
                        break
                    except Exception, e:
                        # We'll also except anything where the exception name is 'StopOnError'
                        if e.__class__.__name__ == 'StopOnError':
                            break
                        else:
                            raise
                            #import pdb; pdb.set_trace()
    # XXX Unflattening the data structure removes the position information
    #     is this a problem, or not?
    result = unflatten(result)
    # Now remove any remaining missing fields and extra keys
    # You can unagument as many times as you like, it shouldn't change
    # the result after the first unagument
    result = unaugment(result, schema)
    #result = unflatten(dict(result), flattened_schema)
    # Now remove any empty error fields
    err = []
    for k, v in errors.iteritems():
        if v != []:
            err.append((k, v))
    #err = unflatten(err, dict_type=dict_type)
    #errors = unflatten(dict(err))
    log.debug('Converted data: %r', result)
    log.debug('Converted errors: %r', err)
    return result, err

def convert_one(value, converter, context=None):
    result = {None: value}
    errors = {None: []}
    convert(converter, None, result, error, context)
    if errors[None]:
        raise Exception(errors[None])
    else:
        return result[None]

def convert(converter, key, converted_data, errors, context):
    # XXX Need to convert this to use inspect instead of TypeError exceptions
    if formencode_present:
        if inspect.isclass(converter) and issubclass(converter, formencode.Validator):
            try:
                value = converted_data.get(key)
                value = converter().to_python(value, state=context)
            except formencode.Invalid, e:
                errors[key].append(e.msg)
            return
        if isinstance(converter, formencode.Validator):
            try:
                value = converted_data.get(key)
                value = converter.to_python(value, state=context)
            except formencode.Invalid, e:
                errors[key].append(e.msg)
            return
    try:
        value = converter(converted_data.get(key))
        converted_data[key] = value
        return
    except TypeError, e:
        if not converter.__name__ in str(e):
            raise
    except Invalid, e:
        errors[key].append(e.error)
        return
    try:
        converter(key, converted_data, errors, context)
        return
    except TypeError, e:
        if not converter.__name__ in str(e):
            raise
    try:
        value = converter(converted_data.get(key), context)
        converted_data[key] = value
        return
    except Invalid, e:
        errors[key].append(e.error)
        return

def unflatten(flattened_data):
    """\
    Unflatten a list of keys or a dict whos keys are tuples. Here's an example:

    ::

        >>> schema = {"one": {"two": {"three": []}}}
        >>> # data = { "one": [{"two": 1}, {"two": 2}]}
        >>> data = {"one": [{"two": [{"three": 3}, {"three": {"some_other": "dict"}}]}]}
        >>> flattened_schema = flatten_schema(schema)
        >>> print pretty(flattened_schema),
        OrderedDict([(('one', 'two', 'three'), [])]
        )
        >>> flattened_data = flatten_dict(data, schema)
        >>> flattened_data
        [(('one', 0, 'two', 0, 'three'), 3), (('one', 0, 'two', 1, 'three'), {'some_other': 'dict'})]
        >>> unflattened = unflatten(dict(flattened_data))
        >>> unflattened == {
        ...     'one': [
        ...         {
        ...             'two': [
        ...                 {
        ...                     'three': 3
        ...                 },
        ...                 {
        ...                     'three': {'some_other': 'dict'}
        ...                 }
        ...             ]
        ...         }
        ...     ]
        ... }
        True
        >>> unflattened == data
        True

    """
    unflattened = {}#dict_type()
    flattened_data_ = flattened_data
    if not isinstance(flattened_data, dict):
        flattened_data_ = OrderedDict(flattened_data)
    sorted_flattened_data = sorted(flattened_data_.keys())
    junk = []
    for flattened_key in sorted_flattened_data:
        if not isinstance(flattened_key, (list, tuple)):
            raise Exception('Expected the key %r to be a list or tuple. Invalid flattened_data %r'%(flattened_key, flattened_data))
        current_pos = unflattened
        for key in flattened_key[:-1]:
            try:
                current_pos = current_pos[key]
            except KeyError:
                new_pos = []
                current_pos[key] = new_pos
                current_pos = new_pos
            except IndexError:
                new_pos = {}#dict_type()
                current_pos.append(new_pos)
                current_pos = new_pos
        log.debug('Setting %r to %r in %r', flattened_key[-1], flattened_data[flattened_key], current_pos)
        current_pos[flattened_key[-1]] = flattened_data[flattened_key]
    return unflattened

#
# Helpers
#

def sibling_key(key, new_key):
    return tuple(list(key[:-1])+[new_key])

def format_key(key, name='data'):
    result=name
    for part in key:
        if isinstance(part, int):
            result += '[%s]'%part
        else:
            result += u"['%s']"%part
    return result

def format_errors(errors, name='data'):
    result = 'The following errors occurred:\n'
    for k, v in errors:
        result += '    %s: %s\n'%(format_key(k, name), '; '.join(v))
    return result

#
# Validators
#

def identity_converter(key, data, errors, context):
    return

def single_dict(schema, error_msg='Failed to validate against the schema'):
    def validate_dict_converter(key, data, errors, context):
        value = data[key]
        result, err = validate(value, schema)
        if result:
            data[key] = result
        else:
            errors[key] = error_msg
    return validate_dict_converter

def keep_extras(key, data, errors, context):
    extras = data.pop(key, {})
    for extras_key, value in extras.iteritems():
        data[key[:-1] + (extras_key,)] = value

def instance_of(type_):
    def instance_of_converter(key, data, errors, context):
        if not isinstance(data[key], type_):
            errors[key].append(_stdtrans('Not a %r'%type_))
            raise StopOnError()
    return instance_of_converter

def stop_if_missing(key, data, errors, context):
    value = data.get(key)
    if value == missing:
        raise StopOnError()

def split(on=','):
    def split_converter(key, data, errors, context):
        value = data.get(key)
        if value == missing:
            errors[key].append(_stdtrans('Missing value'))
            raise StopOnError()
        else:
            data[key] = [x.strip() for x in value.split(on)]
    return split_converter

def not_present(key, data, errors, context):
    value = data.get(key)
    if value != missing:
        errors[key].append(_stdtrans('Unexpected value'))
        raise StopOnError()

def not_missing(key, data, errors, context):
    value = data.get(key)
    if value == missing:
        errors[key].append(_stdtrans('Missing value'))
        raise StopOnError()

def not_empty(key, data, errors, context):
    value = data.get(key)
    if not value or value == missing:
        errors[key].append(_stdtrans('Missing value'))
        raise StopOnError()

def if_empty_same_as(other_key):
    def callable(key, data, errors, context):
        value = data.get(key)
        if not value or value == missing:
            data[key] = data[key[:-1] + (other_key,)]
    return callable

def both_not_empty(other_key):
    def callable(key, data, errors, context):
        value = data.get(key)
        other_value = data.get(key[:-1] + (other_key,))
        if (not value or value == missing and
            not other_value or other_value == missing):
            errors[key].append(_stdtrans('Missing value'))
            raise StopOnError()
    return callable

def empty(key, data, errors, context):
    value = data.pop(key, None)
    if value and value != missing:
        errors[key].append(_stdtrans(
            'The input field %(name)s was not expected.') % {"name": key[-1]})

def ignore(key, data, errors, context):
    value = data.pop(key, None)
    raise StopOnError()

def existing_directory(key, data, errors, context):
    value = data.get(key)
    if value == missing:
        errors[key].append('No directory specified')
        raise StopOnError()
    elif not value:
        errors[key].append('No directory specified')
        raise StopOnError()
    elif not os.path.exists(value):
        errors[key].append('No such directory')
        raise StopOnError()
    elif not os.path.isdir(value):
        errors[key].append('Not a directory')
        raise StopOnError()

def existing_file(key, data, errors, context):
    value = data.get(key)
    if not value:
        errors[key].append('No file specified')
        raise StopOnError()
    elif value == missing:
        errors[key].append('No file specified')
        raise StopOnError()
    elif not os.path.exists(value):
        errors[key].append('No such file')
        raise StopOnError()
    elif os.path.isdir(value):
        errors[key].append('Not a file')
        raise StopOnError()
    
def default(default_value):
    def default_converter(key, data, errors, context):
        value = data.get(key)
        if not value or value == missing:
            data[key] = default_value
    return default_converter

def ignore_missing(key, data, errors, context):
    value = data.get(key)
    if not value or value == missing:
        data.pop(key, None)
        raise StopOnError()

def convert_int(value, context):
    try:
        return int(value)
    except ValueError:
        raise Invalid(_stdtrans('Please enter an integer value'))

def add_extras_to(value):
    def converter(key, data, errors, context):
        pass # XXX to fix
    return converter

def common_identifier_for(type='facility'):
    def common_identifier_for_converter(key, data, errors, context):
        if data[key] == missing:
            raise Exception('No %s key specified'%format_key(key))
        if data[key].lower() in case_insensitive_reserved_words or data[key] in case_sensitive_reserved_words:
            errors[key].append('%r is a reserved word and cannot be used for %s'%(data[key], type))
    return common_identifier_for_converter


#############################################################################
#
# CommandTool
#

import warnings
import getopt
import logging
import sys
import os
from logging.config import fileConfig

def strip_none(d):
    result = type(d)()
    for k, v in d.iteritems():
        if v is not None:
            result[k] = v
    return result

#
# Help helpers
#

def help_opt_specs(command):
    output = ''
    rows = []
    for opt_spec in command.definition.opt_specs:
        # XXX Look into why this isn't an obj already
        opt_spec = obj(opt_spec)
        cur_opts = []
        if not opt_spec.get('metavar'):
            cur_opts += opt_spec.flags
        else:
            metavar = opt_spec.metavar
            for flag in opt_spec.flags:
                if flag.startswith('--'):
                    cur_opts.append('%s=%s'%(flag, metavar))
                else:
                    cur_opts.append('%s %s'%(flag, metavar))
        rows.append((' '.join(cur_opts), opt_spec.get('help_msg', '')))
    if rows:
        output += 'Options:\n'
        output += two_cols(rows)
    return output

def help_arg_specs(command):
    output = ''
    rows = []
    for arg_spec in command.definition.arg_specs:
        rows.append((arg_spec['metavar'], arg_spec['help_msg']))
    if rows:
        output += 'Arguments:\n'
        output += two_cols(rows)
    return output

def help_child_command_specs(child_command_specs=None):
    if child_command_specs is None:
        return ""
    output = ''
    rows = []
    for child_command_spec in child_command_specs:
        if child_command_spec.get('summary') is None:
            res = summary_from_spec(
                child_command_spec.get('definition'), 
                child_command_spec.get('spec'), 
                child_command_spec.name, 
            )
            if not child_command_spec.has_key('definition') and res.definition is not None:
                child_command_spec['definition'] = res.definition
            child_command_spec['summary'] = res.summary
        rows.append([
            child_command_spec.name,
            child_command_spec.summary,
        ])
    if rows:
        output += 'Commands:\n'
        output += two_cols(rows)
    return output

help_template = """\
%(summary)s
%(usage)s

%(args)s

%(opts)s

%(tip)s"""

main_help_template = """\
%(summary)s
%(usage)s

%(opts)s

%(args)s

%(child_commands)s

%(tip)s"""

def summary_from_spec(definition=None, spec=None, name=None):
    summary = None
    if not definition:
        try:
            definition = import_and_return(spec)
        except Exception, e:
            if logging._handlers:
                log.warning(
                    'Couldn\'t load command %r for summary text. Error was: %s', 
                    name,
                    text_traceback(),
                )
            return obj(
                summary = 'ERROR: Could not be loaded',
		# XXX It is a bit hacky to use the exception as the definition
		# but it will do for now, it certainly prevents mistakes!
                definition = e,
            )
    summary = getattr(definition, 'summary', None)
    if summary is None:
        # We can't use .__doc__ here because that would refer to the
        # definition type's __doc__ attribute, not the module's one
        summary = (definition.get('__doc__') or '').split('\n\n')[0].replace('\n', ' ').strip()
    if not summary:
        summary = 'ERROR: No summary available'
    return obj(
        summary = summary,
        definition = definition,
    )

import textwrap
def assemble_help(
    command,
    child_command_specs,
    summary=None,
    wrap_width=default_wrap_width,
):
    template = getattr(command.definition, 'help_template')
    if summary is None:
        summary = getattr(command.definition, 'summary', '')
    usage = 'Usage: %s'%command.program
    if command.parent:
        usage += ' %s'%command.name
    if command.definition.opt_specs:
        usage += ' [OPTIONS]'
    if command.definition.arg_specs:
        usage += ' [ARGS]'
    if child_command_specs:
        usage += ' COMMAND [ARGS] [OPTIONS]'
    if child_command_specs:
        tip = (
            '\nType `%(program)s COMMAND --help\' '
            'for help on individual commands.'
        ) % {
           'program': command.program,
        }
    else:
        tip = ''
        if command.parent:
            tip = (
                '\nType `%(program)s --help\' for '
                'parent command options, arguments and other commands.'
            ) % {
               'program': command.parent.program,
            }
    variables = dict(
        summary = summary,
        usage = usage,
        opts = help_opt_specs(command),
        args = help_arg_specs(command),
        child_commands = help_child_command_specs(child_command_specs),
        program = command.program,
        tip = tip,
    )
    if command.parent:
        variables['parent_opts'] = help_opt_specs(command.parent),
        variables['parent_args'] = help_arg_specs(command.parent),
    # Try to render the help template string
    attempt = 0
    while attempt < 100:
        try:
            output = (template % variables).strip()
        except KeyError, e:
            variable = "%%(%s)s"%(str(e)[1:-1],)
            template.replace('%', '%%')
            template = template.replace(
                variable,
                '%'+variable,
            )
            log.debug("'help_template' string contains an invalid variable %r", str(e)[1:-1])
            attempt += 1
        else:
            break
    while '\n\n\n' in output:
        output = output.replace('\n\n\n', '\n\n')
    result = ''
    for line in output.split('\n'):
        result += '\n'.join(textwrap.wrap(line, wrap_width))+'\n'
    return result.strip()

def _logging_run(command):
    if command.opts.get('logging') and (command.opts.quiet or command.opts.verbose):
        raise getopt.GetoptError(
            'You cannot specify a LOGGING_FILE and also use the '
            '-q or -v options'
        )
    if command.opts.get('logging'):
        if not os.path.exists(command.opts.logging):
            raise getopt.GetoptError('No such file %r'%command.opts.logging)
        fileConfig(command.opts.logging)
    else:
        format="%(levelname)s: %(message)s"
        if command.opts.quiet:
            logging.basicConfig(level=logging.WARNING, format=format)
            logging.root.setLevel(logging.WARNING)
        elif command.opts.verbose:
            logging.basicConfig(level=logging.DEBUG, format=format)
            logging.root.setLevel(logging.DEBUG)
        else:
            logging.basicConfig(level=logging.INFO, format=format)
            logging.root.setLevel(logging.INFO)

help_opt_spec = obj(
    name = 'help',
    flags = ['-h', '--help'],
    help_msg = 'display this message'
)

logging_command = obj(
    help_template=main_help_template,
    opt_specs = [
        help_opt_spec,
        dict(
            name = 'verbose',
            flags = ['-v', '--verbose'],
            help_msg = 'Print lots of information about what\'s going on',
        ),
        dict(
            name = 'quiet',
            flags = ['-q', '--quiet'],
            help_msg = 'Only show really important messages',
        ),
        dict(
            name = 'logging',
            flags = ['-l', '--logging'],
            help_msg = 'Specify a logging file',
            metavar='LOGGING_FILE',
        ),
    ],
    run = _logging_run,
)

def default_summary_from_definition(key, data, errors, context):
    if data[key] == missing: 
        definition = data.get(sibling_key(key, 'definition'))
        spec = data.get(sibling_key(key, 'spec'))
        res = summary_from_spec(
            definition != missing and definition or None,
            spec != missing and spec or None,
            data[sibling_key(key, 'name')],
        )
        if definition == missing:
            data[sibling_key(key, 'definition')] = res.definition
        data[key] = res.summary

def get_missing_definitions(key, data, errors, context):
    looking_for = sibling_key(key, 'definition')
    if not data.has_key(looking_for):
        if data[key] == missing:
            errors[key] = 'No spec key preset'
        else:
            data[looking_for] = import_and_return(data[key])

def format_string(string, *args, **opts):
    if opts.get('end') is None:
        end = '\n'
    else:
        end = opts.get('end')
    if args:
        return (string + end) % args
    else:
        return string + end

def print_fn(string, *args, **opts):
    print format_string(string, *args, **opts),

class Command(object):
    def __init__(
        self,
        stack,
        name,
        definition,
        parent,
        program,
        args,
        opts,
        log=None,
        warn=None,
        out=None,
        err=None,
        alias_specs=None,
        #parsed_argv=None,
        #help_opt_name='help',
        #child_command_specs=None,
    ):
        self.stack = stack
        self.name = name
        self.definition = definition
        self.parent = parent
        self.program = program
        self.args = args
        self.opts = opts
        if log is None:
            self.log = Log(name=self.name)
        else:
            self.log = log
        if warn is None:
            self.warn = Warn()
        else:
            self.warn = warn
        self.out = out
        self.err = err
        self.aliases = obj([(k, k) for k in self.definition.get('facility_names', [])])
        for alias_spec in alias_specs or []:
            self.aliases[alias_spec['name']] = alias_spec['facility']
        if self.parent and self.parent.name in self.aliases.keys():
            raise NameError(
                'The alias %r has the same name as the parent command'%(
                    self.parent.name
                )
            )

    def __getitem__(self, name):
        if self.parent and name == self.parent.name:
            return self.parent
        elif self.stack and name in self.aliases:
            alias = self.aliases[name]
            if not alias in self.stack.started.facilities:
                self.stack.start(alias)
            return self.stack[alias]
        elif self.stack and name in self.stack.shared.facility_specs_by_name:
            if not self.stack.has_key(name):
                self.stack.start(name)
            return self.stack[name]
        else:
            raise KeyError('No such facility or parent named %r'%name)

    def __getattr__(self, name):
        if name in self.__dict__:
            return self.__dict__[name]
        return self.__getitem__(name)

reserved_child_command_names = [
    'warn',
    'err',
    'log',
    'args',
    'opts',
    '_args',
    '_opts',
    '_parents',
]

import string
def uppercase_alpha(key, data, errors, context):
    for char in data[key]:
        if not char in string.uppercase+'_':
            raise Exception('Invalid metavar %r, metavars should contain only uppercase characters'%data[key])

def valid_options(key, data, errors, context):
    allowed = string.lowercase+string.uppercase
    options = []
    if not isinstance(data[key], (list, tuple)):
        raise Exception(
            "Expected the option list to be a list or tuple, not %r"%data[key]
        )
    for opt in data[key]:
        if opt.startswith('--'):
            if opt[2:] in options:
                raise Exception('The option %r has already been used'%opt[2:])
            for char in opt[:2:]:
                if char not in allowed+'-':
                    raise Exception(
                        '%r is not an allowed option name, it contains the '
                        'character %r'%(opt, char)
                    )
            options.append(opt[2:])
        elif opt.startswith('-'):
            if len(opt) != 2:
                raise Exception(
                    "%r is not an allowed option name, options starting "
                    "with a single '-' character should only be one letter "
                    "long"%(opt, char)
                )
            if opt[1] in options:
                raise Exception('The option %r has already been used'%opt[1])
            if opt[1] not in allowed:
                raise Exception(
                    "%r is not an allowed option name, it contains the "
                    "character %r"%(opt, opt[1])
                )
            options.append(opt[1])
        else:
            raise Exception(
                "%r is not an allowed option name, options must start with "
                "'-' or '--' characters, not %r"%(opt, char)
            )

def ensure_no_default_or_converter_if_missing(key, data, errors, context):
    if data[key] == missing:
        for disallowed in ['default', 'converter']:
            other_key = sibling_key(key, disallowed)
            if data[other_key] != missing:
                raise Exception(
                    'You cannot specify a %r value for option %r unless a '
                    'metavar is specified too, otherwise the option doesn\'t '
                    'take a value'%(
                        disallowed,
                        data[sibling_key(key, 'name')],
                    )
                )


def parse_argv(
    arg_specs,
    opt_specs,
    argv,
    allow_remaining_args=True,
    allow_variable_arg_spec=True,
    help_opt_name='help',
):
    """\
    Options must be specified before args in the ``argv`` list, otherwise
    they will be treated as arguments too.

    Here's an example:

    ::

        >>> arg_specs = [
        ...     dict(metavar='ONE', help_msg='the first argument'),
        ...     dict(metavar='SECOND', help_msg='the second argument'),
        ...     dict(
        ...         metavar='ARGS',
        ...         min=1,
        ...         help_msg='at least one extra argument',
        ...     ),
        ... ]
        >>> opt_specs = [
        ...     help_opt_spec,
        ...     dict(
        ...         name = 'verbose',
        ...         flags = ['-v', '--verbose'],
        ...         help_msg = 'Print lots of information about what is going on',
        ...     ),
        ...     dict(
        ...         name = 'quiet',
        ...         flags = ['-q', '--quiet'],
        ...         help_msg = 'Only show really important messages',
        ...     ),
        ...     #dict(
        ...     #    name = 'ignore',
        ...     #    flags = ['-i', '--ignore'],
        ...     #    help_msg = 'Hide extensionts',
        ...     #    multiple=True,
        ...     #    metavar='EXT',
        ...     #),
        ...     dict(
        ...         name = 'logging',
        ...         flags = ['-l', '--logging'],
        ...         help_msg = 'Specify a logging file',
        ...         metavar='LOGGING_FILE',
        ...     ),
        ... ]
        >>> # Notice that when an arg comes first, everything is treated as an arg
        >>> result = parse_argv(arg_specs, opt_specs, ['one', '-l', 'log.conf', '--help', 'two', 'three'])
        >>> print pretty(result),
        {'arg_error': None,
         'args': ['one', '-l', 'log.conf', '--help', 'two', 'three'],
         'flags': {},
         'getopt': {'args': ['one', '-l', 'log.conf', '--help', 'two', 'three'],
                    'flags': []},
         'opts': {'help': False, 'logging': None, 'quiet': False, 'verbose': False},
         'position': {},
         'remaining_args': [],
         'values': {}}
        >>> # Normally the behaviour is this:
        >>> result = parse_argv(arg_specs, opt_specs, ['-l', 'log.conf', '--help', 'one', 'two', 'three'])
        >>> print pretty(result),
        {'arg_error': None,
         'args': ['one', 'two', 'three'],
         'flags': {'help': ['--help'], 'logging': ['-l']},
         'getopt': {'args': ['one', 'two', 'three'],
                    'flags': [('-l', 'log.conf'), ('--help', '')]},
         'opts': {'help': True,
                  'logging': 'log.conf',
                  'quiet': False,
                  'verbose': False},
         'position': {'help': [1], 'logging': [0]},
         'remaining_args': [],
         'values': {'help': [''], 'logging': ['log.conf']}}
    """
    # 1. Validate the opts_specs
    # 2. Validate the arg_specs
    result, errors = validate(
        {
            'arg_specs': arg_specs,
            'opt_specs': opt_specs,
        },
        obj({
            'arg_specs': arg_specs_schema,
            'opt_specs': opt_specs_schema,
        }),
    )
    if errors:
        raise Exception(format_errors(errors, name='command'))
    # Otherwise use the fitted values
    arg_specs = result.arg_specs
    opt_specs = result.opt_specs
    number_of_min = 0
    for arg_spec in arg_specs:
        if arg_spec.has_key('min'):
            number_of_min += 1
    if number_of_min:
        if number_of_min > 1:
            raise Exception(
                "Invalid arg spec, more than one dictionary in the list "
                "contains a 'min' key"
            )
        if not arg_specs[-1].has_key('min'):
            raise Exception(
                "Invalid arg spec, only the last dictionary in the list "
                "can contain a 'min' key"
            )
        if not allow_variable_arg_spec:
            raise Exception(
                "Invalid arg spec, the 'min' key is not allowed when the "
                "command has child commands"
            )

    # 3. Parse argv by arranging flags
    help_flags = []
    short_flags = ''
    long_flags = []
    for opt_spec in opt_specs:
        for flag in opt_spec.flags:
            if opt_spec.name == help_opt_name:
                help_flags.append(flag)
            if flag.startswith('--'):
                long_flag = flag[2:]+(opt_spec.get('metavar') and '=' or '')
                log.debug(
                    'Treating option %r flag %r as the long flag %r',
                    opt_spec.name,
                    flag,
                    long_flag,
                )
                long_flags.append(long_flag)
            elif flag.startswith('-'):
                short_flag = flag[1:]+(opt_spec.get('metavar') and ':' or '')
                log.debug(
                    'Treating option %r flag %r as the short flag %r',
                    opt_spec.name,
                    flag,
                    short_flag,
                )
                short_flags += short_flag
    log.debug(
        'Parsing %r with getopt as short: %r; long: %r',
        argv,
        short_flags,
        long_flags,
    )
    try:
        flags, args = getopt.getopt(argv, short_flags, long_flags)
    except getopt.GetoptError, e:
        if str(e).startswith('option ') and str(e).endswith('not recognized'):
            for help_flag in help_flags:
                if help_flag in [arg.strip() for arg in argv]:
                    # There is a bad option but we may need to display the help
                    # They are probably asking for help
                    log.error(str(e))
                    # Return a dummy object that will trigger help
                    return obj(
                        opts = obj(help=True),
                        args = [],
                    )
        raise
    log.debug('Getopt returned args: %r and flags: %r', args, flags)
    getopt_result = obj(flags=flags, args=args)

    # Now put the opts in a more usable form
    internal_opts = obj()
    # 4. Setup the defaults
    for opt_spec in opt_specs:
        if not opt_spec.get('metavar', ''):
            if opt_spec.get('multiple', ''):
                internal_opts[opt_spec.name] = []
            else:
                internal_opts[opt_spec.name] = False
        else:
            if opt_spec.has_key('default'):
                internal_opts[opt_spec.name] = opt_spec.default
            else:
                if opt_spec.get('multiple', ''):
                    internal_opts[opt_spec.name] = []
                else:
                    # Otherwise, default to None
                    internal_opts[opt_spec.name] = None
    # 5. Loop through the options that were actually found and update the
    #    defaults
    flags_used = obj()
    values_used = obj()
    position = obj()
    i = 0
    for flag, value in getopt_result.flags:
        for opt_spec in opt_specs:
            if flag in opt_spec.flags:
                multiple = opt_spec.get('multiple', False)
                if flags_used.has_key(opt_spec.name) and not multiple:
                    raise getopt.GetoptError(
                        'The flag %r is unexpected (the related flag %r '
                        'has already been used)'%(
                            flag,
                            flags_used[opt_spec.name][-1],
                        )
                    )
                else:
                    value_to_set = value
                    if not opt_spec.get('metavar', ''):
                        value_to_set = True
                    elif opt_spec.get('converter'):
                        value_to_set = convert_one(
                            value_to_set,
                            opt_spec.get('converter')
                        )
                    if multiple:
                        internal_opts[opt_spec.name].append(value_to_set)
                    else:
                        internal_opts[opt_spec.name] = value_to_set
                    if flags_used.has_key(opt_spec.name):
                        flags_used[opt_spec.name].append(flag)
                        values_used[opt_spec.name].append(value)
                        position[opt_spec.name].append(i)
                    else:
                        flags_used[opt_spec.name] = [flag]
                        values_used[opt_spec.name] = [value]
                        position[opt_spec.name] = [i]
        i += 1
    # 6. Parse the args
    our_args = []
    remaining_args = args[:]
    arg_error = None
    if len(arg_specs):
        # If we are expecting arguments, process them now
        for arg_spec in arg_specs:
            if arg_spec.has_key('min'):
                # This is a special case where we allow a variable number of
                # arguments
                if len(remaining_args) < arg_spec.min:
                    # We might be able to get an error
                    arg_error = arg_spec.get(
                        'not_enough_extra_args_error',
                        'Not enough arguments',
                    )
                    break
                else:
                    our_args += remaining_args
                    while remaining_args:
                        remaining_args.pop()
                break
            else:
                if not remaining_args:
                    arg_error = 'Not enough arguments'
                else:
                    our_args.append(remaining_args.pop(0))
    if not arg_error and (remaining_args and not allow_remaining_args):
        for help_flag in help_flags:
            if help_flag in [arg.strip() for arg in argv]:
                return obj(
                    opts = obj(help=True),
                    args = [],
                )
        if len(remaining_args) > 1:
            arg_error = 'Unexpected arguments: %s'%(
                ', '.join([str(arg) for arg in remaining_args])
            )
        else:
            arg_error = 'Unexpected argument %s'%(remaining_args[0])
    result = obj(
        getopt = getopt_result,
        arg_error = arg_error,
        opts=internal_opts,
        flags=flags_used,
        values=values_used,
        position=position,
        args=our_args,
        remaining_args=remaining_args,
    )
    log.debug('Result: %r', dict(result))
    return result

def handle_command(
    argv,
    definition,
    name='command',
    summary=None,
    child_command_specs=None,
    program=None,
    parent=None,
    stack=None,
    out=print_fn,
    err=print_fn,
    help_opt_name='help',
    #facility_specs=None,
    spec=None,
    alias_specs=None,
):
    """\
    Run the appropriate commands based on ``argv`` from the ``definition`` given.

    Here's an example:

    ::

        >>> def run(main):
        ...     main.out(repr([main.args, main.opts]))
        >>> result = handle_command(
        ...     definition = logging_command,
        ...     child_command_specs = [
        ...         {'name': 'test', 'definition': obj({'run':run})}
        ...     ],
        ...     argv = ['test', '--help'],
        ... )
        [[], {'help': True}]
        >>> result
        0
        >>> result = handle_command(
        ...     definition = logging_command,
        ...     child_command_specs = [
        ...         {'name': 'test', 'definition': obj({'run':run})}
        ...     ],
        ...     argv = ['test'],
        ... )
        [[], {'help': False}]
        >>> result
        0

    Allowed args are:

    ``argv``
        A list of unicode strings representing all args and options
        specified on the command line apart from the program name itself and
        any reference to the ``python`` application. For example, if the
        command was ``python -m module.run main --verbose command -a --b c d e``
        then ``command_line_parts`` would be ``[u'main', u'--verbose',
        u'command', u'-a', u'--b', 'c']``. Often ``sys.argv[1:]`` is used as
        this argument.

    ``definition``
        The definition of the command to use as the main
        command. Most of the time this is ``facilify.logging_command`` which
        provides basic logging facility_specs.

    ``name``
        A name for the main command, used in its logging. Defaults to ``'command'``

    ``child_command_specs``
        A list of dictionaries representing child commands that might be run.

        Each dictionary must have a ``name`` key representing the
        name that a user will write on the command line after the main
        command's options and args to run the child command. For example, in
        the case of the ``hg pull`` comamnd, you can imagine ``pull`` might
        be the child command name. Next each dictionary must have either a
        ``spec`` key representing how the command definition can be
        imported, or an ``definition`` key representing the
        implemetation itself. If a ``spec`` key is used, it is recommended
        that a ``summary`` key should also be added so that the command
        definition doesn't have to be imported in order for the main
        command to display a summary message of it.

        .. caution ::

            There are some restrictions on what you can use as a child command name. Names
            must be valid Python module names, can't start with an underscore
            and can't be any of these reserved names: %s.
            If the child command has its own child commands, the child command can't
            have the same name as any facility alias used by that child command.

    ``program``
        The name that should be used in any help messages that
        display an example command you should run. If not specified
        explictly, a good guess is made.

    ``parent``
        If this is a child command, ``parent`` should be set to the instance
        of the ``Command`` class that was used for the main commnad immediately above
        it.

    ``stack``
        The shared ``SharedStack`` stack() instance that started this command (if it
        was started this way)

    ``out``,
        A custom function that should be used instead of the default
        ``facilify.print_fn`` for output to stdout via the ``command.out()`` call.

    ``err``
        A custom function that should be used instead of the default
        ``facilify.print_fn`` for output to err via the ``command.err()`` call.

    ``help_opt_name``
       The name of the option, which if present should trigger automatic display
       of a help message.


    """#%(str(reserved_child_command_names).replace("'", '``')[1:-1], )
    if program is None:
        program = sys.argv[0]
        if os.sep in sys.argv[0]:
            program = program.split(os.sep)[-1]
    # 1. Validate the command
    shaped_definition, errors = validate(definition, command_definition_schema)
    if errors:
        raise Exception(format_errors(errors, name=name))

    # There is a chance that a main command will implement its own child
    # commands via the child_command_specs attribute of the definition in
    # addition to those defined in child_command_specs passed to
    # handle_command(). In such cases we take the value passed to
    # handle_command() in preference.
    combined_child_command_specs = []
    names_used = []
    for item in child_command_specs or []:
        if not isinstance(item, obj):
            item = obj(item)
        names_used.append(item.name)
        combined_child_command_specs.append(item)
    for item in shaped_definition.child_command_specs:
        if not isinstance(item, obj):
            item = obj(item)
        if item.name not in names_used:
            combined_child_command_specs.append(item)
    next_child_command_spec = None
    try:
        # First parse the option spec for the main command into a to see what args we have:
        is_main_command = combined_child_command_specs is None or not len(combined_child_command_specs)
        parsed_argv = parse_argv(
            arg_specs = shaped_definition.arg_specs,
            opt_specs = shaped_definition.opt_specs,
            argv = argv,
            allow_remaining_args = not is_main_command,
            allow_variable_arg_spec = is_main_command,
            help_opt_name=help_opt_name,
        )
        # Try the run command
        command = Command(
            definition=shaped_definition,
            stack=stack,
            name=name,
            parent=parent,
            program=program,
            alias_specs=alias_specs,
            args=parsed_argv.args,
            opts=parsed_argv.opts,
            out=out,
            err=err,
        )
        # We can handle help messages automatically:
        if help_opt_name and parsed_argv.opts.get(help_opt_name):
            out(assemble_help(command, combined_child_command_specs, summary))
            return 0
        if parsed_argv.arg_error:
            raise getopt.GetoptError(parsed_argv.arg_error)
        try:
            # The run() function has its command passed by position, so that
            # in that function any name can be specified 
            result = shaped_definition.run(command)
        except KeyboardInterrupt, e:
            if hasattr(shaped_definition, 'after'):
                result = shaped_definition.after(command, e) or 1
            else:
                result = 1
        if result:
            # There was an error
            return result
        if not parsed_argv.remaining_args:
            return 0
        # Otherwise assume we have a child command to run
        next_child_command_name = parsed_argv.remaining_args[0]
        for child_command_spec in combined_child_command_specs:
            if not child_command_spec.get('name'):
                raise Exception(
                    'Invalid child command spec %r'%child_command_spec
                )
            if child_command_spec.get('name') == next_child_command_name:
                next_child_command_spec = child_command_spec
                break
        if next_child_command_spec is None:
            raise getopt.GetoptError('No such child command `%s\''%next_child_command_name)
    except getopt.GetoptError, e:
        err('Error: %s'%str(e))
        if help_opt_name is not None:
            option_specs = collect_by(
                'name',
                shaped_definition.opt_specs
            )
            help_opt_spec = option_specs[help_opt_name]
            err(
                "Try `%(program)s %(flag)s' for more information." % {
                    'program': program,
                     # We generally organise the flags shortest first but it
                     # is clearest to show the long option in the help output
                    'flag': help_opt_spec['flags'][-1],
                }
            )
        return 1
    else:
        # At this point we must have a child command to handle
        # Validate the child_spec
        result, errors = validate(
            next_child_command_spec,
            command_specs_schema,
        )
        if errors:
            raise Exception(format_errors(errors, name='child_command_spec'))
        # import the child_command if we need to
        if not result.has_key("definition"):
            try:
                result['definition'] = import_and_return(result["spec"])
            except:
                err('ERROR: The module %r could not be loaded', result['spec'])
                log.info('Loading of %r failed for this reason: %s', result['spec'], text_traceback())
                return 1
        if not isinstance(result.definition, dict):
            raise result.definition
        return handle_command(
            argv=parsed_argv.remaining_args[1:],
            program=('%s %s'%(
                program,
                ' '.join(argv[:-len(parsed_argv.remaining_args)]),
            )).strip(),
            parent=command,
            stack=stack,
            out=out,
            err=err,
            help_opt_name=help_opt_name,
            **result
        )

#############################################################################
#
# PipeStack
#

import textwrap
import os
import sys

class Warn(object):
    """\
    A helper class used by ``Command`` and ``Facility`` to provide their
    ``.warn`` attribute.

    Imagine you have a command or facility called ``blog``, you could then
    run this:

    ::

        blog.warn.deprecated(
            'Please use the two() function instead of one()'
        )
    """
    def deprecated(self, msg):
        warnings.warn(msg)

class Log(object):
    """\
    A helper class used by ``Command`` and ``Facility`` to provide their
    ``.log`` attribute.

    Imagine you have a command or facility called ``blog``, you could then
    run this:

    ::

        blog.log.info("Running the one() function with the value %r", value)

    """
    def __init__(self, name, wrap_width=default_wrap_width, tabwidth=2):
        self.handler = logging.getLogger(name)
        self.wrap_width = wrap_width
        self.tabwidth = tabwidth

    def _log(self, level, string):
        self.handler.log(level, string)
        return string

    def error(self, string, *args):
        return self._log(40, _wrap(string, args, self.wrap_width))

    def warning(self, string, *args):
        return self._log(30, _wrap(string, args, self.wrap_width))

    def info(self, string, *args):
        return self._log(20, _wrap(string, args, self.wrap_width))

    def debug(self, string, *args, **p):
        if p:
            if not p.keys() == ['level']:
                keys = str_keys(p, remove='level').keys()
                raise TypeError('Unexpected argument %r'%keys[0])
            level = k['level']
        else:
             level = 0
        if not isinstance(level, int):
            raise TypeError(
                "Expected the first argument to debug() to be an integer "
                "representing the indentation level"
            )
        if level > 10:
            raise ValueError(
                "%s is an invalid value for the 'level' argument to debug(); "
                "it should be less than or equal to 10"%level
            )
        return self._log(
            10,
            _wrap(string, args, self.wrap_width, level*self.tabwidth)

        )


#
# Run validators
#

def no_duplicate_names(key, data, errors, context):
    # XXX Todo
    pass

def all_aliased_facilites_exist(key, data, errors, context):
    # XXX Todo
    pass

def validate_facility_spec(key, data, errors, context):
    """\
    Facilities can have any of the following specs:

Outstanding areas to consider:

* Use of internal variables
* Sub-modules
* Migrations
* Logic layer

Solution:

Facilities laid out like this:

__init__.py
store.py
api.py
valid.py
right.py


    """
    # XXX Todo
    pass

def import_and_return(spec):
    module_path = None
    imported_object = None
    if ':' in spec:
        # We are importing an object
        if spec.count(':') != 1:
            raise ValueError(
                "Expected just one ':' character in the spec %r"%spec
            )
        module_path, imported_object = spec.split(':')
    else:
        module_path = spec
    try:
        result = __import__(module_path)
    except ImportError, e:
        #import pdb; pdb.set_trace()
        raise
    for part in module_path.split('.')[1:]:
        result = getattr(result, part)
    if imported_object:
        #call = False
        #if imported_object.endswith('()'):
        #    call = True
        #    imported_object = imported_object[:-2]
        if not hasattr(result, imported_object):
            raise ImportError(
                "The %r module contains no object named %r"%(
                    module_path,
                    imported_object,
                )
            )
        result = getattr(result, imported_object)
        #if call:
        #    result = result()
    else:
        result = module_to_obj(result)
    return result

def module_to_obj(module):
    result = []
    for k, v in module.__dict__.iteritems():
        if k != '__builtins__' and not inspect.ismodule(v):
            result.append((k, v))
    result.append(('__doc__', module.__doc__))
    result.append(('__name__', module.__name__))
    result.append(('__package__', module.__package__))
    result.append(('__file__', module.__file__))
    return obj(result)

def importable(key, data, errors, context):
    # XXX
    pass

def if_missing_uncollect_by(var, data_key):
    def if_missing_uncollect_by_converter(key, data, errors, context):
        if data[key] == missing and \
           data.get(sibling_key(key, data_key), missing) != missing:
            data[key] = uncollect_by(var, data[sibling_key(key, data_key)])
    return if_missing_uncollect_by_converter

def add_help_opt_spec(key, data, errors, context):
    help_opt_name = data[sibling_key(key, 'help_opt_name')]
    found = False
    for item in data[key]:
        if item['name'] == help_opt_name:
            found = True
            break
    if not found:
        opt_spec = help_opt_spec.copy()
        opt_spec['name'] = help_opt_name
        data[key].insert(0, opt_spec)

#
# Schema
#

alias_spec_schema = obj({
    'name': [not_missing, common_identifier_for('an alias')],
    'facility': [not_missing, common_identifier_for('a facility')],
    extra_keys: [not_present],
})

opt_specs_schema = obj({
    'name': [not_missing],# common_identifier_for('a name')],
    'flags': [not_missing, valid_options],
    'help_msg': [not_missing],
    'default': [],
    'converter': [],
    'metavar': [ensure_no_default_or_converter_if_missing, stop_if_missing, uppercase_alpha],
    'multiple': [default(False), instance_of(bool)],
    extra_keys: [not_present],
})

arg_specs_schema = obj({
    'metavar': [not_missing, uppercase_alpha],
    'help_msg': opt_specs_schema['help_msg'],
    'min': [stop_if_missing, instance_of(int)],
    'not_enough_extra_args_error': [stop_if_missing, instance_of((unicode, str))],
    extra_keys: [not_present],
})

# Note that we're using an ordered_obj here to keep the order of processing
command_definition_schema = ordered_obj({
    # Optional, can use the __doc__ string if needed
    'summary': [],
    '__doc__': [],
    'arg_specs': [if_missing_uncollect_by('name', 'arg_specs_by_name'), default([])],#, arg_specs_schema],
    'arg_specs_by_name': [],
    # We must process the help_opt_name before opt_specs so that a default for the help can be added
    'help_opt_name': [default('help')],
    # Uses the help_opt_name to automatically add a help option if there isn't one
    'opt_specs': [if_missing_uncollect_by('name', 'opt_specs_by_name'), default([]), add_help_opt_spec],#, opt_specs_schema],
    'opt_specs_by_name': [],
    # These get validated if they are used, we don't validate them here
    'child_command_specs': [default([])],
    'help_template': [default(help_template)],
    # Optional, used to ensure aliase are matched correctly
    'facility_names': [],
    'run': [not_missing],
    # The after callback is optional
    'after': [],
})

command_specs_schema = ordered_obj({
    'name': [not_missing, common_identifier_for('a command')],
    'spec': [get_missing_definitions, stop_if_missing],
    'definition': [stop_if_missing, single_dict(command_definition_schema)],
    # This overrides any summary set as an attribute of the definition
    'summary': [default_summary_from_definition],
    # Optional, used to ensure aliase are matched correctly
    'alias_specs': alias_spec_schema,
    # Optional, extend and override the defintion's child_command_specs
    'child_command_specs': [],
})

# XXX No facility definition yet
# start, stop, error, create, options

facility_specs_schema = obj({
    'name': [not_missing, common_identifier_for('a facility')],
    'spec': [validate_facility_spec],
    'definition': [],
    'alias_specs': alias_spec_schema,
    'hook_specs': obj({
         #'facility': [not_missing, common_identifier_for('the target facility')],
         'importable': [],
         'stack': [],
         'definition': [],
         'name': [],
    })
})

run_schema = command_specs_schema.copy()
run_schema.update({
    'name': [default('command'), common_identifier_for('a name')],
    'definition': [default(logging_command), single_dict(command_definition_schema)],
    #'facility_specs': facility_specs_schema,
    'out': [default(print_fn)],
    'err': [default(print_fn)],
    'help_opt_name': [default('help')],
})

class SharedStack(object):
    def __init__(
        self,
        facility_specs=None,
        option=None,
        config=None,
    ):
        self.facility_specs=[]
        for facility_spec in facility_specs or []:
            result, error = validate(facility_spec, facility_specs_schema)
            if error:
                raise Exception(format_errors(error, name='facility_spec'))
            self.facility_specs.append(result)
        self.option=option or {}
        self.facility_specs_by_name=collect_by("name", self.facility_specs)
        self.shared_facility_state=obj()
        self.stack_count = 0
        self.clone_count = 0
        self.config=obj()
        self.shared_facility_state=obj()

    def stack(self, existing_facility_specs=None):
        """\
        Return a new stack, sharing the same state as any other stacks returned from this multistack
        """
        self.stack_count += 1
        return Stack(
            self,
            existing_facility_specs=existing_facility_specs,
        )

    def clone(self):
        self.clone_count += 1
        return SharedStack(
            facility_specs=self.facility_specs,
            #hook_specs=self.hook_specs,
            option=self.option,
        )

def uncollect_by(var, data):
    result = []
    for k, v in data.iteritems():
        if v.has_key(var) and k != var[v]:
            raise Exception('Cannot uncollect XXX')
        v[var] = k
        result.append(v)
    return result

def collect_by(var='name', data=None):
    result = {}
    if data is None:
        data = {}
    for item in data:
        if not isinstance(item, dict):
            raise Exception('Expected item %r in %r to be a dictionary'%(item, data))
        if not item.has_key(var):
            raise Exception('The item %r has no %r key'%(item, var))
        if result.has_key(item[var]):
            raise Exception('Duplicate item with %s %r'%(var, item[var]))
        else:
            result[item[var]] = item
    return result


import inspect
class Facility(object):

    def __init__(self, stack, name, alias_specs, config, log=None, warn=None):
        self.stack = stack
        self.config = config
        self.name = name
        self.aliases = obj()
        for alias_spec in alias_specs:
            self.aliases[alias_spec['name']] = alias_spec['facility']
        # This gets populated with data from the first time a facility is used
        self.shared = None
        if log is None:
            self.log = Log(self.name)
        else:
            self.log = log
        if warn is None:
            self.warn = Warn()
        else:
            self.warn = warn
        self.local = obj()
        # We need to set this a slightly comlicated way so that it doesn't
        # cause problems with the __getattr__() code below.
        self.__dict__['definition'] = stack.shared.facility_specs_by_name[self.name].definition

    def hooks(self, hook_name):
        return self.stack.hooks(self.name, hook_name)

    def __getattr__(self, name):
        if name in self.__dict__:
            return self.__dict__[name]
        if name in self.__dict__.get('definition', []):
            attribute = self.__dict__['definition'].get(name)
            if attribute and inspect.isfunction(attribute):
                args, varargs, keywords, defaults = inspect.getargspec(attribute)
                if args and (\
                   args[0] == self.__dict__['name'] or args[0] == 'facility'):
                    return FacilityFunction(self, attribute)
                # XXX What about not allowing these attributes? 
                # return self.__getitem__(name)
            return attribute
        return self.__getitem__(name)

    def __getitem__(self, name):
        if name in self.aliases:
            alias = self.aliases[name]
            if not self.stack.has_key(alias):
                self.stack.start(alias)
            return self.stack[alias]
        elif self.stack and name in self.stack.shared.facility_specs_by_name:
            if not self.stack.has_key(name):
                self.stack.start(name)
            return self.stack[name]
        else:
            raise KeyError('No such facility %r'%name)

    def __repr__(self):
        return '<class Facility name=%r stack=%r id=%r>'%(
            self.__dict__['name'],
            id(self.__dict__['stack']),
            id(self),
        )

import cgitb
def text_traceback():
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        res = 'the original traceback:'.join(
            cgitb.text(sys.exc_info()).split('the original traceback:')[1:]
        ).strip()
    return res

class FacilityFunction(object):
    def __init__(self, facility, function):
        self.facility = facility
        self.function = function

    def __call__(self, *k, **p):
        return self.function(self.facility, *k, **p)

    def __repr__(self):
        return '<FacilityFunction %s.%s() id=%r>'%(
            self.facility.name,
            self.function.__name__,
            id(self),
        )

class Stack(object):
    # Keeps self.started.facilities = track of the order of pipes
    def __init__(self, shared, existing_facility_specs=None):
        self.shared = shared
        self.started = obj()
        if existing_facility_specs:
            self.started['facilities'] = OrderedDict(existing_facility_specs[:])
        else:
            self.started['facilities'] = OrderedDict()
        self.finished = False
        self.started['hooks'] = obj()

    def __getitem__(self, name):
        return self.started.facilities[name]

    def has_key(self, name):
        return self.started.facilities.has_key(name)

    def __getattr__(self, name):
        return self.__getitem__(name)

    def __getitem__(self, name):
        if name in self.__dict__:
            return self.__dict__[name]
        elif name in self.started.facilities:
            return self.started.facilities[name]
        else:
            raise AttributeError('No such started facility %r'%name)

    #def extend(self, config, options, alias_specs, hook_specs):
    #"""\
    #New use case:
    #
    #Private facilities.
    #
    #The use cases are:
    #* Internal implementation of a complex component which itself would benefit from a facility architecture but which can't be:
    #  * implemented by a clonek because it relies on other running services
    #
    #Option 1:
    #
    #Create a new stack from the existing sharedstack with stack() if there was the ability to set extra config, facility_specs, aliases and hooks.
    #
    #Need to decide:
    #* How aliases would work
    #  Here we have something like:
    #
    #  ::
    #
    #      html_document.site
    #      html_document.rst_document
    #      file.stack.site.private.html_document
    #
    # 
    #  But then if we want parent.site to be aliased to something else we nen
    #
    #
    #* How configuration would work
    #* How hooks would work
    #
    # because how would the configuration be used?
    #
    #
    #This is all a bit more complicated than it probably needs to be. Life would be simpler, if the sharedstack could be extended with extra information but then how would the other stacks be affected?
    #
    #To make this work we'd need the concept of sub_config
    #
    #::
    #
    #    site->html_document.type = ext
    #
    #
    #
    #
    #
    #Option 2:
    #
    #Make the user add all the facilites at define time
    #Bad: * Causes a lot more work for the user 
    #Option 3:
    #
    #Create a new shared stack just for the private work
    #Bad: * No access to existing facilities
    #
    #
    #Two use cases:
    #* Initialising plugins with logging compatible with the facility
    #* Writing libraries as facilities, but because they are not publicly exposed, not making them part of the main stack.
    #
    #
    #
    #Conclusion:
    #
    #* Just pass the site object around anyway. Later you can rename it to something else with find and replace.
    #* Set local variables like site['name'] = var
    #"""
    #    # XXX This would be used to create an object that behaved like a stack, but proxied any attributes to the parent stack when needed
    #    pass

    def hooks(self, facility_name, hook_name):
        # Merge facility_specs
        hook_specs = []
        used = []
        for facility_spec in self.shared.facility_specs:
            if facility_spec.name == facility_name:
                for hook_spec in facility_spec.get('hook_specs', []):
                    if hook_spec.name == hook_name:
                        hook_specs.append(hook_spec)
        if not facility_name in self.started.facilities:
            self.start(facility_name)
        for hook_spec in self[facility_name].definition.get('hook_specs', []):
            # Convert the hook spec then use attribure access
            if hook_spec['name'] == hook_name:
                hook_specs.append(hook_spec)
        hooks = []
        for hook_spec in hook_specs:
            definition = None
            if hook_spec.has_key('definition'):
                definition = hook_spec['definition']
            else:
                if hook_spec.has_key('importable'):
                    definition = hook_spec['definition'] = \
                       import_and_return(hook_spec['importable'])
                elif hook_spec.has_key('stack'):
                    hook_facility, importable = \
                       hook_spec.stack.split(':')
                    if not self.has_key(hook_facility):
                        self.start(hook_facility)
                    definition = getattr(
                        self, 
                        hook_facility,
                    )
                    for part in importable.split('.'):
                        definition = getattr(
                            definition, 
                            part,
                        )
                else:
                    raise Exception(
                        "A hook spec cannot have both a 'stack' "
                        "and 'importable' key"
                    )
            hooks.append(definition)
        # XXX Currently no way to see if the hook name is correct.
        return hooks

    def finish(self, error=False):
        if self.finished:
            return
        self.finished = True
        for name in self.started.facilities:
            try:
                facility = self.started.facilities[name]
                if not error:
                    try:
                        if hasattr(facility.definition, 'stop'):
                            facility.definition.stop(facility)
                        del self.started.facilities[name]
                    except Exception, e:
                        log.error(
                            "Error occurred calling the __stop__() handler "
                            "of the %r facility. About to call the "
                            "__error__() handler instead. The error was: %s",
                            name,
                            text_traceback(),
                        )
                        if hasattr(facility.definition, 'error'):
                            facility.definition.error(facility)
                        error = True
                else:
                    if hasattr(facility.definition, 'error'):
                        facility.definition.error(facility)
            except Exception, e:
                tb = text_traceback()
                if error:
                    log.error(
                        "Error occurred calling the error() handler of "
                        "the %r facility. The error was: %r",
                        name,
                        tb,
                    )
                else:
                    log.error(
                        "Error occurred calling the stop() handler of "
                        "the %r facility. The error was: %r",
                        name,
                        tb,
                    )
                error = True

    def start(self, name):
        if name in self.started.facilities:
            raise Exception('The facility %r has already been started'%name)
        # Otherwise if the facility is not part of the stack, throw an error
        if not name in self.shared.facility_specs_by_name:
            raise Exception('No such facility named %r'%name)
        # The facility exists and we need to create a ``Facility()``
        # instance for it. Let's try and import it.
        facility_spec = self.shared.facility_specs_by_name[name]
        if not facility_spec.has_key('definition'):
            # We've not used this facility before, import it
            facility_spec['definition'] = import_and_return(facility_spec.spec)
            # We now have the object and the config we can set up the shared state
        # Now ensure any config we need exists
        if not self.shared.config.has_key(name):
            if self.shared.option.has_key(name):
                option = self.shared.option[name]
            else:
                option = {}
            schema = obj(getattr(facility_spec.definition, 'option_schema', {}))
            result, error = validate(option, schema)
            if error:
                raise Exception('Error parsing config file. %s'%format_errors(error, "option['"+name+"']"))
            self.shared.config[name] = result
            result, error = validate(
                {'alias_specs':getattr(facility_spec.definition, 'alias_specs', [])},
                obj({'alias_specs':alias_spec_schema}),
            )
            if error:
                raise Exception(error)
            cur_alias_specs = []
            names_used = []
            for alias_spec in getattr(facility_spec, 'alias_specs', []):
                cur_alias_specs.append(alias_spec)
                names_used.append(alias_spec.name)
            for alias_spec in result.alias_specs:
                if alias_spec.name not in names_used:
                    cur_alias_specs.append(alias_spec)
            # XXX self.shared.config[name] = result
            facility_spec['alias_specs'] = cur_alias_specs
        # XXX Need to check the attributes of the facility don't
        #      interfere with any alias_specs etc
        facility = Facility(
            stack=self,
            name=name,
            config=self.shared.config[name],
            alias_specs=facility_spec.get('alias_specs', {}),
        )
        self.started.facilities[name] = facility
        created = False
        if not self.shared.shared_facility_state.has_key(name):
            created = True
            self.shared.shared_facility_state[name] = obj()
        facility.shared = self.shared.shared_facility_state[name]
        if created and hasattr(facility.definition, 'create'):
            facility.definition.create(facility)
        if hasattr(facility.definition, 'start'):
            facility.definition.start(facility)
        self.started.facilities[name] = facility

def flow(shared, existing_facility_specs=[], ensure=[], run=None):
    for name in ensure:
        if ensure.count(name)>1:
            raise Exception('The facility %r is specified more than once in the ensure argument'%name)
    #if bag is None:
    #    stack = Stack(options={}, config={})
    #else:
    #    for name in reserved:
    #        if stack.has_key(name):
    #            raise Exception('Stacks are not allowed to have a key named %r'%name)
    #    for name in reserved:
    #        if hasattr(bag, name):
    #            raise Exception('Stacks are not allowed to have an attribute named %r'%name)
    stack = shared.stack()
    #for name in ensure:
    #    stack.start(name)
    try:
        result = run(stack)
    except Exception, e:
        #log.error(text_traceback())
        if not stack.finished:
            stack.finish(True)
        raise
    stack.finish(False)
    return result

def find_commands(package, path):
    child_command_specs = []
    if not os.path.isdir(path):
        path = os.path.dirname(path)
    if os.path.exists(path):
        for filename in os.listdir(path):
            if not os.path.isdir(os.path.join(path, filename)):
                if filename.endswith('.py') and \
                   not filename == '__init__.py':
                    # Treat this is a command
                    module = filename[:-3]
                    child_command_specs.append(
                        {
                            'name': module, 
                            'spec': '%s.%s'%(package, module),
                        }
                    )
            elif os.path.exists(os.path.join(path, filename, '__init__.py')):
                module = filename
                child_command_specs.append(
                    {
                        'name': module, 
                        'spec': '%s.%s'%(package, module),
                    }
                )
    return child_command_specs

def run(
    child_command_specs=None,
    argv=None,
    definition=None,
    name=None,
    summary=None,
    facility_specs=None,
    option=None,
    run=None,
    out=print_fn,
    err=print_fn,
    help_opt_name='help',
    alias_specs=None,
):
    """\
    Convenience function to construct a stack and start a flow.

    At this stage we import the commands, but we don't check the facility_specs or the hook_specs.

    We then create a ``SharedStack`` instance and run it so that the ``run()``
    handler runs the command handling. This approach then allows the commands
    themselves to use the facility_specs if needed.

    One of the commands will normally set the ``options`` and the ``config``
    before either calling ``shared.stack()`` to create a stack from the same shared
    stack that was used to run the command, or ``shared.clone()`` to create a new,
    uninitilised shared stack and to start the flow from a stack derived from that.
    """
    data = {
        "name": name,
        "definition": definition,
        "child_command_specs": child_command_specs or [],
        # Facility specs get validated later
        #"facility_specs": facility_specs or [],
        "summary": summary,
        "help_opt_name": help_opt_name,
        "out": out,
        "err": err,
        "alias_specs": alias_specs or [],
    }
    result, errors = validate(data, run_schema)
    if errors:
        raise Exception('Invalid arguments to run(). The error(s) were: %r'%errors)
    result = obj(result)
    shared = SharedStack(
        option=option,
        facility_specs=facility_specs,
    )
    if run is None:
        # All the keys apart from facility specs can be treated as 
        # handle_command() arguments
        def run(stack):
            return handle_command(
                argv = argv or sys.argv[1:],
                stack=stack,
                **result
            )
    return flow(shared, run=run)

#############################################################################
#
# Bare Necessities
#
# These are functions and classes I use so frequently I wish 
# they were in the standard library (in fact one of them is as of Python 2.6!).
# 
# These all work with Python 2.4 and above and may work with earlier versions 
# too.

import logging
import os
import sys

def timedelta_to_seconds(td):
    return (td.days * 24*60*60) + td.seconds

def timedelta_to_days(td, length=7.5):
    return timedelta_to_seconds(td)/(length*60*60)

def day_of_month_in_english(day):
    day = int(str(day).lstrip('0'))
    if day in [4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,24,25,26,27,28,29,30]:
        return '%sth'%day
    elif day in [1,21,31]:
        return '%sst'%day
    elif day in [2,22]:
        return '%snd'%day
    elif day in [3,23]:
        return '%srd'%day
    else: 
        raise Exception('Unknown day %r'%day)

try:
    import posixpath
    relpath = posixpath.relpath
    # relpath path import (available in Python 2.6 and above)
except (NameError, AttributeError):
    from posixpath import curdir, sep, pardir, join
    def relpath(path, start=curdir):
        """Return a relative version of a path"""
        if not path:
            raise ValueError("no path specified")
        start_list = posixpath.abspath(start).split(sep)
        path_list = posixpath.abspath(path).split(sep)
        # Work out how much of the filepath is shared by start and path.
        i = len(posixpath.commonprefix([start_list, path_list]))
        rel_list = [pardir] * (len(start_list)-i) + path_list[i:]
        if not rel_list:
            return curdir
        return join(*rel_list)
except (ImportError):
    # We are in the wrong platform
    def relpath(path, start=curdir):
        raise NotImplementedError(
            'The relpath() function is only implemented on posix platforms'
        )

def walk(top, topdown=True, onerror=None, followlinks=False):

    from os.path import join, isdir, islink
    from os import error, listdir

    # We may not have read permission for top, in which case we can't
    # get a list of the files the directory contains.  os.path.walk
    # always suppressed the exception then, rather than blow up for a
    # minor reason when (say) a thousand readable directories are still
    # left to visit.  That logic is copied here.
    try:
        # Note that listdir and error are globals in this module due
        # to earlier import-*.
        names = listdir(top)
    except error, err:
        if onerror is not None:
            onerror(err)
        return

    dirs, nondirs = [], []
    for name in names:
        if isdir(join(top, name)):
            dirs.append(name)
        else:
            nondirs.append(name)

    if topdown:
        yield top, dirs, nondirs
    for name in dirs:
        path = join(top, name)
        if followlinks or not islink(path):
            for x in walk(path, topdown, onerror, followlinks):
                yield x
    if not topdown:
        yield top, dirs, nondirs

def uniform_path(path):
    """\
    Strips trailing / from a directory.
    """
    path = os.path.abspath(os.path.normcase(os.path.normpath(path)).replace('\\', '/'))
    return path

def file_contents(filename):
    fp = open(filename, 'rb')
    try:
        return fp.read()
    finally:
        fp.close()

#############################################################################
#
# TestPipe
#

"""
Used like this

Run the tests as follows:

::

    cd facilify/test
    python run.py

Run the coverage check as follows:

::

    python /usr/lib/python2.6/dist-packages/coverage.py -x run.py
    python /usr/lib/python2.6/dist-packages/coverage.py -r -m ../__init__.py

Write a test like this:

::

    import facilify
    
    class TestUpdate(facilify.TestCase):
    
        def test_01_shared_present(self):
            self.assertEqual(self.shared.config, {})
    
        def test_02_facility_started(self):
            stack = self.shared.stack()
            stack.start('some_facility')
            self.assertEqual(stack.some_facility.name, 'some_facility')
    
Here's the run.py file:

::

    import logging
    logging.basicConfig(level=logging.ERROR)
    
    if __name__ == "__main__":

        # Normal doctests
        import doctest
        doctest.testmod(facilify, optionflags=doctest.ELLIPSIS)
        doctest.run_docstring_examples(
            facilify.parse_argv, facilify.__dict__
        )

        # Facilify tests
        import facilify
        shared = facilify.SharedStack(...)
        testLoader = facilify.TestLoader(shared)
        facilify.TestProgram(testLoader, module="facilify.test.command")
        facilify.TestProgram(testLoader, module="facilify.test.ordered_dict")
        facilify.TestProgram(testLoader, module="facilify.test.facilities")

"""

import os
import sys
import types
from unittest import TestCase as BaseTestCase, TestSuite, TestLoader as BaseTestLoader, TextTestRunner, TestProgram as BaseTestProgram

class TestCase(BaseTestCase):
    
    def __init__(self, shared, methodName='run'):
        self.shared = shared
        BaseTestCase.__init__(self, methodName)

class TestLoader(BaseTestLoader):
    suiteClass = TestSuite

    def __init__(self, shared):
        self.shared = shared

    def loadTestsFromTestCase(self, testCaseClass):
        """Return a suite of all tests cases contained in testCaseClass"""
        if issubclass(testCaseClass, TestSuite):
            raise TypeError("Test cases should not be derived from TestSuite. Maybe you meant to derive from TestCase?")
        testCaseNames = self.getTestCaseNames(testCaseClass)
        if not testCaseNames and hasattr(testCaseClass, 'runTest'):
            testCaseNames = ['runTest']
        tests = []
        for name in testCaseNames:
             tests.append(testCaseClass(self.shared, name))
        return self.suiteClass(tests)

    def loadTestsFromName(self, name, module=None):
        """Return a suite of all tests cases given a string specifier.

        The name may resolve either to a module, a test case class, a
        test method within a test case class, or a callable object which
        returns a TestCase or TestSuite instance.

        The method optionally resolves the names relative to a given module.
        """
        parts = name.split('.')
        if module is None:
            parts_copy = parts[:]
            while parts_copy:
                try:
                    module = __import__('.'.join(parts_copy))
                    break
                except ImportError:
                    del parts_copy[-1]
                    if not parts_copy: raise
            parts = parts[1:]
        obj = module
        for part in parts:
            parent, obj = obj, getattr(obj, part)

        if type(obj) == types.ModuleType:
            return self.loadTestsFromModule(obj)
        elif (isinstance(obj, (type, types.ClassType)) and
              issubclass(obj, TestCase)):
            return self.loadTestsFromTestCase(obj)
        elif (type(obj) == types.UnboundMethodType and
              isinstance(parent, (type, types.ClassType)) and
              issubclass(parent, TestCase)):
            # @@@ This is the line we changed.
            return TestSuite([parent(self.shared, obj.__name__)])
        elif isinstance(obj, TestSuite):
            return obj
        elif hasattr(obj, '__call__'):
            test = obj()
            if isinstance(test, TestSuite):
                return test
            elif isinstance(test, TestCase):
                return TestSuite([test])
            else:
                raise TypeError("calling %s returned %s, not a test" %
                                (obj, test))
        else:
            raise TypeError("don't know how to make test from: %s" % obj)

class TestProgram(BaseTestProgram):
    def __init__(self, testLoader=None, module='__main__', defaultTest=None,
                 argv=None, testRunner=None):
        BaseTestProgram.__init__(self, module=module, defaultTest=defaultTest,
                 argv=argv, testRunner=testRunner,
                 testLoader=testLoader)

    def runTests(self):
        if self.testRunner is None:
            self.testRunner = TextTestRunner

        if isinstance(self.testRunner, (type, types.ClassType)):
            try:
                testRunner = self.testRunner(verbosity=self.verbosity)
            except TypeError:
                # didn't accept the verbosity argument
                testRunner = self.testRunner()
        else:
            # it is assumed to be a TestRunner instance
            testRunner = self.testRunner
        result = testRunner.run(self.test)
        return not result.wasSuccessful()

#############################################################################
#
# New helpers
#

def str_keys(dictionary, ignore=None):
    """\
    Python <2.6 cannot accept dictionaries where the keys are Unicode strings as
    arguments to functions using the ``**`` operator, even if they are only made of
    characters ``a-zA-Z0-9_``. ``str_keys()`` takes such a dictionary with
    Unicode keys and turns the keys into 8-bit strings.


    Used like this to convert dictionaries with Unicode keys to ones without so
    that they can be used with the ``**`` operator to call functions.
    
    ::
    
        >>> import sys
        >>> 
        >>> def test(a=None, b=None):
        ...     print a, b
        >>> test(**str_keys({u'a': u'1', u'b': u'2'}))
        1 2
    
    In Python 2.6 and above this works without needing ``str_keys()``.

    ``str_keys()`` also takes an optional argument ``ignore`` which should be a list
    of keys to not include in the final dictionary:

    ::

        >>> new_dict = str_keys({u'a': u'1', u'b': u'2'}, ignore=['a'])
        >>> new_dict
        {'b': u'2'}
        >>> test(**new_dict)
        None 2

    """
    if ignore is None:
        ignore = []
    new_dict = {}
    for k, v in dictionary.iteritems():
        if not isinstance(k, (str, unicode)):
            raise TypeError('Expected the key %r to be a string'*k)
        if not k in ignore:
            new_dict[str(k)] = v
    return obj(new_dict)

def getcallargs(func, *positional, **named):
    """Get the mapping of arguments to values when calling func(*positional, **named).

    A dict is returned, with keys the function argument names (including the
    names of the * and ** arguments, if any), and values the respective bound
    values from 'positional' and 'named'.

    For example:

    ::

        >>> getcallargs(uniform_path, 'test')
        {'path': 'test'}

    """
    args, varargs, varkw, defaults = inspect.getargspec(func)
    f_name = func.__name__
    arg2value = {}

    # the following closures are basically because of tuple parameter unpacking
    assigned_tuple_params = []
    def assign(arg, value):
        if isinstance(arg, str):
            arg2value[arg] = value
        else:
            assigned_tuple_params.append(arg)
            value = iter(value)
            for i, subarg in enumerate(arg):
                try:
                    subvalue = next(value)
                except StopIteration:
                    raise ValueError('need more than %d %s to unpack' %
                                     (i, 'values' if i>1 else 'value'))
                assign(subarg,subvalue)
            try: next(value)

            except StopIteration: pass
            else: raise ValueError('too many values to unpack')
    def is_assigned(arg):
        if isinstance(arg,str):
            return arg in arg2value
        return arg in assigned_tuple_params
    if inspect.ismethod(func):
        # implicit 'self' (or 'cls' for classmethods) argument
        if func.im_self is not None:
            positional = (func.im_self,) + positional
        elif not positional or not isinstance(positional[0], func.im_class):
            got = ('%s instance' % type(positional[0]).__name__ if positional
                                                                else 'nothing')
            raise TypeError('unbound method %s() must be called with %s '
                            'instance as first argument (got %s instead)' %
                            (f_name, func.im_class.__name__, got))
    num_pos = len(positional)

    num_total = num_pos + len(named)
    num_args = len(args)
    num_defaults = len(defaults) if defaults else 0
    for arg, value in zip(args, positional):
        assign(arg, value)
    if varargs:
        if num_pos > num_args:
            assign(varargs, positional[-(num_pos-num_args):])
        else:
            assign(varargs, ())
    elif 0 < num_args < num_pos:

        raise TypeError('%s() takes %s %d %s (%d given)' % (
            f_name, 'at most' if defaults else 'exactly', num_args,
            'arguments' if num_args>1 else 'argument', num_total))
    elif num_args == 0 and num_total:
        raise TypeError('%s() takes no arguments (%d given)' % (f_name, num_total))
    for arg in args:
        if isinstance(arg, str) and arg in named:
            if is_assigned(arg):
                raise TypeError("%s() got multiple values for keyword "
                                "argument '%s'" % (f_name, arg))
            else:
                assign(arg, named.pop(arg))
    if defaults:    # fill in any missing values with the defaults
        for arg, value in zip(args[-num_defaults:], defaults):
            if not is_assigned(arg):
                assign(arg, value)

    if varkw:
        assign(varkw, named)
    elif named:
        unexpected = next(iter(named))
        if isinstance(unexpected, unicode):
            unexpected = unexpected.encode(sys.getdefaultencoding(), 'replace')
        raise TypeError("%s() got an unexpected keyword argument '%s'" %
                        (f_name, unexpected))
    unassigned = num_args - len([arg for arg in args if is_assigned(arg)])
    if unassigned:
        num_required = num_args - num_defaults
        raise TypeError('%s() takes %s %d %s (%d given)' % (
            f_name, 'at least' if defaults else 'exactly', num_required,
            'arguments' if num_required>1 else 'argument', num_total))
    return arg2value

#import functools
def conform(schema):
    def conform_decorator(func):
        #@functools.wraps(func)
        def conform_function_wrapper(facility, *args, **kwargs):
            # Check it is valid
            data = getcallargs(func, facility, *args, **kwargs)
            args, varargs, keywords, defaults = inspect.getargspec(func)
            # Don't validate the facility itself!
            del data[args[0]]
            result, errors = validate(data, schema)
            if errors:
                raise Exception(format_errors(errors, name=func.__name__+'() args'))
            return func(facility, **result)
        return conform_function_wrapper
    return conform_decorator

import subprocess
import threading
import StringIO
def process(
    cmd,
    out=None,
    err=None,
    in_data=None,
    merge=False,
    echo=False,
    **popen_args
):
    """\
    For most cases ``in_data`` should end with a \n.
    """
    out_data = StringIO.StringIO()
    err_data = StringIO.StringIO()
    if out is None:
        def out(fh, stdin, output):
            while True:
                line = fh.readline()
                if not line:
                    break
                if echo:
                    print line
                output.write(line)
    elif merge:
        raise Exception("The 'merge' option doesn't work with a custom 'out' function")
    elif echo:
        raise Exception("The 'echo' option doesn't work with a custom 'out' function")
    if err is None:
        def err(fh, stdin, output):
            while True:
                line = fh.readline()
                if not line:
                    break
                if echo:
                    print line
                output.write(line)
    elif merge:
        raise Exception("The 'merge' option doesn't work with a custom 'err' function")
    elif echo:
        raise Exception("The 'echo' option doesn't work with a custom 'err' function")
    process = subprocess.Popen(
        cmd, 
        stdin=subprocess.PIPE, 
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE,
        **popen_args
    )
    stdout_thread = threading.Thread(
        target=out,
        args=(process.stdout, process.stdin, out_data)
    )
    stdout_thread.setDaemon(True)
    stdout_thread.start()
    stderr_thread = threading.Thread(
        target=err,
        args=(process.stderr, process.stdin, merge and out_data or err_data)
    )
    stderr_thread.setDaemon(True)
    stderr_thread.start()
    if in_data is not None:
        process.stdin.write(in_data)
    retcode = process.wait()
    stdout_thread.join()
    stderr_thread.join()
    result = obj(
        stdout=out_data.getvalue(),
        stderr=err_data.getvalue(),
        retcode=retcode,
    )
    return result

from unicodedata import decomposition
import string
def char_string(text, replace='-', allowed='-.'):
    result = u''
    for c in text:
        d = decomposition(c)
        if d:
            result += unichr(int(d.split()[0], 16))
        elif c in allowed+string.lowercase+string.uppercase+allowed:
            result += c
        else:
            result += '-'
    while '--' in result:
        result = result.replace('--', '-')
    return result
