import os
from uuid import uuid4
from django.shortcuts import render
from rest_framework.views import APIView

# makepassword import
from django.contrib.auth.hashers import make_password, check_password
# Response import
from rest_framework.response import Response

from django_study.settings import MEDIA_ROOT

from .models import User

# Create your views here.
class Join(APIView):
    def get(self, request):
        return render(request, 'user/join.html')
    # todo 회원가입 
    def post(self, request):
        email = request.data.get("email", None)
        user_id = request.data.get("user_id", None)
        name = request.data.get("name", None)
        password = request.data.get("password", None)

        User.objects.create(email= email, user_id= user_id, name= name, password= make_password(password), profile_image= "default_profile.jpg")

        return  Response(status=200)

class LogIn(APIView):
    def get(self, request):
        return render(request, 'user/login.html')

    def post(self, request):
        # todo 로그인  
        email = request.data.get("email", None)
        password = request.data.get("password", None)

        user = User.objects.filter(email= email).first()

        if user is None:
            return Response(status=400, data={"message": "회원정보가 잘못되었습니다."})

        if user.check_password(password):
            
            request.session['email'] = email

            return Response(status=200)
        else:
            return Response(status=400, data={"message": "회원정보가 잘못되었습니다."})
    
class LogOut(APIView):
    def get(self, request):
        request.session.flush()
        return render(request, 'user/login.html')
    
class UploadProfile(APIView):
    def post(self, request):
        file = request.FILES['file']
        
        email = request.data.get('email')
        uuid_name = uuid4().hex
        save_path = os.path.join(MEDIA_ROOT, uuid_name)

        with open(save_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        profile = uuid_name
        user = User.objects.filter(email= email).first()

        user.profile_image = profile

        user.save()

        return Response(status=200)