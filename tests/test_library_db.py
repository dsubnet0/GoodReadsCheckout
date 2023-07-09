import pytest
from mock import patch, Mock
from src.library_db import LibraryDB

def test_init():
    ldb = LibraryDB(base_url='foo')
    assert type(ldb) is LibraryDB
    assert ldb.base_url == 'foo'


def test_get_book_by_isbn():
    query_result = [
        {
            'title': 'title1',
            'availability': 'availability1',
            'call_number': 'call_number1'
        }
    ]
    ldb = LibraryDB(base_url='foo')
    ldb._query_library_by_isbn = Mock(return_value=query_result)
    ldb._query_library_by_title = Mock()
    ldb.get_book('title1', 'isbn1', 'format1')
    ldb._query_library_by_isbn.assert_called_once_with('isbn1', 'format1')
    ldb._query_library_by_title.assert_not_called()


def test_get_book_by_title():
    ldb = LibraryDB(base_url='foo')
    ldb._query_library_by_isbn = Mock(return_value=[])
    ldb._query_library_by_title = Mock(return_value=[])
    ldb.get_book('title1', 'isbn1', 'format1')
    ldb._query_library_by_isbn.assert_called_once_with('isbn1', 'format1')
    ldb._query_library_by_title.assert_called_once_with('title1', 'format1')