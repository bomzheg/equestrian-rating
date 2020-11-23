from django.db import models


class Discipline(models.Model):
    """Наименование дисциплины"""
    name = models.CharField(max_length=64, verbose_name="Название дисциплины")

    class Meta:
        db_table = "disciplines"
        verbose_name = "Дисциплина"

    def __str__(self):
        return self.name


class Standard(models.Model):
    """Разновидность норматива"""
    name = models.CharField(max_length=256, verbose_name="Название стандарта")
    fulfilled_standard = models.ForeignKey(
        Discipline,
        on_delete=models.PROTECT,
        related_name="standards",
        verbose_name="Стандарт",
    )

    class Meta:
        db_table = "standards"
        verbose_name = "Норматив"

    def __str__(self):
        return self.name


class Result(models.Model):
    """Данные о конкретном случае выполненного норматива."""
    fulfilled_standard = models.ForeignKey(
        Standard,
        on_delete=models.PROTECT,
        related_name="results",
        verbose_name="Выполненный стандарт",
    )
    date = models.DateField(verbose_name="Дата соревнований")
    horse_name = models.CharField(max_length=64, verbose_name="Лошадь")
    athlete_name = models.CharField(max_length=128, verbose_name="Спортсмен")
    club_name = models.CharField(max_length=64, verbose_name="Клуб")

    class Meta:
        db_table = "results"
        verbose_name = "Выполнившие норматив"

    def __str__(self):
        return (
            f"{self.date}: {self.athlete_name} "
            f"на лошади по кличке {self.horse_name}"
            f"из {self.club_name}"
        )
