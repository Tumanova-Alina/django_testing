from http import HTTPStatus

from django.contrib.auth import get_user_model
import pytest

from news.forms import WARNING
from news.models import Comment

User = get_user_model()


def test_anonymous_user_cant_create_comment(client, detail_url, form_data):
    client.post(detail_url, data=form_data)
    comments_count = Comment.objects.count()
    assert comments_count == 0


def test_authorized_user_can_create_comment(authorized_client, detail_url,
                                            form_data, news, authorized_user):
    response = authorized_client.post(detail_url, data=form_data)
    assert response.status_code == 302
    assert response.url == f'{detail_url}#comments'
    # Проверяем, что комментарий был добавлен в базу
    comments_count = Comment.objects.count()
    assert comments_count == 1
    # Получаем созданный комментарий
    comment = Comment.objects.first()
    assert comment.text == form_data['text']
    assert comment.news == news
    assert comment.author == authorized_user


def test_user_cant_use_bad_words(
        authorized_client, detail_url, bad_words_data):
    # Отправляем данные с плохими словами.
    response = authorized_client.post(detail_url, data=bad_words_data)
    # Проверяем, что форма вернула ошибку.
    assert response.status_code == 200
    assert 'form' in response.context
    assert response.context['form'].errors['text'] == [WARNING]
    assert Comment.objects.count() == 0


@pytest.mark.parametrize(
    'action, method, client_fixture, expected_status, comment_final_text',
    [
        # Тесты на удаление
        ('delete', 'delete', 'author_client', HTTPStatus.FOUND, None),
        ('delete', 'delete', 'not_author_client',
         HTTPStatus.NOT_FOUND, 'Текст комментария'),
        # Тесты на редактирование
        ('edit', 'post', 'author_client',
         HTTPStatus.FOUND, 'Обновлённый комментарий'),
        ('edit', 'post', 'not_author_client',
         HTTPStatus.NOT_FOUND, 'Текст комментария')
    ]
)
def test_comment_actions(
    request, action, method, client_fixture, expected_status, url,
    new_form_data, comment, comment_final_text
):
    client = request.getfixturevalue(client_fixture)
    if method == 'delete':
        response = client.delete(url)
    elif method == 'post':
        response = client.post(url, data=new_form_data)
    assert response.status_code == expected_status
    if comment_final_text is None:
        with pytest.raises(Comment.DoesNotExist):
            comment.refresh_from_db()
    else:
        comment.refresh_from_db()
        assert comment.text == comment_final_text
