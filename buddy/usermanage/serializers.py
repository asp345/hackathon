from rest_framework.serializers import ModelSerializer
from .models import usermanage
from account.serializers import UserIdUsernameSerializer

class UserSerializer(ModelSerializer):
    author = UserIdUsernameSerializer(read_only=True)
    class Meta:
        model = usermanage
        fields = "__all__"
