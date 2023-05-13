from django.urls import path
from . import views
path('<int:question_id>/', views.detail, name='detail')