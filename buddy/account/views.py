#### 1
from django.contrib.auth.models import User
from .models import UserProfile
from .serializers import UserSerializer, UserProfileSerializer

#### 2
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response


#### view
class SignupView(APIView):
    def post(self, request):
        college = request.data.get("college")
        major = request.data.get("major")

        #### 3
        user_serialier = UserSerializer(data=request.data)
        if user_serialier.is_valid(raise_exception=True):
            user = user_serialier.save()

        user_profile = UserProfile.objects.create(
            user=user, college=college, major=major
        )
        #### 4
        serialized_data = UserProfileSerializer(user_profile).data
        #### 5
        return Response(serialized_data, status=status.HTTP_201_CREATED)


class SigninView(APIView):
    def post(self, request):
        try:
            user = User.objects.get(
                username=request.data["username"], password=request.data["password"]
            )
        except:
            return Response(
                {"detail": "아이디 또는 비밀번호를 확인해주세요."}, status=status.HTTP_400_BAD_REQUEST
            )
        user_profile = UserProfile.objects.get(user=user)
        serialized_data = UserProfileSerializer(user_profile).data
        return Response(serialized_data, status=status.HTTP_200_OK)

class LogoutView(APIView):
    def post(self, request):
        if not request.user.is_authenticated:
            return Response({"detail": "로그인 후 다시 시도해주세요."}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(status=status.HTTP_204_NO_CONTENT)