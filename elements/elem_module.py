from collections import OrderedDict
from .base import ElementBase, SymbolTable, VlogSyntaxError

try:
    from syntax.vlog_general import str_list_net_type
except ImportError:
    from vlogapy.syntax.vlog_general import str_list_net_type


__author__ = 'mochen'


class ElemModule(ElementBase):
    """
    """
    class ModuleSymTab(SymbolTable):
        """
            Subclass of SymbolTable for overriding method-put
            ----------        ------------
           |ElemModule|      |ModuleSymTab|
           |----------|      |------------|
           |symbol_tab|----> |            |
           |          |<---- |   module   |
           |          |      |            |
            ----------        ------------
            ElemModule.put calls ModuleSymTab.put
            In ModuleSymTab.put, if new symbol is ElemPort, ModuleSymTab.put calls ElemModule.add_io_decl
        """
        def __init__(self, module):
            super(ElemModule.ModuleSymTab, self).__init__()
            self.module = module

        def put(self, name_symbol=None, name=None, symbol=None):
            """
                For symbols founded in module scope, it needs to mark IO variables
                after adding them into symbol table
            """
            putted_symbl = super(ElemModule.ModuleSymTab, self).put(name_symbol=name_symbol, name=name, symbol=symbol)
            if isinstance(putted_symbl, ElemPort):
                self.module.add_io_decl(putted_symbl)

    def __init__(self, **kwargs):
        if 'name' not in kwargs:
            raise ValueError
        self._name = kwargs['name']
        self._exported_ports = OrderedDict()
        self.symbol_tab = ElemModule.ModuleSymTab(self)
        self.all_io = {}

    def __str__(self):
        s_ports = [str(p) for p in self.ports.values()]
        s = '%s[%s]' % (self.name, ','.join(s_ports))
        return s

    def __repr__(self):
        return str(self)

    def add_io_decl(self, io_decl):
        if not isinstance(io_decl, ElemPort):
            raise TypeError('Method add_io_decl only accept ElemPort as argument')
        io_list = self.all_io.setdefault(io_decl.direction, {})
        io_list[io_decl.name] = io_decl
        # io_list.append(io_decl)

    def add_port(self, a_port):
        if not isinstance(a_port, ElemExportPort):
            raise TypeError
        self._exported_ports[a_port.name] = a_port

    def put(self, **kwargs):
        # Can this method be added automatically after instantiating a SymbolTable object?
        self.symbol_tab.put(**kwargs)

    def resolve(self):
        """
            Resolve all undefined symbols
        """
        # Find defines for all ports
        for port_name, port in self.ports.items():
            if not isinstance(port, ElemExportPort):
                print('hha')
            for k, p in port.items():
                name, bit_range = k
                if p:
                    continue
                not_find = True
                for io_list in self.all_io.values():
                    if name in io_list:
                        port[k] = io_list[name]
                        not_find = False
                        break
                if not_find:
                    raise VlogSyntaxError('A port defined in port list of module is NOT defined as input/output/inout')

    @property
    def name(self):
        return self._name

    @property
    def ports(self):
        return self._exported_ports

    @property
    def inputs(self):
        return self.all_io.get('input', None)

    @property
    def outputs(self):
        return self.all_io.get('output', None)

    @property
    def inouts(self):
        return self.all_io.get('inout', None)

    @property
    def scope(self):
        return self.symbol_tab


