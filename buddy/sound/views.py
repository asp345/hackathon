from django.shortcuts import render
from rest_framework.response import Response
from .models import sound
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from .serializers import UserSerializer
from django.http import StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt
import time
from django.contrib import messages
import random
from sound import ultrasonic
from .models import usermanage
import pydub

@csrf_exempt
@api_view(['POST'])
def play_sound(request):
    randomkey=request.POST.get('randint')
    ultrasonic.send_ultrasonic(randomkey, 12000, 'sound/static/sound/'+str(randomkey)+'.wav')
    time.sleep(1)
    # 오디오 파일을 읽습니다.
    """  fl=pydub.AudioSegment.from_wav('sound/static/sound/'+str(randomkey)+'.wav')
    fl.export(str(randomkey)+'.flac',format='flac')
    """
    with open('sound/static/sound/'+str(randomkey)+'.wav', 'rb') as f:
        recording = f.read()

    # 오디오를 재생합니다.
    response = StreamingHttpResponse(streaming_content=(chunk for chunk in recording), content_type='audio/wav')
    response['Content-Length'] = len(recording)
    return response


@csrf_exempt
@api_view(['PUT'])
def record_sound(request):
    # 오디오 녹음을 위한 파일 개체를 만듭니다.
    recid=request.PUT.get('receiverid')
    recording = request.FILES['recording']
    # 파일을 서버에 저장합니다.
    with open(recid+'.wav', 'wb') as f:
        f.write(recording.read())
    key=ultrasonic.receive_ultrasonic(12000,recid+'.wav')
    KeyUpdateView.put({"receiverid" : recid},key)
    return HttpResponse('Success!', status=200)
    # 성공 응답을 반환합니다.
    #return HttpResponse('Success!', status=200)

import os
from django.conf import settings
from django.core.files.storage import default_storage
from django.http import JsonResponse

def record_audio(request):
    if request.method == 'PUT':
        audio_file = request.FILES.get('audio')

        # 파일 저장 경로
        file_path = default_storage.save('recorded_audio.wav', audio_file)

        # 여기서부터 음성 데이터를 처리하는 로직을 구현합니다.
        # 예시로 파일 경로를 출력하는 코드를 작성합니다.
        full_file_path = os.path.join(settings.MEDIA_ROOT, file_path)
        print('음성 데이터가 저장되었습니다:', full_file_path)
        rep=ultrasonic.receive_ultrasonic(12000,'record_audio.wav')
        # 음성 데이터 처리 완료 후 응답을 반환합니다.
        return JsonResponse({'message': rep})

    # PUT 요청 외에 다른 요청 방식은 허용하지 않습니다.
    return JsonResponse({'message': '잘못된 요청입니다.'}, status=400)


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