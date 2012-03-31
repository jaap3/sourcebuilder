=============
SourceBuilder
=============

SourceBuilder is a simple way to write (python) code using python code.

Example
=======

Say you want to generate stub class definitions for two clases named ``Foo``
and ``Bar``. This can be achieved using the following code::

  >>> from sourcebuilder import SourceBuilder
  >>> klasses = ['Foo', 'Bar']
  >>> sb = SourceBuilder()
  >>> for klass in klasses:
  ...     sb.writeln()
  ...     sb.writeln('class {0}(object)'.format(klass))
  ...     with sb.indent:
  ...         sb.writeln('def __init__(self):')
  ...         with sb.indent:
  ...             sb.writeln('pass')
  ...     sb.writeln()
  ...
  >>> source = sb.end()
  >>> print source

  class Foo(object)
      def __init__(self):
          pass


  class Bar(object)
      def __init__(self):
          pass


Usage
=====

Create a SourceBuilder instance and write code to it to line by line.

Methods
-------

``__init__(self, indent_with='    ')``
Initialize SourceBuilder, ``indent_with`` is set to 4 spaces by default.

``close(self)``
Close the internal stream.

``dedent(self)``
Decrease the current indentation level. Should only be used if the indent
context manager is not used.

``end(self)``
Get the output and close the internal stream.

``write(self, code)``
Write code at the current indentation level.

``writeln(self, code='')``
Write a line at the current indentation level.
If no code is given only a newline is written.

Indentation
-----------

The code is indented by 4 spaces each level by default. This can be
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

It's not advised to combine ``sb.indent`` in ``with`` statements and
``sb.dedent()`` or ``sb.indent()`` at the same time.

Compatibility
=============

SourceBuilder has 100% test coverage and passes all its tests in Python 2.5,
2.6 and 2.7.

Credits
=======

This project was started on Sat Mar 31 2012 by Jaap Roes.

It is in part tnspired by
'`A Python Code Generator <http://effbot.org/zone/python-code-generator.htm>`_'
by Fredrik Lundh, Mar 1998
