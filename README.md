## CarMaker use with Python API

---
## CarMakerUI.py

* cmapi, python api로 간단하게 CarMaker 실행하는 예제
* Test 실행을 설정하고 매개변수화
* 실행 중인 Simulation을 제어
* 여러 Simulation을 실행해서 자동화 범위를 손쉽게 함
* CarMaker Interface Toolbox 응용 프로그램 관리

---
## Autonomous.py

* Script Control, cmapi 사용
* import CameraRSI.py, Lanedetection.py
* CarMaker에서 CameraRSI 센서에서 나오는 Tcp 데이터를 읽어옴
* 데이터를 읽어서 Opencv 라이브러리를 사용해 차선 인식 및 검출
* CarMaker에 DVA Write하는 방식으로 작동해 Delay 발생하기 때문에 차선 인식만 실행

---
## Setting

* CarMaker 12ver 예시로 진행중이며 버전 별로 다른 세부 정보는 공식 문서 참조
* CarMaker 버전에 맞는 Python 버전은 C: > IPG > carmaker > {Os - version} 안에 있는 Setup Python-API-py3.6..3.10Add-On 파일을 참조
* 위 파일 이름에서 Python3.6 ~ 3.10 버전을 지원함을 확인
* 적절한 python ver 다운 후 환경변수에 설치 경로 추가
* python API 검색경로 추가 - window 기준 shell 열어서

```
$env:PYTHONPATH = "C:/IPG/carmaker/win64-버전명/Python/python버전;$env:PYTHONPATH"

```
또는 아래와 같이 환경변수 설정
```
set PYTHONPATH=C:/IPG/carmaker/win64-버전명/Python/python버전;%PYTHONPATH%

```
12.0.1 ver에 python3.8을 사용하기 떄문에 아래와 같이 입력

```
$env:PYTHONPATH = "C:/IPG/carmaker/win64-12.0.1/Python/python3.8;$env:PYTHONPATH"

```
## Run

* cmd 창 열고 C:\IPG\carmaker\win64-12.0.1\Examples\Python 들어가서 runtime_minimal_example.py 편집기로 실행
* PythonAPI 경로 추가, 프로젝트 경로 입력(위 Setting에서 환경변수 인지 못할 때)

```python
import sys
sys.path.append("C:/IPG/carmaker/win64-12.0.1/Python/python3.8")

    project_path = Path("C:\CM_Projects\프로젝트명")

```
* runtime_minimal_example.py에서 터미널 열고
```
python3 runtime_minimal_example.py
```
* python이 3버전만 깔려있으면
```
python runtime_minimal_example.py
```