from rest_framework.serializers import ModelSerializer
from .models import usermanage

class UserSerializer(ModelSerializer):
    class Meta:
        model = usermanage
        fields = "__all__"