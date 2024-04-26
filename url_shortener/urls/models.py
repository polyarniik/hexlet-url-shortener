from django.contrib.auth import get_user_model
from django.db import models
from urls.utils import get_hash

User = get_user_model()


class URL(models.Model):
    url = models.URLField(verbose_name="URL")
    hash = models.CharField(max_length=20)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        related_name="urls",
    )
    visits_count = models.IntegerField(default=0, verbose_name="Количество нажатий")
    create_at = models.DateTimeField(auto_now_add=True, verbose_name="Создан")

    def __str__(self) -> str:
        return f"{self.url} | {self.hash}"

    def __get_url_hash(self):
        hash = get_hash(self.url)
        while URL.objects.filter(hash=hash).exists():
            hash = get_hash(self.url)
        return hash

    def save(self, *args, **kwargs):
        if not self.pk:
            self.hash = self.__get_url_hash()
        return super().save(*args, **kwargs)
