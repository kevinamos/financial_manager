from django.urls import path

from . import views

urlpatterns = [
    path('', views.UserListView.as_view()),
    path('<uuid:pk>/', views.UserDetailView.as_view()),
    path('register/', views.RegistrationView.as_view()),
    path('login/', views.LoginView.as_view())

]
