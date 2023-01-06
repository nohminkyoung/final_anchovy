from django.shortcuts import render
from anchovy_train.models import Train
from datetime import datetime
from ast import literal_eval
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import HttpResponse
import numpy as np

def index(request):
    return render(request, 'anchovy_train/train.html')

def choice(request):
    return render(request, 'anchovy_train/train_choice.html')



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

@csrf_exempt
def push_up(request):
    lis_landmarks = request.POST.get('landmark')
    landmarks = literal_eval(lis_landmarks[1:-1])
    
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
    
    # 변수 받아오기 
    first_y = {}
    if first_y == {}:
        first_y = landmarks[0]['y']
    else:
        pass
    
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
    # 점수 만들기 
    score = 0
    result = {'full_count': 0, 'excellent_count': 0}
    # down
    # print(first_y - nose['y'])
    print(first_y)
    print(nose['y'])
    print(calculate_angle(l_shoulder, l_elbow, l_wrist))
    if (first_y - nose['y'] >=0.2) and (calculate_angle(l_shoulder, l_elbow, l_wrist)<100) : 
        print('내려가기~~!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        if (60<calculate_angle(l_shoulder, l_elbow, l_wrist))and(calculate_angle(l_shoulder, l_elbow, l_wrist)<90): # 팔꿈치
            score += 1
        if (0<calculate_angle( l_elbow, l_shoulder, l_hip))and(calculate_angle( l_elbow, l_shoulder, l_hip)<20): # 겨드랑이
            score += 1
        if (160<rev_calculate_angle(l_shoulder, l_hip, l_knee))and(rev_calculate_angle(l_shoulder, l_hip, l_knee)<180): # 엉덩이
            score += 1
        if (140<calculate_angle(l_hip, l_knee, l_ankle))and(calculate_angle(l_hip, l_knee, l_ankle)<170): # 무릎
            score += 1
        if (75<calculate_angle(l_eye, nose, l_shoulder))and(calculate_angle(l_eye, nose, l_shoulder)<95): # 목
            score += 1
        if (calculate_width(l_shoulder,r_shoulder)*1.2 < calculate_width(l_wrist,r_wrist)) \
            and (calculate_width(l_shoulder,r_shoulder)*1.5 > calculate_width(l_wrist,r_wrist)) : # 팔 너비
            score += 1
            
        # up
        if (first_y - nose['y'] <0.2) and (calculate_angle(l_shoulder, l_elbow, l_wrist)>100) : 
            print('올라가기~~!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
            if (165<calculate_angle(l_shoulder, l_elbow, l_wrist))and(calculate_angle(l_shoulder, l_elbow, l_wrist)<180): # 팔꿈치
                score += 1
            if (35<calculate_angle( l_elbow, l_shoulder, l_hip))and(calculate_angle( l_elbow, l_shoulder, l_hip)<60): # 겨드랑이
                score += 1
            if (160<rev_calculate_angle(l_shoulder, l_hip, l_knee))and(rev_calculate_angle(l_shoulder, l_hip, l_knee)<180): # 엉덩이
                score += 1
            if (140<calculate_angle(l_hip, l_knee, l_ankle))and(calculate_angle(l_hip, l_knee, l_ankle)<170): # 무릎
                score += 1
            if (75<calculate_angle(l_eye, nose, l_shoulder))and(calculate_angle(l_eye, nose, l_shoulder)<95): # 목
                score += 1
            if (calculate_width(l_shoulder,r_shoulder)*1.2 < calculate_width(l_wrist,r_wrist)) \
                and (calculate_width(l_shoulder,r_shoulder)*1.5 > calculate_width(l_wrist,r_wrist)) : # 팔 너비
                score += 1

                # 점수 계산
                if score == 10: 
                    result['excellent_count'] += 1
                    result['full_count'] += 1 
                else:
                    result['full_count'] += 1
    


    
    

    return HttpResponse(json.dumps({'result':result})) 



def train_train(request):
    return render(request, 'anchovy_train/train_train.html')


def train_practice(request):
    return render(request, 'anchovy_train/train_practice.html')

def test(request):
    return render(request, 'anchovy_train/test.html')
