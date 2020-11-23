from django.db import models

from app.settings import BASE_DIR
from rating.services.parsing_excel import parse_workbook, save_results


class ExcelTableFile(models.Model):
    """Файлы с нормативами"""
    file = models.FileField(
        verbose_name="Файл с результатами",
        upload_to=str(BASE_DIR / 'uploads/'),
    )
    to_standard = models.ForeignKey(
        "Standard",
        on_delete=models.PROTECT,
        related_name="excel_files",
        verbose_name="Норматив",
    )

    class Meta:
        db_table = "excel_files"
        verbose_name = "Файл с выполненными нормативами"
        verbose_name_plural = "Файлы с выполненными нормативами"

    def save(self, *args, **kwargs):
        results = parse_workbook(self.file)
        save_results(results, self.to_standard)
        super(ExcelTableFile, self).save(*args, **kwargs)
