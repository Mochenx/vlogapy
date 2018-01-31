#encoding = utf-8

from .vlog_general import *
from .vlog_base import *

try:
    from pyparsing import oneOf, Forward, delimitedList, Group, Optional, ZeroOrMore, OneOrMore, dblQuotedString
except ImportError:
    from vlogapy.pyparsing import oneOf, Forward, delimitedList, Group, Optional, ZeroOrMore, OneOrMore, dblQuotedString

__author__ = 'mochen'


__all__ = ['UNI_OP', 'BIN_OP', 'VlogExpr']

UNI_OP = oneOf('+  -  !  ~  &  ~&  |  ^|  ^  ~^')
BIN_OP = oneOf('+  -  *  /  %  ==  !=  ===  !==  &&  '
               '||  <  <=  >  >=  &  |  ^  ^~  >>  << ** <<< >>>')


class VlogExpr(VlogBase):
    """
        Building Order:
            _constant_expr_fwd with priority 50
            _constant_primary with priority 15
            _constant_expr
    """

    def __repr__(self):
        return 'VlogExpr'

    @syntax_tree('VlogExpr', priority=50, with_name='constant_expression')
    def _constant_expr_fwd(self):
        """
            Forward define of property:constant_expression
        """
        const_expr = Forward()
        return const_expr

    @syntax_tree('VlogExpr', priority=49, with_name='expression')
    def _expr_fwd(self):
        ###############################################
        # Experimental codes
        # expr = self.constant_expression
        ###############################################
        expr = Forward()
        return expr

    @syntax_tree('VlogExpr', priority=31, with_name='range_expression')
    def _range_expr(self):
        """
            base_expression ::= expression
            lsb_constant_expression ::= constant_expression
            msb_constant_expression ::= constant_expression
            width_constant_expression ::= constant_expression
            range_expression ::= expression
                                | msb_constant_expression : lsb_constant_expression
                                | base_expression +: width_constant_expression
                                | base_expression -: width_constant_expression
        """
        range_expr = Group((self.expression + Group(oneOf('+ -') + ':') + self.constant_expression)
                           | (self.constant_expression + COLON + self.constant_expression)
                           | self.expression)
        return range_expr

    @syntax_tree('VlogExpr', priority=30, with_name='hierarchical_identifier')
    def _hier_id(self):
        """
            hierarchical_identifier ::= { identifier [ [ constant_expression ] ] . } identifier
        """
        hier_id = ZeroOrMore(identifier + Optional(LBRACKET + self.constant_expression + RBRACKET) + POINT) + identifier
        return hier_id

    @syntax_tree('VlogExpr', priority=1)
    def _expr(self):
        """
            expression ::= primary
                          | unary_operator { attribute_instance } primary
                          | expression binary_operator { attribute_instance } expression
                          | conditional_expression
            Not Implemented Yet:
                          | conditional_expression
        """
        bin_expr = Forward()
        uni_expr = self.primary | Group(UNI_OP + self.primary)
        bin_expr << (uni_expr + ZeroOrMore(BIN_OP + bin_expr))
        self.expression << (Group(bin_expr + '?' + self.expression + ':' + self.expression) | bin_expr)

        # self.expression << ((UNI_OP + self.primary)
        #                     | (self.primary + BIN_OP + self.expression)
        #                     # | (self.primary + "?" +
        #                     #    self.expression + ":" + self.expression)
        #                     | self.primary)
        return self.expression

    @syntax_root('VlogExpr')
    def _constant_expr(self):
        """
            constant_expression ::= constant_primary
                | unary_operator { attribute_instance } constant_primary
                | constant_expression binary_operator { attribute_instance } constant_expression
                | constant_expression ? { attribute_instance } constant_expression : constant_expression
        """
        bin_expr = Forward()
        uni_expr = self.constant_primary | Group(UNI_OP + self.constant_primary)
        bin_expr << (uni_expr + ZeroOrMore(BIN_OP + bin_expr))
        self.constant_expression << (Group(bin_expr + '?' + self.constant_expression + ':' + self.constant_expression)
                                     | bin_expr)

        # self.constant_expression << ((UNI_OP + self.constant_primary)
        #                              | (self.constant_primary + BIN_OP + self.constant_expression)
        #                              # | (self.constant_expression + BIN_OP + self.constant_expression)
        #                              # | (self.constant_expression + "?" +
        #                              | (self.constant_primary + "?" +
        #                                 self.constant_expression + ":" + self.constant_expression)
        #                              | self.constant_primary)
        return self.constant_expression

    @syntax_tree('VlogExpr', priority=15, with_name='constant_primary')
    def _constant_primary(self):
        """
            constant_mintypmax_expression ::= constant_expression
                                             | constant_expression : constant_expression : constant_expression
            constant_concatenation ::= { constant_expression { , constant_expression } }
            constant_multiple_concatenation ::= { constant_expression constant_concatenation }
            constant_primary ::= number
                | parameter_identifier [ [ constant_range_expression ] ]
                | specparam_identifier [ [ constant_range_expression ] ]
                | constant_concatenation
                | constant_multiple_concatenation
                | constant_function_call
                | constant_system_function_call
                | ( constant_mintypmax_expression )
                | string
        """
        # TODO: Test the first branch of const_mintypmax_expression
        self.const_mintypmax_expression = ((self.constant_expression + COLON + self.constant_expression +
                                            COLON + self.constant_expression)
                                           | self.constant_expression)
        const_concat = Group(LBRACE + delimitedList(self.constant_expression) + RBRACE)
        const_multi_concat = Group(LBRACE + self.constant_expression + const_concat + RBRACE)
        _constant_primary = (number
                             | Group(LPARENTH + self.const_mintypmax_expression + RPARENTH)
                             | const_multi_concat
                             | self.const_func_call
                             | self.const_sys_func_call
                             | const_concat
                             | dblQuotedString
                             # constant_primary ::= parameter_identifier [ [ constant_range_expression ] ]
                             #                      | specparam_identifier [ [ constant_range_expression ] ]
                             | (identifier + Optional(LBRACKET + self.range_expression + RBRACKET)))
        return _constant_primary

    @syntax_tree('VlogExpr', priority=16, with_name='primary')
    def _primary(self):
        """
            mintypmax_expression ::= expression
                                    | expression : expression : expression

            concatenation ::= { expression { , expression } }
            multiple_concatenation ::= { constant_expression concatenation }
            primary ::= number
                       | hierarchical_identifier [ { [ expression ] } [ range_expression ] ]
                       | concatenation
                       | multiple_concatenation
                       | function_call
                       | system_function_call
                       | ( mintypmax_expression )
                       | string
        """
        # TODO: Test the first branch of mintypmax_expression
        self.mintypmax_expression = ((self.expression + COLON + self.expression + COLON + self.expression)
                                     | self.expression)
        concat = Group(LBRACE + delimitedList(self.expression) + RBRACE)
        multi_concat = Group(LBRACE + self.constant_expression + concat + RBRACE)

        # hierarchical_identifier [ { [ expression ] } [ range_expression ] ]
        self.hier_id_with_sel = Group(self.hierarchical_identifier +
                                 Group(OneOrMore(Group(LBRACKET + self.expression + RBRACKET)))('IndexList') +
                                 Group(LBRACKET + self.range_expression + RBRACKET)('Slice')) \
                           | Group(self.hierarchical_identifier +
                                   Group(LBRACKET + self.range_expression + RBRACKET)('Slice')) \
                           | self.hierarchical_identifier
        _primary = (number
                    | Group(LPARENTH + self.mintypmax_expression + RPARENTH)
                    | multi_concat('multi_concat')
                    | self.func_call
                    | self.sys_func_call
                    | concat('concat')
                    | self.hier_id_with_sel
                    | dblQuotedString
                    )
        return _primary

    @syntax_tree('VlogExpr', priority=14)
    def _left_value(self):
        """
            net_lvalue ::= hierarchical_net_identifier [ { [ constant_expression ] } [ constant_range_expression ] ]
                          | { net_lvalue { , net_lvalue } }
            variable_lvalue ::= hierarchical_variable_identifier [ { [ expression ] } [ range_expression ] ]
                               | { variable_lvalue { , variable_lvalue } }
        """
        self.net_lvalue = Forward()
        self.net_lvalue << (Group(LBRACE + delimitedList(self.net_lvalue) + RBRACE) | self.hier_id_with_sel)

        self.var_lvalue = Forward()
        self.var_lvalue << (Group(LBRACE + delimitedList(self.var_lvalue) + RBRACE) | self.hier_id_with_sel)

    @syntax_tree('VlogExpr', priority=29)
    def func_call(self):
        """
            constant_function_call ::= function_identifier { attribute_instance }
                                    ( constant_expression { , constant_expression } )
            constant_system_function_call ::= system_function_identifier
                                    ( constant_expression { , constant_expression } )
            function_call ::= hierarchical_function_identifier{ attribute_instance } ( expression { , expression } )
            system_function_call ::= system_function_identifier [ ( expression { , expression } ) ]
        """
        self.const_func_call = identifier + LPARENTH + delimitedList(self.constant_expression) + RPARENTH
        self.const_sys_func_call = sysfunc_identifier + LPARENTH + delimitedList(self.constant_expression) + RPARENTH
        self.func_call = self.hierarchical_identifier + LPARENTH + delimitedList(self.expression) + RPARENTH
        self.sys_func_call = sysfunc_identifier + Optional(LPARENTH + delimitedList(self.expression) + RPARENTH)


