
#
#   YaLafi module for LaTeX package geometry
#

from yalafi import defs
from yalafi.defs import Macro, InitModule

require_packages = []

#
#   Please note:
#   - For all undeclared maths macros, which are not blacklisted in
#     Parameters.math_ignore (yalafi/parameters.py), we assume that
#     a part of a mathematical term or an operator is left.
#   - The spacing macros and \notag are imporant for correct parsing
#     of maths material.
#
def init_module(parser, options):
    parms = parser.parms

    macros_latex = ""

    macros_python = [

        Macro(parms, '\\xspace', args='OA', repl=h_xspace),

    ]

    environments = []

    return InitModule(macros_latex=macros_latex, macros_python=macros_python,
                        environments=environments)


xspace_excl = ['.', ',', "'", '/', '?', ';', ':', '!', '~', '-', ')', '$', '\\footnote']


def h_xspace(parser, buf, mac, args, pos):
    if len(args) >= 1:
        arg = args[1]
        if hasattr(arg[0], 'txt'):
            if not arg[0].txt in xspace_excl:
                arg.insert(0, defs.SpecialToken(pos+1, '\\;'))
    return arg
