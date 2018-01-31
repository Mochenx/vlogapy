# encoding = utf-8

from .vlog_base import *
from .vlog_declaration import VlogDeclaration
from .vlog_expr import VlogExpr, UNI_OP, BIN_OP
from .vlog_general import *
from .vlog_primitive import VlogPrimitive
from .vlog_specify import VlogSpecify
from .vlog_stmt import VlogStmt

try:
    from elements import ElemModule, ElemExportPort, ElemPort
    from pyparsing import (Group, ZeroOrMore, oneOf, Optional, delimitedList, Suppress, Keyword, Forward, OneOrMore)
except ImportError:
    from vlogapy.elements import ElemModule, ElemExportPort, ElemPort
    from vlogapy.pyparsing import (Group, ZeroOrMore, oneOf, Optional, delimitedList, Suppress, Keyword, Forward, OneOrMore)

__author__ = 'mochen'


class VlogPModule(VlogBase):
    @staticmethod
    def build_elem_port_list(tokens):
        tkn = tokens
        kwargs = {}
        kwargs['direction'] = tkn[0]
        if 'Type' in tkn:
            kwargs['var_type'] = tkn.Type
        if 'Signed' in tkn:
            kwargs['signed'] = True
        if 'Range' in tkn:
            kwargs['port_range'] = tkn.Range[0]

        return [ElemPort(name=var_id, **kwargs) for var_id in tkn.IDList]

    def push_scope(self, scope):
        if not hasattr(self, 'symbl_stack'):
            self.symbl_stack = []
        self.symbl_stack.append(scope)

    def pop_scope(self):
        self.symbl_stack.pop()

    def put(self, name_symbol=None, name=None, symbol=None):
        self.symbl_stack[-1].put(name_symbol=name_symbol, name=name, symbol=symbol)

    def __repr__(self):
        return 'VlogPModule'

    @syntax_tree('VlogPModule', priority=100)
    def _before_everything(self):
        self.expr = VlogExpr()
        self.stmt = VlogStmt()
        self.decl = VlogDeclaration(statement=self.stmt)
        self.specify = VlogSpecify()
        self.primitive = VlogPrimitive()

    @syntax_tree('VlogPModule', priority=99, with_name='generate_region')
    def _gen_blk_prepare(self):
        self.gen_region = Forward()
        self.gen_var_decl = Forward()
        self.cond_gen = Forward()
        self.loop_gen = Forward()
        return self.gen_region

    @syntax_tree('VlogPModule', priority=20, with_name='module_item')
    def _module_items(self):
        """
            module_item ::= port_declaration ;
                           | non_port_module_item

            module_or_generate_item ::= { attribute_instance } module_or_generate_item_declaration
                                       | { attribute_instance } local_parameter_declaration ;
                                       | { attribute_instance } parameter_override
                                       | { attribute_instance } continuous_assign
                                       | { attribute_instance } gate_instantiation
                                       | { attribute_instance } udp_instantiation
                                       | { attribute_instance } module_instantiation
                                       | { attribute_instance } initial_construct
                                       | { attribute_instance } always_construct
                                       | { attribute_instance } loop_generate_construct
                                       | { attribute_instance } conditional_generate_construct

            module_or_generate_item_declaration ::= net_declaration
                                                   | reg_declaration
                                                   | integer_declaration
                                                   | real_declaration
                                                   | time_declaration
                                                   | realtime_declaration
                                                   | event_declaration
                                                   | genvar_declaration
                                                   | task_declaration
                                                   | function_declaration

            non_port_module_item ::= module_or_generate_item
                                    | generate_region
                                    | specify_block
                                    | { attribute_instance } parameter_declaration ;
                                    | { attribute_instance } specparam_declaration
        Not Implemented Yet:
        |  udp_instantiation
        """
        ENDMODULE = Suppress(Keyword('endmodule'))

        # TODO: task_declaration & function_declaration are not tested in module scale
        module_or_generate_item_declaration = (self.decl.net_declaration |
                                               self.decl.reg_declaration |
                                               self.decl.integer_declaration |
                                               self.decl.time_declaration |
                                               self.decl.event_decl |
                                               self.decl.real_decl |
                                               self.decl.realtime_decl |
                                               self.decl.task_declaration |
                                               self.decl.function_declaration |
                                               self.gen_var_decl)

        self.module_or_generate_item = (module_or_generate_item_declaration |
                                        (self.decl.local_param_decl + SEMI) |
                                        self.decl.param_override |
                                        self.stmt.continuous_assign |
                                        self.primitive.top |
                                        self.module_instantiation |
                                        self.stmt.initial_construct |
                                        self.stmt.always_construct |
                                        self.loop_gen |
                                        self.cond_gen)
        non_port_module_item = (self.module_or_generate_item |
                                self.generate_region |
                                self.specify.top |
                                (self.decl.parameter_declaration + SEMI) |
                                self.decl.specparam_decl)

        def f_io_decl(t):
            for x in t:
                self.put((x.name, x))

        self.module_item = ~ENDMODULE + (
            (self.port_declaration + SEMI).setParseAction(
                lambda t: VlogPModule.build_elem_port_list(t.PortDecl if 'PortDecl' in t else t)
            ).addParseAction(f_io_decl) |
            non_port_module_item
        )

    @syntax_root('VlogPModule')
    def _module_decl(self):
        """
        BNF from IEEE1364-2005
        module_declaration ::=
            { attribute_instance } module_keyword module_identifier [ module_parameter_port_list ]
                list_of_ports ; { module_item }
                endmodule
            | { attribute_instance } module_keyword module_identifier [ module_parameter_port_list ]
                [ list_of_port_declarations ] ; { non_port_module_item }
                endmodule
        module_keyword ::= module | macromodule
        module_identifier ::= identifier

        Unimplemented features:
            { attribute_instance }
        """
        ENDMODULE = Suppress(Keyword('endmodule'))

        def f_new_module(t):
            try:
                new_module = ElemModule(name=t.ModuleHeader.Name)
            except Exception as e:
                print(e)
            for each_port in t.ModuleHeader.PortList:
                if isinstance(each_port, ElemExportPort):
                    new_module.add_port(each_port)
                else:
                    elem_list = VlogPModule.build_elem_port_list(each_port)

                    for n in elem_list:
                        np = ElemExportPort(name=n.name)
                        np.set_port(name=n.name, obj=n)
                        new_module.put(name=n.name, symbol=n)
                        new_module.add_port(np)
            return new_module

        # Names in module parsing result
        # module_decl = ['ModuleHeader': ['Name': ...,
        #                                 'PortList':[...]],
        #                'ModuleItems': ...]
        module_hdr = Group(Suppress(oneOf("module macromodule")) + identifier('Name') +
                           Optional(self.module_parameter_port_list)('ParamDeclList') +
                           Optional(LPARENTH + Group(Optional(delimitedList(
                               # Group(oneOf("input output") +
                               #       (netDecl1Arg | netDecl2Arg | netDecl3Arg)) |
                               self.port_declaration |
                               self.port('Port')))).setResultsName('PortList') + RPARENTH) +
                           SEMI).setResultsName('ModuleHeader').setParseAction(f_new_module)

        module_hdr.setDebug(False)
        self.module_decl = Group(module_hdr.addParseAction(lambda t: self.push_scope(t.ModuleHeader.scope)) +
                                 Group(ZeroOrMore(self.module_item)).setResultsName('ModuleItems') +
                                 ENDMODULE).setParseAction(lambda t: self.pop_scope())
        return self.module_decl

    @syntax_tree('VlogPModule', priority=40, with_name='port_declaration')
    def _port_decl(self):
        """
            output_variable_type ::= integer | time
            port_identifier ::= identifier

            list_of_port_identifiers ::= port_identifier { , port_identifier }
            list_of_variable_port_identifiers ::= port_identifier [ = constant_expression ]
                                                    { , port_identifier [ = constant_expression ] }

            inout_declaration ::= inout [ net_type ] [ signed ] [ range ] list_of_port_identifiers
            input_declaration ::= input [ net_type ] [ signed ] [ range ] list_of_port_identifiers
            output_declaration ::= output [ net_type ] [ signed ] [ range ] list_of_port_identifiers
                                   | output reg [ signed ] [ range ] list_of_variable_port_identifiers
                                   | output output_variable_type list_of_variable_port_identifiers
        """
        INPUT_KW = Keyword('input')
        INOUT_KW = Keyword('inout')
        OUTPUT_KW = Keyword('output')
        IO_KW = INPUT_KW | INOUT_KW | OUTPUT_KW  # oneOf('input inout output')
        SIGNED_KW = Keyword('signed')
        REG_KW = Keyword('reg')
        INT_TIME_KW = oneOf('integer time')

        # It uses ':' as separator to make user utilize MSB & LSB easily
        # self.const_range = Group(LBRACKET +
        #                          self.expr.constant_expression + ':' + self.expr.constant_expression +
        #                          RBRACKET)

        l_var_port_id = delimitedList(~IO_KW + identifier + Optional(Group('=' + self.expr.constant_expression)))

        input_decl = Group(INPUT_KW + Optional(net_type)('Type') +
                           Optional(SIGNED_KW)('Signed') + Optional(self.decl.the_range)('Range') +
                           delimitedList(~IO_KW + identifier).setResultsName('IDList')).setResultsName('PortDecl')
        output_decl = Group(OUTPUT_KW + ((REG_KW('Type') + Optional(SIGNED_KW)('Signed') +
                                          Optional(self.decl.the_range)('Range') + l_var_port_id('IDList')) |
                                         INT_TIME_KW('Type') + l_var_port_id('IDList') |
                                         (Optional(net_type)('Type') +
                                          Optional(SIGNED_KW)('Signed') + Optional(self.decl.the_range)('Range') +
                                          delimitedList(~IO_KW + identifier).setResultsName('IDList')))
                            ).setResultsName('PortDecl')
        inout_decl = Group(INOUT_KW + Optional(net_type)('Type') +
                           Optional(SIGNED_KW)('Signed') + Optional(self.decl.the_range)('Range') +
                           delimitedList(~IO_KW + identifier).setResultsName('IDList')).setResultsName('PortDecl')
        self._port_decl = (inout_decl | input_decl | output_decl)
        self._port_decl.setDebug(False)
        return self._port_decl

    @syntax_tree('VlogPModule', priority=3)
    def _para_n_ports(self):
        """
        BNF from IEEE1364-2005
            module_parameter_port_list ::= # ( parameter_declaration { , parameter_declaration } )
            list_of_ports ::= ( port { , port } )
            list_of_port_declarations ::=
                ( port_declaration { , port_declaration } )
                | ( )
            port ::=
                [ port_expression ]
                | . port_identifier ( [ port_expression ] )
            port_expression ::=
                port_reference
                | { port_reference { , port_reference } }
            port_reference ::=
                port_identifier [ [ constant_range_expression ] ]
            port_declaration ::=
                {attribute_instance} inout_declaration
                | {attribute_instance} input_declaration
                | {attribute_instance} output_declaration
            port_identifier ::= identifier
        """

        # Define actions for constructing AST
        # f_port_ref returns a {'PortExprName': name, 'PortExprList': [(name, range), ()...]}
        f_port_ref = lambda t: {'PortExprName': t.PortExprName,
                                'PortExprList': [(t.PortExprName,
                                                  t.PortExprRange[0] if 'PortExprRange' in t else None)]}

        def f_mul_port_ref(pt_list):
            """
                f_mul_port_ref returns a {'PortExprName': combined names,
                                          'PortExprList': [(name0, range), (name1, range)...]}
            """
            # New PortExprName, combined from all names of given list
            name = []
            # New PortExprList, concatenation of all PortExprList from given list
            expr_list = []
            for pt_ref in pt_list:
                try:
                    name.append(pt_ref['PortExprName'])
                    expr_list.extend(pt_ref['PortExprList'])
                except Exception as e:
                    print(e)
            # New name is 'name0+name1+...'
            r = '+'.join(name)
            return {'PortExprName': r, 'PortExprList': expr_list}

        def f_port(tkns):
            """
                For pattern: .id(port expression), id is used as port name
                For pattern: port expression, attribute PortExprName in port expression is used as port name
            """
            # Pattern: .id(port expression)
            if 'ExportName' in tkns and 'ExportExpr' in tkns:
                r = ElemExportPort(name=tkns.ExportName)
                expr_list = tkns.ExportExpr['PortExprList']
            # Pattern: port expression
            else:
                if len(tkns) > 1:
                    raise ValueError("Port token shouldn't be longer than 1")
                tkn = tkns[0] if isinstance(tkns[0], dict) else tkns
                if 'PortExprName' in tkn:
                    r = ElemExportPort(name=tkn['PortExprName'])
                    expr_list = tkn['PortExprList']
                else:
                    raise AttributeError('No attribute-PortExprName is found in given token list(%s)' % str(tkns))
            for a_port in expr_list:
                r.set_port(name=a_port[0], obj=None, sel_range=a_port[1])
            return r

        # BNF starts here
        self.module_parameter_port_list = Group(SHARP + LPARENTH +
                                                delimitedList(self.decl.parameter_declaration) + RPARENTH)
        port_ref = identifier('PortExprName') + Optional(self.decl.the_range)('PortExprRange')
        port_expr = ((LBRACE + delimitedList(port_ref) + RBRACE).setParseAction(f_mul_port_ref)
                     | port_ref.setParseAction(f_port_ref))
        self.port = ((POINT + identifier('ExportName') + LPARENTH + port_expr('ExportExpr') +
                      RPARENTH).setParseAction(f_port)
                     | port_expr.setParseAction(f_port))

        self.port.setDebug(False)

    @syntax_tree('VlogPModule', priority=30, with_name='module_instantiation')
    def _module_inst(self):
        """
            module_identifier ::= identifier
            module_instance_identifier ::= identifier

            module_instantiation ::= module_identifier [ parameter_value_assignment ]
                                        module_instance { , module_instance } ;
            module_instance ::= name_of_module_instance ( [ list_of_port_connections ] )
            name_of_module_instance ::= module_instance_identifier [ range ]
            list_of_port_connections ::= ordered_port_connection { , ordered_port_connection }
                                        | named_port_connection { , named_port_connection }
            ordered_port_connection ::= { attribute_instance } [ expression ]
            named_port_connection ::= { attribute_instance } . port_identifier ( [ expression ] )

            parameter_value_assignment ::= # ( list_of_parameter_assignments )
            list_of_parameter_assignments ::= ordered_parameter_assignment { , ordered_parameter_assignment }
                                             | named_parameter_assignment { , named_parameter_assignment }
            ordered_parameter_assignment ::= expression
            named_parameter_assignment ::= . parameter_identifier ( [ mintypmax_expression ] )
        """

        ordered_port_connection = Optional(self.expr.expression)
        named_port_connection = Group(POINT + identifier('PortName') +
                                      LPARENTH + Optional(self.expr.expression) + RPARENTH)
        l_port_connections = Group(delimitedList(named_port_connection)
                                   | delimitedList(ordered_port_connection))
        name_of_module_inst = identifier + Optional(self.decl.the_range)
        module_instance = Group(name_of_module_inst('InstanceName') +
                                LPARENTH + Optional(l_port_connections('ConnectionList')) + RPARENTH)
        # Parameter assignments when instantiating module
        ordered_param_assign = self.expr.expression
        named_param_assig = POINT + identifier + LPARENTH + Optional(self.expr.mintypmax_expression) + RPARENTH
        l_param_assignments = delimitedList(ordered_param_assign) | delimitedList(named_param_assig)
        parameter_value_assignment = SHARP + LPARENTH + l_param_assignments + RPARENTH

        module_instantiation = Group(identifier('ModuleName') + Optional(parameter_value_assignment) +
                                     delimitedList(module_instance)('InstanceList') + SEMI)
        return module_instantiation

    @syntax_tree('VlogPModule', priority=10)
    def _gen_block(self):
        """
            genvar_declaration ::= genvar list_of_genvar_identifiers ;
            list_of_genvar_identifiers ::= genvar_identifier { , genvar_identifier }
            genvar_primary ::= constant_primary | genvar_identifier
            genvar_expression ::= genvar_primary
                            | unary_operator { attribute_instance } genvar_primary
                            | genvar_expression binary_operator { attribute_instance } genvar_expression
                            | genvar_expression ? { attribute_instance } genvar_expression : genvar_expression
            genvar_initialization ::= genvar_identifier = constant_expression
            genvar_iteration ::= genvar_identifier = genvar_expression

            generate_block ::= module_or_generate_item
                            | begin [ : generate_block_identifier ] { module_or_generate_item } end
            generate_block_or_null ::= generate_block | ;

            loop_generate_construct ::= for ( genvar_initialization ; genvar_expression ; genvar_iteration )
                                            generate_block
            if_generate_construct ::= if ( constant_expression ) generate_block_or_null [ else generate_block_or_null ]
            case_generate_item ::= constant_expression { , constant_expression } : generate_block_or_null
                                | default [ : ] generate_block_or_null
            case_generate_construct ::= case ( constant_expression ) case_generate_item { case_generate_item } endcase
            conditional_generate_construct ::= if_generate_construct | case_generate_construct
            generate_region ::= generate { module_or_generate_item } endgenerate
        """
        gen_kw = Keyword('generate')
        endgen_kw = Keyword('endgenerate')
        genvar_kw = Keyword('genvar')

        genvar_primary = self.expr.constant_primary | identifier

        # To reduce left-recursive in parsing
        # genvar_expr = (UNI_OP + genvar_primary
        #                | genvar_expr + BIN_OP + genvar_expr
        #                | genvar_expr + '?' + genvar_expr + ':' + genvar_expr
        #                | genvar_primary)
        self.genvar_expr = Forward()
        bin_expr = Forward()
        uni_expr = genvar_primary | (UNI_OP + genvar_primary)
        bin_expr << (uni_expr + ZeroOrMore(BIN_OP + bin_expr))
        self.genvar_expr << ((bin_expr + '?' + self.genvar_expr + ':' + self.genvar_expr) | bin_expr)

        genvar_init = identifier + '=' + self.expr.constant_expression
        genvar_iter = identifier + '=' + self.genvar_expr
        self.gen_var_decl << genvar_kw + delimitedList(identifier) + SEMI

        generate_block = (self.module_or_generate_item
                          | (Keyword('begin') + Optional(COLON + identifier) +
                             ZeroOrMore(self.module_or_generate_item) + Keyword('end')))
        gen_block_or_null = generate_block | SEMI
        # Loop
        self.loop_gen << (Keyword('for') + LPARENTH + Group(genvar_init) + SEMI + Group(self.genvar_expr) +
                          SEMI + Group(genvar_iter) + RPARENTH +
                          generate_block)
        # If
        if_gen = (Keyword('if') + LPARENTH + self.expr.constant_expression + RPARENTH +
                  gen_block_or_null +
                  Optional(Keyword('else') + gen_block_or_null))
        # Case
        case_generate_item = (delimitedList(self.expr.constant_expression) + COLON + gen_block_or_null
                              | Keyword('default') + Optional(COLON) + gen_block_or_null)
        case_gen = (Keyword('case') + LPARENTH + self.expr.constant_expression + RPARENTH +
                    OneOrMore(case_generate_item) + Keyword('endcase'))
        self.cond_gen << if_gen | case_gen

        self.gen_region << gen_kw + ZeroOrMore(~endgen_kw + self.module_or_generate_item) + endgen_kw
