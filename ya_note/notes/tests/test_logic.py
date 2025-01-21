from http import HTTPStatus

from django.contrib.auth import get_user_model
from pytils.translit import slugify

from notes.models import Note
from notes.tests.base import BaseTestCase
from notes.tests.constants import (
    LOGIN_URL, ADD_URL, SUCCESS_URL, EDIT_URL, DELETE_URL)
from notes.forms import WARNING

User = get_user_model()


class TestNoteCreation(BaseTestCase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

    def test_anonymous_user_cant_create_note(self):
        response = self.client.post(ADD_URL, data=self.form_data)
        self.assertRedirects(response, f'{LOGIN_URL}?next={ADD_URL}')
        notes_count = Note.objects.filter(
            title=self.form_data['title']).count()
        self.assertEqual(notes_count, 0)

    def test_user_can_create_note(self):
        response = self.auth_client.post(ADD_URL, data=self.form_data)
        self.assertRedirects(response, SUCCESS_URL)
        notes_count = Note.objects.filter(
            title=self.form_data['title'], text=self.form_data['text']).count()
        self.assertEqual(notes_count, 1)
        note = Note.objects.get(title=self.form_data['title'])
        self.assertEqual(note.text, self.form_data['text'])
        self.assertEqual(note.author, self.author)
        self.assertIsNotNone(
            note.slug, "Slug should be automatically generated.")

    def test_no_duplicate_slug(self):
        form_data_with_duplicate_slug = self.form_data.copy()
        form_data_with_duplicate_slug['slug'] = self.note.slug
        response = self.auth_client.post(
            ADD_URL, data=form_data_with_duplicate_slug)
        self.assertFormError(
            response, 'form', 'slug', self.note.slug + WARNING)

    def test_slug_auto_generation(self):
        response = self.auth_client.post(ADD_URL, data=self.form_data)
        self.assertRedirects(response, SUCCESS_URL)
        note = Note.objects.get(title=self.form_data['title'])
        expected_slug = slugify(self.form_data['title'])
        self.assertEqual(note.slug, expected_slug)
        self.assertEqual(note.title, self.form_data['title'])
        self.assertEqual(note.text, self.form_data['text'])
        self.assertEqual(note.author, self.author)

    def test_author_can_delete_note(self):
        # Получаем данные до удаления
        note_before = Note.objects.get(id=self.note.id)
        response = self.author_client.delete(DELETE_URL)
        self.assertRedirects(response, SUCCESS_URL)
        notes_after = list(Note.objects.values_list('id', flat=True))
        self.assertNotIn(self.note.id, notes_after)
        # Проверяем, что поля удаляемой записи не исказились
        self.assertEqual(note_before.title, self.note.title)
        self.assertEqual(note_before.text, self.note.text)
        self.assertEqual(note_before.author, self.author)

    def test_user_cant_delete_note_of_another_user(self):
        # Получаем данные до удаления
        note_before = Note.objects.get(id=self.note.id)
        response = self.reader_client.delete(DELETE_URL)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        note_after = Note.objects.get(id=self.note.id)
        self.assertEqual(note_after.id, note_before.id)
        # Проверяем, что поля удаленной записи не исказились
        self.assertEqual(note_after.title, note_before.title)
        self.assertEqual(note_after.text, note_before.text)
        self.assertEqual(note_after.author, note_before.author)

    def test_author_can_edit_note(self):
        response = self.author_client.post(
            EDIT_URL, data=self.new_form_data)
        self.assertRedirects(response, SUCCESS_URL)
        note = Note.objects.get(id=self.note.id)
        self.assertEqual(note.title, self.new_form_data['title'])
        self.assertEqual(note.text, self.new_form_data['text'])
        self.assertEqual(note.slug, self.new_form_data['slug'])
        self.assertEqual(note.author, self.author)

    def test_user_cant_edit_note_of_another_user(self):
        original_note = Note.objects.get(id=self.note.id)
        response = self.reader_client.post(EDIT_URL, data=self.form_data)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        note = Note.objects.get(id=self.note.id)
        self.assertEqual(note.title, original_note.title)
        self.assertEqual(note.text, original_note.text)
        self.assertEqual(note.slug, original_note.slug)
        self.assertEqual(note.author, original_note.author)
