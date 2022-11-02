# JG copied and adapted from biblatex file
# for description of citep citet see e.g. http://merkel.texture.rocks/Latex/natbib.php
#
#   YaLafi module for LaTeX package biblatex
#
#   very simple approximation
#   - citation text is fixed --> variable cite_text
#   - we always add [] brackets (even for \cite and \footcite)
#

from yalafi import defs
from yalafi.defs import Macro, InitModule
from yalafi.packages import biblatex

require_packages = []

cite_text = '0'
cite_work = 'some work'

def init_module(parser, options, position):
    parms = parser.parms

    macros_latex = ''

    macros_python = [

        Macro(parms, '\\bibliography', args='OA', repl=''),
        Macro(parms, '\\bibliographystyle', args='OA', repl=''),
        Macro(parms, '\\cite', args='*OOA', repl=h_cite),
        Macro(parms, '\\citep', args='*OOA', repl=h_cite),
        Macro(parms, '\\citet', args='*OOA', repl=cite_work),

    ]

    environments = []

    return InitModule(macros_latex=macros_latex, macros_python=macros_python,
                        environments=environments)


def h_cite(parser, buf, mac, args, delim, pos):
    opt1 = args[1]
    opt2 = args[2]
    if len(opt1) == 1 and type(opt1[0]) is defs.VoidToken:
        # only [] given
        opt1 = []
    if opt2:
        pre = opt1
        if len(opt2) == 1 and type(opt2[0]) is defs.VoidToken:
            # only [] given
            opt2 = []
        post = opt2
    else:
        pre = []
        post = opt1
        
    out = [defs.TextToken(pos, '[', pos_fix=True)]
    if pre:
        out += pre
        out.append(defs.SpaceToken(out[-1].pos, ' ', pos_fix=True))
    out.append(defs.TextToken(out[-1].pos, cite_text, pos_fix=True))
    if post:
        out += [defs.TextToken(out[-1].pos, ',', pos_fix=True),
                    defs.SpaceToken(out[-1].pos, ' ', pos_fix=True)]
        out += post
    out += [defs.TextToken(out[-1].pos, ']', pos_fix=True),
                defs.ActionToken(out[-1].pos)]
    return out

def h_footcite(parser, buf, mac, args, delim, pos):
    out = [defs.MacroToken(pos, '\\footnote'),
                defs.SpecialToken(pos, '{')]
    out += h_cite(parser, buf, mac, args, delim, pos)
    out += [defs.TextToken(out[-1].pos, '.', pos_fix=True),
                    defs.SpecialToken(out[-1].pos, '}'),
                    defs.ActionToken(out[-1].pos)]
    return out

