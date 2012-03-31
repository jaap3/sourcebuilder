try:
    from cStringIO import StringIO
except ImportError:  # pragma: no cover
    from StringIO import StringIO

INDENT = ' ' * 4


class IndentManager(object):
    '''
    A context manager for indentation. Used internally by the source manager
    to provide the indent context manager. And the indent and dedent methods.
    '''

    def __init__(self):
        self.level = 0

    def __call__(self):
        '''
        Raise the indentation level if this instance is called like a method.
        '''
        self.indent()

    def __enter__(self):
        '''
        Start of an indentation context.
        '''
        self.indent()
        return self

    def __exit__(self, *exc_info):
        '''
        Ends of an indentation context, so dedent.
        '''
        self.dedent()

    def indent(self):
        '''
        Raise the indentation level by 1.
        '''
        self.level = self.level + 1
        return self

    def dedent(self):
        '''
        Decrease the indentation level by one. If the indentation level is
        already at zero an exception is raised.
        '''
        if self.level == 0:
            raise Exception('Indent level is already at zero.')
        self.level = self.level - 1


class SourceBuilder(object):
    '''
    A basic source code writer.
    '''

    def __init__(self):
        self._out = StringIO()
        self.indent = IndentManager()

    def write(self, code):
        '''
        Write something at the current indentation level.
        '''
        self._out.write(INDENT * self.indent.level)
        self._out.write(code)

    def writeln(self, code=''):
        '''
        Write a line at the current indentation level.
        If no code is given only a newline is written.
        '''
        if code:
            self.write(code)
        self._out.write('\n')

    def dedent(self):
        '''
        Decrease the current indentation level. Should only be used if
        the indent context manager is not used.
        '''
        self.indent.dedent()

    def end(self):
        '''
        Get the output and close the internal stream.
        '''
        value = self._out.getvalue()
        self.close()
        return value

    def close(self):
        '''
        Close the internal stream.
        '''
        self._out.close()
