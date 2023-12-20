from django.contrib import auth
from django.contrib.auth import authenticate
#from django.contrib.auth.models import User
from .models import User
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from .forms import CustomUserChangeForm, CustomUserCreationForm
import requests
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.authtoken.models import Token



def signup(request):
    if request.method == 'POST':
        if request.POST['password1'] == request.POST['password2']:
            user = User.objects.create_user(
                                            username=request.POST['username'],
                                            password=request.POST['password1'],
                                            useremail=request.POST['email'],
                                            weight=request.POST['weight'],
                                            diabetes=request.POST['diabetes'],
                                            blood_pressure=request.POST['blood_pressure']
                                            )
            auth.login(request, user)
            return redirect('/')
        return render(request, 'accounts/signup.html')
    return render(request, 'accounts/signup.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('post_list')
        else:
            return render(request, 'accounts/login.html', {'error': 'username or password is incorrect.'})
    else:
        return render(request, 'accounts/login.html')

def logout(request):
    auth.logout(request)
    return redirect('home')

def home(request):
    return render(request, 'accounts/home.html')

def app_login_first(request):
    if request.method == 'POST':
        
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(username=username, password=password)
        
        HOST = 'http://192.168.0.102:8000'
        res = requests.post(HOST + '/api-token-auth/', {
            'username':username,
            'password':password,
            })
        res.raise_for_status()
        token = res.json()['token']
        
        if user:
            #auth.login(request, user)
            user_me = User.objects.get(username=username)
            user_me_list = {
                            'useremail': user_me.useremail, 
                            'username': user_me.username,
                            'age': user_me.age, 
                            'sex': user_me.sex, 
                            'weight': str(user_me.weight), 
                            'diabetes': str(user_me.diabetes), 
                            'blood_pressure': str(user_me.blood_pressure)
                            }
            
            response_data = {
                'code': '0000',
                'msg': '로그인성공입니다.',
                'token': token,
                'user_info': user_me_list
            }
            #user_list = serializers.serialize('json', users, ensure_ascii=False)
            #return HttpResponse(response_data, content_type="text/json-comment-filtered")
            return JsonResponse(response_data, status=200)
        else:
            return JsonResponse({'code': '1001', 'msg': '로그인실패입니다.'}, status=200)
    else:
        return render(request, 'accounts/login.html')
    
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
def app_login(request):
    if request.method == 'POST':
        
        
        authorization_header = request.META.get('HTTP_AUTHORIZATION', '')
        token = Token.objects.get(key=authorization_header)
        user = token.user #choi
        
        #username = token.user
        #user = authenticate(username=username, password=password)
        
        if user:
            #auth.login(request, user)
            user_me = User.objects.get(username=user)
            user_me_list = {
                            'username': user_me.username,
                            'useremail': user_me.useremail, 
                            'nickname': user_me.nickname, 
                            'introduce_text': user_me.introduce_text, 
                            'profile_img': str(user_me.profile_img), 
                            'background_img': str(user_me.background_img), 
                            'propensity': user_me.propensity
                            }
            
            response_data = {
                'code': '0000',
                'msg': '로그인성공입니다.',
                #'token': token,
                'user_info': user_me_list
            }
            #user_list = serializers.serialize('json', users, ensure_ascii=False)
            #return HttpResponse(response_data, content_type="text/json-comment-filtered")
            return JsonResponse(response_data, status=200)
        else:
            return JsonResponse({'code': '1001', 'msg': '로그인실패입니다.'}, status=200)
    else:
        return render(request, 'accounts/login.html')    
    
    
def app_signup(request):
    if request.method == 'POST':
        if request.POST['password1'] == request.POST['password2']:
            
            user = User.objects.create_user(
                                            username=request.POST['username'],
                                            password=request.POST['password1'],
                                            useremail=request.POST['email'],
                                            weight=request.POST['weight'],
                                            diabetes=request.POST['diabetes'],
                                            blood_pressure=request.POST['blood_pressure'],)
            auth.login(request, user)
            
            return JsonResponse({'code': '0000', 'msg': '회원가입 성공입니다.'}, status=200)
            
        else:
            return JsonResponse({'code': '1001', 'msg': '회원가입 실패입니다.'}, status=200)
        return render(request, 'accounts/signup.html')
    return render(request, 'accounts/signup.html')
    
def user_json(request):
    users = User.objects.all()
    user_list = serializers.serialize('json', users, ensure_ascii=False)
    return HttpResponse(user_list, content_type="text/json-comment-filtered")

def update(request):
    if request.method == "POST":
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            user = form.save(commit=False)
            
            try:
	            user.profile_img = request.FILES['profile_img']
            except:
	            user.profile_img = user.profile_img
            
            try:
	            user.background_img = request.FILES['background_img']
            except:
	            user.background_img = user.background_img
            
            user.save()
            return redirect('post_list')
    else:
        form = CustomUserChangeForm(instance=request.user)
    context = {'form':form}
    return render(request, 'accounts/update.html', context)

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
def app_update(request):
    if request.method == "POST":
        
        authorization_header = request.META.get('HTTP_AUTHORIZATION', '')
        token = Token.objects.get(key=authorization_header)
        user = token.user
        
        form = CustomUserChangeForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            
            user = form.save()

            # 프로필 이미지 및 배경 이미지 업로드 처리
            if 'profile_img' in request.FILES:
                user.profile_img = request.FILES['profile_img']
            if 'background_img' in request.FILES:
                user.background_img = request.FILES['background_img']

            user.save()
            return JsonResponse({'code': '0000', 'msg': '회원정보 수정 성공입니다.'}, status=200)
        else:
            # 폼이 유효하지 않을 때 오류 메시지 반환
            return JsonResponse({'code': '1001', 'msg': '회원정보 수정 실패입니다.'}, status=200)
    else:
        form = CustomUserChangeForm(instance=request.user)
        context = {'form': form}
        return render(request, 'accounts/update.html', context)
    
    
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
def get_username(request):
    # 현재 요청을 보낸 사용자의 username을 가져옵니다.
    #username = request.user.username
    
    #token_value = "fa580e9df802c0e85cce4144e329507d479826dd"
    authorization_header = request.META.get('HTTP_AUTHORIZATION', '')
    
    token = Token.objects.get(key=authorization_header)
    user = token.user
    username = user.username
    
    # username을 응답으로 반환합니다.
    return Response({'username': username})


