from http import HTTPStatus

from django.contrib.auth import get_user_model

from notes.tests.base import (
    BaseTestCase, LIST_URL, ADD_URL, SUCCESS_URL,
    EDIT_URL, DELETE_URL, DETAIL_URL,
    LOGOUT_URL, LOGIN_URL, HOME_URL,
    LOGIN_ADD_URL, LOGIN_LIST_URL, SIGNUP_URL,
    LOGIN_SUCCESS_URL, LOGIN_DETAIL_URL,
    LOGIN_EDIT_URL, LOGIN_DELETE_URL
)


User = get_user_model()


class TestRoutes(BaseTestCase):

    def test_status_codes(self):
        """Контролирует коды возврата для доступных страниц."""
        test_cases = [
            # (Пользователь, URL, Ожидаемый код возврата)
            (self.client, HOME_URL, HTTPStatus.OK),
            (self.client, LOGIN_URL, HTTPStatus.OK),
            (self.client, LOGOUT_URL, HTTPStatus.OK),
            (self.client, SIGNUP_URL, HTTPStatus.OK),
            (self.client, LIST_URL, HTTPStatus.FOUND),
            (self.client, ADD_URL, HTTPStatus.FOUND),
            (self.client, SUCCESS_URL, HTTPStatus.FOUND),
            (self.client, DETAIL_URL, HTTPStatus.FOUND),
            (self.client, EDIT_URL, HTTPStatus.FOUND),
            (self.client, DELETE_URL, HTTPStatus.FOUND),
            (self.author_client, DETAIL_URL, HTTPStatus.OK),
            (self.reader_client, DETAIL_URL, HTTPStatus.NOT_FOUND),
            (self.author_client, EDIT_URL, HTTPStatus.OK),
            (self.reader_client, EDIT_URL, HTTPStatus.NOT_FOUND),
            (self.author_client, DELETE_URL, HTTPStatus.OK),
            (self.reader_client, DELETE_URL, HTTPStatus.NOT_FOUND),
        ]
        for client, url, expected_status in test_cases:
            with self.subTest(client=client, url=url):
                response = client.get(url)
                self.assertEqual(response.status_code, expected_status)

    def test_redirects_for_anonymous(self):
        """Контролирует перенаправления на страницу логина."""
        protected_urls = [
            (LIST_URL, LOGIN_LIST_URL),
            (ADD_URL, LOGIN_ADD_URL),
            (SUCCESS_URL, LOGIN_SUCCESS_URL),
            (DETAIL_URL, LOGIN_DETAIL_URL),
            (EDIT_URL, LOGIN_EDIT_URL),
            (DELETE_URL, LOGIN_DELETE_URL),
        ]
        for url, expected_redirect in protected_urls:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertRedirects(response, expected_redirect)
