from django.urls import reverse
from notes.models import Note
from django.contrib.auth.models import User
from notes.tests.base import BaseTestCase


# Константные слаги
# NOTE_SLUG = 'test-note'

# Урлы
HOME_URL = reverse('notes:home')
LOGIN_URL = reverse('users:login')
LOGOUT_URL = reverse('users:logout')
SIGNUP_URL = reverse('users:signup')

# # Урлы, зависящие от параметров
# DETAIL_URL = reverse('notes:detail', constants.NOTE_SLUG)
# EDIT_URL = reverse('notes:edit', constants.NOTE_SLUG)
# DELETE_URL = reverse('notes:delete', constants.NOTE_SLUG)
LIST_URL = reverse('notes:list')
ADD_URL = reverse('notes:add')
SUCCESS_URL = reverse('notes:success')


# class Urls(BaseTestCase):
#     def urls_with_parameter(self):
#         DETAIL_URL = reverse('notes:detail', args=(self.note.slug,))
#         EDIT_URL = reverse('notes:edit', args=(self.note.slug,))
#         DELETE_URL = reverse('notes:delete', args=(self.note.slug,))
# DETAIL_URL_TEMPLATE = 'notes:detail'
# EDIT_URL_TEMPLATE = 'notes:edit'
# DELETE_URL_TEMPLATE = 'notes:delete'


# def get_detail_url(slug):
#     return reverse(DETAIL_URL_TEMPLATE, args=(slug,))


# def get_edit_url(slug):
#     return reverse(EDIT_URL_TEMPLATE, args=(slug,))


# def get_delete_url(slug):
#     return reverse(DELETE_URL_TEMPLATE, args=(slug,))
