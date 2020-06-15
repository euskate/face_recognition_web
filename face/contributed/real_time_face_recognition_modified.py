# coding=utf-8
"""Performs face detection in realtime.

Based on code from https://github.com/shanren7/real_time_face_recognition
"""
# MIT License
#
# Copyright (c) 2017 François Gervais
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# 2020-05-27 Unknown과 Accuracy 영상에 출력되도록 수정
import age_gender_estimate
import random
import argparse
import sys
import time
import cv2
import face # Original
# import contributed.face # Modified

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
        # print( 'number of face', len(faces) ) # Modified
        # frame, faces, frame_rate를 overlay하기 위해 변수를 담아준다
        add_overlays(frame, faces, frame_rate)
        frame_count += 1
        # frame 출력
        cv2.imshow('Video', frame)

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
    main(parse_arguments(sys.argv[1:]))