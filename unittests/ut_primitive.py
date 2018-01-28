# encoding = utf-8

import unittest
from parser.vlog_primitive import VlogPrimitive
from random import randrange


__author__ = 'mochenx'


class TestVlogPrimitive(unittest.TestCase):
    def setUp(self):
        self.DUT = VlogPrimitive()

    def gen_strength(self):
        pull_ = ['(%s, %s)' % (s0, s1) for s0 in ['supply0', 'strong0', 'pull0', 'weak0']
                   for s1 in ['supply1', 'strong1', 'pull1', 'weak1']]
        pull_.extend(['(%s, %s)' % (s1, s0) for s0 in ['supply0', 'strong0', 'pull0', 'weak0']
                      for s1 in ['supply1', 'strong1', 'pull1', 'weak1']])
        pullup_ = pull_[:]
        pulldown_ = pull_[:]
        pullup_.extend(['(supply1)', '(strong1)', '(pull1)', '(weak1)'])
        pulldown_.extend(['(supply0)', '(strong0)', '(pull0)', '(weak0)'])
        return pullup_, pulldown_

    def gen_drive_strength(self):
        s0s = ['supply0', 'strong0', 'pull0', 'weak0']
        s1s = ['supply1', 'strong1', 'pull1', 'weak1']
        z0 = ['highz0']
        z1 = ['highz1']

        f_get_list_comb = lambda s0, s1: ['(%s, %s)' % (s0, s1) for s0 in ['supply0', 'strong0', 'pull0', 'weak0']
                                          for s1 in ['supply1', 'strong1', 'pull1', 'weak1']]
        strength = f_get_list_comb(s0s, s1s)
        strength.extend(f_get_list_comb(s1s, s0s))
        strength.extend(f_get_list_comb(s0s, z1))
        strength.extend(f_get_list_comb(s1s, z0))
        strength.extend(f_get_list_comb(z0, s1s))
        strength.extend(f_get_list_comb(z1, s0s))

        return strength

    def testNInputsGate(self):
        """
            gate_instantiation ::= n_input_gatetype [drive_strength] [delay2]
                                    n_input_gate_instance { , n_input_gate_instance } ;
            n_input_gate_instance ::= [ name_of_gate_instance ] ( output_terminal , input_terminal
                                        { , input_terminal } )
        """
        n_input_gatetype = ['and', 'nand', 'or', 'nor', 'xor', 'xnor']
        exprs = [['out', '1 + 2 *3 '], ['out', 'id + id * id'], ['out', '1 + id * 3'], ['out', 'id, 100']]
        self.common_test_proc(n_input_gatetype, exprs)

    def testEnGate(self):
        """
            gate_instantiation ::= enable_gatetype [drive_strength] [delay3]
                                    enable_gate_instance { , enable_gate_instance } ;
            enable_gate_instance ::= [ name_of_gate_instance ] ( output_terminal , input_terminal , enable_terminal )
        """
        enable_gatetype = ['bufif0', 'bufif1', 'notif0', 'notif1']
        exprs = [['out', '1 + 2 *3 ', 'en'], ['out', 'id + id * id', 'en'],
                 ['out', '1 + id * 3', 'en'], ['out', 'id', 'en']]
        self.common_test_proc(enable_gatetype, exprs, delays=['# 1', '#(1:1:1)',
                                                              '#(1:1:1, 2:2:2)', '#(1:1:1, 2:2:2, 3:3:3)'])

    def testCMOSGate(self):
        """
            gate_instantiation ::= cmos_switchtype [delay3] cmos_switch_instance { , cmos_switch_instance } ;
            cmos_switch_instance ::= [ name_of_gate_instance ] ( output_terminal , input_terminal ,
                                    ncontrol_terminal , pcontrol_terminal )
        """

        cmos_switchtype = ['cmos', 'rcmos']
        exprs = [['out', '1 + 2 *3 ', 'nctrl', 'pctrl'], ['out', 'id + id * id', 'nctrl', 'pctrl'],
                 ['out', '1 + id * 3', 'nctrl', 'pctrl'], ['out', 'id', 'nctrl', 'pctrl']]
        self.common_test_proc(cmos_switchtype, exprs, strength=[], delays=['# 1', '#(1:1:1)',
                                                                           '#(1:1:1, 2:2:2)', '#(1:1:1, 2:2:2, 3:3:3)'])

    def testMOSGate(self):
        """
            gate_instantiation ::= mos_switchtype [delay3] mos_switch_instance { , mos_switch_instance } ;
            mos_switch_instance ::= [ name_of_gate_instance ] ( output_terminal , input_terminal , enable_terminal )
        """
        mos_switchtype = ['nmos', 'pmos', 'rnmos', 'rpmos']
        exprs = [['out', '1 + 2 *3 ', 'en'], ['out', 'id + id * id', 'en'],
                 ['out', '1 + id * 3', 'en'], ['out', 'id', 'en']]
        self.common_test_proc(mos_switchtype, exprs, strength=[], delays=['# 1', '#(1:1:1)',
                                                                          '#(1:1:1, 2:2:2)', '#(1:1:1, 2:2:2, 3:3:3)'])

    def testNOutput(self):
        """
            gate_instantiation ::= n_output_gatetype [drive_strength] [delay2]
                                    n_output_gate_instance { , n_output_gate_instance } ;
            n_output_gate_instance ::= [ name_of_gate_instance ] ( output_terminal { , output_terminal } ,
                                        input_terminal )
        """
        n_output_gatetype = ['buf', 'not']
        exprs = [['out0', 'out0', '1 + 2 *3 '], ['out0', 'out', 'id + id * id'],
                 ['out0', 'out0', '1 + id * 3'], ['out0', 'out1', 'id']]
        self.common_test_proc(n_output_gatetype, exprs)

    def testPassEn(self):
        """
            gate_instantiation ::= pass_en_switchtype [delay2]
                                    pass_enable_switch_instance { , pass_enable_switch_instance } ;
            pass_enable_switch_instance ::= [ name_of_gate_instance ] ( inout_terminal , inout_terminal ,
                                        enable_terminal )
        """
        pass_en_switchtype = ['tranif0', 'tranif1', 'rtranif1', 'rtranif0']
        exprs = [['out0', 'inout0', 'en'], ['out0', 'inout0', 'en'],
                 ['out0', 'inout0', 'en'], ['out0', 'inout1', 'en']]
        self.common_test_proc(pass_en_switchtype, exprs, strength=[])

    def testPass(self):
        """
            gate_instantiation ::= pass_switchtype pass_switch_instance { , pass_switch_instance } ;
            pass_switch_instance ::= [ name_of_gate_instance ] ( inout_terminal , inout_terminal )
        """
        pass_switchtype = ['tran', 'rtran']
        exprs = [['out0', 'inout0'], ['out0', 'inout0'],
                 ['out0', 'inout0'], ['out0', 'inout1']]
        self.common_test_proc(pass_switchtype, exprs, delays=[''], strength=[])

    def testPullup(self):
        """
            gate_instantiation ::= pullup [pullup_strength] pull_gate_instance { , pull_gate_instance } ;
            pull_gate_instance ::= [ name_of_gate_instance ] ( output_terminal )
        """
        pass_switchtype = ['pullup']
        exprs = [['out0']]
        self.common_test_proc(pass_switchtype, exprs, delays=[''], strength=self.gen_strength()[0])

    def testPulldown(self):
        """
            gate_instantiation ::= pulldown [pulldown_strength] pull_gate_instance { , pull_gate_instance } ;
            pull_gate_instance ::= [ name_of_gate_instance ] ( output_terminal )
        """
        pass_switchtype = ['pulldown']
        exprs = [['out0']]
        self.common_test_proc(pass_switchtype, exprs, delays=[''], strength=self.gen_strength()[1])

    def common_test_proc(self, gate_type, exprs, **kwargs):
        if 'strength' in kwargs:
            strength = kwargs['strength']
        else:
            strength = self.gen_drive_strength()
        strength.append('')
        if 'delays' in kwargs:
            delays = kwargs['delays']
        else:
            delays = ['# 1', '#(1:1:1)', '#(1:1:1, 2:2:2)']
        names = ['', 'a_name']

        cnt = 0
        for t in gate_type:
            for s in strength:
                for d in delays:
                    for n in names:
                        for e in exprs:

                            inst = ['%s (%s)' % (n, ','.join(e)) for _ in range(randrange(3)+1)]
                            tc_codes = '%s %s %s %s;' % (t, s, d, ','.join(inst))
                            tkns = None
                            try:
                                tkns = self.DUT.parse(tc_codes)
                            except Exception as e:
                                print(e)
                                pass
                            self.assertIsNotNone(tkns)
                            try:
                                self.assertEqual(tkns.Name, 'a_name')
                            except AssertionError:
                                try:
                                    self.assertEqual(tkns.Name, '')
                                except Exception as e:
                                    raise(e)
                            self.assertEqual(tkns.Type, t)
                            cnt += 1
            print('%d tests finished' % cnt)

