from django.shortcuts import render
from django.views.generic.base import View

from rating.models import Standard, Result, Discipline


class JumpingView(View):
    def get(self, request):
        disciplines = Discipline.objects.all()
        current_discipline = disciplines[0]
        standards = Standard.objects.filter(discipline=current_discipline).all()
        results = Result.objects.filter(fulfilled_standard=standards[0]).all()
        return render(request, 'jumping_rating.html', {
            "results": results,
            "standard": standards[0],
            "discipline": current_discipline,
            "standards": standards
        })
