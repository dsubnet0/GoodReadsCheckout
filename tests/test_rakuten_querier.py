import pytest
from mock import MagicMock, patch

from src.rakuten_querier import RakutenQuerier


@pytest.fixture()
def rq():
    rq = RakutenQuerier('foo', 0)
    yield rq

@pytest.fixture()
def query_result():
    query_result = [
        {
            'title': 'title1',
            'url': 'url1'
        }
    ]
    yield query_result

def test_init(rq):
    assert type(rq) is RakutenQuerier
    assert rq.base_url == 'foo'
    assert rq.application_id == 0


@patch('src.rakuten_querier.requests')
def test_query_by_isbn13(mock_requests, rq):
    # Arrange
    test_result = {'test':'result'}
    mock_get = MagicMock()
    mock_get.json.return_value = test_result
    mock_requests.get.return_value = mock_get

    # Act
    result = rq.query_by_isbn13(0)

    # Assert
    mock_requests.get.assert_called_once_with('foo?applicationId=0&itemNumber=0')
    assert result == {'test':'result'}


@patch('src.rakuten_querier.requests')
def test_query_by_title(mock_requests, rq):
    # Arrange
    test_result = {'test':'result'}
    mock_get = MagicMock()
    mock_get.json.return_value = test_result
    mock_requests.get.return_value = mock_get

    # Act
    result = rq.query_by_title('bar baz')

    # Assert
    mock_requests.get.assert_called_once_with('foo?applicationId=0&title=bar%20baz')
    assert result == {'test':'result'}


def test_get_book_by_isbn(rq, query_result):
    # rq = RakutenQuerier('base_url', 'app_id')
    rq.query_by_isbn13 = MagicMock(return_value=query_result)
    rq.query_by_title = MagicMock(return_value=[])
    rq.get_book('title1', 'isbn1')
    rq.query_by_isbn13.assert_called_once_with('isbn1')
    rq.query_by_title.assert_not_called()


def test_get_book_by_title():
    rq = RakutenQuerier('base_url', 'app_id')
    rq.query_by_isbn13 = MagicMock(return_value=[])
    rq.query_by_title = MagicMock(return_value=[])
    rq.get_book('title1', 'isbn1')
    rq.query_by_isbn13.assert_called_once_with('isbn1')
    rq.query_by_title.assert_called_once_with('title1')


def test_format_results(rq):
    # Arrange
    test_query_result = {
        'Items':
            [
                {
                    'Item': {
                        'title': 'title1',
                        'itemUrl': 'url1'
                    }
                }
            ]
        }

    # Act
    formatted_results = rq.format_results(test_query_result)

    # Assert
    assert formatted_results == ['title1 - url1']
