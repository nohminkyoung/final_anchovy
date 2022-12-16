from django.contrib import auth
from django.contrib.auth import authenticate,login
from django.shortcuts import render, redirect
from anchovy_common.forms import UserForm


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


def logout(request):
    auth.logout(request)
    return redirect('login')




def signup(request):
    if request.method == "POST": # 포스트로 넘어올 때 
        
        form = UserForm(request.POST) 
        nickname = request.POST.get('nickname',None) #input으로 받아진 데이터
        username = request.POST.get('username',None) 
        password1 = request.POST.get('password1',None)
        password2 = request.POST.get('password2',None)        
        errMsg={}
        
        
        if  form.is_valid(): # 회원가입 폼
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)  # 사용자 인증
            login(request, user)  # 로그인
            return redirect('tutorial')
            
        # 에러시작
        #닉네임 에러
        if " " in nickname : 
            errMsg['error_nick'] ='* 닉네임에는 공백을 추가 할 수 없습니다.'
            
        elif not nickname :
            errMsg['error_nick'] ='* 닉네임은 필수사항입니다.'
        
        #아이디 에러
        if " " in username :
            errMsg['error_id'] ='* 아이디에는 공백을 추가 할 수 없습니다.'
        elif not username :
            errMsg['error_id'] ='* 아이디는 필수사항 입니다.'
        
        
        #pw1만의 에러
        if not password1 :
            errMsg['error_pw1'] = '* 비밀번호는 필수사항 입니다. '
        
        elif password1.isdigit() :
            errMsg['error_pw1'] = '* 비밀번호가 전부 숫자로만 되어 있습니다. '
        
         #pw1+pw2의 에러
        else:  
            if password1 != password2:
                errMsg['error_pw2_no'] = '* 비밀번호를 다시 확인해주세요'
            elif password1 == password2:
                errMsg['error_pw2_ok'] = '* 사용가능한 비밀번호입니다'

                
        return render(request, 'anchovy_common/signup2.html',{'form': form, 'errMsg':errMsg}) #에러메세지와 같이 불러오기
    
    else: # 포스트 아닐 때 
        form = UserForm()
    
    return render(request, 'anchovy_common/signup2.html',{'form': form}) #form을 통헤 db에 저장

def tutorial(request):
    return render(request, 'anchovy_common/tutorial.html')
    
    
    