from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse

from notes.models import Note


class BaseTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Лев Толстой')
        cls.reader = User.objects.create(username='Читатель простой')
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)
        cls.reader_client = Client()
        cls.reader_client.force_login(cls.reader)
        cls.note = Note.objects.create(title='Заголовок',
                                       text='Текст заметки',
                                       author=cls.author,
                                       )
        cls.auth_client = Client()
        cls.auth_client.force_login(cls.author)

        cls.form_data = {'title': 'Новая Заметка',
                         'text': 'Обновлённая заметка'}

        cls.note_by_author = Note.objects.create(
            title='Заметка автора', text='Текст заметки', author=cls.author
        )
        cls.note_by_reader = Note.objects.create(
            title='Заметка читателя', text='Текст заметки', author=cls.reader
        )

        cls.DETAIL_URL = reverse(
            'notes:detail', kwargs={'slug': cls.note.slug}
        )
        cls.EDIT_URL = reverse(
            'notes:edit', kwargs={'slug': cls.note.slug}
        )
        cls.DELETE_URL = reverse(
            'notes:delete', kwargs={'slug': cls.note.slug}
        )
        # Остальные урлы
        cls.HOME_URL = reverse('notes:home')
        cls.LOGIN_URL = reverse('users:login')
        cls.LOGOUT_URL = reverse('users:logout')
        cls.SIGNUP_URL = reverse('users:signup')
        cls.LIST_URL = reverse('notes:list')
        cls.ADD_URL = reverse('notes:add')
        cls.SUCCESS_URL = reverse('notes:success')
        cls.IF_LOGIN_ADD_URL = f'{cls.LOGIN_URL}?next={cls.ADD_URL}'
        cls.IF_LOGIN_LIST_URL = f'{cls.LOGIN_URL}?next={cls.LIST_URL}'
        cls.IF_LOGIN_SUCCESS_URL = f'{cls.LOGIN_URL}?next={cls.SUCCESS_URL}'
        cls.IF_LOGIN_DETAIL_URL = f'{cls.LOGIN_URL}?next={cls.DETAIL_URL}'
        cls.IF_LOGIN_EDIT_URL = f'{cls.LOGIN_URL}?next={cls.EDIT_URL}'
        cls.IF_LOGIN_DELETE_URL = f'{cls.LOGIN_URL}?next={cls.DELETE_URL}'
