from __future__ import with_statement
import textwrap
from contextlib import contextmanager
from sourcebuilder import SourceBuilder

INDENT = ' ' * 4
TRIPLE_QUOTES = '"' * 3
DOCSTRING_WIDTH = 72


class PySourceBuilder(SourceBuilder):
    '''
    A special SourceBuilder that provides some convenience context managers
    for writing well formatted Python code.
    '''

    def __init__(self, indent_with=INDENT):
        super(PySourceBuilder, self).__init__(indent_with=indent_with)
        self._out = SourceBuilder()

    def end(self):
        '''
        Get the output and close the internal stream.
        '''
        return self._out.end()

    @contextmanager
    def block(self, code, lines_before=0):
        '''
        A context manager for block structures,

        A generic way to start a control structure (if, try, while, for etc.)
        or a class, function or method definition.

        The given ``code`` will be printed preceded by 0 or more blank lines,
        controlled by the ``lines_before`` parameter.

        An indent context is then started.
        '''
        for i in range(lines_before):
            self.writeln()
        self.writeln(code)
        with self.indent:
            yield

    def docstring(self, doc, delimiter=TRIPLE_QUOTES, width=DOCSTRING_WIDTH):
        '''
        Write a docstring. The given ``doc`` is surrounded by triple double
        quotes ("""). This can be changed by passing a different ``delimiter``
        (triple single quotes).

        The docstring is reformatted to not run past 72 characters per line.
        This can be changed by passing a different ``width`` parameter.
        '''
        max_width = width - len(str(self.indent))
        lines = doc.splitlines()
        if len(lines) == 1 and len(doc) < max_width - len(delimiter) * 2:
            self.writeln(u'%s%s%s' % (delimiter, doc, delimiter))
        else:
            self.writeln(delimiter)
            for line in lines:
                for wrap in textwrap.wrap(line, max_width):
                    self.writeln(wrap)
            self.writeln(delimiter)
