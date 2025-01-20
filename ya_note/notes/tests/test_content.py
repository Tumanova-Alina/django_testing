import unittest
from django.test import Client
from django.urls import reverse
from notes.models import Note
from django.contrib.auth import get_user_model
from notes.forms import NoteForm
from http import HTTPStatus
from notes.tests.base import BaseTestCase
from notes.tests.constants import LIST_URL, ADD_URL, LOGIN_URL

User = get_user_model()


class TestPages(BaseTestCase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.note_by_author = Note.objects.create(
            title='Заметка автора', text='Текст заметки', author=cls.author
        )
        cls.note_by_reader = Note.objects.create(
            title='Заметка читателя', text='Текст заметки', author=cls.reader
        )
        cls.edit_url = reverse('notes:edit', args=[cls.note.slug])

    def test_list_page_shows_notes(self):
        response = self.author_client.get(LIST_URL)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIn('object_list', response.context)
        self.assertIn(self.note_by_author, response.context['object_list'])
        self.assertContains(response, self.note_by_author.title)

    def test_notes_list_for_author(self):
        response = self.author_client.get(LIST_URL)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertNotIn(self.note_by_reader, response.context['object_list'])

    def test_pages_have_form(self):
        urls_with_expected_status = [
            (ADD_URL, HTTPStatus.FOUND),
            (self.edit_url, HTTPStatus.FOUND)
        ]

        for url, expected_status in urls_with_expected_status:
            # Тест для анонимного пользователя
            response_anonymous = self.client.get(url)
            self.assertEqual(response_anonymous.status_code, expected_status)
            self.assertRedirects(response_anonymous, f'{LOGIN_URL}?next={url}')
            self.assertIsNone(response_anonymous.context)

        # Повторяем тест для авторизованного пользователя
        for url, _ in urls_with_expected_status:
            response_authenticated = self.author_client.get(url)
            self.assertEqual(response_authenticated.status_code, HTTPStatus.OK)
            self.assertIn('form', response_authenticated.context)
            self.assertIsInstance(
                response_authenticated.context['form'], NoteForm)
