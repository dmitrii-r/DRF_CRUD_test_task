from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from api.serializers import PostSerializer
from posts.models import Post


@extend_schema(
    request=PostSerializer,
    methods=["GET"],
    responses={
        status.HTTP_200_OK: PostSerializer(many=True),
    },
)
@extend_schema(
    request=PostSerializer,
    methods=["POST"],
    responses={
        status.HTTP_201_CREATED: PostSerializer,
        status.HTTP_400_BAD_REQUEST: OpenApiResponse(
            response=None, description="Не заполнено обязательное поле"
        ),
        status.HTTP_403_FORBIDDEN: OpenApiResponse(
            response=None, description="Пользователь на авторизован"
        ),
    },
)
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


@extend_schema(
    request=PostSerializer,
    responses={
        status.HTTP_200_OK: PostSerializer,
        status.HTTP_404_NOT_FOUND: OpenApiResponse(
            response=None,
            description="Попытка запроса несуществующей публикации",
        ),
    },
    methods=["GET"],
)
@extend_schema(
    request=PostSerializer,
    responses={
        status.HTTP_200_OK: PostSerializer,
        status.HTTP_400_BAD_REQUEST: OpenApiResponse(
            response=None, description="Не заполнено обязательное поле"
        ),
        status.HTTP_403_FORBIDDEN: OpenApiResponse(
            response=None, description="Попытка изменить чужой контент"
        ),
        status.HTTP_404_NOT_FOUND: OpenApiResponse(
            response=None,
            description="Попытка запроса несуществующей публикации",
        ),
    },
    methods=["PUT", "PATCH"],
)
@extend_schema(
    request=PostSerializer,
    responses={
        status.HTTP_204_NO_CONTENT: OpenApiResponse(
            response=None, description="Удачное выполнение запроса"
        ),
        status.HTTP_403_FORBIDDEN: OpenApiResponse(
            response=None, description="Попытка изменить чужой контент"
        ),
        status.HTTP_404_NOT_FOUND: OpenApiResponse(
            response=None,
            description="Попытка запроса несуществующей публикации",
        ),
    },
    methods=["DELETE"],
)
@api_view(["GET", "PUT", "PATCH", "DELETE"])
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

    elif post.author == request.user or request.user.is_superuser:
        if request.method in ["PUT", "PATCH"]:
            serializer = PostSerializer(post, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

        elif request.method == "DELETE":
            post.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        return Response(
            {"error": "Попытка изменить чужой контент"},
            status=status.HTTP_403_FORBIDDEN,
        )
