from http import HTTPStatus

from django.contrib.auth import get_user_model
from pytils.translit import slugify

from notes.models import Note
from notes.tests.base import BaseTestCase
from notes.forms import WARNING

User = get_user_model()


class TestNoteCreation(BaseTestCase):

    def test_anonymous_user_cant_create_note(self):
        Note.objects.all().delete()
        response = self.client.post(self.ADD_URL, data=self.form_data)
        self.assertRedirects(response, self.IF_LOGIN_ADD_URL)
        note_exists = Note.objects.exists()
        self.assertFalse(
            note_exists,
            "Заметка должна быть создана зарегистрированным пользователем."
        )

    def test_user_can_create_note(self):
        Note.objects.all().delete()
        response = self.auth_client.post(self.ADD_URL, data=self.form_data)
        self.assertRedirects(response, self.SUCCESS_URL)
        note_count = Note.objects.count()
        self.assertEqual(note_count, 1,
                         "Должна быть создана только одна заметка.")
        note = Note.objects.first()
        expected_slug = slugify(self.form_data['title'])
        self.assertEqual(note.slug, expected_slug)
        self.assertEqual(note.title, self.form_data['title'])
        self.assertEqual(note.text, self.form_data['text'])
        self.assertEqual(note.author, self.author)

    def test_no_duplicate_slug(self):
        self.form_data['slug'] = self.note.slug
        response = self.auth_client.post(
            self.ADD_URL, data=self.form_data)
        self.assertFormError(
            response, 'form', 'slug', self.note.slug + WARNING)
        notes_with_duplicate_slug = Note.objects.filter(
            slug=self.note.slug).count()
        self.assertEqual(
            notes_with_duplicate_slug, 1,
            "Не должно быть создано больше одной заметки с одинаковым slug."
        )

    def test_slug_auto_generation(self):
        Note.objects.all().delete()
        self.form_data.pop('slug', None)
        response = self.auth_client.post(self.ADD_URL, data=self.form_data)
        self.assertRedirects(response, self.SUCCESS_URL)
        note = Note.objects.first()
        expected_slug = slugify(self.form_data['title'])
        self.assertEqual(note.slug, expected_slug)
        self.assertEqual(note.title, self.form_data['title'])
        self.assertEqual(note.text, self.form_data['text'])
        self.assertEqual(note.author, self.author)

    def test_author_can_delete_note(self):
        # Получаем данные до удаления
        response = self.author_client.delete(self.DELETE_URL)
        self.assertRedirects(response, self.SUCCESS_URL)
        note_exists = Note.objects.filter(id=self.note.id).exists()
        self.assertFalse(note_exists, "Заметка должна быть удалена автором.")

    def test_user_cant_delete_note_of_another_user(self):
        # Получаем данные до удаления
        response = self.reader_client.delete(self.DELETE_URL)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        note_exists_after = Note.objects.filter(id=self.note.id).exists()
        self.assertTrue(note_exists_after,
                        "Заметка другого автора не должна быть удалена!")
        note_after = Note.objects.get(id=self.note.id)
        self.assertEqual(note_after.title, self.note.title)
        self.assertEqual(note_after.text, self.note.text)
        self.assertEqual(note_after.author, self.note.author)
        self.assertEqual(note_after.slug, self.note.slug)

    def test_author_can_edit_note(self):
        response = self.author_client.post(
            self.EDIT_URL, data=self.form_data)
        self.assertRedirects(response, self.SUCCESS_URL)
        note = Note.objects.get(id=self.note.id)
        expected_slug = slugify(self.form_data['title'])
        self.assertEqual(note.title, self.form_data['title'])
        self.assertEqual(note.text, self.form_data['text'])
        self.assertEqual(note.slug, expected_slug)
        self.assertEqual(note.author, self.note.author)

    def test_user_cant_edit_note_of_another_user(self):
        response = self.reader_client.post(self.EDIT_URL, data=self.form_data)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        note = Note.objects.get(id=self.note.id)
        self.assertEqual(note.title, self.note.title)
        self.assertEqual(note.text, self.note.text)
        self.assertEqual(note.slug, self.note.slug)
        self.assertEqual(note.author, self.note.author)
