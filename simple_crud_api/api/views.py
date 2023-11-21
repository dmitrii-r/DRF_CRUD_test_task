from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from api.permissions import IsAdminOwnerOrReadOnly
from api.serializers import PostSerializer
from posts.models import Post


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticatedOrReadOnly])
def api_posts(request):
    """
    API-вью для работы с постами.
    Метод GET возвращает все опубликованные посты.
    Метод POST создает новый пост для авторизованного пользователя.
    """
    if request.method == "GET":
        posts = Post.objects.filter(is_published=True)
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author_id=request.user.id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "PATCH", "DELETE"])
@permission_classes([IsAdminOwnerOrReadOnly])
def api_posts_detail(request, pk):
    """
    API-вью для работы с конкретными постами по их ID.
    Метод GET возвращает конкретный пост.
    МетодЫ PUT, PATCH обновляют информацию о конкретном посте.
    Метод DELETE удаляет конкретный пост.
    Методы PUT, PATCH и DELETE доступны только для автора или администратора.
    """
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return Response(
            {"error": "Поста с таким ID не существует"},
            status=status.HTTP_404_NOT_FOUND,
        )

    if request.method == "GET":
        serializer = PostSerializer(post)
        return Response(serializer.data)

    elif request.method in ["PUT", "PATCH"]:
        serializer = PostSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
