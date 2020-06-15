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
import argparse
import sys
import time

import cv2

import face # Original
# import contributed.face # Modified

import psycopg2
conn_string = "host='192.168.0.59' dbname ='testdb' user='user' password='password'"
conn = psycopg2.connect(conn_string)
cur = conn.cursor()

def add_overlays(frame, faces, frame_rate):
    if faces is not None:
        # print(faces)
        # faces -> labels (maybe)
        # for face, accuracy in faces, accuracys:
        # global face.accuracy
        # if face.accuracy < 0.8 : # Modified
            # face.name = "unknown" # Modified
            # face.accuracy = "unknown" # Modified
        for i, face in enumerate(faces):
            # print("=== face.name, face.accuracy =", face.name, face.accuracy)
            # print(face.accuracy,"######################################################")
            face_bb = face.bounding_box.astype(int)
            cv2.rectangle(frame,
                        (face_bb[0], face_bb[1]), (face_bb[2], face_bb[3]),
                        (0, 255, 0), 2)

            # ### 이미지 캡쳐 시작
            # time_st = time.strftime("%Y%m%d_%H%M%S")
            # cap_name = './capture/{}.png'.format(time_st)
            # cv2.imwrite(cap_name, face.image)
            # ### 이미지 캡쳐 끝

            # if face.name is not None and face.accuracy <0.7:
            #     cv2.putText(frame, "Unknown", (face_bb[0], face_bb[3]),
            #                 cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255),
            #                 thickness=2, lineType=2)
            
            if face.name is not None:
                cv2.putText(frame, face.name, (face_bb[0], face_bb[3]),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0),
                            thickness=2, lineType=2)
                cv2.putText(frame, str(round(face.accuracy,2)*100)+"%", (face_bb[0]-10, face_bb[3]-30),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0),
                            thickness=2, lineType=4)



    cv2.putText(frame, str(frame_rate) + " fps", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0),
                thickness=2, lineType=2)

def main(args):
    frame_interval = 5  # Number of frames after which to run face detection 
    fps_display_interval = 20  # seconds
    # fps_display_interval = 5  # seconds
    frame_rate = 0
    frame_count = 0
    
    video_capture = cv2.VideoCapture("http://192.168.0.101:8091/?action=stream") # Original
    face_recognition = face.Recognition()
    start_time = time.time()
    if args.debug:
        print("Debug enabled")
        face.debug = True

    while True:
        # Capture frame-by-frame
        ret, frame = video_capture.read()
        frame = cv2.flip(frame,0) # 뒤집기
        # print('While2') # Modified
        # print("frame : ", frame) # Modified
        # print("frame.shape : ", frame.shape) # Modified
        if (frame_count % frame_interval) == 0:
            
            # faces, accuracys = face_recognition.identify(frame) # Modified
            faces = face_recognition.identify(frame)
            # accuracy have to be Class object
            print("in def main(args)", faces)
            
            # print("faces : ", faces) # Modified

            # Check our current fps
            end_time = time.time()
            if (end_time - start_time) > fps_display_interval:
                frame_rate = int(frame_count / (end_time - start_time))
                start_time = time.time()
                frame_count = 0

        add_overlays(frame, faces, frame_rate)
        frame_count += 1
        cv2.imshow('Video', frame)
        # break # Modified
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cur.close()
            conn.close()
            break
        ## w 키 : capture # 사진 캡처
        if cv2.waitKey(1) & 0xFF == ord('w'):
            time_st = time.strftime("%Y%m%d_%H%M%S")
            cap_name = './capture/{}.png'.format(time_st)
            cv2.imwrite(cap_name, frame)
        ## e 키 :
        if cv2.waitKey(1) & 0xFF == ord('e'):
            # if faces is not None:
            if faces is not None:
                for i, fac in enumerate(faces):
                    if fac.name is not None:
                        print(fac.name)
                        sql = """INSERT INTO testt(name) VALUES(%s);"""
                        cur.execute(sql, (fac.name,))
                        conn.commit()
                        print("DB Insert", fac.name)

            pass


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
