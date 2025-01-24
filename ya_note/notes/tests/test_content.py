from http import HTTPStatus

from django.contrib.auth import get_user_model

from notes.forms import NoteForm
from notes.tests.base import BaseTestCase, ADD_URL, EDIT_URL, LIST_URL

User = get_user_model()


class TestPages(BaseTestCase):

    def test_list_page_shows_notes(self):
        response = self.author_client.get(LIST_URL)
        self.assertIn('object_list', response.context)
        self.assertIn(self.note_by_author, response.context['object_list'])
        note_in_context = response.context['object_list'].get(
            pk=self.note_by_author.pk)
        self.assertEqual(self.note_by_author.title, note_in_context.title)
        self.assertEqual(self.note_by_author.text, note_in_context.text)
        self.assertEqual(self.note_by_author.author, note_in_context.author)
        self.assertEqual(self.note_by_author.slug, note_in_context.slug)

    def test_notes_list_for_author(self):
        response = self.author_client.get(LIST_URL)
        self.assertNotIn(self.note_by_reader, response.context['object_list'])

    def test_authenticated_user_has_form(self):
        urls = [ADD_URL, EDIT_URL]

        for url in urls:
            with self.subTest(url=url):
                response = self.author_client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)
                self.assertIn('form', response.context)
                self.assertIsInstance(response.context['form'], NoteForm)
