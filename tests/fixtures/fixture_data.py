import pytest

from posts.models import Post


@pytest.fixture
def post(user):
    return Post.objects.create(
        name='Пост 1',
        text='Текст поста 1',
        author=user
    )


@pytest.fixture
def another_post(another_user):
    return Post.objects.create(
        name='Пост 2',
        text='Текст поста 2',
        author=another_user
    )
