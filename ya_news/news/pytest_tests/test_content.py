from django.conf import settings
from django.urls import reverse
from django.contrib.auth import get_user_model
from news.forms import CommentForm
import pytest

User = get_user_model()


@pytest.mark.django_db
def test_news_count(client, create_news, home_url):
    # Загружаем главную страницу
    response = client.get(home_url)
    object_list = response.context['object_list']
    news_count = object_list.count()
    # Проверяем, что на странице именно 10 новостей
    assert news_count == settings.NEWS_COUNT_ON_HOME_PAGE


@pytest.mark.django_db
def test_news_order(client, create_news, home_url):
    response = client.get(home_url)
    object_list = response.context['object_list']
    # Получаем даты новостей в том порядке, как они выведены на странице
    all_dates = [news.date for news in object_list]
    sorted_dates = sorted(all_dates, reverse=True)
    assert all_dates == sorted_dates


@pytest.mark.django_db
def test_comments_order(client, create_test_data):
    news, detail_url, _ = create_test_data
    response = client.get(detail_url)
    assert 'news' in response.context
    news_in_context = response.context['news']
    all_comments = news_in_context.comment_set.all()
    all_timestamps = [comment.created for comment in all_comments]
    sorted_timestamps = sorted(all_timestamps)
    assert all_timestamps == sorted_timestamps


@pytest.mark.parametrize(
    'client_fixture, should_see_form',
    [
        (pytest.lazy_fixture('author_client'), True),
        (pytest.lazy_fixture('client'), False),
    ]
)
@pytest.mark.parametrize(
    'name, args',
    (
        ('news:detail', pytest.lazy_fixture('id_for_args')),
    )
)
def test_form_visibility(client_fixture, should_see_form,
                         create_test_data, name, args):
    # Формируем URL.
    url = reverse(name, args=args)
    # Используем переданный клиент для запроса.
    response = client_fixture.get(url)
    # Условие наличия/отсутствия формы.
    if should_see_form:
        assert 'form' in response.context
        assert isinstance(response.context['form'], CommentForm)
    else:
        assert 'form' not in response.context
