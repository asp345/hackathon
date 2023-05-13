from django.shortcuts import render
from rest_framework.response import Response
from .models import usermanage
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
@api_view(['POST'])
def CreateUserView(request):
    realname = request.data.get('realname')
    userid = request.data.get('userid')
    content = request.data.get('content')
    userobj = usermanage.objects.create(realname=realname, userid=userid, content=content)
    return Response({"msg":f"'{userobj.realnane}'이 등록되었습니다"})

@api_view(['GET'])
def ReadAllUserView(request):
    users = usermanage.objects.all()
    contents = [{userobj.title:userobj.content} for userobj in users]
    return Response({"users":contents})