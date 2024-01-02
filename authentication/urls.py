from django.urls import path

from authentication.views import consumer_login_view, consumer_dashboardview, consumer_registration_formview

app_name = "authentication"

urlpatterns = [
    path('consumer_login', consumer_login_view, name='consumer_login'),
    path('consumer_dashboard', consumer_dashboardview, name='consumer_dashboard'),
    path('consumer_registration_form', consumer_registration_formview, name='consumer_registration_form'),

]