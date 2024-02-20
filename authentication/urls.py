from django.urls import path

from authentication.views import consumer_login_view, consumer_dashboardview, consumer_registration_formview, \
    forgot_password_view, send_otp_view, enter_otp_view, password_reset_view, consumer_update_view

app_name = "authentication"

urlpatterns = [
    path('consumer_login', consumer_login_view, name='consumer_login'),
    path('consumer_dashboard', consumer_dashboardview, name='consumer_dashboard'),
    path('consumer_registration_form', consumer_registration_formview, name='consumer_registration_form'),

    path('forgot_password', forgot_password_view, name='forgot_password'),
    path('send_otp', send_otp_view, name='send_otp'),
    path('enter_otp', enter_otp_view, name='enter_otp'),
    path('password_reset', password_reset_view, name='password_reset'),

    path('consumer_update', consumer_update_view, name='consumer_update'),
]