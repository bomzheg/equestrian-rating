from django.urls import path

from app.rating.views import DefaultView

urlpatterns = [path('/', DefaultView.as_view())]

