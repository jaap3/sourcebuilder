import unittest
from sourcebuilder.sourcebuilder import IndentManager, DedentException


class TestIndentManager(unittest.TestCase):

    def test_identation_level_starts_at_zero(self):
        im = IndentManager()
        self.assertEqual(im.level, 0)

    def test_calling_instance_increases_indentation_level(self):
        im = IndentManager()
        im()
        self.assertEquals(1, im.level)

    def test_indent_increased_indentation_level(self):
        im = IndentManager()
        im.indent()
        self.assertEquals(1, im.level)

    def test_indent_then_dedent_decreased_indentation_level(self):
        im = IndentManager()
        im.indent()
        im.dedent()
        self.assertEquals(0, im.level)

    def test_dedent_raises_exception_if_indentation_level_is_zero(self):
        im = IndentManager()
        self.assertRaises(DedentException, im.dedent)

    def test_indent_with_tab_str(self):
        im = IndentManager(indent_with='\t')
        im.indent()
        self.assertEqual('\t', str(im))
        im.indent()
        self.assertEqual('\t\t', str(im))

    def test_reset(self):
        im = IndentManager()
        im.indent()
        im.reset()
        self.assertEquals(0, im.level)

