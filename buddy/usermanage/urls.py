from django.urls import path
from .views import ReadAllUserView, CreateUserView, UserListView, UserDetailView, UserUpdateView
import usermanage.views as views
app_name = 'usermanage'
urlpatterns = [
    # FBV url path
    path("register_user/", CreateUserView, name='post'),
    path("see_user/", ReadAllUserView, name="get"),
    # CBV url path
    path("", UserListView.as_view()), 
    path("<int:user_id>/", UserDetailView.as_view()),
    path("<int:user_id>/update/", UserUpdateView.as_view()),
    path('page/', views.index, name='index'),
    path('new/', views.new, name='new'),
    path('page/<int:id>/', views.show, name='show'),
    path('page/<int:id>/delete/', views.delete, name='delete'),
]
