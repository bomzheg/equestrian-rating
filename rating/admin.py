from django.contrib import admin
from django.http import HttpResponseRedirect
from django.conf.urls import url

from .models import Discipline, Standard, Result, ExcelTableFile
from .services.parser_equestrian import _save_page, write_csv, parse, _load_page

admin.site.register(Discipline)
admin.site.register(Standard)
admin.site.register(Result)


@admin.register(ExcelTableFile)
class ImportAdmin(admin.ModelAdmin):
    change_list_template = "import.html"

    def get_urls(self):
        urls = super(ImportAdmin, self).get_urls()
        custom_urls = [
            url('^import/$', self.process_import, name='process_import'),
        ]
        return custom_urls + urls

    def process_import(self, request):
        _save_page()
        write_csv(parse(_load_page()))
        self.message_user(request, f"Успешно импортированно")
        return HttpResponseRedirect("../")