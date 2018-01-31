#encoding = utf-8

from .vlog_base import *
try:
    from pyparsing import (Group, ZeroOrMore, Keyword, Regex, )
except ImportError:
    from vlogapy.pyparsing import (Group, ZeroOrMore, Keyword, Regex, )


__author__ = 'mochen'


class VlogSpecify(VlogBase):
    def __repr__(self):
        return 'VlogSpecify'

    # @syntax_tree('VlogSpecify', priority=, with_name='')
    # @syntax_root('VlogSpecify')

    @syntax_root('VlogSpecify')
    def _specify_block(self):
        """
        specify_block ::= specify { specify_item } endspecify
        specify_item ::= specparam_declaration
                        | pulsestyle_declaration
                        | showcancelled_declaration
                        | path_declaration
                        | system_timing_check
        """

        specify_kw = Keyword('specify')
        endspecify_kw = Keyword('endspecify')

        ##############################################################
        # The following specify_item is used only as experimental
        specify_item = ~endspecify_kw + Regex(r'[^\s]+')
        ##############################################################

        specify_block = specify_kw + Group(ZeroOrMore(specify_item)) + endspecify_kw
        return specify_block
