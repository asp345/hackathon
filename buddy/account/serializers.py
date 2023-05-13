from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User
from .models import UserProfile

### 🔻 이 부분만 추가 ####
from rest_framework.serializers import ValidationError

### 🔺 이 부분만 추가 ####


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "password", "email"]

    ### 🔻 이 부분만 추가 ####
    def validate(self, attrs):
        username = attrs.get("username", "")
        password = attrs.get("password", "")
        email = attrs.get("email", "")
        if not (username and password and email):
            raise ValidationError(
                {"detail": "[email, password, username] fields missing."}
            )
        return attrs


### 🔺 이 부분만 추가 ####
### 방금 붙인 코드 아래에 붙여주세요! ###
from .models import UserProfile


class UserProfileSerializer(ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = UserProfile
        fields = "__all__"

class UserIdUsernameSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username"]