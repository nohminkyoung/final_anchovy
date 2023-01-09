from django.shortcuts import render
from anchovy_train.models import Train
from datetime import datetime
from ast import literal_eval
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import HttpResponse
import numpy as np
import time

def index(request):
    return render(request, 'anchovy_train/train.html')

def choice(request):
    return render(request, 'anchovy_train/train_choice.html')

def test(request):
    return render(request, 'anchovy_train/test.html')


def train_result(request):
    login_user = request.user # 로그인 유저
    now = datetime.now() # 현재 날짜 가져오기 위함
    
    # 로그인정보가 같고, 오늘 날짜와 같은 데이터 불러오기
    train_data = Train.objects.filter(username=login_user).filter(train_date=now.date()) 
    train_time_sort = train_data.order_by('-train_time').values() # 최근순으로 정력
    
    
    # 가장 최근 데이터를 set의 값에 따라 가져오도록 만들기 위함 (3세트 하면 3개의 연속된 데이터)
    data_list = []
    for i in range(train_time_sort[0]['train_set']): # 세트 수 만큼 반복
        data_list.append(train_time_sort[i]) # 세트 수에 맞는 데이터들만 가져오기

    all_score = 0
    accurate_score = 0
    for i,data in enumerate(data_list):
        data['set'] = i+1 # 몇번째 세트수인지
        all_score += data['train_all_count'] # 만점일 경우의 점수 
        accurate_score += data['train_accurate_count'] # 정확하게 한 점수
        
    kind = data_list[0]['train_kind'] # 운동 종류 뽑기
    persent = round((accurate_score/all_score)*100) # 몇 퍼센트 달성인지
    
    return render(request, 'anchovy_train/train_result.html',
                  {'data_list':data_list,'all_score':all_score,'accurate_score':accurate_score,'persent':persent,'kind':kind})


'''
     // 푸쉬업 계산을 위한 함수를 전달합니다. 
      /* 0 : nose  /  1 : left_eye_inner  /  2 : left_eye  /  3 : left_eye_outer */
      /* 4 : right_eye_inner  /   5 : right_eye  /  6 : right_eye_outer  /  7 : left_ear */
      /* 8 : right_ear  /  9 : mouth_left  /  10 : mouth_right  /  11 : left_shoulder */ 
      /* 12 : right_shoulder  /  13 : left_elbow  /  14 : right_elbow  /  15 : left_wrist */
      /* 16 : right_wrist  /  17 : left_pinky  /  18 : right_pinky  /  19 : left_index */
      /* 20 : right_index  /  21 : left_thumb  /  22 : right_thumb  /  23 : left_hip  */
      /* 24 : right_hip  /  25 : left_knee  /  26 : right_knee / 27 : left_ankle  */
      /* 28 : right_ankle  /  29 : left_heel  /  30 right_heel  /  31 : left_foot_index */
      /* 32 : right_foot_index  */
'''
def train_train(request):
    return render(request, 'anchovy_train/train_train.html')


def train_practice(request):
    return render(request, 'anchovy_train/train_practice.html')


