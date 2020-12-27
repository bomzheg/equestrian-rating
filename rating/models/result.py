from django.db import models


class Result(models.Model):
    """Данные о конкретном случае выполненного норматива."""
    fulfilled_standard = models.ForeignKey(
        "Standard",
        on_delete=models.PROTECT,
        related_name="results",
        verbose_name="Норматив",
    )
    date = models.DateField(verbose_name="Дата соревнований")
    horse_name = models.CharField(max_length=64, verbose_name="Лошадь")
    athlete_name = models.CharField(max_length=128, verbose_name="Спортсмен")
    club_name = models.CharField(max_length=64, verbose_name="Клуб")

    class Meta:
        db_table = "results"
        verbose_name = "Выполнивший норматив"
        verbose_name_plural = "Выполнившие норматив"

    def __str__(self):
        return (
            f"{self.date}: {self.athlete_name} "
            f"на лошади по кличке {self.horse_name}"
            f"из {self.club_name}"
        )
