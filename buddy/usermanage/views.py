from django.shortcuts import render
from rest_framework.response import Response
from .models import usermanage
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
@api_view(['POST'])
def CreateUserView(request):
    author = request.user
    if not author.is_authenticated:
            return Response({"detail": "Authentication credentials not provided"}, status=status.HTTP_401_UNAUTHORIZED)
    realname = request.data.get('realname')
    userid = request.data.get('userid')
    content = request.data.get('content')
    userobj = usermanage.objects.create(realname=realname, userid=userid, content=content)
    return Response({"msg":f"'{userobj.realname}'이 등록되었습니다"})

@api_view(['GET'])
def ReadAllUserView(request):
    users = usermanage.objects.all()
    contents = [{userobj.realname:userobj.content} for userobj in users]
    return Response({"users":contents})

from .serializers import UserSerializer
from rest_framework.views import APIView
from rest_framework import status

class UserListView(APIView):

    def get(self, request): 
        users = usermanage.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    def post(self, request):
        author = request.user
        realname = request.data.get('realname')
        userid = request.data.get('userid')
        content = request.data.get('content')
        if not author.is_authenticated:
            return Response({"detail": "Authentication credentials not provided"}, status=status.HTTP_401_UNAUTHORIZED)
        if not realname or not userid or not content:
            return Response({"detail": "[realname, userid, content] fields missing."}, status=status.HTTP_400_BAD_REQUEST)
        user = usermanage.objects.create(realname=realname, userid=userid, content=content, author = author)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserDetailView(APIView):
    def get(self, request, user_id):
        try:
            user = usermanage.objects.get(id=user_id)
        except:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    def delete(self, request, user_id):
        try:
            user = usermanage.objects.get(id=user_id)
        except:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
#수정하는 함수 안짬

from .models import usermanage
from .serializers import UserSerializer
from rest_framework.views import APIView
from rest_framework import status

class UserUpdateView(APIView):
    def put(self, request, user_id):
        try:
            user = usermanage.objects.get(id=user_id)
        except:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
