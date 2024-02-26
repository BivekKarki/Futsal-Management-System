from django.urls import path

urlpatterns = [
    path('', consumer_login_view, name='consumer_login'),


]