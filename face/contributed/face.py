# coding=utf-8
"""Face Detection and Recognition"""
# MIT License
#
# Copyright (c) 2017 François Gervais
#
# This is the work of David Sandberg and shanren7 remodelled into a
# high level container. It's an attempt to simplify the use of such
# technology and provide an easy to use facial recognition package.
#
# https://github.com/davidsandberg/facenet
# https://github.com/shanren7/real_time_face_recognition
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

import pickle
import os

import cv2
import numpy as np
# import tensorflow.compat.v1 as tf # Modified
# tf.disable_v2_behavior()
import tensorflow as tf # Original
from scipy import misc
import detect_face # Original

# import align.detect_face # Original
# import src.align.detect_face # Modified
# import src.facenet # Modified

import facenet # Original

gpu_memory_fraction = 0.3

# model path가 맞지 않는 이유는 여기서 path를 설정을 제대로 해주지 않아서 그렇다

# facenet_model_checkpoint = os.path.dirname(__file__) + "/../model_checkpoints/20170512-110547" # Original
# classifier_model = os.path.dirname(__file__) + "/../model_checkpoints/my_classifier_1.pkl" # Original
# 20180402-114759 
facenet_model_checkpoint = "/home/team/models/20180402-114759/" # Modified
classifier_model = "/home/team/models/classifier/my_classifier20p.pkl" # Modified
debug = False

# Face 클래스에 담기는 정보 = [이름, bounding_box, image, container_image, embedding값, 정확도]
class Face:
    def __init__(self):
        self.name = None
        self.bounding_box = None
        self.image = None
        self.container_image = None
        self.embedding = None
        self.accuracy = None
        

#  Recognition 클래스 = 얼굴을 인식하는 클래스
class Recognition:
    # 클래스의 멤버 변수로 Detection 클래스, Encoder 클래스, Identifier 클래스를 상속 받는다
    def __init__(self):
        self.detect = Detection()
        self.encoder = Encoder()
        self.identifier = Identifier()

    # 이 함수는 잘 모르겠음 facenet 코드 전체에서 쓰이지 않음
    def add_identity(self, image, person_name):
        faces = self.detect.find_faces(image)
        if len(faces) == 1:
            face = faces[0]
            face.name = person_name
            face.embedding = self.encoder.generate_embedding(face)
            return faces

    # 영상에서 캡쳐되어 들어온 사진들을 embedding(Idenfitier 클래스)시키고, 이름(face.name)과 정확도(face.accuracy)를 Face 클래스의 맴버 변수에 담아주는 함수
    def identify(self, image):
        # faces = Detection 클래스의 find_faces함수를 실행시켜 이미지를 Detecing 한 후 Return 값을 받는 객체이다. 
        # Detection에서 Return 값은 Face 클래스들이 담긴 리스트
        faces = self.detect.find_faces(image) # Modified

        # 보통 len(faces)>1 이므로 faces를 반복문을 돌려 하나의 Face 클래스를 뽑아 낸 후 
        # 각각의 Face클래스의 맴버변수에 embedding과 name, accuracy를 담아준다
        for i, face in enumerate(faces):
            if debug:
                cv2.imshow("Face: " + str(i), face.image)
            
            # Encoder 클래스를 이용하여 embedding한 값을 face의 맴버 변수인 face.embedding에 담아준다
            face.embedding = self.encoder.generate_embedding(face)
            # Idenfifier 클래스를 이용하여 face의 맴버변수인 face.name 과 face.accuracy에 이름과 정확도를 담아준다
            face.name, face.accuracy = self.identifier.identify(face)
        # 각각의 Face 클래스의 맴버 변수들을 정의하고, 그 클래스들이 담긴 faces를 리턴한다 --> real_time_face_recognition에서 실행시키면,
        # 리턴 값으로 얻는 것은 Ex) [ Face 클래스, Face 클래스, Face 클래스 ] 이런 형식이다
        return faces


# Identifier 클래스 = 분류기에 있는 학습된 모델과 class 이름들을 읽어온다
# 하나의 face.embedding 값을 받아 전체 label에서 이 값이 어떤 label에 속할 지에 대한 각각의 확률값을 받는다
# 그 중에 가장 확률이 높은 값 하나를 출력하여 face.accuracy에 담아준다
class Identifier:
    def __init__(self):
        with open(classifier_model, 'rb') as infile:
            # pickle로 저장된 classifier_model을 읽어온 후, 모델과 class_names(labels)를 Identifier 클래스의 맴버변수로 정의한다
            self.model, self.class_names = pickle.load(infile)
            # 정확도를 영상에 출력하고 싶어 수정한 부분. Face 클래스에 accuracy라고 하는 맴버변수에 정확도를 담아주기 위해
            # # Identifier 클래스에 accruacy라고 하는 맴버변수를 정의해 줬다 -> 나중에 face.accuracy에 담기게 될 값이다
            # self.accuracy = None # Modified
    
    # face.embedding 값을 predict_proba 함수에 넣어 확률값을 받는다
    def identify(self, face):
        if face.embedding is not None:
            predictions = self.model.predict_proba([face.embedding]) # Original
            # predictions의 출력값은 마치 [ [ 0.2 ], [ 0.1 ], [ 0.02 ], [ 0.05 ], [ 0.7 ]....] 이런 식으로 구성된다

            # the index number that have best probability in a number of classes
            # np.argmax 함수를 사용하여 가장 값이 높은 확률 값을 가지고 있는 곳의 인덱스 번호를 출력한 후 best_class_indices에 담아준다
            best_class_indices = np.argmax(predictions, axis=1)
            # Identifier의 맴버 변수에 담아 준다 -> 리턴값으로 주기 위해 ( 없어도 될 것 같다 )
            # self.accuracy = predictions[0][best_class_indices[0]]
            # 리턴값으로 하나의 이름과 하나의 정확도가 출력 된다
            return self.class_names[best_class_indices[0]], predictions[0][best_class_indices[0]]


