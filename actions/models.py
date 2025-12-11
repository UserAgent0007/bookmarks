from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

# Create your models here.

class Action(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='actions',
        on_delete=models.CASCADE
    )

    verb = models.CharField(
        max_length=255
    )

    created = models.DateTimeField(auto_now_add=True)
    # ContentType зберіає інформацію про всі моелі в проекті Django
    # Тобто наступний рядок робить універсальне з єднання зі всіма моделями
    # Поле зберігатиме інформацію (якої моделі є пов язаний об єкт), тут лежить тип контенту
    target_ct = models.ForeignKey( # Вказує на модель цільового об'єкта (ContentType)
        ContentType,
        blank=True,
        null=True,
        related_name='target_obj',
        on_delete=models.CASCADE
    )
    # Ключ об'єкта пов'язаної моделі
    target_id = models.PositiveIntegerField(null=True, blank=True) # поле яке зберігатиме Первинний ключ пов язаного об'єкта
    # Обгортка над цими двома полями, де Django бере модель з target_ct і шукає об єкт з target_id
    # При створенні об єкту Action вказується (target=...) і далі Django самостійно заповнює target_ct та target_id

    target = GenericForeignKey('target_ct', 'target_id')

    class Meta:

        indexes = [
            models.Index(fields=['-created']),
            models.Index(fields=['target_ct', 'target_id'])
        ]
        ordering = [
            '-created',
        ]