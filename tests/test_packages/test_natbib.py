

import pytest
from yalafi import parameters, parser, utils

preamble = '\\usepackage{natbib}\n'

def get_plain(latex):
    parms = parameters.Parameters()
    p = parser.Parser(parms)
    plain, nums = utils.get_txt_pos(p.parse(preamble + latex))
    assert len(plain) == len(nums)
    return plain


data_test_macros_python = [

    (r'A\bibliography{xxx}B', 'AB'),
    (r'A\bibliographystyle{xxx}B', 'AB'),
    (r'A\cite[p. 15]{x}B', 'A[0, p. 15]B'),
    (r'A\cite[][p. 15]{x}B', 'A[0, p. 15]B'),
    (r'A\cite[]{x}B', 'A[0]B'),
    (r'A\cite[][]{x}B', 'A[0]B'),
    (r'A\cite[ ]{x}B', 'A[0,  ]B'),
    (r'A\cite[ ][ ]{x}B', 'A[  0,  ]B'),
    (r'A\cite[See][]{x}B', 'A[See 0]B'),
    (r'A\cite[See][p. 15]{x}B', 'A[See 0, p. 15]B'),
    (r'A\citep{x}B', 'A[0]B'),
    (r'A\citet{x}B', 'Asome workB'),
    (r'A \citet{x} B', 'A some work B'),

]

@pytest.mark.parametrize('latex,plain_expected', data_test_macros_python)
def test_macros_python(latex, plain_expected):
    plain = get_plain(latex)
    assert plain == plain_expected

