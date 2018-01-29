#encoding = utf-8

import unittest
from syntax.vlog_expr import VlogExpr


__author__ = 'mochen'


class TestVlogExpr(unittest.TestCase):
    def setUp(self):
        self.DUT = VlogExpr()

    def get_eq(self, i, v):
        def _chk(e):
            self.assertEqual(e[i], v)
            return True
        return _chk

    def get_nest_eq(self, v, *args):
        def _chk(e):
            nxt_layer = e
            for i in args:
                nxt_layer = nxt_layer[i]
            try:
                self.assertEqual(nxt_layer, v)
            except Exception:
                raise
            return True
        return _chk

    def testSimpleExpr(self):
        parsed_tkns = self.DUT.parse('1-2+3*4/5')
        print(parsed_tkns)
        parsed_tkns = self.DUT.parse('(2*2)+((1+2)*5)>>3')
        print(parsed_tkns)

    def testExprPrimary(self):
        """
            A testcase of primary defined in expression
            number : 1, 20, 12'h1_FA
            parentheses : ( a + b * c / 5)
            concatenation {4'h3, var, 8'hF_F}
            multiple concatenation {4{4'h3, var}}
            hier_id : a
                      var[7:0]
                      var[b+1][3*2][s +: 4]
        """
        stimus = [
            ('1', None),
            ('20', None),
            ("12'h1_FA", None),
            ('( a+b *c/  5)', None),
            ("{4'h3, var, 8'hF_F}", None),
            ("{4{4'h3, var}}", None),
            ('a', None),
            ('var[7:0]', None),
            ('var[26]', None),
            ('var[a+1][3*2][s +: 4]', None),
        ]

        for tc_codes, chk_f in stimus:
            print('Testing : %s' % tc_codes)
            parsed_tkns = self.DUT.primary.parseString(tc_codes)
            print(parsed_tkns)
            if chk_f:
                chk_f(parsed_tkns[0])

    def testExprFuncCall(self):
        chk_fun_name = lambda t: self.get_eq(t, 'func_call')
        chk_sysfun_name = lambda t: self.get_eq(t, '$display')
        chk_mod_name = lambda e: self.get_eq(0, e)
        stimus = [
            ('func_call()', lambda t: chk_fun_name(0)(t)),
            ('module1.func_call()', lambda t: chk_mod_name('module1')(t) and chk_fun_name(1)(t)),
            ('module1.module2.func_call()', lambda t: chk_mod_name('module1')(t) and chk_fun_name(2)(t)),
            ('func_call(a, b, c)', lambda t: chk_fun_name(0)(t) and self.get_nest_eq('c', 3)(t)),
            ('func_call(1, 2, 3+4)', lambda t: chk_fun_name(0)(t) and self.get_nest_eq('4', 5)(t)),
            ('module1.func_call(a, b, c)', lambda t: chk_mod_name('module1')(t) and
                                                     chk_fun_name(1)(t) and self.get_nest_eq('c', 4)(t)),
            ('module1.module2.func_call(a, b, c)', lambda t: chk_mod_name('module1')(t) and
                                                             chk_fun_name(2)(t) and self.get_nest_eq('c', 5)(t)),
            ('func_call(a, b, c)', lambda t: chk_fun_name(0)(t) and self.get_nest_eq('c', 3)(t)),
            ('$display', lambda t: chk_sysfun_name(0)(t)),
            ('$display()', lambda t: chk_sysfun_name(0)(t)),
            ('$display(a, b, c)', lambda t: chk_sysfun_name(0)(t) and self.get_nest_eq('c', 3)(t)),
            ('$display(a, b, c+d)', lambda t: chk_sysfun_name(0)(t) and self.get_nest_eq('d', 5)(t)),
            ('$display(1, 2, 3+4)', lambda t: chk_sysfun_name(0)(t) and self.get_nest_eq('4', 5)(t)),
        ]
        for tc_codes, chk_f in stimus:
            print('Testing : %s' % tc_codes)
            parsed_tkns = self.DUT.primary.parseString(tc_codes)
            print(parsed_tkns)
            if chk_f:
                chk_f(parsed_tkns)
