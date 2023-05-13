from django.shortcuts import render
from rest_framework.response import Response
from .models import usermanage
from django.http import HttpResponse
def CreatePostView(request):
    realname = request.data.get('realname')
    userid = request.data.get('userid')
    content = request.data.get('content')
    userobj = usermanage.objects.create(realname=realname, userid=userid, content=content)
    return Response({"msg":f"'{userobj.realnane}'이 등록되었습니다"})

def detail(request, question_id):
    return HttpResponse("You're looking at question %s." % question_id)