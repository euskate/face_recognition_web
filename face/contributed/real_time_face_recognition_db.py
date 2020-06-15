# 2020-05-27 Unknown과 Accuracy 영상에 출력되도록 수정
# 2020-06-01 DB에 적재중
import age_gender_estimate
import random
import argparse
import sys
import time
import cv2
import face # Original
# import contributed.face # Modified
import psycopg2
from functions import *
import os

base_path = '/'.join((os.getcwd()).split('/')[:4])+'/' #/home/team/facenet_master/ 
upload_path = 'project04_objectdetection/data/'
download_path = 'data/images/'
print( '='*80,'\n',"기본경로-> ",base_path," 적재할 파일의 경로 :",upload_path," 다운받을 로컬 경로 :",download_path )

input_path  = base_path + upload_path
output_path = base_path + download_path


# main 함수 내에서 영상 출력 중에 Bounding Box, name, Accuracy 등을 출력하는 함수
def add_overlays(frame, faces, frame_rate):
    if faces:
        # Detecting된 얼굴들 정보가 Class 객체로 담겨 있는 리스트를 for iterator로 출력한다
        for i, face in enumerate(faces):
            # 정확도가 0.8 이상인 경우에 color 정의
            color = ( 255, 0, 0 ) # Modified
            face_bb = face.bounding_box.astype(int)
            # Bounding Box를 출력
            cv2.rectangle(frame,
                        (face_bb[0], face_bb[1]), (face_bb[2], face_bb[3]),
                        (0, 255, 0), 2)
            # 얼굴의 정확도가 0.8 이하인 경우 아래와 같이 정의한다
            if face.accuracy < 0.8 :  
                face.name = "Unknown" # Modified
                color = ( 0, 0, 255 ) # Modified

            # 얼굴 이름, 정확도를 Text로 영상에 출력하는 함수
            cv2.putText(frame, face.name, (face_bb[0], face_bb[3]),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, color,
                        thickness=2, lineType=2)
            cv2.putText(frame, str(round(face.accuracy,2)*100)+"%", (face_bb[0], face_bb[3]-30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, color,
                        thickness=2, lineType=4) # Modified
    # 프레임 수를 출력하는 함수
    cv2.putText(frame, str(frame_rate) + " fps", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0),
                thickness=2, lineType=2)

# main 함수
def main(args):
    # face detection이 실행될 때 프레임의 수 정의
    frame_interval = 5  # Number of frames after which to run face detection 
    # fps가 출력되는 interval
    fps_display_interval = 5  # seconds
    frame_rate = 0
    frame_count = 0
    
    # Opencv함수로 영상 정의
    video_capture = cv2.VideoCapture(0)
    # face.Recognition() 클래스 정의
    face_recognition = face.Recognition()
    # 시작시간 정의
    start_time = time.time()
    if args.debug:
        print("Debug enabled")
        face.debug = True

    # 영상이 돌기 시작
    while True:
        # Capture frame-by-frame
        # 영상을 읽은 프레임 별로 ret, frame에 정의
        ret, frame = video_capture.read()
    
        if (frame_count % frame_interval) == 0:
            faces = face_recognition.identify(frame)
            # Check our current fps
            end_time = time.time()
            if (end_time - start_time) > fps_display_interval:
                frame_rate = int(frame_count / (end_time - start_time))
                start_time = time.time()
                frame_count = 0
        print( 'number of face', len(faces) ) # Modified
        # frame, faces, frame_rate를 overlay하기 위해 변수를 담아준다
        add_overlays(frame, faces, frame_rate)
        frame_count += 1
        # frame 출력
        cv2.imshow('Video', frame)
        tmp = random.randint(1, 10)
        if tmp == 5:
            age, gender = age_gender_estimate.age_gender_estimate()
            # sql = " INSERT {}, {} TO TABLE "
            # cur.excute(sql)
            print("나이, 성별 = ", age, gender)
            return age, gender

        # 키 입력하면 break한다
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything is done, release the capture
    video_capture.release()
    cv2.destroyAllWindows()


def parse_arguments(argv):
    parser = argparse.ArgumentParser()

    parser.add_argument('--debug', action='store_true',
                        help='Enable some debug outputs.')
    return parser.parse_args(argv)

if __name__ == '__main__':
    # main(parse_arguments(sys.argv[1:]))

    # print(face.accuracy)
    # print("+"*80, main.age, main.gender)

# 열결된 db 정보
    connect()

# # 최초 디비생성
    # create_tables()

# # insert one/multiple customer
#     insert_customer(33, 1) # 33세, 남자
#     insert_customer_list([ (29,1),
#         (35,1) ])

# # vendor가 제공하는 part를 연결 추가
#     add_part('SIM Tray', (1, 2))
#     add_part('Speaker', (3, 4))
#     add_part('Vibrator', (5, 6))
#     add_part('Antenna', (6, 7))
#     add_part('Home Button', (1, 5))
#     add_part('LTE Modem', (1, 5))

# # vendor_id 가 1인 사람의 part를 가져오기
#     get_parts(1)

# # id인덱스 리셋시 참고할 시퀸스명
#     sequences()

# # 로컬 이미지 DB적재
    # write_blob(1, input_path+'hong.jpeg', 'jpeg')
#     write_blob(2, input_path+'jennie_makeup.jpg', 'jpg')

# # 적재된 이미지 불러와 로컬에 저장 
    # read_blob( 1, output_path )
    