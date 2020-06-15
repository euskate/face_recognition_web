# 얼굴 인식 프로젝트 웹

- 사용 라이브러리

- 가동시 가상환경과 데이터베이스를 맞추어주어야 합니다.
  - /config/settings.py
  - /face/views.py
  
- 모델 경로 수정
  - /face/face.py
  - /face/views.py

- 모델 분할 압축
  - 모델은 용량 문제로 분할 압축하였습니다. (3종류의 모델 첨부)
  - /models/
    - model2018 : VGG model
    - model_kfcl12 : kface, asian_celeb 전이학습 1차 모델
    - model_kfcl63 : kface, asian_celeb 전이학습 2차 모델

- 웹 : django
- 데이터베이스 : postgreSQL
- 학습 : tensorflow
- 이미지 처리 : openCV
- css framwork : bootstrap
- 주요 라이브러리

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

- pip list
```
Package             Version
------------------- ------------
absl-py             0.9.0
astor               0.8.1
astroid             2.0.4
bleach              3.1.4
certifi             2018.8.24
chardet             3.0.4
cycler              0.10.0
decorator           4.4.2
defusedxml          0.6.0
Django              2.1.7
djangorestframework 3.11.0
entrypoints         0.2.3
gast                0.3.3
grpcio              1.29.0
h5py                2.10.0
html5lib            0.9999999
idna                2.9
importlib-metadata  1.6.0
ipykernel           4.10.0
ipython             5.8.0
ipython-genutils    0.2.0
ipywidgets          7.4.1
isort               4.3.4
Jinja2              2.11.2
joblib              0.14.1
jsonschema          2.6.0
jupyter             1.0.0
jupyter-client      5.3.3
jupyter-console     5.2.0
jupyter-core        4.5.0
kiwisolver          1.1.0
lazy-object-proxy   1.3.1
Markdown            3.2.2
MarkupSafe          1.0
matplotlib          3.0.3
mccabe              0.6.1
mistune             0.8.3
nbconvert           5.5.0
nbformat            5.0.6
notebook            5.6.0
numpy               1.16.2
opencv-python       4.2.0.34
pandas              0.25.3
pandocfilters       1.4.2
pexpect             4.6.0
pickleshare         0.7.4
Pillow              7.1.2
pip                 20.1.1
prometheus-client   0.7.1
prompt-toolkit      1.0.15
protobuf            3.12.0
psutil              5.7.0
psycopg2            2.7.5
ptyprocess          0.6.0
Pygments            2.6.1
pylint              2.1.1
pyparsing           2.4.7
python-dateutil     2.8.1
pytz                2020.1
pyzmq               19.0.1
qtconsole           4.7.4
QtPy                1.9.0
requests            2.23.0
scikit-learn        0.22.2.post1
scipy               1.2.1
Send2Trash          1.5.0
setuptools          40.2.0
simplegeneric       0.8.1
six                 1.14.0
sqlparse            0.3.1
tensorboard         1.7.0
tensorflow          1.7.0
termcolor           1.1.0
terminado           0.8.1
testpath            0.4.4
tornado             5.1.1
traitlets           4.3.2
typed-ast           1.1.0
urllib3             1.25.9
wcwidth             0.1.9
webencodings        0.5.1
Werkzeug            1.0.1
wheel               0.31.1
widgetsnbextension  3.4.1
wrapt               1.10.11
zipp                1.2.0
```

- 가상의 데이터베이스와 뷰를 사용