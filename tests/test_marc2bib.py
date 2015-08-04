import pytest

from pymarc import MARCReader

from marc2bib import convert


@pytest.fixture(scope='function')
def hargittai_reader(request):
    reader = MARCReader(open('tests/hargittai2009.mrc', 'rb'),
                        to_unicode=True, force_utf8=True)
    def fin():
        reader.close()
    request.addfinalizer(fin)
    return reader

def test_general_tagfuncs(hargittai_reader):
    mock = ("@book{Hargittai2009,\n"
            " author = {I. Hargittai, M. Hargittai},\n"
            " edition = {3rd ed.},\n"
            " title = {Symmetry through the eyes of a chemist},\n"
            " year = {2009}\n"
            "}\n\n")

    rec = next(hargittai_reader)
    assert convert(rec, 'book') == mock

def test_custom_tagfuncs(hargittai_reader):
    mock = ("@book{Hargittai2009,\n"
            " author = {I. Hargittai, M. Hargittai},\n"
            " edition = {3rd ed.},\n"
            " title = {Meow.},\n" # Rawr!
            " year = {2009}\n"
            "}\n\n")

    rec = next(hargittai_reader)
    custom_tagfuncs = dict(title=lambda _: 'Meow.')
    assert convert(rec, 'book', tagfuncs=custom_tagfuncs) == mock

def test_extend_tagfuncs(hargittai_reader):
    mock = ("@book{Hargittai2009,\n"
            " author = {I. Hargittai, M. Hargittai},\n"
            " edition = {3rd ed.},\n"
            " title = {Symmetry through the eyes of a chemist},\n"
            # Meet url, a new entry tag.
            " url = {http://dx.doi.org/10.1007/978-1-4020-5628-4},\n"
            " year = {2009}\n"
            "}\n\n")

    rec = next(hargittai_reader)
    new_tagfuncs = dict(url=lambda x: x['856']['u'])
    assert convert(rec, 'book', tagfuncs=new_tagfuncs) == mock

def test_new_bibkey(hargittai_reader):
    mock = ("@book{Hargittai2009Symmetry,\n"
            " author = {I. Hargittai, M. Hargittai},\n"
            " edition = {3rd ed.},\n"
            " title = {Symmetry through the eyes of a chemist},\n"
            " year = {2009}\n"
            "}\n\n")

    rec = next(hargittai_reader)
    assert convert(rec, 'book', bibkey='Hargittai2009Symmetry') == mock
