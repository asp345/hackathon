from django.urls import path
from .views import ReadAllUserView, CreateUserView, UserListView, UserDetailView, UserUpdateView

app_name = 'usermanage'
urlpatterns = [
    # FBV url path
    path("register_user/", CreateUserView, name='post'),
    path("see_user/", ReadAllUserView, name="get"),
    # CBV url path
    path("", UserListView.as_view()), 
    path("<int:user_id>/", UserDetailView.as_view()),
    path("<int:user_id>/update/", UserUpdateView.as_view())
]
