import kydb


def test_uniondb():
    db = kydb.connect('memory://db1;memory://db2')
    assert repr(db) == '<UnionDB memory://db1;memory://db2>'
