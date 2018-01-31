#encoding = utf-8

from .vlog_general import *
from .vlog_base import *
from .vlog_expr import VlogExpr

try:
    from pyparsing import (Group, ZeroOrMore, Optional, delimitedList, Keyword, oneOf, )
except ImportError:
    from vlogapy.pyparsing import (Group, ZeroOrMore, Optional, delimitedList, Keyword, oneOf, )


__author__ = 'mochen'


class VlogDeclaration(VlogBase):
    def __init__(self, **kwargs):
        if 'statement' not in kwargs:
            raise ValueError('VlogDeclaration need a VlogStmt to initialize itself')
        self.stmt = kwargs['statement']
        super(VlogDeclaration, self).__init__()

    def __repr__(self):
        return 'VlogDeclaration'

    @syntax_tree('VlogDeclaration', priority=100)
    def _before_all(self):

        self.signed_kw = Keyword('signed')
        self.expr = VlogExpr()

    @syntax_tree('VlogDeclaration', priority=22)
    def _event_real_decl(self):
        """
            list_of_event_identifiers ::= event_identifier { dimension } { , event_identifier { dimension } }
            event_declaration ::= event list_of_event_identifiers ;

            real_type ::= real_identifier { dimension } | real_identifier = constant_expression
            list_of_real_identifiers ::= real_type { , real_type }
            real_declaration ::= real list_of_real_identifiers ;
            realtime_declaration ::= realtime list_of_real_identifiers ;
        """
        # TODO: test the following all
        l_event_ids = delimitedList(identifier + Optional(self.expr.constant_expression))
        l_real_ids = ((identifier + Optional(self.expr.constant_expression))
                      | (identifier + '=' + self.expr.constant_expression))
        self.event_decl = Keyword('event') + l_event_ids
        self.real_decl = Keyword('real') + l_real_ids
        self.realtime_decl = Keyword('realtime') + l_real_ids

    @syntax_tree('VlogDeclaration', priority=90, with_name='the_range')
    def _build_range(self):
        """
            range ::= [ msb_constant_expression : lsb_constant_expression ]
        """
        # It uses ':' as separator to make user utilize MSB & LSB easily
        # TODO: It only supports [number: number] pattern currently
        _range = Group(LBRACKET + self.expr.constant_expression + ':' + self.expr.constant_expression +
                       RBRACKET).setParseAction(lambda t: (t[0][0], t[0][2]))
        return _range

    @syntax_tree('VlogDeclaration', priority=89)
    def _prep_decl_list(self):
        """
            dimension_constant_expression ::= constant_expression
            dimension ::= [ dimension_constant_expression : dimension_constant_expression ]
            variable_identifier ::= identifier
            variable_type ::= variable_identifier { dimension }
                             | variable_identifier = constant_expression
            list_of_variable_identifiers ::= variable_type { , variable_type }

            net_identifier ::= identifier
            list_of_net_identifiers ::= net_identifier { dimension } { , net_identifier { dimension } }
            net_decl_assignment ::= net_identifier = expression
            list_of_net_decl_assignments ::= net_decl_assignment { , net_decl_assignment }
        Not Implemented Yet:
            real_type ::= real_identifier { dimension }
                         | real_identifier = constant_expression
        """
        dimension = self.the_range

        var_type = ((identifier + '=' + self.expr.constant_expression)
                    | (identifier + ZeroOrMore(dimension)))
        net_decl_assign = Group(identifier + '=' + self.expr.expression)

        self.l_var_ids = Group(delimitedList(var_type))
        self.l_net_idx = Group(delimitedList(identifier + ZeroOrMore(dimension)))
        self.l_net_decl_assign = delimitedList(net_decl_assign)

    @syntax_tree('VlogDeclaration', priority=88, with_name='drive_strength')
    def _strength_decl(self):
        """
            drive_strength ::= ( strength0 , strength1 )
                              | ( strength1 , strength0 )
                              | ( strength0 , highz1 )
                              | ( strength1 , highz0 )
                              | ( highz0 , strength1 )
                              | ( highz1 , strength0 )
            strength0 ::= supply0 | strong0 | pull0 | weak0
            strength1 ::= supply1 | strong1 | pull1 | weak1
            charge_strength ::= ( small ) | ( medium ) | ( large )
        """
        strength0 = Keyword('supply0') | Keyword('strong0') | Keyword('pull0') | Keyword('weak0')
        strength1 = Keyword('supply1') | Keyword('strong1') | Keyword('pull1') | Keyword('weak1')
        highz0 = Keyword('highz0')
        highz1 = Keyword('highz1')

        small_kw = Keyword('small')
        medium_kw = Keyword('medium')
        large_kw = Keyword('large')

        self.charge_strength = Group(LPARENTH + (small_kw | medium_kw | large_kw) + RPARENTH)

        drive_strength = Group(LPARENTH + ((strength0 + ',' + strength1)
                                           | (strength1 + ',' + strength0)
                                           | (strength0 + ',' + highz1)
                                           | (strength1 + ',' + highz0)
                                           | (highz0 + ',' + strength1)
                                           | (highz1 + ',' + strength0)) + RPARENTH)
        return drive_strength

    @syntax_tree('VlogDeclaration', priority=25, with_name='block_item_declaration')
    def _reg_int_time_decl(self):
        """
            reg_declaration ::= reg [ signed ] [ range ] list_of_variable_identifiers ;
            time_declaration ::= time list_of_variable_identifiers ;
            integer_declaration ::= integer list_of_variable_identifiers ;

            block_item_declaration ::= { attribute_instance } reg [ signed ] [ range ] list_of_block_variable_identifiers ;
                                    | { attribute_instance } integer list_of_block_variable_identifiers ;
                                    | { attribute_instance } time list_of_block_variable_identifiers ;
                                    | { attribute_instance } real list_of_block_real_identifiers ;
                                    | { attribute_instance } realtime list_of_block_real_identifiers ;
                                    | { attribute_instance } event_declaration
                                    | { attribute_instance } local_parameter_declaration ;
                                    | { attribute_instance } parameter_declaration ;
        Not Implemented Yet:
            { attribute_instance } event_declaration
            { attribute_instance } real list_of_block_real_identifiers ;
            { attribute_instance } realtime list_of_block_real_identifiers ;
        """
        self.reg_kw = Keyword('reg')

        self.reg_declaration = Group(self.reg_kw + Optional(self.signed_kw) + Optional(self.the_range) +
                                     self.l_var_ids + SEMI)
        self.time_declaration = Group(self.time_kw + self.l_var_ids + SEMI)
        self.integer_declaration = Group(self.integer_kw + self.l_var_ids + SEMI)
        # TODO: I used reg_declaration in block_item_declaration instead of list_of_block_variable_identifiers
        # list_of_block_variable_idenifers is a subset of list_of_variable_identifiers
        _blk_item_decl = (self.reg_declaration
                          | self.time_declaration
                          | self.integer_declaration
                          | (self.local_param_decl + SEMI)
                          | (self.parameter_declaration + SEMI))
        return _blk_item_decl

    @syntax_tree('VlogDeclaration', priority=21, with_name='net_declaration')
    def _net_decl(self):
        """
            delay3 ::= # delay_value
                      | # ( mintypmax_expression [ , mintypmax_expression [ , mintypmax_expression ] ] )
            delay2 ::= # delay_value
                      | # ( mintypmax_expression [ , mintypmax_expression ] )
            delay_value ::= unsigned_number
                           | real_number
                           | identifier
            net_declaration ::= net_type [ signed ] [ delay3 ] list_of_net_identifiers ;
                                | net_type [ drive_strength ] [ signed ]
                                    [ delay3 ] list_of_net_decl_assignments ;
                                | net_type [ vectored | scalared ] [ signed ]
                                    range [ delay3 ] list_of_net_identifiers ;
                                | net_type [ drive_strength ] [ vectored | scalared ] [ signed ]
                                    range [ delay3 ] list_of_net_decl_assignments ;
                                | trireg [ charge_strength ] [ signed ]
                                    [ delay3 ] list_of_net_identifiers ;
                                | trireg [ drive_strength ] [ signed ]
                                    [ delay3 ] list_of_net_decl_assignments ;
                                | trireg [ charge_strength ] [ vectored | scalared ] [ signed ]
                                    range [ delay3 ] list_of_net_identifiers ;
                                | trireg [ drive_strength ] [ vectored | scalared ] [ signed ]
                                    range [ delay3 ] list_of_net_decl_assignments ;
        Not Implemented Yet:
            [ charge_strength ]: Defined in this class but not being used here
            delay_value ::= real_number
        """
        # TODO: delay_val should use unsigned_number instead of number
        delay_val = number | identifier
        self.delay3 = Group(SHARP + ((LPARENTH + self.expr.mintypmax_expression +
                                      Optional(COMMA + self.expr.mintypmax_expression +
                                               Optional(COMMA + self.expr.mintypmax_expression)) + RPARENTH)
                                     | delay_val))
        self.delay2 = Group(SHARP + ((LPARENTH + self.expr.mintypmax_expression +
                                      Optional(COMMA + self.expr.mintypmax_expression) + RPARENTH)
                                     | delay_val))
        vectored_kw = Keyword('vectored')
        scalared_kw = Keyword('scalared')

        # TODO: Review the folloing defines, and trireg with drive_strength has not been tested
        # net_type [ signed ] [ delay3 ] list_of_net_identifiers ;
        net_decl_0 = Group(net_type + Optional(self.signed_kw) + Optional(self.delay3) + self.l_net_idx)
        # trireg [ charge_strength ] [ signed ] [ delay3 ] list_of_net_identifiers ;
        trireg_decl_0 = Group(trireg + Optional(self.charge_strength) + Optional(self.signed_kw) +
                              Optional(self.delay3) + self.l_net_idx)

        # net_type [ drive_strength ] [ signed ] [ delay3 ] list_of_net_decl_assignments ;
        net_decl_1 = Group(net_type + Optional(self.drive_strength) + Optional(self.signed_kw) +
                           Optional(self.delay3) + self.l_net_decl_assign)
        # trireg [ drive_strength ] [ signed ] [ delay3 ] list_of_net_decl_assignments ;
        trireg_decl_1 = Group(trireg + Optional(self.drive_strength) +
                              Optional(self.signed_kw) + Optional(self.delay3) + self.l_net_decl_assign)

        # net_type [ vectored | scalared ] [ signed ] range [ delay3 ] list_of_net_identifiers ;
        net_decl_2 = Group(net_type + Optional(vectored_kw | scalared_kw) + Optional(self.signed_kw) +
                           self.the_range + Optional(self.delay3) + self.l_net_idx)
        # trireg [ charge_strength ] [ vectored | scalared ] [ signed ] range [ delay3 ] list_of_net_identifiers ;
        trireg_decl_2 = Group(trireg + Optional(self.charge_strength) + Optional(vectored_kw | scalared_kw) +
                              Optional(self.signed_kw) + self.the_range + Optional(self.delay3) + self.l_net_idx)

        # net_type [ drive_strength ] [ vectored | scalared ] [ signed ] range [ delay3 ] list_of_net_decl_assignments ;
        net_decl_3 = Group(net_type + Optional(self.drive_strength) + Optional(vectored_kw | scalared_kw) +
                           Optional(self.signed_kw) + self.the_range + Optional(self.delay3) + self.l_net_decl_assign)
        # trireg [ drive_strength ] [ vectored | scalared ] [ signed ] range [ delay3 ] list_of_net_decl_assignments ;
        trireg_decl_3 = Group(trireg + Optional(self.drive_strength) +
                              Optional(vectored_kw | scalared_kw) + Optional(self.signed_kw) +
                              self.the_range + Optional(self.delay3) + self.l_net_decl_assign)

        net_decl = (trireg_decl_3 | trireg_decl_2 | trireg_decl_1 | trireg_decl_0
                    | net_decl_3 | net_decl_2 | net_decl_1 | net_decl_0) + SEMI
        return net_decl

    @syntax_tree('VlogDeclaration', priority=23, with_name='function_declaration')
    def func_decl(self):
        """
            function_declaration ::= function [ automatic ] [ function_range_or_type ] function_identifier ;
                                        function_item_declaration { function_item_declaration }
                                        function_statement
                                        endfunction
                                    | function [ automatic ] [ function_range_or_type ] function_identifier
                                    ( function_port_list ) ;
                                        { block_item_declaration }
                                        function_statement
                                        endfunction
            function_item_declaration ::= block_item_declaration
                                    | { attribute_instance } tf_input_declaration ;
            function_port_list ::= { attribute_instance } tf_input_declaration { , { attribute_instance }
                                    tf_input_declaration }
            function_range_or_type ::= [ signed ] [ range ] | integer | real | realtime | time
        """

        func_kw = Keyword('function')
        end_func_kw = Keyword('endfunction')
        func_range_or_type = (self.integer_kw
                              | self.real_kw
                              | self.realtime_kw
                              | self.time_kw
                              | (Optional(self.signed_kw) + Optional(self.the_range)))


        function_item_declaration = self.block_item_declaration | (self.tf_input_decl + SEMI)
        function_port_list = delimitedList(self.tf_input_decl)
        _function_declaration = ((func_kw + Optional(self.auto_kw) + Optional(func_range_or_type) + identifier('FuncName')
                                  + SEMI + ZeroOrMore(function_item_declaration) + ~end_func_kw + self.stmt.statement +
                                  end_func_kw)
                                 | (func_kw + Optional(self.auto_kw) + Optional(func_range_or_type) +
                                    identifier('FuncName') + LPARENTH + function_port_list + RPARENTH + SEMI +
                                    ZeroOrMore(self.block_item_declaration) + ~end_func_kw + self.stmt.statement +
                                    end_func_kw))

        return _function_declaration

    @syntax_tree('VlogDeclaration', priority=24, with_name='task_declaration')
    def _task_decl(self):
        """
            task_declaration ::= task [ automatic ] task_identifier ;
                                    { task_item_declaration }
                                    statement_or_null
                                    endtask
                                | task [ automatic ] task_identifier ( [ task_port_list ] ) ;
                                    { block_item_declaration }
                                    statement_or_null
                                    endtask
            task_item_declaration ::= block_item_declaration
                                | { attribute_instance } tf_input_declaration ;
                                | { attribute_instance } tf_output_declaration ;
                                | { attribute_instance } tf_inout_declaration ;
            task_port_list ::= task_port_item { , task_port_item }
            task_port_item ::= { attribute_instance } tf_input_declaration
                            | { attribute_instance } tf_output_declaration
                            | { attribute_instance } tf_inout_declaration
            tf_input_declaration ::= input [ reg ] [ signed ] [ range ] list_of_port_identifiers
                            | input task_port_type list_of_port_identifiers
            tf_output_declaration ::= output [ reg ] [ signed ] [ range ] list_of_port_identifiers
                            | output task_port_type list_of_port_identifiers
            tf_inout_declaration ::= inout [ reg ] [ signed ] [ range ] list_of_port_identifiers
                            | inout task_port_type list_of_port_identifiers
            task_port_type ::= integer | real | realtime | time
        """
        self.auto_kw = Keyword('automatic')
        task_kw = Keyword('task')
        endtask_kw = Keyword('endtask')

        input_kw = Keyword('input')
        output_kw = Keyword('output')
        inout_kw = Keyword('inout')
        task_port_type = self.integer_kw | self.real_kw | self.realtime_kw | self.time_kw

        self.tf_input_decl = ((input_kw + Optional(self.reg_kw) + Optional(self.signed_kw) + Optional(self.the_range) +
                               delimitedList(~Keyword('input') + identifier))
                              | (input_kw + task_port_type + delimitedList(identifier)))

        self.tf_output_decl = ((output_kw + Optional(self.reg_kw) + Optional(self.signed_kw) + Optional(self.the_range) +
                                delimitedList(~Keyword('input') + identifier))
                               | (output_kw + task_port_type + delimitedList(identifier)))

        self.tf_inout_decl = ((inout_kw + Optional(self.reg_kw) + Optional(self.signed_kw) + Optional(self.the_range) +
                               delimitedList(~Keyword('input') + identifier))
                              | (inout_kw + task_port_type + delimitedList(identifier)))

        _task_port_item = self.tf_input_decl | self.tf_output_decl | self.tf_inout_decl
        task_port_list = delimitedList(_task_port_item)

        task_item_decl = (self.block_item_declaration
                          | (self.tf_input_decl + SEMI)
                          | (self.tf_output_decl + SEMI)
                          | (self.tf_inout_decl + SEMI))

        task_decl = ((task_kw + Optional(self.auto_kw) + identifier + SEMI +
                      ZeroOrMore(task_item_decl) +
                      self.stmt.statement_or_null + endtask_kw)
                     | (task_kw + Optional(self.auto_kw) + identifier + LPARENTH + Optional(task_port_list) +
                        RPARENTH + SEMI +
                        ZeroOrMore(self.block_item_declaration) +
                        self.stmt.statement_or_null + endtask_kw))

        return task_decl

    @syntax_tree('VlogDeclaration', priority=26, with_name='parameter_declaration')
    def _param_decl(self):
        """
            param_assignment ::= parameter_identifier = constant_mintypmax_expression
            specparam_assignment ::= specparam_identifier = constant_mintypmax_expression | pulse_control_specparam
            list_of_param_assignments ::= param_assignment { , param_assignment }
            list_of_specparam_assignments ::= specparam_assignment { , specparam_assignment }

            local_parameter_declaration ::= localparam [ signed ] [ range ] list_of_param_assignments
                                        | localparam parameter_type list_of_param_assignments
            ', ' ::= parameter [ signed ] [ range ] list_of_param_assignments
                                    | parameter parameter_type list_of_param_assignments
            specparam_declaration ::= specparam [ range ] list_of_specparam_assignments ;
            parameter_type ::= integer | real | realtime | time

            defparam_assignment ::= hierarchical_parameter_identifier = constant_mintypmax_expression
            list_of_defparam_assignments ::= defparam_assignment { , defparam_assignment }
            parameter_override ::= defparam list_of_defparam_assignments ;
        Not Implemented Yet
            pulse_control_specparam
        """
        self.param_kw = Keyword('parameter')
        loc_para_kw = Keyword('localparam')
        spec_para_kw = Keyword('specparam')
        defparam_kw = Keyword('defparam')

        self.time_kw = Keyword('time')
        self.integer_kw = Keyword('integer')
        self.real_kw = Keyword('real')
        self.realtime_kw = Keyword('realtime')

        parameter_type = (self.integer_kw | self.real_kw | self.realtime_kw | self.time_kw)
        param_assignment = identifier + '=' + self.expr.const_mintypmax_expression
        _param_decl = ((self.param_kw + parameter_type + delimitedList(param_assignment))
                      | (self.param_kw + Optional(self.signed_kw) + Optional(self.the_range) +
                         delimitedList(param_assignment)))
        self.local_param_decl = ((loc_para_kw + parameter_type + delimitedList(param_assignment))
                                 | (loc_para_kw + Optional(self.signed_kw) + Optional(self.the_range) +
                                    delimitedList(param_assignment)))
        specparam_assign = param_assignment
        self.specparam_decl = (spec_para_kw + Optional(self.the_range) + delimitedList(specparam_assign) + SEMI)

        defparam_assignment = self.expr.hierarchical_identifier + '=' + self.expr.const_mintypmax_expression
        self.param_override = defparam_kw + delimitedList(defparam_assignment) + SEMI
        return _param_decl
