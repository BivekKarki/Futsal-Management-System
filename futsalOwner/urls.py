from django.urls import path

from futsalOwner.views import owner_login_view

app_name = "futsalOwner"

urlpatterns = [
    path('', owner_login_view, name='owner_login'),


]