# Encoder 클래스 = 정의된 모델을 활용해 입력된 이미지에 대해 하나의 embedding 값을 출력해주는 클래스이다
class Encoder:
    def __init__(self):
        self.sess = tf.Session()
        with self.sess.as_default():
            facenet.load_model(facenet_model_checkpoint)

    def generate_embedding(self, face):
        # Get input and output tensors
        images_placeholder = tf.get_default_graph().get_tensor_by_name("input:0")
        embeddings = tf.get_default_graph().get_tensor_by_name("embeddings:0")
        phase_train_placeholder = tf.get_default_graph().get_tensor_by_name("phase_train:0")

        prewhiten_face = facenet.prewhiten(face.image)

        # Run forward pass to calculate embeddings
        feed_dict = {images_placeholder: [prewhiten_face], phase_train_placeholder: False}
        return self.sess.run(embeddings, feed_dict=feed_dict)[0]


class Detection:
    # face detection parameters
    minsize = 20  # minimum size of face
    threshold = [0.6, 0.7, 0.7]  # three steps's threshold
    factor = 0.709  # scale factor

    def __init__(self, face_crop_size=160, face_crop_margin=32):
        self.pnet, self.rnet, self.onet = self._setup_mtcnn()
        self.face_crop_size = face_crop_size
        self.face_crop_margin = face_crop_margin

    def _setup_mtcnn(self):
        with tf.Graph().as_default():
            gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=gpu_memory_fraction)
            sess = tf.Session(config=tf.ConfigProto(gpu_options=gpu_options, log_device_placement=False))
            with sess.as_default():
                return detect_face.create_mtcnn(sess, None) # Modified
                # return align.detect_face.create_mtcnn(sess, None) # Original

    def find_faces(self, image):
        faces = []

        bounding_boxes, _ = detect_face.detect_face(image, self.minsize,
                                                          self.pnet, self.rnet, self.onet,
                                                          self.threshold, self.factor) # Modified
        # bounding_boxes, _ = align.detect_face.detect_face(image, self.minsize,
        #                                                   self.pnet, self.rnet, self.onet,
        #                                                   self.threshold, self.factor) # Original

        # print("얼굴에 대한 bounding box") # Modified
        # print("in find_faces1 : ", bounding_boxes) # Modified
        for bb in bounding_boxes:
            # global face
            face = Face()
            face.container_image = image
            face.bounding_box = np.zeros(4, dtype=np.int32)
            face.accuracy = None
            # print("얼굴에 대한 bounding box") # Modified
            # print("in find_faces2 : ", bounding_boxes) # Modified
            # 현재 웹캠의 image.shape -> (480,640,3)
            # print("웹캠에서 들어오는 image.shape") # Modified
            # print("image.shape : ", image.shape) # Modified
            # img_size = 웹캠에서 들어오는 raw image size
            img_size = np.asarray(image.shape)[0:2]
            # print("웹캠에서 들어오는 raw image size") # Modified
            # print("img_size : ", img_size) # Modified
            face.bounding_box[0] = np.maximum(bb[0] - self.face_crop_margin / 2, 0)
            face.bounding_box[1] = np.maximum(bb[1] - self.face_crop_margin / 2, 0)
            face.bounding_box[2] = np.minimum(bb[2] + self.face_crop_margin / 2, img_size[1])
            face.bounding_box[3] = np.minimum(bb[3] + self.face_crop_margin / 2, img_size[0])
            cropped = image[face.bounding_box[1]:face.bounding_box[3], face.bounding_box[0]:face.bounding_box[2], :]
            # cropped = 이미지를 바운딩 박스에 따라 슬라이싱 한 것
            # print("cropped : ", cropped) # Modified
            # print("크롭된 이미지 shape ") # Modified
            # print("cropped.shape : ", cropped.shape) # Modified

            # 여기서 크롭된 이미지를 우리가 설정한 크롭 사이즈로 바꿔주는 작업을 하는 것 같다
            face.image = misc.imresize(cropped, (self.face_crop_size, self.face_crop_size), interp='bilinear')

            # print("face.image : ", face.image) # Modified
            # print("얼굴 이미지 shape") # Modified
            # print("face.image.shape : ", face.image.shape) # Modified
            # print("Detect_face == ", face.accuracy) # Modified
            faces.append(face)

        return faces # Modified
