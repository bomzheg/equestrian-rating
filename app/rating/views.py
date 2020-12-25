from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic.base import View


class DefaultView(View):
    def get(self, request):
        res = dict(
            number=1,
            date="2020-12-25",
            rider_name="Анна",
            horse_name="Бузина",
            result="100",
            club_name="Алмаз"
        )
        return render(request, 'rating.html', [res])


