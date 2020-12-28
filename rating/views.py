from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic.base import View

from rating.models import Standard, Result


class DefaultView(View):
    def get(self, request):
        standard = Standard.objects.get(id=1)
        results = Result.objects.filter(fulfilled_standard=standard).all()
        return render(request, 'rating.html', {"results": results, "standard": standard, "discipline": standard.discipline})
