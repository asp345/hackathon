from django.urls import path
from .views import ReadMyKeyView, CreateTempKey, KeyListView, KeyDetailView, KeyUpdateView, play_sound, record_audio

app_name = 'sound'
urlpatterns = [
    # FBV url path
    path("play_sound/", play_sound, name='post'),
    path("addkey/", CreateTempKey, name='post'),
    path("editkey/", KeyUpdateView.as_view(), name='put'),
    path("record_sound/", record_audio, name="put"),
    # CBV url path
    path("", KeyListView.as_view()), 
    path("<int:random_num>/", KeyDetailView.as_view()),
    path("<int:random_num>/update/", KeyUpdateView.as_view()),
]