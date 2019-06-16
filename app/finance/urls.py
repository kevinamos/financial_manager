from django.urls import path

from app.finance import views

urlpatterns = [
    path('tags/', views.TagListCreateView.as_view()),
    path('tags/<uuid:pk>/', views.TagDetailView.as_view()),
    path('transactions/', views.TransactionListCreateView.as_view()),
    path('transactions/<uuid:pk>/', views.TransactionDetailView.as_view()),
    path('limits/', views.LimitListCreateView.as_view()),
    path('limits/<uuid:pk>/', views.LimitDetailView.as_view()),
    path('', views.AccountListCreateView.as_view()),
    path('<uuid:pk>/', views.AccountDetailView.as_view()),
]
