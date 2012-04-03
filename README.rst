=============
SourceBuilder
=============

SourceBuilder is a simple way to write (Python) code using Python code.

Examples
========

Say you want to generate stub class definitions for two Python classes
named ``Foo`` and ``Bar``. This can be achieved using the following code::

    >>> from sourcebuilder import PySourceBuilder
    >>> klasses = ['Foo', 'Bar']
    >>> sb = PySourceBuilder()
    >>> for klass in klasses:
    ...     with sb.block('class {0}(object)'.format(klass):, 2):
    ...         sb.docstring('TODO: Document {0}'.format(klass))
    ...         with sb.block('def __init__(self):'):
    ...             sb.writeln('pass')
    ...
    >>> source = sb.end()
    >>> print source


    class Foo(object):
        """TODO: Document Foo"""
        def __init__(self):
            pass


    class Bar(object):
        """TODO: Document Bar"""
        def __init__(self):
            pass

There's also the generic SourceBuilder. It doesn't come with the block
context manager or docstring method, but it's a starting point for writing
your own custom SourceBuilder implementation.

The following example shows how to use the generic SourceBuilder to generate
(nearly) the same code as the previous example (sans docstrings)::

    >>> from sourcebuilder import SourceBuilder
    >>> sb = SourceBuilder()
    >>> for klass in klasses:
    ...     sb.writeln()
    ...     sb.writeln('class {0}(object):'.format(klass))
    ...     with sb.indent:
    ...         sb.writeln('def __init__(self):')
    ...         with sb.indent:
    ...             sb.writeln('pass')
    ...     sb.writeln()
    ...
    >>> source = sb.end()

Usage
=====

Create a SourceBuilder instance and write code to it to line by line.
Currently there's a generic SourceBuilder and a PySourceBuilder.

Shared Methods
--------------

``__init__(indent_with='    ')``
********************************
Initialize a SourceBuilder, ``indent_with`` is set to 4 spaces by default.

``write(code)``
***************
Write code at the current indentation level.

``writeln(code='')``
********************
Write a line at the current indentation level.
If no code is given only a newline is written.

``end()``
*********
Get the generated source and resets the indent level.

``dedent()``
************
Decrease the current indentation level. Should only be used if the indent
context manager is not used.

``truncate(self)``
******************
Discard generated source and memory buffer and resets the indent level.

``close()``
***********
Convenience method for use with ``contextlib.closing``.
Calls ``self.truncate()``.

Indentation
-----------

The code is indented with 4 spaces each level by default. This can be
changed by setting ``indent_with`` on initialization::

    >>> sb = SourceBuilder(indent_with='\t')

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

PySourceBuilder Methods
-----------------------

PySourceBuilder inherits from the generic SourceBuilder and adds some Python
specific methods and context managers.

``block(code, lines_before=0)``
*******************************

A context manager for block structures. It's a generic way to start a
control structure (if, try, while, for etc.) or a class, function or
method definition.

The given ``code`` will be printed preceded by 0 or more blank lines,
controlled by the ``lines_before`` parameter. An indent context is
then started.

Example::

    sb = PySourceBuilder()
    >>>
    >>> with sb.block('class Hello(object):', 2):
    ...     with sb.block('def __init__(self, what=\'World\'):', 1):
    ...         sb.writeln('pass')
    ...
    >>> print sb.end()


    class Hello(object):

        def __init__(self, what='World'):
            pass

``docstring(doc, delimiter='"""', width=72)``
*********************************************

Write a docstring. The given ``doc`` is surrounded by triple double
quotes ("""). This can be changed by passing a different ``delimiter``
(e.g. triple single quotes).

The docstring is formatted to not run past 72 characters per line (including
indentation). This can be changed by passing a different ``width`` parameter.

Compatibility
=============

SourceBuilder has 100% test coverage and passes all its tests in Python 2.5,
2.6 and 2.7.

Credits
=======

This project was started on Sat Mar 31 2012 by Jaap Roes.

It is in part inspired by
'`A Python Code Generator <http://effbot.org/zone/python-code-generator.htm>`_'
by Fredrik Lundh, Mar 1998
