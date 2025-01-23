from datetime import datetime, timedelta

import pytest
from django.conf import settings
from django.test.client import Client
from django.utils import timezone
from django.urls import reverse

from news.models import News, Comment


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(
    db,  # noqa
):
    pass


@pytest.fixture
def author(db, django_user_model):
    return django_user_model.objects.create(username='Автор')


@pytest.fixture
def not_author(db, django_user_model):
    return django_user_model.objects.create(username='Не автор')


@pytest.fixture
def authorized_user(db, django_user_model):
    return django_user_model.objects.create(
        username='Авторизованный пользователь')


@pytest.fixture
def author_client(db, author):  # Вызываем фикстуру автора.
    # Создаём новый экземпляр клиента, чтобы не менять глобальный.
    client = Client()
    client.force_login(author)  # Логиним автора в клиенте.
    return client


@pytest.fixture
def not_author_client(db, not_author):
    client = Client()
    client.force_login(not_author)  # Логиним обычного пользователя в клиенте.
    return client


@pytest.fixture
def authorized_client(db, authorized_user):
    client = Client()
    client.force_login(authorized_user)
    return client


@pytest.fixture
def news(db):
    news = News.objects.create(
        title='Заголовок',
        text='Текст заметки',
    )
    return news


@pytest.fixture
def all_news(db):
    today = datetime.today()
    all_news = [
        News(
            title=f'Новость {index}',
            text='Просто текст.',
            date=today - timedelta(days=index)
        )
        for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
    ]
    News.objects.bulk_create(all_news)


@pytest.fixture
def home_url(db):
    return reverse('news:home')


@pytest.fixture
def test_data(db, news, author):
    now = timezone.now()
    for index in range(10):
        comment = Comment.objects.create(
            news=news, author=author, text=f'Tекст {index}',
        )
        comment.created = now + timedelta(days=index)
        comment.save()


@pytest.fixture
def comment(db, news, author):
    comment = Comment.objects.create(
        text='Текст комментария', news=news, author=author)
    return comment


@pytest.fixture
def detail_url(db, news):
    return reverse('news:detail', args=(news.id,))


@pytest.fixture
def login_url():
    return reverse('users:login')


@pytest.fixture
def logout_url():
    return reverse('users:logout')


@pytest.fixture
def signup_url():
    return reverse('users:signup')


@pytest.fixture
def edit_url(comment):
    return reverse('news:edit', args=(comment.id,))


@pytest.fixture
def delete_url(comment):
    return reverse('news:delete', args=(comment.id,))


@pytest.fixture
def comments_url(db, detail_url):
    return f'{detail_url}#comments'


@pytest.fixture
def if_login_edit_url(login_url, edit_url):
    return f"{login_url}?next={edit_url}"


@pytest.fixture
def if_login_delete_url(login_url, delete_url):
    return f"{login_url}?next={delete_url}"
