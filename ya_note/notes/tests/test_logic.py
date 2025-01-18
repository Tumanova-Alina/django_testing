from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from pytils.translit import slugify

from notes.models import Note

User = get_user_model()


class TestNoteCreation(TestCase):
    NOTE_TEXT = 'Текст заметки'

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Мимо Крокодил')
        cls.url = reverse('notes:add')
        cls.success_url = reverse('notes:success')
        cls.auth_client = Client()
        cls.auth_client.force_login(cls.author)
        cls.form_data = {'title': 'Новая Заметка', 'text': cls.NOTE_TEXT}

    def test_anonymous_user_cant_create_note(self):
        response = self.client.post(self.url, data=self.form_data)
        self.assertRedirects(response, '/auth/login/?next=/add/')
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, 0)

    def test_user_can_create_note(self):
        response = self.auth_client.post(self.url, data=self.form_data)
        self.assertRedirects(response, self.success_url)
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, 1)
        note = Note.objects.get()
        self.assertEqual(note.title, 'Новая Заметка')
        self.assertEqual(note.text, self.NOTE_TEXT)
        self.assertEqual(note.author, self.author)

    def test_no_duplicate_slug(self):
        Note.objects.create(
            title='Заметка с уникальным слагом', text='Текст',
            author=self.author, slug='unique-slug')
        with self.assertRaises(Exception):
            Note.objects.create(
                title='Еще одна заметка', text='Другой текст',
                author=self.author, slug='unique-slug')

    def test_slug_auto_generation(self):
        form_data = {'title': 'Новая заметка без слага',
                     'text': self.NOTE_TEXT}
        self.auth_client.post(self.url, data=form_data)
        note = Note.objects.get(title='Новая заметка без слага')
        self.assertIsNotNone(note.slug)
        expected_slug = slugify('Новая заметка без слага')
        self.assertEqual(note.slug, expected_slug)


class TestNoteEditDelete(TestCase):
    NOTE_TEXT = 'Текст заметки'
    NEW_NOTE_TEXT = 'Обновлённая заметка'

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Автор заметки')
        cls.note = Note.objects.create(title='Заголовок', text=cls.NOTE_TEXT,
                                       author=cls.author)
        cls.home_url = reverse('notes:home')
        cls.success_url = reverse('notes:success')
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)
        cls.reader = User.objects.create(username='Читатель')
        cls.reader_client = Client()
        cls.reader_client.force_login(cls.reader)
        cls.edit_url = reverse('notes:edit', args=(cls.note.slug,))
        cls.delete_url = reverse('notes:delete', args=(cls.note.slug,))
        cls.form_data = {'text': cls.NEW_NOTE_TEXT}

    def test_author_can_delete_note(self):
        # От имени автора заметки отправляем DELETE-запрос на удаление.
        response = self.author_client.delete(self.delete_url)
        self.assertRedirects(response, self.success_url)
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, 0)

    def test_user_cant_delete_note_of_another_user(self):
        # Выполняем запрос на удаление от пользователя-читателя.
        response = self.reader_client.delete(self.delete_url)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, 1)

    def test_author_can_edit_note(self):
        # Выполняем запрос на редактирование от имени автора заметки.
        self.author_client.post(self.edit_url, data=self.form_data)
        self.note.refresh_from_db()
        self.assertEqual(self.note.text, self.NOTE_TEXT)

    def test_user_cant_edit_note_of_another_user(self):
        # Выполняем запрос на редактирование от имени другого пользователя.
        response = self.reader_client.post(self.edit_url, data=self.form_data)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.note.refresh_from_db()
        self.assertEqual(self.note.text, self.NOTE_TEXT)
