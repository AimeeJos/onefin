from django.urls import path
from core import views

app_name = "core"

urlpatterns = [
    path("register", views.CreateUser.as_view(), name="register"),
    # path("list-users", views.ListUsers.as_view()),
    path('login/', views.UserLogin.as_view(), name='login'),
    path('request-count/', views.RequestCount.as_view(), name="request-count"),
    path('request-count/reset/', views.ResetCount.as_view(), name="reset-count"),
    
    
]
