#encoding = utf-8


from .vlog_base import *
from pyparsing import ZeroOrMore, Combine, oneOf, restOfLine, cppStyleComment, cStyleComment
from .vlog_module import VlogPModule


__author__ = 'mochen'


class VlogSource(VlogBase):

    def __repr__(self):
        return 'VlogSource'

    @syntax_root('VlogSource')
    def _source(self):
        """
        source_text ::= { description }
        description ::= module_declaration
                        | udp_declaration
                        | config_declaration
        """
        self.module = VlogPModule()
        self.source = ZeroOrMore(self.module.top)
        self.source.ignore(cStyleComment)
        self.source.ignore(cppStyleComment)
        self.source.ignore(self.compiler_directive)
        return self.source

    @syntax_tree('VlogSource', priority=10, with_name='compiler_directive')
    def _compiler_directive(self):
        """
            Get rid of Compiler Directives
        """
        # compiler directives
        self._compiler_directive = Combine("`" +
                                           oneOf(
                                               "define undef ifndef ifdef else endif default_nettype "
                                               "include resetall timescale unconnected_drive "
                                               "nounconnected_drive celldefine endcelldefine") +
                                           restOfLine)
        return self._compiler_directive
