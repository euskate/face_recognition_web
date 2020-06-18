# IoT와 얼굴인식 기술을 이용한 매장관리 시스템

## Explanation our service

- **Recommend**  추정한 연령, 성별에 따라 자주 구매하는 제품을 추천상품으로 제안
    - Recommend based on Age, Gender which estimated by AI

- **event** 자신의 얼굴을 등록한 고객이 방문한 경우, 그 고객의 이름과 과거 구매이력을 출력
    - Show previous purchase list and name of customer on the screen,  if they visit a store who enrolled their face info(called VIP) 

- **Enrollment** 얼굴을 등록하지 않은 고객이 얼굴을 등록하고 싶은 경우, 캠을 통해 실시간으로 등록하고 학습시켜 1분 안에 업데이트 되도록 시스템 구성
    - if a customer want to enroll their face to get premium service, we can train classifier in real time and update to classify who they are. 


## Example of Recommend page

![Recommend](https://user-images.githubusercontent.com/58922804/84978955-2f366d80-b169-11ea-8afa-83fe64597123.jpg)

## Example of Enrollment page 

![Train_Classifier](https://user-images.githubusercontent.com/58922804/84978957-2fcf0400-b169-11ea-92e7-df202a9d2131.jpg)

## Video Example

[Video is here](https://youtu.be/DHJ-tMD_6eU)

## 사용 라이브러리

|||
|:------:|:---:|
|Web|Django|
|데이터베이스|Postgre-sql|
|엔진|Tensorflow|
|이미지 처리|opencv|
|css framework|bootstrap|

- 수정해야 하는 부분(DB, Webcam)
- part of modification(for DB, Wencam)
  - /config/settings.py
  - /face/views.py
  
- 모델 경로 수정(checkpoint, pb, classifier(pickle))
- modify model path(need to ckpt, pb, classifier restored as pickle )
  - /face/face.py
  - /face/views.py

- 모델 분할 압축
  - 모델은 용량 문제로 분할 압축하였습니다. (3종류의 모델 첨부)
  - /models/
    - model2018 : VGG model
    - model_kfcl12 : kface, asian_celeb 전이학습 1차 모델
    - model_kfcl63 : kface, asian_celeb 전이학습 2차 모델

- requirements

```
tensorflow          1.7.0
opencv-python       4.2.0.34
pandas              0.25.3
numpy               1.16.2
scipy               1.2.1
Django              2.1.7
djangorestframework 3.11.0
psycopg2            2.7.5
psutil              5.7.0
```
