from django.urls import path
from .views import ReadAllUserView, CreateUserView

app_name = 'usermanage'
urlpatterns = [
    # FBV url path
    path("register_user/", CreateUserView, name='post'),
    path("see_user/", ReadAllUserView, name="get")
]