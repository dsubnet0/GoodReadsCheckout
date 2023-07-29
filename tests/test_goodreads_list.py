from src.goodreads_list import GoodReadsList


def test_init():
    grl = GoodReadsList(user_string='foo')
    assert type(grl) is GoodReadsList
    assert grl.user_string == 'foo'


def test_get_url_nopage():
    grl = GoodReadsList(user_string='foo')
    assert grl.get_url() == 'https://www.goodreads.com/' \
        'review/list/foo?ref=nav_mybooks&shelf=to-read&per_page=50'


def test_get_url_page():
    grl = GoodReadsList(user_string='foo')
    assert grl.get_url(page_number=42) == 'https://www.goodreads.com/' \
        'review/list/foo?page=42&ref=nav_mybooks&shelf=to-read&per_page=50'
