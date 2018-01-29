# encoding = utf-8

from .vlog_base import *
from pyparsing import (Group, ZeroOrMore, Keyword, Regex, )


__author__ = 'mochenx'


class VlogUDP(VlogBase):
    def __repr__(self):
        return 'VlogUDP'

    # @syntax_tree('VlogUDP', priority=, with_name='')
    # @syntax_root('VlogUDP')

    @syntax_root('VlogUDP')
    def _udp_decl(self):
        """
        udp_declaration ::= { attribute_instance } primitive udp_identifier ( udp_port_list ) ;
                            udp_port_declaration { udp_port_declaration }
                            udp_body
                            endprimitive
                        | { attribute_instance } primitive udp_identifier ( udp_declaration_port_list ) ;
                            udp_body
                            endprimitive
        """

        primitive_kw = Keyword('primitive')
        endprimitive_kw = Keyword('endprimitive')

        ##############################################################
        # The following _item is used only as experimental
        _item = ~endprimitive_kw + Regex(r'[^\s]+')
        ##############################################################

        udp_decl = primitive_kw + Group(ZeroOrMore(_item)) + endprimitive_kw
        return udp_decl
