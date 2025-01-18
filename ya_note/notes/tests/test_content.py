from django.test import TestCase
from django.urls import reverse
from notes.models import Note
from django.contrib.auth import get_user_model
from notes.forms import NoteForm
from http import HTTPStatus

User = get_user_model()


class TestNotesListPage(TestCase):
    LIST_URL = reverse('notes:list')

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Автор')
        cls.reader = User.objects.create(username='Читатель')
        cls.note_by_author = Note.objects.create(
            title='Заметка автора', text='Текст заметки', author=cls.author
        )
        cls.note_by_reader = Note.objects.create(
            title='Заметка читателя', text='Текст заметки', author=cls.reader
        )

    def test_list_page_shows_notes(self):
        self.client.force_login(self.author)
        response = self.client.get(self.LIST_URL)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIn('object_list', response.context)

    def test_notes_list_for_author(self):
        self.client.force_login(self.author)
        response = self.client.get(reverse('notes:list'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIn(self.note_by_author, response.context['object_list'])
        self.assertNotIn(self.note_by_reader, response.context['object_list'])

    def test_notes_list_for_reader(self):
        self.client.force_login(self.reader)
        response = self.client.get(reverse('notes:list'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIn(self.note_by_reader, response.context['object_list'])
        self.assertNotIn(self.note_by_author, response.context['object_list'])


class TestNoteAddEditPage(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Автор заметки')

        cls.note = Note.objects.create(
            title='Тестовая заметка',
            text='Тестовый текст.',
            author=cls.author
        )
        cls.add_url = reverse('notes:add')
        cls.edit_url = reverse('notes:edit', args=[cls.note.slug])

    def test_add_page_has_form(self):
        response_add_anonymous = self.client.get(self.add_url)
        self.assertEqual(response_add_anonymous.status_code, 302)
        self.assertRedirects(
            response_add_anonymous, f'/auth/login/?next={self.add_url}')
        self.assertIsNone(response_add_anonymous.context)

        self.client.force_login(self.author)
        response_add_authenticated = self.client.get(self.add_url)
        self.assertEqual(response_add_authenticated.status_code, 200)
        self.assertIn('form', response_add_authenticated.context)
        self.assertIsInstance(
            response_add_authenticated.context['form'], NoteForm)

    def test_edit_page_has_form(self):
        response_edit_anonymous = self.client.get(self.edit_url)
        self.assertEqual(response_edit_anonymous.status_code, 302)
        self.assertRedirects(
            response_edit_anonymous, f'/auth/login/?next={self.edit_url}')
        self.assertIsNone(response_edit_anonymous.context)

        self.client.force_login(self.author)
        response_edit_authenticated = self.client.get(self.edit_url)
        self.assertEqual(response_edit_authenticated.status_code, 200)
        self.assertIn('form', response_edit_authenticated.context)
        self.assertIsInstance(
            response_edit_authenticated.context['form'], NoteForm)
