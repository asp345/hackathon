from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from .models import UserProfile
from .serializers import UserSerializer,UserProfileSerializer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken,AccessToken
from rest_framework_simplejwt.views import TokenRefreshView
from datetime import datetime, timedelta
from rest_framework_simplejwt.settings import api_settings
from rest_framework.status import HTTP_200_OK
from rest_framework_simplejwt.tokens import AccessToken
from .models import UserProfile
from .serializers import UserSerializer, UserProfileSerializer
from django.contrib import auth
from usermanage.models import usermanage

posts = usermanage.objects.all()

# Create your views here.

#### view
def generate_token_in_serialized_data(user:User, user_profile:UserProfile) -> UserSerializer.data:
    token = RefreshToken.for_user(user)
    refresh_token, access_token = str(token), str(token.access_token)
    serialized_data = UserProfileSerializer(user_profile).data
    serialized_data['token']={"access":access_token, "refresh":refresh_token}
    return serialized_data
def set_token_on_response_cookie(user: User) -> Response:
    token = RefreshToken.for_user(user)
    user_profile = UserProfile.objects.get(user=user)
    user_profile_serializer = UserProfileSerializer(user_profile)
    res = Response(user_profile_serializer.data, status=status.HTTP_200_OK)
    res.set_cookie('refresh_token', value=str(token), httponly=True)
    res.set_cookie('access_token', value=str(token.access_token), httponly=True)
    return res
def signuppage(request):
    return render(request, 'account/signuppage.html')
def test(request):
    return render(request, 'account/index1.html')
def login(request):
    if request.method == 'POST':
        user = auth.authenticate(username=request.POST['username'], password=request.POST['password'])
        auth.login(request, user)
        return redirect('/api/usermanage/page/')
    return render(request, 'account/login.html')
class SignupView(APIView):
    def get(self, request):
        return render(request, 'account/account.html')
    def post(self, request):
        college=request.data.get('college')
        major=request.data.get('major')

        user_serialier = UserSerializer(data=request.data)
        if user_serialier.is_valid(raise_exception=True):
            user = user_serialier.save()
            
        user_profile = UserProfile.objects.create(
            user=user,
            college=college,
            major=major
        )
        return set_token_on_response_cookie(user)

class SigninView(APIView):
    def post(self, request):
        try:
            user = User.objects.get(
                username=request.data['username'],
                password=request.data['password']
            )
        except:
            return Response({"detail": "아이디 또는 비밀번호를 확인해주세요."}, status=status.HTTP_400_BAD_REQUEST)
        user_profile = UserProfile.objects.get(user=user)
        serialized_data = generate_token_in_serialized_data(user, user_profile)
        return set_token_on_response_cookie(user)
    
class LogoutView(APIView):
    def post(self, request):
        if not request.user.is_authenticated:
            return Response({"detail": "로그인 후 다시 시도해주세요."}, status=status.HTTP_401_UNAUTHORIZED)
        RefreshToken(request.data['refresh']).blacklist()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class RefreshTokenView(TokenRefreshView):
    def post(self,request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception = True)
        refresh = serializer.validated_data.get('refresh')
        token = AccessToken.for_user(request.user)
        response = Response({"got it"},status=HTTP_200_OK)
        response.set_cookie(key="access_token",value=str(token),httponly=True)
        return response