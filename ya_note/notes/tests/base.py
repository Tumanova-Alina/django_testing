from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse

from notes.models import Note

NOTE_SLUG = 'note_slug'


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
                                       slug=NOTE_SLUG
                                       )
        cls.form_data = {'title': 'Заголовок',
                         'text': 'Обновлённая заметка', 'slug': 'new_slug'}

        cls.note_by_author = Note.objects.create(
            title='Заметка автора', text='Текст заметки', author=cls.author
        )
        cls.note_by_reader = Note.objects.create(
            title='Заметка читателя', text='Текст заметки', author=cls.reader
        )


# Урлы с параметром
DETAIL_URL = reverse(
    'notes:detail', args=(NOTE_SLUG,)
)
EDIT_URL = reverse(
    'notes:edit', args=(NOTE_SLUG,)
)
DELETE_URL = reverse(
    'notes:delete', args=(NOTE_SLUG,)
)

# Остальные урлы
LOGIN_URL = reverse('users:login')
LOGOUT_URL = reverse('users:logout')
SIGNUP_URL = reverse('users:signup')
HOME_URL = reverse('notes:home')
ADD_URL = reverse('notes:add')
LIST_URL = reverse('notes:list')
SUCCESS_URL = reverse('notes:success')
LOGIN_ADD_URL = f'{LOGIN_URL}?next={ADD_URL}'
LOGIN_LIST_URL = f'{LOGIN_URL}?next={LIST_URL}'
LOGIN_SUCCESS_URL = f'{LOGIN_URL}?next={SUCCESS_URL}'
LOGIN_DETAIL_URL = f'{LOGIN_URL}?next={DETAIL_URL}'
LOGIN_EDIT_URL = f'{LOGIN_URL}?next={EDIT_URL}'
LOGIN_DELETE_URL = f'{LOGIN_URL}?next={DELETE_URL}'
