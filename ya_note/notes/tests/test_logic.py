from http import HTTPStatus

from django.contrib.auth import get_user_model
from pytils.translit import slugify

from notes.models import Note
from notes.tests.base import (
    BaseTestCase, ADD_URL, SUCCESS_URL, EDIT_URL, DELETE_URL, LOGIN_ADD_URL
)
from notes.forms import WARNING

User = get_user_model()


class TestNoteCreation(BaseTestCase):

    def test_anonymous_user_cant_create_note(self):
        Note.objects.all().delete()
        response = self.client.post(ADD_URL, data=self.form_data)
        self.assertRedirects(response, LOGIN_ADD_URL)
        note_exists = Note.objects.exists()
        self.assertFalse(note_exists)

    def create_note_and_check(self, expected_slug=None):
        Note.objects.all().delete()
        response = self.author_client.post(ADD_URL, data=self.form_data)
        self.assertRedirects(response, SUCCESS_URL)
        note_count = Note.objects.count()
        self.assertEqual(note_count, 1)
        note = Note.objects.first()
        self.assertEqual(note.title, self.form_data['title'])
        self.assertEqual(note.text, self.form_data['text'])
        self.assertEqual(note.author, self.author)
        if expected_slug:
            self.assertEqual(note.slug, expected_slug)
        else:
            self.assertEqual(note.slug, self.form_data['slug'])

    def test_slug_auto_generation(self):
        self.form_data.pop('slug')
        expected_slug = slugify(self.form_data['title'])
        self.create_note_and_check(expected_slug=expected_slug)

    def test_user_can_create_note(self):
        self.create_note_and_check()

    def test_no_duplicate_slug(self):
        self.form_data['slug'] = self.note.slug
        notes_before = set(Note.objects.values_list('id', flat=True))
        response = self.author_client.post(
            ADD_URL, data=self.form_data)
        self.assertFormError(
            response, 'form', 'slug', self.note.slug + WARNING)
        notes_after = set(Note.objects.values_list('id', flat=True))
        self.assertSetEqual(notes_before, notes_after)

    def test_author_can_delete_note(self):
        # Получаем данные до удаления
        notes_count_before = Note.objects.count()
        response = self.author_client.delete(DELETE_URL)
        self.assertRedirects(response, SUCCESS_URL)
        note_exists = Note.objects.filter(id=self.note.id).exists()
        self.assertFalse(note_exists)
        notes_count_after = Note.objects.count()
        self.assertEqual(notes_count_after, notes_count_before - 1)

    def test_user_cant_delete_note_of_another_user(self):
        # Получаем данные до удаления
        notes_count_before = Note.objects.count()
        response = self.reader_client.delete(DELETE_URL)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        notes_count_after = Note.objects.count()
        self.assertEqual(notes_count_before, notes_count_after)
        note_exists_after = Note.objects.filter(id=self.note.id).exists()
        self.assertTrue(note_exists_after)
        note_after = Note.objects.get(id=self.note.id)
        self.assertEqual(note_after.title, self.note.title)
        self.assertEqual(note_after.text, self.note.text)
        self.assertEqual(note_after.author, self.note.author)
        self.assertEqual(note_after.slug, self.note.slug)

    def test_author_can_edit_note(self):
        response = self.author_client.post(
            EDIT_URL, data=self.form_data)
        self.assertRedirects(response, SUCCESS_URL)
        note = Note.objects.get(id=self.note.id)
        self.assertEqual(note.title, self.form_data['title'])
        self.assertEqual(note.text, self.form_data['text'])
        self.assertEqual(note.slug, self.form_data['slug'])
        self.assertEqual(note.author, self.note.author)

    def test_user_cant_edit_note_of_another_user(self):
        response = self.reader_client.post(EDIT_URL, data=self.form_data)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        note = Note.objects.get(id=self.note.id)
        self.assertEqual(note.title, self.note.title)
        self.assertEqual(note.text, self.note.text)
        self.assertEqual(note.slug, self.note.slug)
        self.assertEqual(note.author, self.note.author)
