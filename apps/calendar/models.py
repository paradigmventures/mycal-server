from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Calendar(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=191, unique=True)
    title = models.CharField(max_length=191)
    # color string values match tailwind color palettes
    COLOR_CHOICES = (
        ('red', 'Red'),
        ('orange', 'Orange'),
        ('amber', 'Amber'),
        ('yellow', 'Yellow'),
        ('lime', 'Lime'),
        ('green', 'Green'),
        ('emerald', 'Emerald'),
        ('teal', 'Teal'),
        ('cyan', 'Cyan'),
        ('sky', 'Sky'),
        ('blue', 'Blue'),
        ('indigo', 'Indigo'),
        ('violet', 'Violet'),
        ('purple', 'Purple'),
        ('fuchsia', 'Fuchsia'),
        ('pink', 'Pink'),
        ('rose', 'Rose'),
    )
    DEFAULT_COLOR = 'blue'
    color = models.CharField(max_length=7, choices=COLOR_CHOICES, default=DEFAULT_COLOR)
    order = models.IntegerField(db_index=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title
