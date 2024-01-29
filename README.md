## CarMaker_Python

CarMaker에서 Python API를 이용해 할 수 있는 동작과 예시 모음

* Test 실행을 설정하고 매개변수화
* 실행 중인 Simulation을 제어
* 여러 Simulation을 실행해서 자동화 범위를 손쉽게 함
* CarMaker Interface Toolbox 응용 프로그램 관리

---
## Setting

* CarMaker 12ver 예시로 진행중이며 버전 별로 다른 세부 정보는 공식 문서 참조
* CarMaker 버전에 맞는 Python 버전은 C: > IPG > carmaker > {Os - version} 안에 있는 Setup Python-API-py3.6..3.10Add-On 파일을 참조
* 위의 파일 이름에서 Python3.6 ~ 3.10 버전을 지원함을 확인
* 적절한 python ver 다운
* python API 검색경로 추가 - window 기준 shell 열어서
```
$env:PYTHONPATH = "C:/IPG/carmaker/win64-버전명/Python/python버전;$env:PYTHONPATH"

```
또는
```
set PYTHONPATH=C:/IPG/carmaker/win64-버전명/Python/python버전;%PYTHONPATH%

```
입력. 나는 12.0.1 ver에 python3.8을 사용하기 떄문에

```
$env:PYTHONPATH = "C:/IPG/carmaker/win64-12.0.1/Python/python3.8;$env:PYTHONPATH"

```
