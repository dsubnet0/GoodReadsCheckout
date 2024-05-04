import pytest
from mock import Mock

from src.library_db import LibraryDB


@pytest.fixture()
def ldb():
    ldb = LibraryDB(base_url='foo')
    yield ldb

@pytest.fixture()
def query_result():
    query_result = [
        {
            'title': 'title1',
            'availability': 'availability1',
            'call_number': 'call_number1'
        }
    ]
    yield query_result


def test_init(ldb):
    assert type(ldb) is LibraryDB
    assert ldb.base_url == 'foo'


def test_get_book_by_isbn(query_result, ldb):
    ldb._query_library_by_isbn = Mock(return_value=query_result)
    ldb._query_library_by_title = Mock(return_value=[])

    book_result_string = ldb.get_book('title1', 'isbn1', 'format1')

    ldb._query_library_by_isbn.assert_called_once_with('isbn1', 'format1')
    ldb._query_library_by_title.assert_not_called()
    assert book_result_string == '\nisbn1 (format1):\ntitle1|availability1|call_number1'


def test_get_book_by_title(query_result, ldb):
    ldb._query_library_by_isbn = Mock(return_value=[])
    ldb._query_library_by_title = Mock(return_value=query_result)

    book_result_string = ldb.get_book('title1', 'isbn1', 'format1')

    ldb._query_library_by_isbn.assert_called_once_with('isbn1', 'format1')
    ldb._query_library_by_title.assert_called_once_with('title1', 'format1')
    assert book_result_string == '\ntitle1 (format1):\ntitle1|availability1|call_number1'


def test_get_book_by_title_multiple(query_result, ldb):
    '''
    If a title search turns up multiple results, only return the first one
    '''
    query_result2 = [
        {
            'title': 'title2',
            'availability': 'availability2',
            'call_number': 'call_number2'
        }
    ]
    query_result3 = [
        {
            'title': 'title3',
            'availability': 'availability3',
            'call_number': 'call_number3'
        }
    ]
    multi_result_list = query_result + query_result2 + query_result3
    ldb._query_library_by_isbn = Mock(return_value=[])
    ldb._query_library_by_title = Mock(return_value=multi_result_list)

    book_result_string = ldb.get_book('title1', 'isbn1', 'format1')

    ldb._query_library_by_isbn.assert_called_once_with('isbn1', 'format1')
    ldb._query_library_by_title.assert_called_once_with('title1', 'format1')
    assert book_result_string == '\ntitle1 (format1):\ntitle1|availability1|call_number1'


def test_get_book_by_empty_isbn(ldb):
    '''
    If get_book() is sent an empty isbn, it should skip right to query by title
    '''
    ldb._query_library_by_isbn = Mock(return_value=[])
    ldb._query_library_by_title = Mock(return_value=[])

    book_result_string = ldb.get_book(title='title1', isbn='', format='format1')

    ldb._query_library_by_isbn.assert_not_called()
    ldb._query_library_by_title.assert_called_once_with('title1', 'format1')


def test_get_book_by_title_newline(ldb):
    '''
    If get_book() is sent a title with newlines, it should query by part of title
    prior to newline
    '''
    ldb._query_library_by_isbn = Mock(return_value=[])
    ldb._query_library_by_title = Mock(return_value=[])

    book_result_string = ldb.get_book(title='title1\ntitle2', isbn='', format='format1')

    ldb._query_library_by_isbn.assert_not_called()
    ldb._query_library_by_title.assert_called_once_with('title1', 'format1')