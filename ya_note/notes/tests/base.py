import unittest
from django.test import TestCase, Client
from django.contrib.auth.models import User
from notes.models import Note
from django.urls import reverse


class BaseTestCase(TestCase):
    NOTE_TEXT = 'Текст заметки'
    NEW_NOTE_TEXT = 'Обновлённая заметка'

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Лев Толстой')
        cls.reader = User.objects.create(username='Читатель простой')
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)
        cls.reader_client = Client()
        cls.reader_client.force_login(cls.reader)
        cls.slug = 'slug'
        cls.note = Note.objects.create(title='Заголовок',
                                       text='Текст заметки',
                                       author=cls.author,
                                       slug=cls.slug
                                       )
        cls.auth_client = Client()
        cls.auth_client.force_login(cls.author)
        cls.form_data = {'title': 'Новая Заметка', 'text': cls.NOTE_TEXT}
        cls.new_form_data = {'title': 'Новая Заметка', 'text': cls.NEW_NOTE_TEXT, 'slug': cls.slug}
