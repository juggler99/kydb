import kydb
from datetime import datetime
import pytest


@pytest.fixture
def db():
    return kydb.connect('memory://unittest')


@pytest.fixture
def list_dir_db():
    db = kydb.connect('memory://unittest')
    db['/root'] = 'root'
    db['/folder1/foo'] = 1
    db['/folder1/bar'] = 2
    db['/folder1/folder2/baz'] = 3
    return db


def test_memory(db):
    key = '/unittests/foo'
    db[key] = 123
    assert db[key] == 123
    db[key] = 456
    assert db[key] == 456
    assert db.read(key, reload=True) == 456
    db.delete(key)
    assert not db.exists(key)


def test_memory_errors(db):
    with pytest.raises(KeyError):
        db['does_not_exist']

    with pytest.raises(KeyError):
        db.delete('does_not_exist')


def test_memory_dict(db):
    key = '/unittests/bar'
    val = {
        'my_int': 123,
        'my_float': 123.456,
        'my_str': 'hello',
        'my_list': [1, 2, 3],
        'my_datetime': datetime.now()
    }
    db[key] = val
    assert db[key] == val
    assert db.read(key, reload=True) == val


def test_memory_with_basepath():
    db = kydb.connect('memory://unittest/my/base/path')
    key = '/apple'
    db[key] = 123
    assert db[key] == 123
    assert db.read(key, reload=True) == 123


def test_list_obj(list_dir_db):
    db = list_dir_db

    def test_list_dir(path, expected):
        assert list(iter(db.list_obj(path))) == expected

    test_list_dir('/', ['root'])
    test_list_dir('', ['root'])
    test_list_dir('/folder1/', ['foo', 'bar'])
    test_list_dir('/folder1', ['foo', 'bar'])


def test_list_subdir(list_dir_db):
    db = list_dir_db

    def test_list_dir(path, expected):
        assert list(iter(db.list_subdir(path))) == expected

    test_list_dir('/', ['folder1'])
    test_list_dir('', ['folder1'])
    test_list_dir('/folder1/', ['folder2'])
    test_list_dir('/folder1', ['folder2'])
    test_list_dir('/folder1/folder2', [])
    test_list_dir('/folder1/folder2/', [])
