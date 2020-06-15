import psycopg2
from functions import *
import real_time_face_recognition_db
# import real_time_face_recognition_db
# from project04_objectdetection import run
import os

base_path = '/'.join((os.getcwd()).split('/')[:4])+'/' #/home/team/facenet_master/ 
upload_path = 'project04_objectdetection/data/'
download_path = 'data/images/'
print( '='*130,'\n',"기본경로-> ",base_path," 적재할 파일의 경로 :",upload_path," 다운받을 로컬 경로 :",download_path )

input_path  = base_path + upload_path
output_path = base_path + download_path

if __name__ == '__main__':
# realtime
    # main()
# # age gender
    # age, gender = run.gender()
    # age, gender = real_time_face_recognition_db.main()
    # print(age, gender)
    # sql = """INSERT INTO vendors(vendor_name)
    #          VALUES(%s) RETURNING vendor_id;"""
# # purchase
#     purchase()

# 열결된 db 정보
    # functions.connect()
    connect()

# # 최초 디비생성
#     create_tables()

# # insert one/multiple vendor
#     insert_vendor("정용희")
#     insert_vendor_list([ ('AKM Semiconductor Inc.',),
#         ('Asahi Glass Co Ltd.',),
#         ('Daikin Industries Ltd.',),
#         ('Dynacast International Inc.',),
#         ('Foster Electric Co. Ltd.',),
#         ('Murata Manufacturing Co. Ltd.',) ])

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
    
