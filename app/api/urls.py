# api/urls.py
from django.urls import include, path

urlpatterns = [
    path('users/', include('app.accounts.urls')),
    path('account/', include('app.finance.urls')),
    path('rest-auth/', include('rest_auth.urls')),
    path('rest-auth/registration/', include('rest_auth.registration.urls')),
]