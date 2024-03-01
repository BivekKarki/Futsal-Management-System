from django.urls import path

from futsalOwner.views import owner_login_view, owner_registration_formview, owner_dashboardview, verification_view

app_name = "futsalOwner"

urlpatterns = [
    path('', owner_login_view, name='owner_login'),
    path('owner_registration_form', owner_registration_formview, name='owner_registration_form'),
    path('activate/<uidb64>/<token>', verification_view, name='activate'),
    path('owner_dashboard', owner_dashboardview, name='owner_dashboard'),
    # path('owner_logout', owner_logout_view, name='owner_logout'),

]