class ElemExportPort(ElementBase, OrderedDict):
    """
    Class ElemExportPort deal with the list of ports, and I call it Exported Ports. Each port defined in module
        has a Exported-Port-Name and a Inner-Port-Name(I use IO declaration in codes sometimes).
        Most time,we don't declare Exported-Port-Name(or called implict port as IEEE's description),
        then the Exported-Port-Name is the same with Inner-Port-Name
        For example:
                     module Test1(.p0({port0, port1}), p2, p3);
                     input [7:0] port0;
                     input [1:0] port1;
                     output reg [1:0] p2, p3;
                     endmodule
               p0, p2, p3 is the Exported-Port-Name
               port0, port1, p2, p3 is the Inner-Port-Name

    From IEEE 1364-2005:
        Each module shall be declared either entirely with the list of ports syntax as described in 12.3.2 or
        entirely using the list_of_port_declarations as described in this subclause.
    """
    def __init__(self, *args, **kwargs):
        self._name = ''
        self._width = -1
        # elem_ports is a dict from (name, msb, lsb) => object mapping
        # self.elem_ports = OrderedDict()
        if 'name' in kwargs:
            self._name = kwargs['name']
            del kwargs['name']
        super(ElemExportPort, self).__init__(*args, **kwargs)
        # if 'ptree' in kwargs:
        #     self.ptree = kwargs['ptree']

    def set_port(self, name, obj, sel_range=None):
        if sel_range:
            if isinstance(sel_range, list):
                if len(sel_range) == 2:
                    msb = sel_range[0]
                    lsb = sel_range[1]
                elif len(sel_range) == 1:
                    msb = lsb = sel_range[0]
                else:
                    raise ValueError
            elif isinstance(sel_range, tuple):
                if len(sel_range) == 2:
                    msb, lsb = sel_range
                elif len(sel_range):
                    msb = lsb = sel_range[0]
                else:
                    raise ValueError
            elif isinstance(sel_range, int):
                msb = lsb = sel_range
            else:
                raise TypeError
            _range = (msb, lsb)
        else:
            _range = None

        # self.elem_ports[(name, _range)] = obj
        self[(name, _range)] = obj

    def __str__(self):
        s = '%s:{%s}' % (self._name, ','.join([name+str(_r) if _r else name for name, _r in self.keys()]))
        return s

    def __repr__(self):
        s = str(self)
        return s

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, val):
        self._name = val

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, val):
        self._width = val


# TODO: provide a base class for variable define classes, such as port/reg/wire define
class ElemPort(ElementBase):
    """
        Port declaration rules:
        1. If a port declaration includes a net or variable type, then the port is considered completely declared,
            and it is an error for the port to be declared again in a variable or net data type declaration.
        2. If a port declaration does not include a net or variable type, then the port can be again declared in a net
            or variable declaration.
        3. If the net or variable is declared as a vector, the range specification between the two
            declarations of a port shall be identical.
    """
    available_net_var_type = ['reg']
    available_net_var_type.extend(str_list_net_type)
    available_direction = ('input', 'output', 'inout')

    def __init__(self, **kwargs):
        if 'direction' not in kwargs or kwargs['direction'] not in ElemPort.available_direction:
            raise ValueError

        if 'name' not in kwargs:
            raise ValueError
        self._name = kwargs['name']
        self.direction = kwargs['direction']

        if 'var_type' in kwargs:
            if kwargs['var_type'] not in ElemPort.available_net_var_type:
                raise ValueError('Current type(%s) is not a type of the supported types(%s)' %
                                 (kwargs['var_type'], ElemPort.available_net_var_type))
            self.var_type = kwargs['var_type']

        if 'port_range' in kwargs:
            self.port_range = kwargs['port_range']

        if 'signed' in kwargs:
            if not isinstance(kwargs['signed'], bool):
                raise TypeError('The type of argument signed must be a Bool variable')
            self.signed = kwargs['signed']

    def __str__(self):
        s_list = [self.direction]
        if hasattr(self, 'var_type'):
            s_list.append(self.var_type)
        if hasattr(self, 'signed'):
            s_list.append('signed')
        if hasattr(self, 'port_range'):
            s_list.append(str(self.port_range))
        s_list.append(self.name)
        return ' '.join(s_list)

    def __repr__(self):
        return str(self)

    @property
    def name(self):
        return self._name

    def merge(self, obj):
        """
            Called by SymbolTable, when another symbol with the same name is added into table
            ElemPort support this because of the port declaration rule 2 in docstring.
        """
        pass

    # def __getitem__(self, item):
    #     lsb = msb = 0
    #     if isinstance(item, int) and item >= 0:
    #         msb = lsb = item
    #     elif isinstance(item, slice) and item.start >= 0 and item.stop >= 0:
    #         msb = item.start if item.start > item.stop else item.stop
    #         lsb = item.stop if item.start > item.stop else item.start
    #         msb += 1
    #     else:
    #         raise ValueError('input type Error:' + str(type(item)))
    #
    #     return bits(self.val%(2**msb)//(2**lsb))


