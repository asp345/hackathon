from django.urls import path
from .views import SignupView,SigninView,LogoutView,RefreshTokenView
import account.views as views


app_name = 'account'
urlpatterns = [
    path("signup/", SignupView.as_view()),
    path("signin/", SigninView.as_view()),
    path("logout/", LogoutView.as_view()),
    path("refresh/",RefreshTokenView.as_view()),
    path('signuppage/',views.signuppage, name='signuppage'),
    path('login/', views.login, name='login')
    
    ] # 추가]