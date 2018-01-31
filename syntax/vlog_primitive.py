# encoding = utf-8

from .vlog_general import *
from .vlog_base import *
from .vlog_expr import VlogExpr
from .vlog_stmt import VlogStmt
from .vlog_declaration import VlogDeclaration
from pyparsing import (Group, Keyword, oneOf, Optional, delimitedList, OneOrMore)


__author__ = 'mochenx'


class VlogPrimitive(VlogBase):
    def __repr__(self):
        return 'VlogPrimitive'

    # @syntax_tree('VlogPrimitive', priority=, with_name='')
    # @syntax_root('VlogPrimitive')

    @syntax_tree('VlogPrimitive', priority=100)
    def _before_everything(self):
        self.expr = VlogExpr()
        self.stmt = VlogStmt()
        self.decl = VlogDeclaration(statement=self.stmt)

    @syntax_tree('VlogPrimitive', priority=10)
    def _gate_n_switch(self):
        """
            cmos_switchtype ::= cmos | rcmos
            enable_gatetype ::= bufif0 | bufif1 | notif0 | notif1
            mos_switchtype ::= nmos | pmos | rnmos | rpmos
            n_input_gatetype ::= and | nand | or | nor | xor | xnor
            n_output_gatetype ::= buf | not
            pass_en_switchtype ::= tranif0 | tranif1 | rtranif1 | rtranif0
            pass_switchtype ::= tran | rtran
        """
        self.cmos_switchtype = (Keyword('cmos') | Keyword('rcmos'))
        self.enable_gatetype = (Keyword('bufif0') | Keyword('bufif1') | Keyword('notif0') | Keyword('notif1'))
        self.mos_switchtype = (Keyword('nmos') | Keyword('pmos') | Keyword('rnmos') | Keyword('rpmos'))
        self.n_input_gatetype = (Keyword('and') | Keyword('nand') | Keyword('or')
                                 | Keyword('nor') | Keyword('xor') | Keyword('xnor'))
        self.n_output_gatetype = (Keyword('buf') | Keyword('not'))
        self.pass_en_switchtype = (Keyword('tranif0') | Keyword('tranif1') | Keyword('rtranif1') | Keyword('rtranif0'))
        self.pass_switchtype = (Keyword('tran') | Keyword('rtran'))

    @syntax_root('VlogPrimitive')
    def _gate_inst(self):
        """
            gate_instantiation ::= cmos_switchtype [delay3] cmos_switch_instance { , cmos_switch_instance } ;
                                | enable_gatetype [drive_strength] [delay3]
                                    enable_gate_instance { , enable_gate_instance } ;
                                | mos_switchtype [delay3]
                                    mos_switch_instance { , mos_switch_instance } ;
                                | n_input_gatetype [drive_strength] [delay2]
                                    n_input_gate_instance { , n_input_gate_instance } ;
                                | n_output_gatetype [drive_strength] [delay2]
                                    n_output_gate_instance { , n_output_gate_instance } ;
                                | pass_en_switchtype [delay2]
                                    pass_enable_switch_instance { , pass_enable_switch_instance } ;
                                | pass_switchtype pass_switch_instance { , pass_switch_instance } ;
                                | pulldown [pulldown_strength]
                                    pull_gate_instance { , pull_gate_instance } ;
                                | pullup [pullup_strength] pull_gate_instance { , pull_gate_instance } ;
            cmos_switch_instance ::= [ name_of_gate_instance ] ( output_terminal , input_terminal ,
                                    ncontrol_terminal , pcontrol_terminal )
            enable_gate_instance ::= [ name_of_gate_instance ] ( output_terminal , input_terminal , enable_terminal )
            mos_switch_instance ::= [ name_of_gate_instance ] ( output_terminal , input_terminal , enable_terminal )
            n_input_gate_instance ::= [ name_of_gate_instance ] ( output_terminal , input_terminal
                                        { , input_terminal } )
            n_output_gate_instance ::= [ name_of_gate_instance ] ( output_terminal { , output_terminal } ,
                                        input_terminal )
            pass_switch_instance ::= [ name_of_gate_instance ] ( inout_terminal , inout_terminal )
            pass_enable_switch_instance ::= [ name_of_gate_instance ] ( inout_terminal , inout_terminal ,
                                        enable_terminal )
            pull_gate_instance ::= [ name_of_gate_instance ] ( output_terminal )
            name_of_gate_instance ::= gate_instance_identifier [ range ]
        """
        ##############################
        # Duplicated codes from VlogDeclaration
        _range = Group(LBRACKET + self.expr.constant_expression + ':' + self.expr.constant_expression + RBRACKET)
        ##############################
        name_of_gate_inst = identifier('Name') + Optional(_range)
        pull_gate_inst = Optional(name_of_gate_inst) + LPARENTH + self.output_term + RPARENTH
        pass_enable_switch_inst = Optional(name_of_gate_inst)('InstName') + (LPARENTH + self.inout_term + COMMA +
                                                                 self.inout_term + COMMA +
                                                                 self.enable_term + RPARENTH)
        pass_switch_inst = Optional(name_of_gate_inst)('InstName') + Group(LPARENTH + self.inout_term + COMMA +
                                                                           self.inout_term + RPARENTH)('Ports')
        # In n_output_gate_inst, delimitedList(self.output_term) + COMMA  => OneOrMore(self.output_term + COMMA)
        n_output_gate_inst = Optional(name_of_gate_inst)('InstName') + Group(LPARENTH +
                                                                             OneOrMore(self.output_term + COMMA) +
                                                                             self.input_term + RPARENTH)('Ports')
        n_input_gate_inst = Optional(name_of_gate_inst)('InstName') + Group(LPARENTH + self.output_term + COMMA +
                                                                            delimitedList(self.input_term) +
                                                                            RPARENTH)('Ports')
        enable_gate_inst = Optional(name_of_gate_inst)('InstName') + Group(LPARENTH + self.output_term + COMMA +
                                                                           self.input_term + COMMA +
                                                                           self.enable_term + RPARENTH)('Ports')
        mos_switch_inst = Optional(name_of_gate_inst)('InstName') + Group(LPARENTH + self.output_term + COMMA +
                                                                          self.input_term + COMMA +
                                                                          self.enable_term + RPARENTH)('Ports')
        cmos_switch_inst = Optional(name_of_gate_inst)('InstName') + Group(LPARENTH + self.output_term + COMMA +
                                                                           self.input_term + COMMA +
                                                                           self.ncontrol_term + COMMA +
                                                                           self.pcontrol_term + RPARENTH)('Ports')
        gate_inst = ((self.cmos_switchtype('Type') + Optional(self.decl.delay3)('delay') +
                      delimitedList(cmos_switch_inst)('Instances') + SEMI)
                     | (self.enable_gatetype('Type') + Optional(self.decl.drive_strength)('strength') +
                        Optional(self.decl.delay3)('delay') + delimitedList(enable_gate_inst)('Instances') + SEMI)
                     | (self.mos_switchtype('Type') + Optional(self.decl.delay3)('delay') +
                        delimitedList(mos_switch_inst)('Instances') + SEMI)
                     | (self.n_input_gatetype('Type') + Optional(self.decl.drive_strength)('strength') +
                        Optional(self.decl.delay2)('delay') + delimitedList(n_input_gate_inst)('Instances') + SEMI)
                     | (self.n_output_gatetype('Type') + Optional(self.decl.drive_strength)('strength') +
                        Optional(self.decl.delay2)('delay') + delimitedList(n_output_gate_inst)('Instances') + SEMI)
                     | (self.pass_en_switchtype('Type') + Optional(self.decl.delay2)('delay') +
                        delimitedList(pass_enable_switch_inst)('Instances') + SEMI)
                     | (self.pass_switchtype('Type') + delimitedList(pass_switch_inst)('Instances') + SEMI)
                     | ((Keyword('pulldown')('Type') + self.pulldown_strength('strength') +
                         delimitedList(pull_gate_inst)('Instances') + SEMI) |
                        (Keyword('pulldown')('Type') + delimitedList(pull_gate_inst)('Instances') + SEMI))
                     | ((Keyword('pullup')('Type') + self.pullup_strength('strength') +
                         delimitedList(pull_gate_inst)('Instances') + SEMI) |
                        (Keyword('pullup')('Type') + delimitedList(pull_gate_inst)('Instances') + SEMI)))

        return gate_inst

    @syntax_tree('VlogPrimitive', priority=9)
    def _prim_strength(self):
        """
            pulldown_strength ::= ( strength0 , strength1 )
                            | ( strength1 , strength0 )
                            | ( strength0 )
            pullup_strength ::= ( strength0 , strength1 )
                            | ( strength1 , strength0 )
                            | ( strength1 )
        """

        # The following two lines are repeated in VlogDecl._strength_decl
        strength0 = oneOf('supply0 strong0 pull0 weak0')
        strength1 = oneOf('supply1 strong1 pull1 weak1')
        self.pulldown_strength = Group(LPARENTH + ((strength0 + ',' + strength1)
                                                   | (strength1 + ',' + strength0)
                                                   | strength0) + RPARENTH)

        self.pullup_strength = Group(LPARENTH + ((strength0 + ',' + strength1)
                                                 | (strength1 + ',' + strength0)
                                                 | strength1) + RPARENTH)

    @syntax_tree('VlogPrimitive', priority=8)
    def _prim_terms(self):
        """
            enable_terminal ::= expression
            inout_terminal ::= net_lvalue
            input_terminal ::= expression
            ncontrol_terminal ::= expression
            output_terminal ::= net_lvalue
            pcontrol_terminal ::= expression
        """
        self.enable_term = self.expr.expression
        self.inout_term = self.expr.net_lvalue
        self.input_term = self.expr.expression
        self.ncontrol_term = self.expr.expression
        self.output_term = self.expr.net_lvalue
        self.pcontrol_term = self.expr.expression
