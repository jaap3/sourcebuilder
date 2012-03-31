=============
SourceBuilder
=============

SourceBuilder is a simple way to write (python) code using python code.

Examples
========

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


As you might have noticed, context managers are used to keep track of the
indentation level. If for some reason your use case doesn't allow for ``with``
statements you can use the following alternative syntax::

  >>> sb = SourceBuilder()
  >>> klasses = ['Foo', 'Bar']
  >>> for klass in klasses:
  ...     sb.writeln()
  ...     sb.writeln('class {0}(object)'.format(klass))
  ...     sb.indent()
  ...     sb.writeln('def __init__(self):')
  ...     sb.indent()
  ...     sb.writeln('pass')
  ...     sb.dedent()
  ...     sb.dedent()
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


Compatibility
=============

SourceBuilder has 100% test coverage and passes all its tests in Python 2.5,
2.6 and 2.7.
