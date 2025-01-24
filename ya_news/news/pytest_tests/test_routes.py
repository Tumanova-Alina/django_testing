from http import HTTPStatus

import pytest
from pytest_lazyfixture import lazy_fixture
from django.contrib.auth import get_user_model

from yanews.settings import LOGIN_URL

User = get_user_model()

HOME_URL = lazy_fixture('home_url')
DETAIL_URL = lazy_fixture('detail_url')
EDIT_URL = lazy_fixture('edit_url')
DELETE_URL = lazy_fixture('delete_url')
LOGOUT_URL = lazy_fixture('logout_url')
SIGNUP_URL = lazy_fixture('signup_url')
LOGIN_EDIT_URL = lazy_fixture('login_edit_url')
LOGIN_DELETE_URL = lazy_fixture('login_delete_url')
CLIENT = lazy_fixture('client')
AUTHOR_CLIENT = lazy_fixture('author_client')
NOT_AUTHOR_CLIENT = lazy_fixture('not_author_client')


@pytest.mark.parametrize(
    'url, parametrized_client, expected_status',
    [
        (HOME_URL, CLIENT, HTTPStatus.OK),
        (DETAIL_URL, CLIENT, HTTPStatus.OK),
        (LOGIN_URL, CLIENT, HTTPStatus.OK),
        (LOGOUT_URL, CLIENT, HTTPStatus.OK),
        (SIGNUP_URL, CLIENT, HTTPStatus.OK),
        (EDIT_URL, NOT_AUTHOR_CLIENT, HTTPStatus.NOT_FOUND),
        (EDIT_URL, AUTHOR_CLIENT, HTTPStatus.OK),
        (EDIT_URL, CLIENT, HTTPStatus.FOUND),
        (DELETE_URL, NOT_AUTHOR_CLIENT, HTTPStatus.NOT_FOUND),
        (DELETE_URL, AUTHOR_CLIENT, HTTPStatus.OK),
        (DELETE_URL, CLIENT, HTTPStatus.FOUND),
    ]
)
def test_response_status_codes(url, parametrized_client,
                               expected_status):
    response = parametrized_client.get(url)
    assert response.status_code == expected_status


@pytest.mark.parametrize(
    'url, expected_url',
    [
        (EDIT_URL, LOGIN_EDIT_URL),
        (DELETE_URL, LOGIN_DELETE_URL)
    ]
)
def test_redirects(client, url, expected_url):
    response = client.get(url)
    assert response.url == expected_url
