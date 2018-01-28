class ElementBase(object):
    """
        This class is the base class of all objects which compose the AST
    """
    def __init__(self, *args, **kwargs):
        super(ElementBase, self).__init__(*args, **kwargs)


class SymbolTable(dict):
    def put(self, name_symbol=None, name=None, symbol=None):
        """
            Put a new symbol into symbol table if it doesn't exist, otherwise merge it if merge method is supported
            by current object in symbol table with same name
        """
        if name_symbol and isinstance(name_symbol, tuple):
            _name, _symbl = name_symbol
        elif name and symbol:
            _name, _symbl = name, symbol
        else:
            raise ValueError('add_symbol must be called with a tuple(name,symbol) or with keywords(name=, symbol=)')
        if _name in self:
            if hasattr(self, 'merge'):
                self[_name].merge(_symbl)
            else:
                raise AttributeError('Duplicated token name(%) encountered' % _name)
        else:
            self[_name] = _symbl
        return _symbl


class VlogSyntaxError(Exception):
    def __init__(self, m):
        self.m = m

    def __str__(self):
        return self.m