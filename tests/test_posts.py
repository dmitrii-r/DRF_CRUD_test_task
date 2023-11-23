from http import HTTPStatus

import pytest

from posts.models import Post


@pytest.mark.django_db
class TestPosts:

    post_list_url = '/posts/'
    post_detail_url = '/posts/{post_id}/'
    VALID_DATA = {
        'name': 'Измененное название',
        'text': 'Измененный текст',
        'is_published': True
    }

    def test_post_not_found(self, client, post):
        response = client.get(self.post_list_url)

        assert response.status_code != HTTPStatus.NOT_FOUND, (
            f'Эндпоинт `{self.post_list_url}` не найден, проверьте настройки '
            'в *urls.py*.'
        )

    def test_post_single_not_found(self, client, post):
        response = client.get(self.post_detail_url.format(post_id=post.id))
        assert response.status_code != HTTPStatus.NOT_FOUND, (
            f'Эндпоинт `{self.post_detail_url}` не найден, проверьте '
            'настройки в *urls.py*.'
        )

    def test_post_list_not_auth(self, client, post):
        response = client.get(self.post_list_url)

        assert response.status_code == HTTPStatus.OK, (
            'Проверьте, что GET-запрос неавторизованного пользователя к '
            f'`{self.post_list_url}` возвращает ответ со статусом 200.'
        )

    def test_post_single_not_auth(self, client, post):
        response = client.get(self.post_detail_url.format(post_id=post.id))

        assert response.status_code == HTTPStatus.OK, (
            'Проверьте, что GET-запрос неавторизованного пользователя к '
            f'`{self.post_detail_url}` возвращает ответ со статусом 200.'
        )

    def test_posts_auth_get(self, user_client, post, another_post):
        response = user_client.get(self.post_list_url)
        assert response.status_code == HTTPStatus.OK, (
            f'Проверьте, что GET-запрос авторизованного пользователя к '
            f'`{self.post_list_url}` возвращает статус 200.'
        )

        test_data = response.json()
        assert isinstance(test_data, list), (
            'Проверьте, что GET-запрос авторизованного пользователя к '
            f'`{self.post_list_url}` возвращает список.'
        )

        assert len(test_data) == Post.objects.filter(
            is_published=True
        ).count(), (
            'Проверьте, что GET-запрос авторизованного пользователя к '
            f'`{self.post_list_url}` возвращает список всех опубликованных '
            'постов.'
        )

    def test_post_create_auth_with_invalid_data(self, user_client):
        posts_count = Post.objects.count()
        response = user_client.post(self.post_list_url, data={})
        assert response.status_code == HTTPStatus.BAD_REQUEST, (
            'Проверьте, что для авторизованного пользователя POST-запрос с '
            f'некорректными данными к `{self.post_list_url}` возвращает ответ '
            'со статусом 400.'
        )
        assert posts_count == Post.objects.count(), (
            f'Проверьте, что POST-запрос с некорректными данными, '
            f'отправленный к `{self.post_list_url}`, не создаёт новый пост.'
        )

    def test_post_create_auth_with_valid_data(self, user_client, user):
        post_count = Post.objects.count()
        data = {'name': "Пост 3", 'text': 'Текст поста 3'}
        response = user_client.post(self.post_list_url, data=data)
        assert response.status_code == HTTPStatus.CREATED, (
            'Проверьте, что для авторизованного пользователя  POST-запрос с '
            f'корректными данными к `{self.post_list_url}` возвращает ответ '
            'со статусом 201.'
        )
        post_count += 1
        assert post_count == Post.objects.count(), (
            'Проверьте, что POST-запрос с корректными данными от '
            f'авторизованного пользователя к `{self.post_list_url}` создаёт '
            'новый пост.'
        )
        test_data = response.json()
        assert isinstance(test_data, dict), (
            'Проверьте, что для авторизованного пользователя POST-запрос к '
            f'`{self.post_list_url}` возвращает ответ, содержащий данные '
            'нового поста в виде словаря.'
        )
        assert test_data.get('name') == data['name'], (
            'Проверьте, что для авторизованного пользователя POST-запрос к '
            f'`{self.post_list_url}` возвращает ответ, содержащий текст '
            'нового поста в неизменном виде.'
        )
        assert test_data.get('text') == data['text'], (
            'Проверьте, что для авторизованного пользователя POST-запрос к '
            f'`{self.post_list_url}` возвращает ответ, содержащий название '
            'нового поста в неизменном виде.'
        )
        assert not test_data.get('is_published'), (
            'Проверьте, что для авторизованного пользователя POST-запрос к '
            f'`{self.post_list_url}` возвращает ответ, в котором поле '
            'is_published определено как False.'
        )
        assert test_data.get('author') == user.username, (
            'Проверьте, что для авторизованного пользователя при создании '
            f'поста через POST-запрос к `{self.post_list_url}` ответ содержит '
            'поле `author` с именем пользователя, отправившего запрос.'
        )

        data = {'name': 'Пост 4'}
        response = user_client.post(self.post_list_url, data=data)
        assert response.status_code == HTTPStatus.BAD_REQUEST, (
            f'Если в POST-запросе, отправленном авторизованным пользователем '
            f'на `{self.post_list_url}`, не переданы все необходимые поля - '
            'должен вернуться ответ со статусом 400.'
        )

    def test_post_unauth_create(self, client, user, another_user):
        posts_count = Post.objects.count()

        data = {
            'name': 'Новый пост',
            'text': 'Текст нового поста',
            'author': another_user.id,
        }
        response = client.post(self.post_list_url, data=data)
        assert response.status_code == HTTPStatus.FORBIDDEN, (
            'Проверьте, что POST-запрос неавторизованного пользователя к '
            f'`{self.post_list_url}` возвращает ответ со статусом 403.'
        )

        assert posts_count == Post.objects.count(), (
            'Проверьте, что POST-запрос неавторизованного пользователя к '
            f'`{self.post_list_url}` не создаёт новый пост.'
        )

    def test_post_get_current(self, user_client, post):
        response = user_client.get(
            self.post_detail_url.format(post_id=post.id)
        )

        assert response.status_code == HTTPStatus.OK, (
            'Проверьте, что GET-запрос авторизованного пользователя к '
            f'`{self.post_detail_url}` возвращает ответ со статусом 200.'
        )

    @pytest.mark.parametrize('http_method', ('put', 'patch'))
    def test_post_change_auth_with_valid_data(self, user_client, post,
                                              another_post, http_method):
        request_func = getattr(user_client, http_method)
        response = request_func(
            self.post_detail_url.format(post_id=post.id),
            data=self.VALID_DATA
        )
        http_method = http_method.upper()
        assert response.status_code == HTTPStatus.OK, (
            f'Проверьте, что {http_method}-запрос авторизованного '
            f'пользователя, отправленный на `{self.post_detail_url}` к '
            'собственному посту, вернёт ответ со статусом 200.'
        )

        test_post = Post.objects.filter(id=post.id).first()
        assert test_post, (
            f'Проверьте, что {http_method}-запрос авторизованного '
            f'пользователя, отправленный на `{self.post_detail_url}` к '
            'собственному посту, не удаляет редактируемый пост.'
        )
        assert test_post.name == self.VALID_DATA['name'], (
            f'Проверьте, что {http_method}-запрос авторизованного '
            f'пользователя, отправленный на `{self.post_detail_url}` к '
            f'собственному посту, вносит изменения в {test_post.name} поста.'
        )
        assert test_post.text == self.VALID_DATA['text'], (
            f'Проверьте, что {http_method}-запрос авторизованного '
            f'пользователя, отправленный на `{self.post_detail_url}` к '
            f'собственному посту, вносит изменения в {test_post.text} поста.'
        )
        assert test_post.is_published == self.VALID_DATA['is_published'], (
            f'Проверьте, что {http_method}-запрос авторизованного '
            f'пользователя, отправленный на `{self.post_detail_url}` к '
            'собственному посту, вносит изменения '
            f'в {test_post.is_published} поста.'
        )

    @pytest.mark.parametrize('http_method', ('put', 'patch'))
    def test_post_change_not_author_with_valid_data(self, user_client,
                                                    another_post, http_method):
        request_func = getattr(user_client, http_method)
        response = request_func(
            self.post_detail_url.format(post_id=another_post.id),
            data=self.VALID_DATA
        )
        http_method = http_method.upper()
        assert response.status_code == HTTPStatus.FORBIDDEN, (
            f'Проверьте, что {http_method}-запрос авторизованного '
            f'пользователя, отправленный на `{self.post_detail_url}` к чужому '
            'посту, возвращает ответ со статусом 403.'
        )

        db_post = Post.objects.filter(id=another_post.id).first()
        assert db_post.text != self.VALID_DATA['text'], (
            f'Проверьте, что {http_method}-запрос авторизованного '
            f'пользователя, отправленный на `{self.post_detail_url}` к чужому '
            'посту, возвращает ответ со статусом 403.'
        )

    @pytest.mark.parametrize('http_method', ('put', 'patch'))
    def test_post_patch_auth_with_invalid_data(self, user_client, post,
                                               http_method):
        request_func = getattr(user_client, http_method)
        response = request_func(
            self.post_detail_url.format(post_id=post.id),
            data={'text': {}},
            format='json'
        )
        assert response.status_code == HTTPStatus.BAD_REQUEST, (
            f'Проверьте, что {http_method}-запрос с некорректными данными от '
            f'авторизованного пользователя к `{self.post_detail_url}` '
            'возвращает ответ с кодом 400.'
        )

    def test_post_delete_by_author(self, user_client, post):
        response = user_client.delete(
            self.post_detail_url.format(post_id=post.id)
        )
        assert response.status_code == HTTPStatus.NO_CONTENT, (
            'Проверьте, что для автора поста DELETE-запрос к '
            f'`{self.post_detail_url}` возвращает ответ со статусом 204.'
        )

        test_post = Post.objects.filter(id=post.id).first()
        assert not test_post, (
            'Проверьте, что DELETE-запрос автора поста к '
            f'`{self.post_detail_url}` удаляет этот пост.'
        )

    def test_post_delete_not_author(self, user_client, another_post):
        response = user_client.delete(
            self.post_detail_url.format(post_id=another_post.id)
        )
        assert response.status_code == HTTPStatus.FORBIDDEN, (
            'Проверьте, что DELETE-запрос авторизованного пользователя, '
            f'отправленный на `{self.post_detail_url}` к чужому посту, вернёт '
            'ответ со статусом 403.'
        )

        test_post = Post.objects.filter(id=another_post.id).first()
        assert test_post, (
            'Проверьте, что авторизованный пользователь не может удалить '
            'чужой пост.'
        )

    def test_post_unauth_delete_current(self, client, post):
        response = client.delete(
            self.post_detail_url.format(post_id=post.id)
        )
        assert response.status_code == HTTPStatus.FORBIDDEN, (
            'Проверьте, что DELETE-запрос неавторизованного пользователя '
            f'к `{self.post_detail_url}` вернёт ответ со статусом 403.'
        )
        test_post = Post.objects.filter(id=post.id).first()
        assert test_post, (
            'Проверьте, что DELETE-запрос неавторизованного пользователя '
            f'к `{self.post_detail_url}` не удаляет запрошенный пост.'
        )

    @pytest.mark.parametrize('http_method', ('put', 'patch'))
    def test_post_change_by_superuser(self, superuser_client, post,
                                      http_method):
        request_func = getattr(superuser_client, http_method)
        response = request_func(
            self.post_detail_url.format(post_id=post.id),
            data=self.VALID_DATA
        )
        http_method = http_method.upper()
        assert response.status_code == HTTPStatus.OK, (
            f'Проверьте, что {http_method}-запрос авторизованного суперюзера, '
            f'отправленный на `{self.post_detail_url}` к чужому посту, '
            f'вернёт ответ со статусом 200.'
        )

        test_post = Post.objects.filter(id=post.id).first()
        assert test_post, (
            f'Проверьте, что {http_method}-запрос авторизованного суперюзера, '
            f'отправленный на `{self.post_detail_url}` к чужому посту, '
            f'не удаляет редактируемый пост.'
        )
        assert test_post.name == self.VALID_DATA['name'], (
            f'Проверьте, что {http_method}-запрос авторизованного суперюзера, '
            f'отправленный на `{self.post_detail_url}` к чужому посту, '
            f'вносит изменения в {test_post.name} поста.'
        )
        assert test_post.text == self.VALID_DATA['text'], (
            f'Проверьте, что {http_method}-запрос авторизованного суперюзера, '
            f'отправленный на `{self.post_detail_url}` к чужому посту, '
            f'вносит изменения в {test_post.text} поста.'
        )
        assert test_post.is_published == self.VALID_DATA['is_published'], (
            f'Проверьте, что {http_method}-запрос авторизованного суперюзера, '
            f'отправленный на `{self.post_detail_url}` к чужому посту, '
            f'вносит изменения в {test_post.is_published} поста.'
        )

    def test_post_delete_by_superuser(self, superuser_client, post):
        response = superuser_client.delete(
            self.post_detail_url.format(post_id=post.id)
        )
        assert response.status_code == HTTPStatus.NO_CONTENT, (
            'Проверьте, что для авторизованного суперюзера DELETE-запрос к '
            f'`{self.post_detail_url}` возвращает ответ со статусом 204.'
        )

        test_post = Post.objects.filter(id=post.id).first()
        assert not test_post, (
            'Проверьте, что для авторизованного суперюзера DELETE-запрос к '
            f'`{self.post_detail_url}` удаляет этот пост.'
        )
