from __future__ import with_statement
from contextlib import closing
import unittest
from sourcebuilder import SourceBuilder

HELLO_WORLD_FUNC = '''
def hello_world():
    print('Hello World')

'''

HELLO_WORLD_CLASS = '''
class Hello(object):

    def __init__(self, what):
        self.what = what

    def say(self):
        print('Hello {0}'.format(self.what))

'''


class TestSourceBuilder(unittest.TestCase):

    def test_hello_world(self):
        sb = SourceBuilder()
        sb.writeln('print(\'Hello World\')')
        self.assertEquals('print(\'Hello World\')\n', sb.end())

    def test_hello_world_func(self):
        sb = SourceBuilder()
        sb.writeln()
        sb.writeln('def hello_world():')
        with sb.indent:
            sb.writeln('print(\'Hello World\')')
        sb.writeln()
        self.assertEquals(HELLO_WORLD_FUNC, sb.end())

    def test_hello_world_class(self):
        sb = SourceBuilder()
        sb.writeln()
        sb.writeln('class Hello(object):')
        sb.writeln()
        with sb.indent:
            sb.writeln('def __init__(self, what):')
            with sb.indent:
                sb.writeln('self.what = what')
            sb.writeln()
            sb.writeln('def say(self):')
            with sb.indent:
                sb.writeln('print(\'Hello {0}\'.format(self.what))')
        sb.writeln()
        self.assertEquals(HELLO_WORLD_CLASS, sb.end())

    def test_closing_truncates(self):
        CODE = 'print "hello world"'
        out = []
        sb = SourceBuilder()
        for i in range(3):
            with closing(sb):
                sb.writeln(CODE)
                out.append(sb.end())
        self.assertEqual([CODE + '\n'] * 3, out)
