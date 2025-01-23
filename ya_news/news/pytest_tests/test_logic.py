from http import HTTPStatus

from django.contrib.auth import get_user_model

from news.forms import WARNING, BAD_WORDS
from news.models import Comment


FORM_DATA = {'text': 'Текст комментария'}
BAD_WORDS_DATA = {'text': f'Какой-то текст, {BAD_WORDS[0]}, еще текст'}
NEW_FORM_DATA = {'text': 'Обновлённый комментарий'}

User = get_user_model()


def test_anonymous_user_cant_create_comment(client, detail_url):
    response = client.post(detail_url, data=FORM_DATA)
    assert response.status_code == HTTPStatus.FOUND
    comments_count = Comment.objects.count()
    assert comments_count == 0


def test_authorized_user_can_create_comment(authorized_client, detail_url,
                                            news, authorized_user,
                                            comments_url):
    response = authorized_client.post(detail_url, data=FORM_DATA)
    assert response.status_code == HTTPStatus.FOUND
    assert response.url == comments_url
    # Проверяем, что комментарий был добавлен в базу
    comments_count = Comment.objects.count()
    assert comments_count == 1
    comment = Comment.objects.get()
    assert comment.text == FORM_DATA['text']
    assert comment.news == news
    assert comment.author == authorized_user


def test_user_cant_use_bad_words(detail_url, authorized_client):
    # Отправляем данные с плохими словами.
    response = authorized_client.post(detail_url, data=BAD_WORDS_DATA)
    assert response.status_code == HTTPStatus.OK
    assert 'form' in response.context
    assert response.context['form'].errors['text'] == [WARNING]
    assert Comment.objects.count() == 0


def test_author_can_delete_comment(author_client, comment, delete_url):
    response = author_client.delete(delete_url)
    assert response.status_code == HTTPStatus.FOUND
    assert not Comment.objects.filter(id=comment.id).exists()


def test_not_author_cant_delete_comment(
        not_author_client, comment, delete_url):
    response = not_author_client.delete(delete_url)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert Comment.objects.filter(id=comment.id).exists()
    existing_comment = Comment.objects.get(id=comment.id)
    assert existing_comment.text == comment.text
    assert existing_comment.news == comment.news
    assert existing_comment.author == comment.author


def test_author_can_edit_comment(author_client, comment, edit_url):
    original_news = comment.news
    original_author = comment.author
    response = author_client.post(edit_url, data=NEW_FORM_DATA)
    assert response.status_code == HTTPStatus.FOUND
    comment = Comment.objects.get(id=comment.id)
    assert comment.text == NEW_FORM_DATA['text']
    assert comment.news == original_news
    assert comment.author == original_author


def test_not_author_cant_edit_comment(not_author_client, comment, edit_url):
    original_text = comment.text
    original_news = comment.news
    original_author = comment.author
    response = not_author_client.post(edit_url, data=NEW_FORM_DATA)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comment = Comment.objects.get(id=comment.id)
    assert comment.text == original_text
    assert comment.news == original_news
    assert comment.author == original_author
