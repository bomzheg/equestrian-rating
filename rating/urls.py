from django.urls import path

from rating import views

urlpatterns = [
    path("about/", views.AboutView.as_view())
]
