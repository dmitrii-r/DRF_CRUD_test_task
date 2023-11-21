from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Post(models.Model):
    name = models.CharField("Название", max_length=settings.TITLE_MAX_LENGTH)
    text = models.TextField("Текст")
    created = models.DateTimeField("Дата создания", auto_now_add=True)
    is_published = models.BooleanField("Опубликовано", default=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"
        ordering = ["-created"]
        constraints = [
            models.UniqueConstraint(
                fields=["author", "name"],
                name="unique_author_post",
                violation_error_message=(
                    "У автора уже есть запись с таким названием"
                ),
            ),
        ]

    def __str__(self):
        return self.name
