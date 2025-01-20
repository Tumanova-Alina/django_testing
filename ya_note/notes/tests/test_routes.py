import unittest
from http import HTTPStatus
from django.contrib.auth import get_user_model
from django.urls import reverse
from notes.tests.base import BaseTestCase
from notes.tests.constants import (
    HOME_URL, LOGIN_URL, LOGOUT_URL, SIGNUP_URL, LIST_URL,
    ADD_URL, SUCCESS_URL, DETAIL_URL, EDIT_URL, DELETE_URL
)

User = get_user_model()


# class TestRoutes(BaseTestCase):
#     def test_pages_availability(self):
#         urls = (
#             ('notes:home', None),
#             ('users:login', None),
#             ('users:logout', None),
#             ('users:signup', None)
#         )
#         for name, args in urls:
#             with self.subTest(name=name):
#                 url = reverse(name, args=args)
#                 response = self.client.get(url)
#                 self.assertEqual(response.status_code, HTTPStatus.OK)

#     def test_availability_for_note_edit_delete_and_view(self):
#         users_statuses = (
#             (self.author, HTTPStatus.OK),
#             (self.reader, HTTPStatus.NOT_FOUND),
#         )
#         for user, status in users_statuses:
#             self.client.force_login(user)
#             # Для каждой пары "пользователь - ожидаемый ответ"
#             # перебираем имена тестируемых страниц:
#             for name in ('notes:detail', 'notes:delete', 'notes:edit'):
#                 with self.subTest(user=user, name=name):
#                     url = reverse(name, args=(self.note.slug,))
#                     response = self.client.get(url)
#                     self.assertEqual(response.status_code, status)

#     def test_redirect_for_anonymous_client(self):
#         login_url = reverse('users:login')
#         urls_with_args = (
#             ('notes:list', None),
#             ('notes:add', None),
#             ('notes:success', None),
#             ('notes:detail', (self.note.slug,)),
#             ('notes:edit', (self.note.slug,)),
#             ('notes:delete', (self.note.slug,)),
#         )

#         for name, args in urls_with_args:
#             with self.subTest(name=name):
#                 url = reverse(name, args=args if args else ())
#                 redirect_url = f'{login_url}?next={url}'
#                 response = self.client.get(url)
#                 self.assertRedirects(response, redirect_url)


class TestRoutes(BaseTestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

    def test_status_codes(self):
        """Контролирует коды возврата для доступных страниц."""
        test_cases = [
            # (Пользователь, URL, Ожидаемый код возврата)
            (None, HOME_URL, HTTPStatus.OK),
            (None, LOGIN_URL, HTTPStatus.OK),
            (None, LOGOUT_URL, HTTPStatus.OK),
            (None, SIGNUP_URL, HTTPStatus.OK),
            (self.author, DETAIL_URL, HTTPStatus.OK),
            (self.reader, DETAIL_URL, HTTPStatus.NOT_FOUND),
            (self.author, EDIT_URL, HTTPStatus.OK),
            (self.reader, EDIT_URL, HTTPStatus.NOT_FOUND),
            (self.author, DELETE_URL, HTTPStatus.OK),
            (self.reader, DELETE_URL, HTTPStatus.NOT_FOUND),
        ]
        for user, url, expected_status in test_cases:
            with self.subTest(user=user, url=url):
                if user:
                    self.client.force_login(user)
                response = self.client.get(url)
                self.assertEqual(response.status_code, expected_status)

    def test_redirects_for_anonymous(self):
        """Контролирует перенаправления на страницу логина."""
        protected_urls = [
            LIST_URL, ADD_URL, SUCCESS_URL,
            DETAIL_URL, EDIT_URL, DELETE_URL
        ]
        for url in protected_urls:
            with self.subTest(url=url):
                response = self.client.get(url)
                redirect_url = f'{LOGIN_URL}?next={url}'
                self.assertRedirects(response, redirect_url)
