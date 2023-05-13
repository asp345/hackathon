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
