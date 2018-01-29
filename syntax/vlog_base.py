#encoding = utf-8

__all__ = ['VlogBase', 'syntax_root', 'syntax_tree']


__author__ = 'mochen'


class VlogBase(object):
    """
        This class is the base class of all syntax parsers
    """
    all_syntax_builders = {}

    def __init__(self):
        self._syntax_done = False
        self.build_syntax()

    def build_syntax(self):
        """
        """
        syntax_builders = VlogBase.all_syntax_builders.get(repr(self))
        if syntax_builders is None:
            return
        for _i, method_name in sorted(syntax_builders.items(), reverse=True):
            build_method = getattr(self, method_name)
            build_method()
        self._syntax_done = True

    def parse(self, code_str):
        return self.top.parseString(code_str)


def _syntax_tree(cls_name, priority, set_attr=None):
    def _decorator(func):
        syntax_builders = VlogBase.all_syntax_builders.setdefault(cls_name, {})
        if not isinstance(priority, int):
            raise TypeError('The type of second argument of syntax_root must be integer')
        elif priority in syntax_builders:
            raise KeyError('Priority:%0d exists in %s' % (priority, cls_name))
        syntax_builders[priority] = func.__name__

        def wrapper(inst):
            _ret_val = func(inst)
            if set_attr and _ret_val:
                if not isinstance(set_attr, str):
                    raise TypeError('The set_attr argument should be a string')
                setattr(inst, set_attr, _ret_val)
        return wrapper
    return _decorator


def syntax_root(cls_name):
    return _syntax_tree(cls_name, 0, set_attr='top')


def syntax_tree(cls_name, priority, with_name=None):
    if not isinstance(priority, int):
        raise TypeError('The type of second argument of syntax_root must be integer')
    elif priority <= 0:
        raise ValueError('The priority must be larger then 0 for a syntax_tree')

    return _syntax_tree(cls_name, priority, set_attr=with_name)


