# [모듈] 장고 모듈
from django.shortcuts import render, redirect
from django.http import HttpResponse,StreamingHttpResponse, JsonResponse
from django.views.decorators import gzip
from django.views.decorators.csrf import csrf_exempt

from .models import Customers, Menus, Sales

# [모듈] 시스템 모듈
import os 

# [모듈] 얼굴인식 모듈 import
import cv2
import time
from . import face

# [모듈] Database 모듈 import 및 접속 설정
import pandas as pd
import psycopg2
# conn_string = "host='192.168.0.59' dbname ='testdb' user='user' password='password'"
conn_string = "host='192.168.0.59' dbname ='face_db' user='user' password='password'"
conn = psycopg2.connect(conn_string)
cur = conn.cursor()

# [모듈] timestamp
from datetime import datetime


# [전역변수 선언] face 객체 활용 전역변수 리스트 선언
face_lists = list()

# [얼굴인식] 카메라 인식 Class - fps 부분은 삭제
class VideoCamera(object):
    def __init__(self):
        # 얼굴인식 관련 멤버변수 설정
        self.frame_interval = 5  # Number of frames after which to run face detection 
        self.fps_display_interval = 20  # seconds
        self.frame_count = 0
        self.face_recognition = face.Recognition()
        self.start_time = time.time()
        # self.face_lists
        self.trigger = 0

        # 라즈베리 파이 카메라 모듈로 촬영된 스트리밍(mjpg-streamer)을 가져온다.
        self.video = cv2.VideoCapture('http://192.168.0.101:8091/?action=stream')

    def __del__(self):
        self.video.release()

    # 바인딩 박스 추가하는 메소드
    def add_overlays(self, frame, faces):
        if faces is not None:
            for i, face in enumerate(faces):
                face_bb = face.bounding_box.astype(int) # 사각형 좌표 리스트
                cv2.rectangle(frame, # 이미지
                            (face_bb[0], face_bb[1]), (face_bb[2], face_bb[3]), # 시작좌표, 종료좌표
                            (63, 28, 1), 2) # 색상(B, G, R), 두께 pixel

                # 얼굴의 정확도가 0.75 이하인 경우 아래와 같이 정의한다
                if face.accuracy < 0.6 :  
                    face.name = "Unknown" # Modified
                    color = ( 0, 0, 255 ) # Modified

                if face.name is not None:
                    # 이름 텍스트 추가 
                    cv2.putText(frame, face.name, (face_bb[0], face_bb[3]),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (165, 123, 18),
                                thickness=2, lineType=2)

                    ## 정확도 막대 구현
                    # x1,y1,x2,y2 = face_bb[0], face_bb[1], face_bb[2], face_bb[3]
                    bar_height_origin = face_bb[3] - face_bb[1]
                    acc = round(face.accuracy,2)
                    bar_height = int(bar_height_origin * acc)
                    # print("bar_height_origin : ", bar_height_origin)
                    # print("acc : ", acc)
                    # print("bar_height : ", bar_height)
                    # print("pt1=(face_bb[2], face_bb[3]+bar_height)", (face_bb[2], face_bb[3]+bar_height) )
                    # print("pt2=(face_bb[2]+10, face_bb[3])", (face_bb[2]+10, face_bb[3]) )
                    
                    # 사각형 추가
                    cv2.rectangle(img=frame, pt1=(face_bb[2], face_bb[3]-bar_height), pt2=(face_bb[2]+7, face_bb[3]), color=(63, 28, 1), thickness=7) 
                    age = str()
                    if face.age == 0:
                        age = '20_24'
                    elif face.age == 1:
                        age = '25_29'
                    elif face.age == 2:
                        age = '30_34'
                    elif face.age == 3:
                        age = '35_39'
                    cv2.putText(frame, age, (face_bb[0], face_bb[3]+20),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.75, color=(255,0,),
                                thickness=2, lineType=2)
                    gender = str()
                    if face.gender == 0:
                        gender = "M"
                    elif face.gender == 1:
                        gender = "F"
                    cv2.putText(frame, gender, (face_bb[0]+80, face_bb[3]+20),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.75, color=(0,0,255),
                                thickness=2, lineType=2) # Modified
                    # 정확도
                    # cv2.putText(frame, str(round(face.accuracy,2)*100)+"%", (face_bb[0], face_bb[3]-30),
                    #             cv2.FONT_HERSHEY_SIMPLEX, 1, (38, 165, 101),
                    #             thickness=2, lineType=2)

    # 프레임을 가져오는 메소드
    def get_frame(self):
        ret,frame = self.video.read()
        frame = cv2.flip(frame,0) # 상하반전
        global face_lists
        # 가져온 프레임에서 얼굴 id 인식 - 설정된 interval 마다 수행
        if (self.frame_count % self.frame_interval) == 0:
            face_lists = self.face_recognition.identify(frame)

        # 바운딩 박스 및 텍스트를 추가
        self.add_overlays(frame, face_lists)
        self.frame_count += 1

        # jpeg 이미지 인코딩
        ret,jpeg = cv2.imencode('.jpg',frame)
        return jpeg.tobytes()

