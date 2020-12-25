from django.urls import path

from rating.views import DefaultView

urlpatterns = [path('', DefaultView.as_view())]

