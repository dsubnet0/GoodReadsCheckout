import pytest
from mock import MagicMock, patch

from src.rakuten_querier import RakutenQuerier


@pytest.fixture()
def rq():
    rq = RakutenQuerier('foo', 0)
    yield rq


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
