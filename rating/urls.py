from django.urls import path

from rating.views import JumpingView

urlpatterns = [
    path('jumping/', JumpingView.as_view()),
]
