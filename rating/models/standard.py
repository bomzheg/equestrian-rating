from django.db import models


class Standard(models.Model):
    """Разновидность норматива"""
    name = models.CharField(max_length=256, verbose_name="Название стандарта")
    description = models.CharField(max_length=512, verbose_name="Описание", null=True)
    discipline = models.ForeignKey(
        "Discipline",
        on_delete=models.PROTECT,
        related_name="standards",
        verbose_name="Дисциплина",
    )
    link = models.CharField(max_length=64, verbose_name="Имя для ссылки")

    class Meta:
        db_table = "standards"
        verbose_name = "Норматив"
        verbose_name_plural = "Нормативы"

    def __str__(self):
        return self.name
