#encoding = utf-8

from pyparsing import Forward, Keyword, Group, Optional, OneOrMore, ZeroOrMore, oneOf, delimitedList
from .vlog_general import *
from .vlog_base import *
from .vlog_expr import VlogExpr
from .vlog_declaration import VlogDeclaration


__author__ = 'mochen'


class VlogStmt(VlogBase):
    """
        Building Order:
    """

    def __repr__(self):
        return 'VlogStmt'

    @syntax_tree('VlogStmt', priority=100, with_name='statement')
    def _fwd_n_prepare(self):
        """
            Forward define of property:statement
        """
        _stmt = Forward()
        self.expr = VlogExpr()
        return _stmt

    @syntax_tree('VlogStmt', priority=99,  with_name='statement_or_null')
    def _stmt_or_null_prep(self):
        _stmt_or_null = Forward()
        return _stmt_or_null

    @syntax_tree('VlogStmt', priority=93, with_name='seq_block')
    def _seq_block(self):
        """
            seq_block ::= begin [ : block_identifier { block_item_declaration } ] { statement } end
            block_identifier ::= identifier
        """
        self.decl = VlogDeclaration(statement=self)
        begin_kw = Keyword('begin')
        end_kw = Keyword('end')
        # TODO: block_item_declaration in sequence block is untested
        _seq_block = Group((begin_kw + Optional(COLON + identifier('BlockID')) +
                      ZeroOrMore(self.decl.block_item_declaration) +
                      Group(ZeroOrMore(~end_kw + self.statement)).setResultsName('StatementList') + end_kw))
        return _seq_block

    @syntax_tree('VlogStmt', priority=92, with_name='par_block')
    def _par_block(self):
        """
            par_block ::= begin [ : block_identifier { block_item_declaration } ] { statement } end
            block_identifier ::= identifier
        """
        fork_kw = Keyword('fork')
        join_kw = Keyword('join')
        # TODO: block_item_declaration in sequence block is untested
        _par_block = Group((fork_kw + Optional(COLON + identifier('BlockID')) +
                            ZeroOrMore(self.decl.block_item_declaration) +
                            Group(ZeroOrMore(~join_kw + self.statement)).setResultsName('StatementList') + join_kw))
        return _par_block

    @syntax_tree('VlogStmt', priority=20)
    def _init_always(self):
        """
            initial_construct ::= initial statement
            always_construct ::= always statement
        """
        self.initial_construct = Group(Keyword('initial') + self.statement)
        self.always_construct = Group(Keyword('always') + self.statement)

    @syntax_tree('VlogStmt', priority=84, with_name='continuous_assign')
    def _continuous_assign(self):
        """
        Continuous assignment:
            continuous_assign ::= assign [ drive_strength ] [ delay3 ] list_of_net_assignments ;
            list_of_net_assignments ::= net_assignment { , net_assignment }
            net_assignment ::= net_lvalue = expression
        """
        assign_kw = Keyword('assign')

        # net_lvalue = Forward()
        # net_lvalue << (Group(LBRACE + delimitedList(net_lvalue) + RBRACE) | self.expr.hier_id_with_sel)
        self.net_assignment = Group(self.expr.net_lvalue + '=' + self.expr.expression)
        l_net_assignments = Group(delimitedList(self.net_assignment))
        continuous_assign = Group(assign_kw + Optional(self.decl.drive_strength) +
                                  Optional(self.decl.delay3) + l_net_assignments + SEMI)

        return continuous_assign

    @syntax_tree('VlogStmt', priority=81)
    def _proc_assignments(self):
        """
        Procedural assignment:
            blocking_assignment ::= variable_lvalue = [ delay_or_event_control ] expression
            nonblocking_assignment ::= variable_lvalue <= [ delay_or_event_control ] expression
            procedural_continuous_assignments ::= assign variable_assignment
                                                 | deassign variable_lvalue
                                                 | force variable_assignment
                                                 | force net_assignment
                                                 | release variable_lvalue
                                                 | release net_lvalue
            variable_assignment ::= variable_lvalue = expression
        Not Implemented Yet:
            procedural_continuous_assignments ::= assign variable_assignment
                                                 | deassign variable_lvalue
                                                 | force variable_assignment
                                                 | force net_assignment
                                                 | release variable_lvalue
                                                 | release net_lvalue
        """
        # _lvalue = Forward()
        #
        # _lvalue << (Group(LBRACE + delimitedList(_lvalue) + RBRACE) | self.expr.hier_id_with_sel)

        self.blk_assign = Group(self.expr.var_lvalue + "=" +
                                Optional(self.delay_or_event_control) + self.expr.expression)
        self.nonblk_assign = Group(self.expr.var_lvalue + "<=" +
                                   Optional(self.delay_or_event_control) + self.expr.expression)
        self.var_assign = Group(self.expr.var_lvalue + "=" + self.expr.expression)

        assign_kw = Keyword('assign')
        deassign_kw = Keyword('deassign')
        force_kw = Keyword('force')
        release_kw = Keyword('release')
        self.proc_continuous_assign = ((assign_kw + self.var_assign)
                                       | (deassign_kw + self.expr.var_lvalue)
                                       | (force_kw + self.var_assign)
                                       | (force_kw + self.net_assignment)
                                       | (release_kw + self.expr.var_lvalue)
                                       | (release_kw + self.expr.net_lvalue))

    @syntax_tree('VlogStmt', priority=10)
    def _stmt(self):
        """
            statement ::= { attribute_instance } blocking_assignment ;
                         | { attribute_instance } case_statement
                         | { attribute_instance } conditional_statement
                         | { attribute_instance } disable_statement
                         | { attribute_instance } event_trigger
                         | { attribute_instance } loop_statement
                         | { attribute_instance } nonblocking_assignment ;
                         | { attribute_instance } par_block
                         | { attribute_instance } procedural_continuous_assignments ;
                         | { attribute_instance } procedural_timing_control_statement
                         | { attribute_instance } seq_block
                         | { attribute_instance } system_task_enable
                         | { attribute_instance } task_enable
                         | { attribute_instance } wait_statement
        """
        self.statement << ((self.blk_assign + SEMI)
                           | self.case_statement
                           | self.conditional_statement
                           | self.disable_stmt
                           | self.event_trigger
                           | self.loop_statement
                           | (self.nonblk_assign + SEMI)
                           | self.par_block
                           | (self.proc_continuous_assign + SEMI)
                           | self.proc_timing_ctrl_statement
                           | self.seq_block
                           | self.sys_task_en
                           | self.task_en
                           | self.wait_statement)

    @syntax_tree('VlogStmt', priority=90)
    def _stmt_or_null(self):
        """
            statement_or_null ::= statement | { attribute_instance } ;
        """
        self.statement_or_null << (self.statement | SEMI)

    @syntax_tree('VlogStmt', priority=80,  with_name='conditional_statement')
    def _cond_stmt(self):
        """
            conditional_statement ::= if ( expression ) statement_or_null [ else statement_or_null ]
                                     | if_else_if_statement
            if_else_if_statement ::= if ( expression ) statement_or_null
                                     { else if ( expression ) statement_or_null }
                                     [ else statement_or_null ]
        """

        if_kw = Keyword('if')
        else_kw = Keyword('else')

        if_else_if_stmt = Group(if_kw + Group(LPARENTH + self.expr.expression + RPARENTH) +
                                self.statement_or_null.setResultsName('IfStatement') +
                                Group(OneOrMore(Group(Group(else_kw + if_kw) +
                                                Group(LPARENTH + self.expr.expression + RPARENTH) +
                                      self.statement_or_null.setResultsName('ElseIfStatement')))
                                      ).setResultsName('ElseIfStatementList') +
                                Optional(else_kw + self.statement_or_null.setResultsName('ElseStatement')))
        if_else_stmt = Group(if_kw + Group(LPARENTH + self.expr.expression + RPARENTH) +
                             self.statement_or_null.setResultsName('IfStatement') +
                             Optional(else_kw + self.statement_or_null.setResultsName('ElseStatement')))
        _cond_stmt = if_else_if_stmt | if_else_stmt
        return _cond_stmt

    @syntax_tree('VlogStmt', priority=70,  with_name='loop_statement')
    def _loop_stmt(self):
        """
            loop_statement ::= forever statement
                              | repeat ( expression ) statement
                              | while ( expression ) statement
                              | for ( variable_assignment ; expression ; variable_assignment ) statement
        """
        forever_kw = Keyword('forever')
        repeat_kw = Keyword('repeat')
        while_kw = Keyword('while')
        for_kw = Keyword('for')

        _forever_stmt = (forever_kw + self.statement('Body'))
        _repeat_stmt = (repeat_kw + Group(LPARENTH + self.expr.expression + RPARENTH) +
                        self.statement('Body'))
        _while_stmt = (while_kw + Group(LPARENTH + self.expr.expression + RPARENTH) +
                       self.statement('Body'))
        _for_stmt = (for_kw +
                     Group(LPARENTH + self.var_assign + SEMI +
                           Group(self.expr.expression) + SEMI +
                           self.var_assign + RPARENTH) +
                     self.statement('Body'))

        _loop_stmt = Group(_forever_stmt | _repeat_stmt | _while_stmt | _for_stmt)
        return _loop_stmt

    @syntax_tree('VlogStmt', priority=71,  with_name='case_statement')
    def _case_stmt(self):
        """
            case_statement ::= case ( expression ) case_item { case_item } endcase
                              | casez ( expression ) case_item { case_item } endcase
                              | casex ( expression ) case_item { case_item } endcase
            case_item ::= expression { , expression } : statement_or_null
                         | default [ : ] statement_or_null
        """
        case_kw = oneOf('case casez casex')
        end_case_kw = oneOf('endcase')
        def_kw = Keyword('default')

        case_item = Group((delimitedList(self.expr.expression) + COLON + self.statement_or_null('Body'))
                          | (def_kw + Optional(COLON) + self.statement_or_null('Body')))
        case_stmt = Group(case_kw + Group(LPARENTH + self.expr.expression + RPARENTH) +
                          Group(OneOrMore(case_item)).setResultsName('BodyList') +
                          end_case_kw)

        return case_stmt

    @syntax_tree('VlogStmt', priority=82, with_name='delay_or_event_control')
    def _timing_ctrl(self):
        """
           hierarchical_event_identifier ::= hierarchical_identifier
           delay_value ::= unsigned_number
                          | real_number
                          | identifier

           delay_control ::= # delay_value
                            | # ( mintypmax_expression )
           delay_or_event_control ::= delay_control
                                     | event_control
                                     | repeat ( expression ) event_control
           disable_statement ::= disable hierarchical_task_identifier ;
                                | disable hierarchical_block_identifier ;
           event_control ::= @ hierarchical_event_identifier
                            | @ ( event_expression )
                            | @*
                            | @ (*)
           event_trigger ::= -> hierarchical_event_identifier { [ expression ] } ;
           event_expression ::= expression
                               | posedge expression
                               | negedge expression
                               | event_expression or event_expression
                               | event_expression , event_expression
           procedural_timing_control ::= delay_control
                                        | event_control
           procedural_timing_control_statement ::= procedural_timing_control statement_or_null
           wait_statement ::= wait ( expression ) statement_or_null

        Not Implemented Yet:
            delay_value ::= identifier
        """
        # Pay Attention!!!
        # Current delay_value gets a larger range than that described in BNF
        disable_kw = Keyword('disable')
        delay_value = number
        delay_ctrl = SHARP + ((LPARENTH + self.expr.mintypmax_expression + RPARENTH) | delay_value('DelayControl'))
        event_expr = Forward()

        # event_expression ::= expression
        #                     | posedge expression
        #                     | negedge expression
        event_expr_partial = (Optional(oneOf('posedge negedge')) + self.expr.expression)
        # event_expression += event_expression or event_expression
        #                    | event_expression , event_expression
        event_expr << Group(event_expr_partial + Optional((Keyword('or') | ',') + event_expr))

        self.disable_stmt = disable_kw + self.expr.hierarchical_identifier + SEMI

        event_ctrl = Group(AT_SYMBOL + ((LPARENTH + event_expr + RPARENTH)
                                        | '*'
                                        | (LPARENTH + '*' + RPARENTH)
                                        | self.expr.hierarchical_identifier))
        repeat_event_ctrl = Group(Keyword('repeat') + (LPARENTH + self.expr.expression + RPARENTH) + event_ctrl)
        delay_or_event_control = (delay_ctrl
                                  | event_ctrl
                                  | repeat_event_ctrl)

        # TODO: Test the following syntax
        # procedural_timing_control
        self.proc_timing_ctrl = delay_ctrl | event_ctrl
        # procedural_timing_control_statement
        self.proc_timing_ctrl_statement = self.proc_timing_ctrl + self.statement_or_null
        # wait_statement ::= wait ( expression ) statement_or_null
        self.wait_statement = Group(Keyword('wait') + (LPARENTH + self.expr.expression + RPARENTH) +
                                    self.statement_or_null)

        self.event_trigger = Group('->' + self.expr.hierarchical_identifier +
                                   ZeroOrMore(LBRACKET + self.expr.expression + RBRACKET))

        return delay_or_event_control

    @syntax_tree('VlogStmt', priority=72)
    def task_enable(self):
        """
            system_task_enable ::= system_task_identifier [ ( [ expression ] { , [ expression ] } ) ] ;
            task_enable ::= hierarchical_task_identifier [ ( expression { , expression } ) ] ;
        """
        # The following is a little different with the BNF in docstring
        self.sys_task_en = ((sysfunc_identifier + Optional(LPARENTH + RPARENTH) + SEMI)
                            | (sysfunc_identifier + LPARENTH + delimitedList(self.expr.expression) + RPARENTH + SEMI))
        self.task_en = self.expr.hierarchical_identifier + \
                       Optional(LPARENTH + delimitedList(self.expr.expression) + RPARENTH) + SEMI
