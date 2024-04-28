import pytest
from mock import Mock, MagicMock, patch

from src.goodreads_list import GoodReadsList


def _mock_response(
        status=200,
        content='CONTENT',
        json_data={'content': 'CONTENT'},
        raise_for_status=None):
    """
    Source:
    https://gist.github.com/sahilsk/8ff32c378c13312e797ec2a7130767da
    """
    mock_resp = Mock()
    # mock raise_for_status call w/optional error
    mock_resp.raise_for_status = Mock()
    if raise_for_status:
        mock_resp.raise_for_status.side_effect = raise_for_status
    # set status code and content
    mock_resp.status_code = status
    mock_resp.content = content
    # add json data if provided
    if json_data:
        mock_resp.json = Mock(
            return_value=json_data
        )
    return mock_resp


@pytest.fixture()
def grl():
    grl = GoodReadsList(user_string='foo', verbose=True)
    yield grl


def test_init(grl: GoodReadsList):
    assert type(grl) is GoodReadsList
    assert grl.user_string == 'foo'


def test_get_url_nopage(grl: GoodReadsList):
    assert grl.get_url() == 'https://www.goodreads.com/' \
        'review/list/foo?ref=nav_mybooks&shelf=to-read&per_page=50'


def test_get_url_page(grl: GoodReadsList):
    assert grl.get_url(page_number=42) == 'https://www.goodreads.com/' \
        'review/list/foo?page=42&ref=nav_mybooks&shelf=to-read&per_page=50'


def test_headers_containers_useragent(grl: GoodReadsList):
    assert 'User-Agent' in grl.get_headers().keys()
    assert grl.get_headers()['User-Agent']


@patch('src.goodreads_list.requests')
def test_toread_list_get_exception(mock_requests, grl: GoodReadsList):
    mock_requests.get.side_effect = Exception("exception in requests.get")

    with pytest.raises(Exception):
        l = grl.toread_list


@patch('src.goodreads_list.requests')
@patch('src.goodreads_list.GoodReadsList._parse_fields_from_results')
def test_toread_list_called_with_headers(mock_parse, mock_requests, grl):
    mock_requests.get.return_value = 'TEST'
    mock_parse.return_value = []

    l = grl.toread_list

    mock_requests.get.assert_called_once_with(
        grl.get_url(page_number=1),
        headers=grl.get_headers()
    )
