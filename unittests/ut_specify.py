#encoding = utf-8

import unittest
from parser.vlog_specify import VlogSpecify


__author__ = 'mochen'


class TestVlogStmt(unittest.TestCase):
    def setUp(self):
        self.DUT = VlogSpecify()

    def testConsumeSpecify(self):
        codes ='specify specparam CDS_LIBNAME  = "eu_usi_tx"; specparam CDS_CELLNAME = "usi_tx_phy_timingmodel"; specparam CDS_VIEWNAME = "schematic"; endspecify'

        parsed_tkns = self.DUT.parse(codes)
        print(parsed_tkns)
