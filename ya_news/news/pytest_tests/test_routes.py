from http import HTTPStatus
from django.contrib.auth import get_user_model
import pytest
from pytest_lazyfixture import lazy_fixture
from yanews.settings import LOGIN_URL

User = get_user_model()

HOME_URL = lazy_fixture('home_url')
DETAIL_URL = lazy_fixture('detail_url')
EDIT_URL = lazy_fixture('edit_url')
DELETE_URL = lazy_fixture('delete_url')
LOGOUT_URL = lazy_fixture('logout_url')
SIGNUP_URL = lazy_fixture('signup_url')


@pytest.mark.parametrize(
    'url, client_fixture, expected_status',
    [
        (HOME_URL, 'client', HTTPStatus.OK),
        (DETAIL_URL, 'client', HTTPStatus.OK),
        (LOGIN_URL, 'client', HTTPStatus.OK),
        (LOGOUT_URL, 'client', HTTPStatus.OK),
        (SIGNUP_URL, 'client', HTTPStatus.OK),
        (EDIT_URL, 'not_author_client', HTTPStatus.NOT_FOUND),
        (EDIT_URL, 'author_client', HTTPStatus.OK),
        (DELETE_URL, 'not_author_client', HTTPStatus.NOT_FOUND),
        (DELETE_URL, 'author_client', HTTPStatus.OK),
    ]
)
def test_response_status_codes(url, client_fixture,
                               expected_status, request, client):
    client = request.getfixturevalue(client_fixture)
    response = client.get(url)
    assert response.status_code == expected_status


@pytest.mark.parametrize(
    'url_fixture',
    [
        EDIT_URL,
        DELETE_URL,
    ]
)
def test_redirects(client, url_fixture, request):
    url = url_fixture
    expected_url = f"{LOGIN_URL}?next={url}"
    response = client.get(url)
    assert response.status_code == HTTPStatus.FOUND
    assert response.url == expected_url
