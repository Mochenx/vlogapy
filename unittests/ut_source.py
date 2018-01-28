#encoding = utf-8

import unittest
from parser import *
from pyparsing import ParserElement


__author__ = 'mochen'


class TestVlogSource(unittest.TestCase):
    def setUp(self):
        self.DUT = VlogSource()
        ParserElement.verbose_stacktrace = True

    def test_tc1(self):
        exp_tkns =[  # source
            [  # module
                ['_test_source', ['in0', 'clkout', 'ckin0', 'ckin1', 'pw', 'out0', 'out1']],  # module header
                [['output', 'out0'], ['input', 'in0'], ['output', 'out1']]  # module items
            ]
        ]
        with open('unittests/vlog_files/source_tc1.v', 'r') as f:
            codes = f.read()
        parsed_tokens = self.DUT.source.parseString(codes)
        # self.assertEqual(str(parsed_tokens), str(exp_tkns))
        self.assertEqual(len(parsed_tokens), 1)
        module = parsed_tokens[0]
        self.assertEqual(module['ModuleHeader'].name, '_test_source')

    def test_tc2(self):
        with open('unittests/vlog_files/source_tc2.v', 'r') as f:
            codes = f.read()
        parsed_tokens = self.DUT.source.parseString(codes)
        self.assertGreater(len(parsed_tokens), 0)
        print(parsed_tokens)
