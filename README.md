
![image](https://user-images.githubusercontent.com/111229365/218350616-b691f95f-6aa4-43f9-b9c7-eaeb61afa2ac.png)


## 개요

### 배경
<img width="797" alt="image" src="https://user-images.githubusercontent.com/111229365/218349224-38c751d0-a75d-4557-a230-aacd7934c948.png">

### 목적
![image](https://user-images.githubusercontent.com/111229365/218349502-a31e6991-5a1e-409f-a015-c9cfa02211ad.png)

### 기대효과
![image](https://user-images.githubusercontent.com/111229365/218349522-d1ffdfd8-a9fa-48d6-88fa-f13f6ee4f480.png)

### 서비스 장점
![image](https://user-images.githubusercontent.com/111229365/218349550-28d741ad-ad22-4775-8385-75a839eb9a24.png)

![image](https://user-images.githubusercontent.com/111229365/218349584-38743bcf-56c8-46c8-9558-de2e1f33bbb8.png)

![image](https://user-images.githubusercontent.com/111229365/218349599-92425b18-42b1-4f66-9338-8be622e9bd1b.png)

### 개발환경
![image](https://user-images.githubusercontent.com/111229365/218349612-5f811e25-6ba2-441e-928a-bacbec80da00.png)

***
## 모델 history

### CNN

![image](https://user-images.githubusercontent.com/111229365/218349864-2db52d94-671d-4701-94de-0e58c6d2d650.png)
<br>CNN으로 분류모델을 제작하기 위해 AI HUB에서 필요한 데이터를 수집하였고, 모델의 정확성을 올리기 위해 전처리를 진행하였습니다.

![image](https://user-images.githubusercontent.com/111229365/218349917-64bfb463-bcdf-42f1-ba80-f753b572b218.png)
분류모델을 제작하기 위해 사용된 데이터는 986개이며, 원본 및 전처리 데이터를 사용했습니다.
검증데이터를 활용한 모델 정확도는 81% 나왔으며, 이후 정확도를 가시적으로 확인하기 위해 일어나 있는 자세 및 앉아있는 자세를 직접 대입하여 테스트를 진행한 결과, 각 77%의 정확도가 나왔습니다.

![image](https://user-images.githubusercontent.com/111229365/218349938-4681317f-f4b5-4d5b-bec3-a96abc125266.png)
CNN 모델의 정확도가 낮은 편은 아니였지만, 이미지 분류 모델만으로는 앤초비가 추구하는 정확한 자세 코칭 서비스를 구현하기 어렵다고 생각하였습니다. 
원활한 서비스 구현을 위해서는 스켈레톤 추출 모델이 필요하다고 느끼게 되었습니다. 
다만 스켈레톤 추출모델을 자체 생성하기에는 시간 및 자원이 부족하였기 때문에 오픈 소스를 활용하는 것으로 결론을 내렸습니다.

### open source
![image](https://user-images.githubusercontent.com/111229365/218349967-4454549b-1bb8-42cc-ac33-31286425d857.png)
![image](https://user-images.githubusercontent.com/111229365/218349996-9536ed28-3eaf-4cd8-b7f1-0d7e6a6588d0.png)
![image](https://user-images.githubusercontent.com/111229365/218350006-16bc3a1d-91c0-47d1-8845-76b36c818f87.png)
![image](https://user-images.githubusercontent.com/111229365/218350020-f10053d7-fe50-462e-8935-7ac529c43bd8.png)
![image](https://user-images.githubusercontent.com/111229365/218350027-65bcd750-7597-4e17-880a-ddb94d4a522a.png)
***
## 서비스 
### 개념도
![image](https://user-images.githubusercontent.com/111229365/218350780-c6020379-67c9-442a-a362-70f01b2508fd.png)

### ERD
![image](https://user-images.githubusercontent.com/111229365/218350964-f09f8943-8b70-4e41-9a33-2004008c90c9.png)

### 구현
![image](https://user-images.githubusercontent.com/111229365/218350998-04084a05-4737-4c9d-bac4-a17f36d551d4.png)
사람들의 모습과 스켈레톤 정보를 화면에 출력하기 위한 코드입니다.
미디어 파이프에 내장되어 있는 API 카메라를 통해 사용자의 핸드폰 카메라를 연결하고 데이터를전달 받습니다. 
다음으로 스켈레톤을 추출하기 위해 데이터의 한 프레임을 미디어 파이프에 전달합니다. 
이 프레임에 대한 랜드마크 정보를 미디어파이프가 추출하고, 이 결과를 바탕으로 랜드마크를 연결한 스켈레톤 정보를 입력받은 프레임과 함께 보여줍니다 
이 과정이 연속적으로 반복되어 영상처럼 보여지게 됩니다.

![image](https://user-images.githubusercontent.com/111229365/218351032-3eede75c-8141-4fb8-aa16-c287959add98.png)
올바른 자세를 뽑아 내기 위해서는 각도가 필요하고, 그 자세를 판단하기 위한 기준을 정하였습니다.
푸쉬업은 엉덩이, 무릎 및 목을 일직선으로 유지하고, 양팔사이가 너무 멀어지거나 좁혀지지 않도록 각각의 거리를 비교하여 적절한 자세인지 판단하였습니다.
스쿼트는 몸이 한쪽으로 기울어지지 않도록 좌우 어깨, 엉덩이, 무릎 사이의 각도를 동일한 각도로 유지하고, 앉았을 때 양쪽 무릎이 모이지 않도록 양쪽 무릎, 양발 사이 거리를 비교하여 적절한 자세인지 판단하였습니다.
이 지표에 필요한 정보는 운동 youtuber 영상데이터와 팀원의 운동 영상데이터를 이용하여 추출하였습니다.

![image](https://user-images.githubusercontent.com/111229365/218351068-d0e0bd9d-4f62-4cc3-a1a8-8f59d13639f2.png)
![image](https://user-images.githubusercontent.com/111229365/218351095-62c069eb-f949-4ac6-9956-098e3a78a075.png)
저희가 처음 알고리즘을 구현하기 시작했을 때 기준이 되는 y좌표와 사용자의 현재 상태의 y좌표를 비교해 동작을 판단하면 될것이라고 생각했습니다 

하지만 에이젝스를 이용해 데이터를 주고받는 과정에서 데이터가 끝없이 들어와 모든 데이터가 첫번째 좌표로 인식이 되어 비교가 불가능한 상태로 판단되었습니다

따라서 단계를 세분화 하여 조금 더 세밀한 알고리즘을 만들고자 다음과 같은 방법으로 진행하였습니다

![image](https://user-images.githubusercontent.com/111229365/218351115-32e78e63-87c0-4d1e-bba9-d446a09594bb.png)
사용자가 세트, 횟수, 휴식시간을 선택한 후 운동이 시작되면 다음과 같은 알고리즘이 실행됩니다. 
(1) 사용자의 자세를 비교하기 위해 운동이 시작되면 최초 상태의 좌표를 기준에 저장합니다. 이 때 스쿼트는 골반, 푸쉬업은 코 좌표를 사용합니다. 
(2) 기준 좌표보다 아래로 내려가면 모델이 다운 상태로 인식하게 되고 이 상태에서, 앞서 설명드린 각각의 기준을 하나씩 만족할 때마다 스코어 점수를 1점씩 가중합니다. 
(3) 스코어 점수 계산이 완료되면 3번으로 넘어가 앉은 상태에서의 좌표를 기준에 갱신합니다.
(4) 기준 좌표보다 위로 올라가면 2번과 동일한 과정을 반복하게 되고, 1번부터 4번까지 모두 완료되면 점수 합산인 5번 단계로 넘어갑니다.
(5) 이 단계에서는 선택한 횟수를 만족했는지를 판단하는 점수와 바른 자세로 운동했을 때만 측정되는 점수, 총 2가지가 존재합니다. 첫번째 점수는 1점이 항상 더해집니다. 두번째는 2번과 4번에서 얻은 스코어 점수가 일정 수준 이상 도달했을 때만 부과됩니다.

(6) 이후에 첫번째 점수가 사용자가 선택한 1세트당 횟수와 동일해진다면 휴식시간으로 넘어가고 그렇지 않으면 다시 1번부터 반복진행됩니다. 
(7) 휴식시간동안 1세트에 대한 데이터를 DB에 저장하고 휴식이 끝나면 모든 세트가 완료될 때까지 
(8) 재진행됩니다. 

![image](https://user-images.githubusercontent.com/111229365/218351129-6b7eb098-fde3-4811-a94f-50e1aef0cf89.png)

***
## 시연영상
https://drive.google.com/file/d/1oK9f5HALQoajJ0BRhkdvAM1RnVUPmap8/view?usp=share_link
***
## 팀원 정보
|이름|git|e-mail|
|---|---|---|
|노민경|nohminkyoung|nmk1188@naver.com|
|박소정|psjeong|sj926thwjdk@naver.com|
|전유진|yudyudy|dbwlsier@naver.com|
|전정훈|wjswjdgns|wjswjdgns7@naver.com|

