from django.shortcuts import render
from rest_framework.response import Response
from .models import sound
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from .serializers import UserSerializer
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import time
from django.contrib import messages
import random
from sound import ultrasonic
from .models import usermanage

@csrf_exempt
@api_view(['POST'])
def play_sound(request):
    randomkey=request.POST.get('randint')
    ultrasonic.send_ultrasonic(randomkey,2000,str(randomkey)+'.wav')
    # 오디오 파일을 읽습니다.
    with open(str(randomkey)+'.wav', 'rb') as f:
        recording = f.read()

    # 오디오를 재생합니다.
    response = HttpResponse(recording, content_type='audio/wav')
    response['Content-Length'] = len(recording)

    # 성공 메시지를 보냅니다.
    messages.success(request, 'Sound is playing!')

    return Response({"msg":"키 생성 및 소리 재생 완료"})


@csrf_exempt
@api_view(['POST'])
def record_sound(request):
    # 오디오 녹음을 위한 파일 개체를 만듭니다.
    recid=request.POST.get('receiverid')
    recording = request.FILES['recording']
    # 파일을 서버에 저장합니다.
    with open(recid+'.wav', 'wb') as f:
        f.write(recording.read())
    key=ultrasonic.receive_ultrasonic(16000,recid+'.wav')
    KeyUpdateView.put({"receiverid" : recid},key)
    return HttpResponse('Success!', status=200)
    # 성공 응답을 반환합니다.
    #return HttpResponse('Success!', status=200)

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages




# Create your views here.
@csrf_exempt
@api_view(['POST'])
def CreateTempKey(request):
    senderid = str(request.POST.get('senderid'))
    random_num = str(request.POST.get('randint'))
    keyobj = sound.objects.create(senderid=senderid, random_num=random_num)
    return Response({"msg":f"'{keyobj.senderid}'이 임시 키를 생성했습니다"})

@api_view(['GET'])
def ReadMyKeyView(request):
    receivednum=request.random_num
    keys = sound.objects.filter(random_num=receivednum)
    contents = [{key.senderid:key.random_num} for key in keys]
    return Response({"keys":contents})

from rest_framework.views import APIView
from rest_framework import status

class KeyListView(APIView):

    def get(self, request): 
        keys = sound.objects.all()
        serializer = UserSerializer(keys, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    def post(self, request):
        random_num=request.random_num
        senderid=request.senderid
        key = sound.objects.create(senderid=senderid, random_num=random_num)
        serializer = UserSerializer(key)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class KeyDetailView(APIView):
    def get(self, request, user_id):
        try:
            user = sound.objects.get(id=user_id)
        except:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    def delete(self, request, user_id):
        try:
            user = sound.objects.get(id=user_id)
        except:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    




from .models import sound
from rest_framework.views import APIView
from rest_framework import status
class KeyUpdateView(APIView):
    def put(self, request, random_num):
        try:
            key = sound.objects.get(random_num=random_num)
        except:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(key, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# blogPosts/views.py

def sio(request):
    #users = usermanage.objects.all()
    user=request.user
    return render(request, 'sound/sio.html',{'user': user})