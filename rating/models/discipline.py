from django.db import models


class Discipline(models.Model):
    """Наименование дисциплины"""
    name = models.CharField(max_length=64, verbose_name="Название дисциплины")
    link = models.CharField(max_length=64, verbose_name="Название для ссылки")

    class Meta:
        db_table = "disciplines"
        verbose_name = "Дисциплина"
        verbose_name_plural = "Дисциплины"

    def __str__(self):
        return self.name
