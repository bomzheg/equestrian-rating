from django.contrib import admin

from .models import Discipline, Standard, Result

admin.register(Discipline, Standard, Result)
