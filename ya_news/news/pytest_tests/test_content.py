from django.conf import settings
from django.contrib.auth import get_user_model

from news.forms import CommentForm


User = get_user_model()


def test_news_count(client, all_news, home_url):
    # Загружаем главную страницу
    response = client.get(home_url)
    news_in_context = response.context['object_list']
    news_count = news_in_context.count()
    # Проверяем, что на странице именно 10 новостей
    assert news_count == settings.NEWS_COUNT_ON_HOME_PAGE


def test_news_order(client, all_news, home_url):
    response = client.get(home_url)
    news_in_context = response.context['object_list']
    # Получаем даты новостей в том порядке, как они выведены на странице
    all_dates = [news.date for news in news_in_context]
    sorted_dates = sorted(all_dates, reverse=True)
    assert all_dates == sorted_dates


def test_comments_order(client, news, detail_url):
    response = client.get(detail_url)
    assert 'news' in response.context
    news_in_context = response.context['news']
    all_comments = news_in_context.comment_set.all()
    all_timestamps = [comment.created for comment in all_comments]
    sorted_timestamps = sorted(all_timestamps)
    assert all_timestamps == sorted_timestamps


def test_form_visibility_for_author(author_client,
                                    create_test_data, detail_url):
    response = author_client.get(detail_url)
    assert isinstance(response.context.get('form'), CommentForm)


def test_form_visibility_for_anonymous(client, create_test_data, detail_url):
    response = client.get(detail_url)
    assert response.context.get('form') is None
