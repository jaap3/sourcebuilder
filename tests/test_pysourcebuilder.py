from __future__ import with_statement
import unittest
from sourcebuilder import PySourceBuilder

HELLO_WORLD_FUNC = '''
def hello_world():
    """prints Hello World"""
    print('Hello World')

'''

HELLO_WORLD_CLASS = '''

class Hello(object):

    def __init__(self, what='World'):
        """
        Initialize Hello. The ``what`` parameter controls the output of
        ``say`` and is 'World' by default.

        """
        self.what = what

    def say(self):
        """prints 'Hello ' + the value of ``self.what``."""
        print('Hello {0}'.format(self.what))

'''

MULTILINE_DOCSTRING = '''"""
Lorem ipsum dolor sit amet, consectetur adipiscing elit.

  Duis tincidunt
  Dui non adipiscing faucibus

Odio diam fermentum enim, ut facilisis quam dolor nec metus.

"""
'''

INDENTED_DOCSTRING = '''            """
            Lorem ipsum dolor sit amet, consectetur adipiscing elit.
            Phasellus accumsan molestie lectus, sed ornare dui volutpat
            fermentum.

                Duis tincidunt
                    Dui non adipiscing faucibus
                        Consectetur adipiscing elit

            Odio diam fermentum enim, ut facilisis quam dolor nec metus.
            Integer ac velit nisl. Etiam eu nisl orci. Lorem ipsum dolor
            sit amet.

            """
'''


class TestPySourceBuilder(unittest.TestCase):

    def test_hello_world_func(self):
        sb = PySourceBuilder()
        with sb.block('def hello_world():', 1):
            sb.docstring('prints Hello World')
            sb.writeln('print(\'Hello World\')')
        sb.writeln()
        self.assertEquals(HELLO_WORLD_FUNC, sb.end())

    def test_hello_world_class(self):
        sb = PySourceBuilder()
        with sb.block('class Hello(object):', 2):
            with sb.block('def __init__(self, what=\'World\'):', 1):
                sb.docstring('Initialize Hello. The ``what`` parameter ' +
                             'controls the output of ``say`` and is ' +
                             '\'World\' by default.')
                sb.writeln('self.what = what')
            with sb.block('def say(self):', 1):
                sb.docstring("prints 'Hello ' + the value of ``self.what``.")
                sb.writeln('print(\'Hello {0}\'.format(self.what))')
        sb.writeln()
        self.assertEquals(HELLO_WORLD_CLASS, sb.end())

    def test_multiline_docstring(self):
        sb = PySourceBuilder()
        sb.docstring('''
        Lorem ipsum dolor sit amet, consectetur adipiscing elit.

          Duis tincidunt
          Dui non adipiscing faucibus

        Odio diam fermentum enim, ut facilisis quam dolor nec metus.''')
        self.assertEquals(MULTILINE_DOCSTRING, sb.end())



    def test_indented_multiline_docstring(self):
        sb = PySourceBuilder()
        sb.indent()
        sb.indent()
        sb.indent()
        sb.docstring('''
        Lorem ipsum dolor sit amet, consectetur adipiscing elit.
        Phasellus accumsan molestie lectus, sed ornare dui volutpat fermentum.

            Duis tincidunt
                Dui non adipiscing faucibus
                    Consectetur adipiscing elit

        Odio diam fermentum enim, ut facilisis quam dolor nec metus.
        Integer ac velit nisl. Etiam eu nisl orci. Lorem ipsum dolor sit amet.
        ''')
        self.assertEquals(INDENTED_DOCSTRING, sb.end())
