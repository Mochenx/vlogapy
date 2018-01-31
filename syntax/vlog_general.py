#encoding = utf-8

try:
    from pyparsing import (alphas, alphanums, Regex, nums, Combine, Optional, Word, Suppress, oneOf, ZeroOrMore, Keyword)
except ImportError:
    from vlogapy.pyparsing import (alphas, alphanums, Regex, nums, Combine, Optional, Word, Suppress, oneOf, ZeroOrMore, Keyword)


__author__ = 'mochen'
__all__ = ['identifier', 'sysfunc_identifier', 'number', 'net_type', 'trireg', 'str_list_net_type',
           'LPARENTH', 'RPARENTH', 'LBRACKET', 'RBRACKET', 'LBRACE', 'RBRACE', 'SEMI', 'POINT', 'COLON',
           'COMMA', 'SHARP', 'AT_SYMBOL',
           ]


class _BaseTokens(object):
    # Identifier related variables
    id_1st = alphas+'_'
    id_sysfunc_1st = alphas+'$_'
    id_body = alphanums+'$_'
    identifier1 = Regex(r'['+id_1st+']['+id_body+']*')  #.setName('BaseID')
    identifier2 = Regex(r'\\\S+').setParseAction(lambda t: t[0])  #.setName('EscapedID')

    # Number related variables
    hexnums = nums + 'abcdefABCDEF' + '_?'
    base = Regex("'[bBoOdDhH]")  #.setName('base')
    # Based number is a number like : 12'hA_12, or 'hA12
    basedNumber = Combine(Optional(Word(nums + '_')) + base + Word(hexnums+'xXzZ'),
                          joinString=' ', adjacent=False)  #.setName('BasedNumber')

(LPARENTH, RPARENTH, LBRACKET, RBRACKET, LBRACE, RBRACE, SEMI, POINT, COLON,
 COMMA, SHARP, AT_SYMBOL) = map(Suppress, "()[]{};.:,#@")
# BNF
# number ::= decimal_number
#           | octal_number
#           | binary_number
#           | hex_number
#           | real_number
# And my codes
# number = octal_number/binary_number/hex_number
#         | decimal_number/real_number
number = (_BaseTokens.basedNumber |
          Regex(r'\b[+-]?[0-9_]+(\.[0-9_]*)?([Ee][+-]?[0-9_]+)?\b'))  # .setName('DecOrReal')

identifier = _BaseTokens.identifier1 | _BaseTokens.identifier2
sysfunc_identifier = Regex(r'\$['+_BaseTokens.id_sysfunc_1st+']['+_BaseTokens.id_body+']*')


str_list_net_type = ['wire', 'tri', 'tri1', 'supply0', 'wand', 'triand', 'tri0', 'supply1', 'wor', 'trior']
for i, t in enumerate(str_list_net_type):
    if i == 0:
        net_type = Keyword(t)
    else:
        net_type |= Keyword(t)
# net_type = oneOf(' '.join(str_list_net_type))
trireg = Keyword('trireg')

