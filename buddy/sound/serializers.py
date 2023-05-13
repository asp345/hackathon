from rest_framework.serializers import ModelSerializer
from .models import sound
from account.serializers import UserIdUsernameSerializer

class UserSerializer(ModelSerializer):
    author = UserIdUsernameSerializer(read_only=False)
    class Meta:
        model = sound
        fields = "__all__"
