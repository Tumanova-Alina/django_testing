import pytest
from django.contrib.auth.models import User
from django.test.client import Client
from django.utils import timezone
from django.urls import reverse
from news.models import News, Comment
from django.conf import settings
from datetime import datetime, timedelta
from news.forms import BAD_WORDS


@pytest.fixture
# Используем встроенную фикстуру для модели пользователей django_user_model.
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
def client(db):
    return Client()


@pytest.fixture
def authorized_client(db, authorized_user):
    client = Client()
    client.force_login(authorized_user)
    return client


@pytest.fixture
def news(db):
    news = News.objects.create(  # Создаём объект заметки.
        title='Заголовок',
        text='Текст заметки',
    )
    return news


@pytest.fixture
def create_news(db):  # db — фикстура pytest для работы с базой данных
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
def create_test_data(db):
    news = News.objects.create(title='Тестовая новость', text='Просто текст.')
    detail_url = reverse('news:detail', args=(news.id,))
    author = User.objects.create(username='Комментатор')
    now = timezone.now()
    for index in range(10):
        comment = Comment.objects.create(
            news=news, author=author, text=f'Tекст {index}',
        )
        comment.created = now + timedelta(days=index)
        comment.save()
    return news, detail_url, author


@pytest.fixture
# Фикстура запрашивает другую фикстуру создания заметки.
def id_for_args(db, news):
    # И возвращает кортеж, который содержит slug заметки.
    # На то, что это кортеж, указывает запятая в конце выражения.
    return (news.id,)


@pytest.fixture
def comment(db, news, author):
    comment = Comment.objects.create(
        text='Текст комментария', news=news, author=author)
    # Например, установленная дата для целей тестирования
    comment.created = timezone.now() - timezone.timedelta(days=1)
    comment.save()
    return comment


@pytest.fixture
def form_data(db):
    return {'text': 'Текст комментария'}


@pytest.fixture
def detail_url(db, news):
    return reverse('news:detail', args=(news.id,))


@pytest.fixture
def bad_words_data(db):
    # Возвращаем данные с плохим словом.
    return {'text': f'Какой-то текст, {BAD_WORDS[0]}, еще текст'}


@pytest.fixture
def url(db, comment, action):
    # Генерируем URL для редактирования или удаления комментария.
    return reverse(f'news:{action}', args=(comment.id,))


@pytest.fixture
def new_form_data(db):
    # Данные для редактирования комментария.
    return {'text': 'Обновлённый комментарий'}