# [인코딩] VideoCapture로부터 프레임을 가져와 jpeg 타입의 이미지를 생성하는 함수
def gen(camera):
    while True:
        frame = camera.get_frame()
        yield(b'--frame\r\n'
        b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

# [스트리밍] 반복되어 변경되는 jpg 형식의 이미지를 http로 스트리밍 해주는 함수
@gzip.gzip_page
def stream(request): 
    try:
        return StreamingHttpResponse(gen(VideoCamera()),content_type="multipart/x-mixed-replace;boundary=frame")
    except HttpResponseServerError as e:
        print("aborted")

# [Ajax] 캡처 동작을 실행하는 함수 
@csrf_exempt
def capture(request):
    data = dict()
    if face_lists == []: print("no face")
    else:
        time_st = time.strftime("%Y%m%d_%H%M%S")
        print(os.getcwd())
        cap_name = './face/capture/{}_{}.png'.format(face_lists[0].name, time_st)
        cv2.imwrite(cap_name, face_lists[0].image)                
        print("capture", face_lists[0].name)
        # for i, face in enumerate(face_lists):
        #     # ### 이미지 캡쳐 시작
        #     print(face.name)
        #     time_st = time.strftime("%Y%m%d_%H%M%S")
        #     cap_name = './capture/{}_{}.png'.format(face.name, time_st)
        #     cv2.imwrite(cap_name, face.image)                
    return JsonResponse(data)

# [Ajax] face 객체가 웹으로 잘 전송되었는지 확인하는 함수
@csrf_exempt
def caps(request):
    data = dict()
    # data['caps_var'] = 'none'

    # if request.method == 'POST':
    if face_lists == []:
        data['f_name'] = 'none'
        data['f_accuracy'] = 'none'
        data['f_time'] = 'none'
        # data['f_image'] = 'none'
    else:
        print(face_lists)
        # print(face_lists[0])
        print(face_lists[0].name)
        data['f_name'] = face_lists[0].name
        data['f_accuracy'] = face_lists[0].accuracy
        data['f_time'] = time.strftime("%Y년%m월%d일 %H시%M분%S초")
        # data['f_image'] = face_lists[0].image

    # print(data)
    return JsonResponse(data)

# [Ajax] DB input 테스트
def check(request):
    data = dict()
    if face_lists == []:
        data['f_name'] = 'none'
        data['han_name'] = '없음'
    else:
        print(face_lists)
        print(face_lists[0].name)
        data['f_name'] = face_lists[0].name
        face = face_lists[0]
        age = str()
        age_cat = str()
        if face.age == 0:
            age = '20대 초반(20~24)'
            age_cat = '20_24'
        elif face.age == 1:
            age = '20대 후반(25~29)'
            age_cat = '25_29'
        elif face.age == 2:
            age = '30대 초반(30~34)'
            age_cat = '30_34'
        elif face.age == 3:
            age = '30대 후반(35~39)'
            age_cat = '35_39'
        gender = str()
        gender_cat = str()
        if face.gender == 0:
            gender = "남성"
            gender_cat = "M"
        elif face.gender == 1:
            gender = "여성"
            gender_cat = "F"
        data['age'] = age
        data['gender'] = gender
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        
        # sql = """INSERT INTO test2(name, time) VALUES(%s, %s);""" # 삽입 sql문
        # cur.execute(sql, (data['f_name'], timestamp))
        # conn.commit()
        # print("DB Insert", data['f_name'], timestamp)
        
        # sql = """SELECT name_kor FROM customer WHERE name_eng='{}';""".format(data['f_name']) # 한글 이름 찾는 sql문
        # result = pd.read_sql(sql, conn)
        # sql = """SELECT name_kor FROM customer WHERE name_eng=%s;""" # 한글 이름 찾는 sql문
        try:
            obj = Customers.objects.get(eng_name=data['f_name'])
            data['han_name'] = obj.han_name
            data['customer_id'] = obj.customer_id
            print(data['han_name'])
        except:pass
        try:
            # 연령별 성별 추천 메뉴 SQL 조회 (3개)
            sql = """
            SELECT menu_name
            FROM seg 
            WHERE gender='{}' AND AGE='{}'
            LIMIT 3;
            """.format(gender_cat, age_cat)
            cur.execute(sql)
            result = cur.fetchall()
            # print(result) # [('자몽 요거트',), ('바나나 생과일요플레',), ('블루베리 요거트',)]
            age_favorite_menus = [ tpl[0] for tpl in result ]
            # print(age_favorite_menus) # ['자몽 요거트', '바나나 생과일요플레', '블루베리 요거트']
            data['age_menus'] = age_favorite_menus
        except:pass


        # sql = """SELECT han_name FROM face_customers WHERE eng_name=%s;""" # 한글 이름 찾는 sql문
        # try:
        #     cur.execute(sql, (data['f_name'],))
        #     result = cur.fetchone()
        #     print(result)
        #     han_name = result[0]
        #     print(han_name)
        #     data['han_name'] = han_name
            # sql = """
            # SELECT
            #     메뉴
            # FROM
            #     (SELECT * FROM sales WHERE 이름=(SELECT name_kor FROM customer WHERE name_eng='{}')) AS t1
            # GROUP BY
            #     메뉴
            # ORDER BY
            #     COUNT(메뉴) DESC
            # LIMIT 3;
            # """.format(data['f_name'])
            # 개인별 성별 추천 메뉴 SQL 조회 (3개)
        try:
            sql = """
            SELECT menu_name 
            FROM client 
            WHERE han_name='{}'
            LIMIT 3;
            """.format(data['han_name'])
            cur.execute(sql)
            result = cur.fetchall()
            favorite_menus = [ tpl[0] for tpl in result ]
            print(result)
            data['fav_menus'] = favorite_menus
        except:pass

    return JsonResponse(data)

# [Ajax] 분류기를 업데이트하는 함수
@csrf_exempt
def classifier(request):
    data = dict()
    # 얼굴을 카메라가 인식할 수 있게 위치하라는 메시지를 던진다
    # 이름을 입력받는다. 한글이름(DB 쿼리 및 서비스용도)과 영문이름(분류기용)
    print(request.POST['han_name'])
    print(request.POST['eng_name'])
    han_name = request.POST['han_name']
    eng_name = request.POST['eng_name']
    # 입력 받은 이름을 데이터베이스에 등록한다.

    # sql = """INSERT INTO customer(name_eng, name_kor) VALUES(%s, %s);"""
    sql = """INSERT INTO face_customers(eng_name, han_name) VALUES(%s, %s);"""
    cur.execute(sql, (eng_name, han_name))
    conn.commit()    

    # 입력받은 영문이름으로 폴더를 생성한다.
    try:
        os.mkdir('./face/capture/'+eng_name)
    except: pass # 이미 존재할 경우 
    # 30초 동안사진을 10 ~ 20장 정도 반복 캡쳐한다
    for i in range(30):
        try:
            time_st = time.strftime("%Y%m%d_%H%M%S")
        # 캡쳐한 사진을 영문이름 폴더 내부에 저장한다.
            cap_name = './face/capture/{}/{}_{}.png'.format(eng_name, face_lists[0].name, time_st)
            cv2.imwrite(cap_name, face_lists[0].image)
            print("capture", face_lists[0].name)
        except:
            pass
        finally:
            time.sleep(1)
    # 기존의 분류기.pkl의 파일 이름을 변경하여 백업한다.
    time_st = time.strftime("%Y%m%d_%H%M%S")
    clf_path = './face/classifier/rasp_classifier.pkl'
    os.rename(clf_path, clf_path+time_st+'.backup')

    # clfassify를 시스템 실행하여 새로운 분류기 피클을 생성한다.
    # os.system('python ./face/classifier.py TRAIN ./face/capture/ /home/team/models/20180402-114759/20180402-114759.pb ./face/classifier/rasp_classifier.pkl --batch_size 1000') # VGG model
    os.system('python ./face/classifier.py TRAIN ./face/capture/ /home/team/models/facenet/celeb_kface/20200609-161902 ./face/classifier/rasp_classifier.pkl --batch_size 1000') # 전이학습 모델

    # 업데이트 중이라는 메세지를 남긴다.
    # 분류기 업데이트가 완료되면 페이지를 새로 고침한다.
    return JsonResponse(data)

# [Ajax] 구매하여 DB에 입력하는 함수
@csrf_exempt
def purchase(request):
    data = dict()
    message = str()
    mng_message = str()
    # 페이지에서 선택된 구매 상품 아이디를 받아온다.
    print("['selectedMenu']: ", request.POST['selectedMenu'])
    print("['name']: ", request.POST['name'])
    print("['customer_id']: ", request.POST['customer_id'])
    selectedMenu = request.POST['selectedMenu']
    customer_id = request.POST['customer_id']
    message = "구매에 실패하였습니다. 다시 시도해주세요."
    # 선택되지 않았을 때 메시지 반환
    if selectedMenu == "-1":
        message = "메뉴를 선택한 후 구매 버튼을 눌러주세요."
        print(message)
    else:
        # obj = Customers.objects.get(eng_name=data['f_name'])
        obj = Menus.objects.get(menu_name=selectedMenu)
        selectedMenu_id = obj.menu_id
        data['menu_name'] = obj.menu_name
        data['menu_price'] = obj.menu_price
        print(data['menu_name'], data['menu_price'] )
        print(customer_id)
        #try:
        if customer_id == "-1":
            # 프리미엄 회원의 경우 "고객님 이름으로 5%의 포인트가 적립되었습니다."
            # 획득되지 않은 경우 => 일반 구매
            Sales.objects.create(menu_id=selectedMenu_id)
            print("일반 구매 DB insert")
            message = "고객 메시지 : "+data['menu_name']+"을 구매하셨습니다. "+str(data['menu_price'])+"원을 결제해 주세요."
            mng_message = "관리자 메시지 : 결제 내역이 데이터베이스에 입력되었습니다."
            
        else:
            # 얼굴 정보에서 고객 아이디를 획득한다.
            cusObj = Customers.objects.get(customer_id=int(customer_id))
            cus_name = cusObj.han_name
            # 획득된 경우 => 프리미엄 구매
            # DB에 메뉴 아이디와 고객 아이디(프리미엄)를 삽입한다.
            Sales.objects.create(customer_id=int(customer_id), menu_id=selectedMenu_id)
            point = round(int(data['menu_price']) * 0.05)
            print("프리미엄 구매 DB insert")
            message = data['menu_name']+"을 구매하셨습니다. "+str(data['menu_price'])+"원을 결제해 주세요. 프리미엄 회원 "+cus_name+"님 앞으로 프리미엄 포인트 "+str(point)+" point가 적립되었습니다."
            mng_message = "관리자 메시지 : 결제 내역이 데이터베이스에 입력되었습니다."
        #except:pass
        # 메시지를 반환한다.
        # 성공했을 경우 "(상품)을 구매하셨습니다."
            # 포인트 오브젝트에 

        # 실패했을 경우 "구매에 실패하였습니다. 다시 시도해주세요."

    data['message'] = message
    data['mng_message'] = mng_message
    

    return JsonResponse(data)
    
# [렌더링] 서비스 페이지를 렌더링하는 함수
def service(request):
    if request.method == 'GET':
        return render(request, 'index.html')
    # elif request.method == 'POST':
    #     return redirect('/face/capture')
    # name='Jang Won1'
    # age=36
    # gender=0
    # image=1 
    # if request.method == 'POST':
    #     print(face_lists)
    #     # print(face_lists[0].name)
    # pass


    # return render(request, 'index.html', context={'name':name, 'age':age, 'gender':gender, 'image' : image })