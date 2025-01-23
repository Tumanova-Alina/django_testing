from http import HTTPStatus

from django.contrib.auth import get_user_model

from notes.tests.base import BaseTestCase


User = get_user_model()


class TestRoutes(BaseTestCase):

    def test_status_codes(self):
        """Контролирует коды возврата для доступных страниц."""
        test_cases = [
            # (Пользователь, URL, Ожидаемый код возврата)
            (self.client, self.HOME_URL, HTTPStatus.OK),
            (self.client, self.LOGIN_URL, HTTPStatus.OK),
            (self.client, self.LOGOUT_URL, HTTPStatus.OK),
            (self.client, self.SIGNUP_URL, HTTPStatus.OK),
            (self.client, self.LIST_URL, HTTPStatus.FOUND),
            (self.client, self.ADD_URL, HTTPStatus.FOUND),
            (self.client, self.SUCCESS_URL, HTTPStatus.FOUND),
            (self.client, self.DETAIL_URL, HTTPStatus.FOUND),
            (self.client, self.EDIT_URL, HTTPStatus.FOUND),
            (self.client, self.DELETE_URL, HTTPStatus.FOUND),
            (self.author_client, self.DETAIL_URL, HTTPStatus.OK),
            (self.reader_client, self.DETAIL_URL, HTTPStatus.NOT_FOUND),
            (self.author_client, self.EDIT_URL, HTTPStatus.OK),
            (self.reader_client, self.EDIT_URL, HTTPStatus.NOT_FOUND),
            (self.author_client, self.DELETE_URL, HTTPStatus.OK),
            (self.reader_client, self.DELETE_URL, HTTPStatus.NOT_FOUND),
        ]
        for client, url, expected_status in test_cases:
            with self.subTest(client=client, url=url):
                response = client.get(url)
                self.assertEqual(response.status_code, expected_status)

    def test_redirects_for_anonymous(self):
        """Контролирует перенаправления на страницу логина."""
        protected_urls = [
            (self.LIST_URL, self.IF_LOGIN_LIST_URL),
            (self.ADD_URL, self.IF_LOGIN_ADD_URL),
            (self.SUCCESS_URL, self.IF_LOGIN_SUCCESS_URL),
            (self.DETAIL_URL, self.IF_LOGIN_DETAIL_URL),
            (self.EDIT_URL, self.IF_LOGIN_EDIT_URL),
            (self.DELETE_URL, self.IF_LOGIN_DELETE_URL),
        ]
        for url, expected_redirect in protected_urls:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertRedirects(response, expected_redirect)
