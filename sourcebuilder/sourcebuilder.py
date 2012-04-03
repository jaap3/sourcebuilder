try:
    from cStringIO import StringIO
except ImportError:  # pragma: no cover
    from StringIO import StringIO

INDENT = ' ' * 4


class DedentException(Exception):
    """
    Raised to signify that decreasing the indent level beyond zero
    is impossible.
    """


class IndentManager(object):
    """
    A context manager for indentation. Used internally by the source manager
    to provide the indent context manager. And the indent and dedent methods.

    """
    def __init__(self, indent_with=INDENT):
        self.indent_with = indent_with
        self.level = 0

    def __call__(self):
        """
        Raise the indentation level if this instance is called like a method.

        """
        self.indent()

    def __str__(self):
        """
        self.indent_with multiplied by the current indentation level.
        Used to indent strings to the correct depth.

        """
        return self.indent_with * self.level

    def __enter__(self):
        """
        Start of an indentation context.

        """
        self.indent()
        return self

    def __exit__(self, *exc_info):
        """
        Ends of an indentation context, so dedent.

        """
        self.dedent()

    def indent(self):
        """Raise the indentation level by 1."""
        self.level = self.level + 1
        return self

    def dedent(self):
        """
        Decrease the indentation level by one. If the indentation level is
        already at zero a ``DedentException`` is raised.

        """
        if self.level == 0:
            raise DedentException('Indent level is already at zero.')
        self.level = self.level - 1

    def reset(self):
        """
        Reset the indentation level to zero.

        """
        self.level = 0


class SourceBuilder(object):
    """
    A basic source code writer.

    Usage
    -----

    Create a SourceBuilder instance  and write code to it to line by line.
    By using the ``indent`` context manager each line gets correctly indented
    and the input indentation will resemble the output::

      >>> sb = SourceBuilder()
      >>> sb.writeln()
      >>> sb.writeln('def hello_world():')
      >>> with sb.indent:
      ...     sb.writeln('print \'Hello World\'')
      ...
      ...
      >>> sb.writeln()
      >>> sb.writeln('hello_world()')
      >>> source = sb.end()
      >>> print source

      def hello_world():
          print 'Hello World'

      hello_world()

    If for some reason context managers can't be used ``indent`` also works
    as a method. Combined with the ``dedent`` method code indentation levels
    can be controlled manually.::

      >>> sb = SourceBuilder()
      >>> sb.writeln()
      >>> sb.writeln('def hello_world():')
      >>> sb.indent()
      >>> sb.writeln('print \'Hello World\'')
      >>> sb.dedent()
      >>> sb.writeln()
      >>> sb.writeln('hello_world()')
      >>> source = sb.end()
      >>> print source

      def hello_world():
           print 'Hello World'

      hello_world()

    It's not advised to use ``sb.indent`` in ``with`` statements in combination
    with calls to ``sb.dedent()`` or ``sb.indent()``.

    """
    def __init__(self, indent_with=INDENT):
        """
        Initialize SourceBuilder, ``indent_with`` is set to 4 spaces
        by default.

        """
        self._out = StringIO()
        self.indent = IndentManager(indent_with=indent_with)

    def write(self, code):
        """
        Write code at the current indentation level.

        """
        self._out.write(str(self.indent))
        self._out.write(code)

    def writeln(self, code=''):
        """
        Write a line at the current indentation level.
        If no code is given only a newline is written.

        """
        if code:
            self.write(code)
        self._out.write('\n')

    def dedent(self):
        """
        Decrease the current indentation level. Should only be used if
        the indent context manager is not used.

        Raises a ``DedentException`` if decreasing indentation level is not
        possible.

        """
        self.indent.dedent()

    def end(self):
        """
        Get the generated source and resets the indent level.

        """
        self.indent.reset()
        return self._out.getvalue()

    def truncate(self):
        '''
        Discard generated source and memory buffer and resets the indent level.

        '''
        if not self._out.closed:
            self._out.close()
        self._out = StringIO()
        self.indent.reset()

    def close(self):
        '''
        Convenience method for use with ``contextlib.closing``.
        Calls ``self.truncate()``.
        '''
        self.truncate()
