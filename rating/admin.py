from django.contrib import admin

from .models import Discipline, Standard, Result, ExcelTableFile

admin.site.register(Discipline)
admin.site.register(Standard)
admin.site.register(Result)
admin.site.register(ExcelTableFile)
