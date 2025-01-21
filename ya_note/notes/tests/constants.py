from django.urls import reverse

# Константные слаги
NOTE_SLUG = 'slug'

# Урлы
HOME_URL = reverse('notes:home')
LOGIN_URL = reverse('users:login')
LOGOUT_URL = reverse('users:logout')
SIGNUP_URL = reverse('users:signup')
LIST_URL = reverse('notes:list')
ADD_URL = reverse('notes:add')
SUCCESS_URL = reverse('notes:success')

# Урлы, зависящие от параметров
DETAIL_URL = reverse('notes:detail', kwargs={'slug': NOTE_SLUG})
EDIT_URL = reverse('notes:edit', kwargs={'slug': NOTE_SLUG})
DELETE_URL = reverse('notes:delete', kwargs={'slug': NOTE_SLUG})
