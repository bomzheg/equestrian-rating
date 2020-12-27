from django.db import models

from app.settings import BASE_DIR
from rating.services.parsing_excel import parse_workbook, save_results


class ExcelTableFile(models.Model):
    """Файлы с нормативами"""
    file = models.FileField(
        verbose_name="Файл с результатами",
        upload_to=str(BASE_DIR / 'uploads/'),
    )
    to_discipline = models.ForeignKey(
        "Discipline",
        on_delete=models.PROTECT,
        related_name="excel_files",
        verbose_name="Дисциплина",
    )

    class Meta:
        db_table = "excel_files"
        verbose_name = "Файл с выполненными нормативами"
        verbose_name_plural = "Файлы с выполненными нормативами"

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        results = parse_workbook(self.file)
        save_results(results, using)
        super(ExcelTableFile, self).save(
            force_insert=force_insert,
            force_update=force_update,
            using=using,
            update_fields=update_fields
        )