@csrf_exempt
def push_up(request):
    lis_landmarks = request.POST.get('landmark')
    landmarks = literal_eval(lis_landmarks[1:-1])
    
    check_status = request.POST.get('check_status') # 맨 처음 과정 
    check_stand = request.POST.get('check_stand') # 일어나 있는 목 y값
    full_count = request.POST.get('full_count') # 맨 처음 과정 
    prev = request.POST.get('prev') # 이전 단계
    excellent_count = request.POST.get('excellent_count') # 일어나 있는 목 y값
    score = request.POST.get('score') # 일어나 있는 목 y값
    
    max_set = request.POST.get('max_set') # 일어나 있는 목 y값
    max_count = request.POST.get('max_count') # 일어나 있는 목 y값
    sleep = request.POST.get('sleep') # 일어나 있는 목 y값
    
    
    
    result = {'full_count': int(full_count), 'excellent_count': int(excellent_count), 'check_status': check_status,'prev':prev, 'check_stand': check_stand, 'score': int(score),
              'rest':False}
    
    # 휴식 중일 경우 이전 값 갱신 없이 그대로 보낸다
    if result['rest'] == True:
        print('아직 휴식중입니다.')
        return HttpResponse(json.dumps({'result':result})) 
        
    # 휴식시간 문구 알림
    if full_count == max_count:
        result['rest'] = True
        return HttpResponse(json.dumps({'result':result})) # 초 진행 후 
    
    # 프레임별 같은 화면 일 때는 계산을 진행하지 않고 이전 값 그대로 바로 넘겨라
    if check_status == prev:
        return HttpResponse(json.dumps({'result':result})) 
    
    # 기본 값
    
    # 함수시작 #####################
    # 각도 구하기
    def calculate_angle(a,b,c):
        list_a = [a['x'],a['y']]
        list_b = [b['x'],b['y']]
        list_c = [c['x'],c['y']]
        a = np.array(list_a) # First
        b = np.array(list_b) # Mid
        c = np.array(list_c) # End
        
        radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
        angle = np.abs(radians*180.0/np.pi)

        
        if angle >180.0:
            angle = 360-angle
            
        return angle 
    
    # 엉덩이 각도 구하기 
    def rev_calculate_angle(a,b,c):
        list_a = [a['x'],a['y']]
        list_b = [b['x'],b['y']]
        list_c = [c['x'],c['y']]
        a = np.array(list_a) # First
        b = np.array(list_b) # Mid
        c = np.array(list_c) # End
        
        radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
        angle = np.abs(radians*180.0/np.pi)
        
        angle = 360 - angle
        
        return angle 
    
    # 거리구하기
    def calculate_width(a,b):
        list_a = [a['x'],a['y']]
        list_b = [b['x'],b['y']]
        a = np.array(list_a) # First
        b = np.array(list_b) # End   
        
        width = ((a[1]-b[1])**2+(a[0]-b[0])**2)**0.5
        
        return width
    
    ##########################
    # 변수 받아오기 --> 10초 후 구현이 필요하네    
    l_elbow = landmarks[13]
    r_elbow = landmarks[14]
    l_shoulder = landmarks[11]
    r_shoulder= landmarks[12]
    l_hip = landmarks[23]
    r_hip = landmarks[24]
    l_knee = landmarks[25]
    r_knee = landmarks[26]
    l_ankle = landmarks[27]
    r_ankle = landmarks[28]
    l_eye = landmarks[2]
    r_eye = landmarks[5]
    nose = landmarks[0]
    l_wrist = landmarks[15]
    r_wrist = landmarks[16]
    
    #########################################
    
    # 대기 시간 (코 y좌표 위치 지정) 
    if result['check_status'] == '1':
        #print('올림 좌표 고정')
        result['check_stand'] = landmarks[0]['y'] # 처음 시작 시 목의 y값을 지정 
        result['prev'] = '1'
        result['check_status'] = '2' # 푸쉬업 내림 완료 단계 변경
        return HttpResponse(json.dumps({'result':result})) 
    
    # 푸쉬업 내림 시작
    elif result['check_status'] == '2':
        #print('내려갔다!!!!!!!')
        if (nose['y'] - float(check_stand) >=0.2) and (calculate_angle(l_shoulder, l_elbow, l_wrist)<100) :
            # 팔꿈치 각도 59 ~ 89
            if (60<=int(calculate_angle(l_shoulder, l_elbow, l_wrist)))and (int(calculate_angle(l_shoulder, l_elbow, l_wrist))<=90):
                result['score'] = result['score'] + 1
                print('팔꿈치 다운')
            else:
                print('팔꿈치 다운',calculate_angle( l_shoulder, l_elbow, l_wrist))
            # 겨드랑이 각도 1 ~ 19
            if (0<=int(calculate_angle( l_elbow, l_shoulder, l_hip)))and (int(calculate_angle( l_elbow, l_shoulder, l_hip))<=20): 
                result['score'] = result['score'] + 1
                print('겨드랑이 다운')
            else:
                print('겨드랑이 다운',calculate_angle( l_elbow, l_shoulder, l_hip))
            # 엉덩이 각도 160 ~ 180 .... 난이도 개빡셈
            if (160<int(rev_calculate_angle(l_shoulder, l_hip, l_knee)))and (int(rev_calculate_angle(l_shoulder, l_hip, l_knee)<=180)): # 엉덩이
                result['score'] = result['score'] + 1
                print('엉덩이 다운')
            else:
                print('엉덩이 다운',rev_calculate_angle(l_shoulder, l_hip, l_knee))
            # 목 각도 75 ~ 95
            if (75<=int(calculate_angle(l_eye, nose, l_shoulder)))and (int(calculate_angle(l_eye, nose, l_shoulder))<=95): 
                result['score'] = result['score'] + 1
                print('목 다운')
            else:
                print('목 다운',calculate_angle( l_eye, nose, l_shoulder))
            # 팔 너비와 팔 너비 비교 완료
            if (calculate_width(l_shoulder,r_shoulder)*1.2 < calculate_width(l_wrist,r_wrist)) \
                and (calculate_width(l_shoulder,r_shoulder)*1.5 > calculate_width(l_wrist,r_wrist)) : 
                result['score'] = result['score'] + 1
                print('팔 너비 다운')
            result['prev'] = '2'
            result['check_status'] = '3' # 푸쉬업 내림 완료 단계 변경
        return HttpResponse(json.dumps({'result':result})) 
    
    # 푸쉬업 내림 완료 (코 y좌표 체크)
    elif result['check_status'] == '3':
        #print('내림 좌표 고정!')
        result['check_stand'] = landmarks[0]['y'] # 처음 시작 시 목의 y값을 지정
        result['prev'] = '3'
        result['check_status'] = '4' #푸쉬업 내림 시작 단계 변경 
        
        return HttpResponse(json.dumps({'result':result})) 
    
    
    # 푸쉬업 오름 시작
    elif result['check_status'] == '4':
        #print('올라갔다 !!!!!!!!!')
        if (float(check_stand)-nose['y'] >= 0.2) and (calculate_angle(l_shoulder, l_elbow, l_wrist)>100) : 
            if (165<=int(calculate_angle(l_shoulder, l_elbow, l_wrist)))and(int(calculate_angle(l_shoulder, l_elbow, l_wrist))<=180): # 팔꿈치
                result['score'] = result['score'] + 1
                print('팔꿈치 스탠드')
            else:
                print('팔꿈치 스탠드 ',calculate_angle(l_shoulder, l_elbow, l_wrist))
                
            if (35<=int(calculate_angle( l_elbow, l_shoulder, l_hip)))and (int(calculate_angle( l_elbow, l_shoulder, l_hip))<=60): # 겨드랑이
                result['score'] = result['score'] + 1
                print('겨드랑이 스탠드')
            else:
                print('겨드랑이 스탠드',calculate_angle( l_elbow, l_shoulder, l_hip))
            if (160<=int(rev_calculate_angle(l_shoulder, l_hip, l_knee)))and(int(rev_calculate_angle(l_shoulder, l_hip, l_knee))<=180): # 엉덩이
                result['score'] = result['score'] + 1
                print('엉덩이 스탠드')
            else:
                print(rev_calculate_angle(l_shoulder, l_hip, l_knee))
                
            if (140<=int(calculate_angle(l_hip, l_knee, l_ankle)))and(int(calculate_angle(l_hip, l_knee, l_ankle))<=170): # 무릎
                result['score'] = result['score'] + 1
                print('무릎 스탠드')
            else:
                print('무릎 스탠드',calculate_angle(l_hip, l_knee, l_ankle))
            if (75<=int(calculate_angle(l_eye, nose, l_shoulder)))and(int(calculate_angle(l_eye, nose, l_shoulder))<=95): # 목
                result['score'] = result['score'] + 1
                print('목 스탠드')
            else:
                print('목 스탠드',calculate_angle(l_eye, nose, l_shoulder))
                
            if (calculate_width(l_shoulder,r_shoulder)*1.2 < calculate_width(l_wrist,r_wrist)) \
                and (calculate_width(l_shoulder,r_shoulder)*1.5 > calculate_width(l_wrist,r_wrist)) : # 팔 너비
                result['score'] = result['score'] + 1
                print('팔 너비 스탠드')
            result['prev'] = '4'
            result['check_status'] = '5' #푸쉬업 내림 시작 단계 변경
        return HttpResponse(json.dumps({'result':result})) 
    
    # 계산 값 정산 시작
    elif result['check_status'] == '5':
        print('점수 정산 중')
        if result['score'] > 6: # 7점 이상일 경우에만 진행
            result['score'] = 0
            result['excellent_count'] = result['excellent_count'] + 1
            result['full_count'] =  result['full_count'] + 1
            result['check_status'] = '1' #푸쉬업 내림 시작 단계 변경 
            result['prev'] = '5'
        else:
            result['score'] = 0
            result['full_count'] =  result['full_count'] + 1
            result['check_status'] = '1' #푸쉬업 내림 시작 단계 변경 
            result['prev'] = '5'
        
            
        return HttpResponse(json.dumps({'result':result})) 
          


    # 4번 진행 시 풀카운트가 받아온 값과 동일 해질 때까지 1~4번 과정을 반복한다.