from django.contrib import auth
from django.contrib.auth import authenticate,login
from django.shortcuts import render, redirect
from anchovy_common.forms import UserForm
from anchovy_common.models import User_status, Custom_User
from datetime import datetime, date, time
import re 

import json # Ajax를 통해 json을 보내기 위해서 import
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse # 데이터만 html에 전달 시 사용 


def make_login(request): #auth의 login과 혼동이 안되게 이름 지정
    if request.method == 'POST': # 포스트 방식으로 넘어올때
        username = request.POST.get('username', None)  # input으로 받아진 데이터들
        password = request.POST.get('password', None)
        
        # 입력된 데이터를 활용해 일치하는 유저 데이터
        user = auth.authenticate(request, username=username, password=password) 
        errMsg={}
        
        # 유저가 존재하면 로그인 
        if user is not None: 
            login(request, user) #auth의 로그인을 이용해 로그인
            return redirect('main') # 로그인 후 인덱스 페이지로 이동
        
        # 에러메세지 시작
        elif not (username and password): # 아이디나 비번이 하나라도 없을때 
            errMsg['error'] = "모든 값을 입력하세요"
            
        else:  # 그 외의 모든 잘못된 것들 
                errMsg['error'] = "아이디와 비밀번호를 확인해주세요."
                
    else: # 포스트가 아닌 방식으로 넘어올 때
        return render(request, 'anchovy_common/login3.html')
                
    return render(request, 'anchovy_common/login3.html', errMsg) # 에레메세지와 같이 불러오기





def signup(request):
    if request.method == "POST": # 포스트로 넘어올 때 
        
        form = UserForm(request.POST) 
        duplication = request.POST.get('duplication_check') 
        nickname = request.POST.get('nickname',None) #input으로 받아진 데이터
        username = request.POST.get('username',None) 
        password1 = request.POST.get('password1',None)
        password2 = request.POST.get('password2',None)
        errMsg={}
        now = datetime.now()
        error_check = 0 # 에러 체크용

        reg = re.compile(r'^[A-Z|a-z|1-9]+$')

         # 에러시작
        #닉네임 에러
        if ' ' in nickname : 
            errMsg['error_nick'] ='* 닉네임에는 공백을 추가 할 수 없습니다.'
            error_check = 1
            
        elif not nickname :
            errMsg['error_nick'] ='* 닉네임은 필수사항입니다.'
            error_check = 1

        #아이디 에러
        if ' ' in username :
            errMsg['error_id'] ='* 아이디에는 공백을 추가 할 수 없습니다.'
            error_check = 1
        elif not username :
            errMsg['error_id'] ='* 아이디는 필수사항 입니다.'
            error_check = 1
        elif duplication == '0':
            errMsg['error_id'] ='* 중복체크를 진행해주세요'
            error_check = 1
        elif not reg.match(username):
            errMsg['error_id'] ='* 아이디에서 한글은 포함할 수 없습니다.'
        

        # 이미 한번 중복체크를 했다면 그 다음에는 진행할 필요 없도록 만들기
        if duplication == '1':
            errMsg['duplication_check'] = 1
        
        #pw1만의 에러
        if not password1 :
            errMsg['error_pw1'] = '* 비밀번호는 필수사항 입니다. '
            error_check = 1
        
        elif password1.isdigit() :
            errMsg['error_pw1'] = '* 비밀번호가 전부 숫자로만 되어 있습니다. '
            error_check = 1
        
         #pw1+pw2의 에러
        else:  
            if password1 != password2:
                errMsg['error_pw2_no'] = '* 비밀번호를 다시 확인해주세요'
                error_check = 1

        # 위 작업에서 에러가 체킹 되었다면 회원가입을 진행하지 않고 반환한다.
        if error_check == 1:    
            return render(request, 'anchovy_common/signup2.html',{'form': form, 'errMsg':errMsg}) #에러메세지와 같이 불러오기
        
        # 오류가 없다면 회원가입을 진행한다.
        else:
            # find_korean = re.compile('[ㄱ-ㅣ가-힣]')
            if  form.is_valid(): # 회원가입 폼
                form.save()
                username = form.cleaned_data.get('username')
                raw_password = form.cleaned_data.get('password1')
                user = authenticate(username=username, password=raw_password)  # 사용자 인증
                login(request, user)  # 로그인
                
                # user_status에 테이블 자동 생성################################
                log_user = Custom_User.objects.get(username=request.user)
            
                create_date = date(now.year, now.month, now.day)
                create_time = time(now.hour, now.minute, 0)

                # User_status(모델에 생성한 class이름 사용)의 각 컬럼에 들어갈 데이터 들을 지정해줌(컬럼명=데이터)
                status_data = User_status(author_id = log_user.id, username=log_user.username, nickname=log_user.nickname, 
                                        protein=0, coupon = 0, recent_date = create_date, recent_time=create_time, 
                                        character_lv=0, week_train_count=0)

                # 반드시 save를 해줘야 데이터가 저장됨
                status_data.save()
                
                return redirect('tutorial')
            
       
    else: # 포스트 아닐 때 
        form = UserForm()
    
    return render(request, 'anchovy_common/signup2.html',{'form': form}) #form을 통헤 db에 저장

def tutorial(request):
    return render(request, 'anchovy_common/tutorial.html')
    
    
@csrf_exempt 
def duplication(request):
    if request.POST:
        if request.POST.get('id') == '':
            result = 2
            return HttpResponse(json.dumps({'duplication': result }))

        else:
            try: 
                check_id = request.POST.get('id')
                Custom_User.objects.get(username=check_id)
            # 존재하지 않았을 경우
            except Custom_User.DoesNotExist:
                result = 1
            # 이미 존재하는 경우
            else:
                result = 0
            finally:
                reg = re.compile(r'^[A-Z|a-z|1-9]+$')
                if not reg.match(check_id):
                    result = 3
                
            
            return HttpResponse(json.dumps({'duplication': result }))