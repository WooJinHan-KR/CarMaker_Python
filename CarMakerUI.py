import sys
import subprocess
import cmapi
import pathlib
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QFileDialog, QLabel
from PyQt5.QtGui import QIcon

class SimpleGUI(QWidget):
    def __init__(self):
        super().__init__()

        self.project_path = None

        self.init_ui()

    def init_ui(self):
        # Create Button
        self.start_button = QPushButton('Start', self)
        self.stop_button = QPushButton('Stop', self)
        self.open_button = QPushButton('Open', self)
        self.select_path_button = QPushButton('프로젝트 경로 선택', self)
        self.load_project_button = QPushButton('프로젝트 불러오기', self)

        # Create Event Handler connected for button
        self.start_button.clicked.connect(self.start_clicked)
        self.stop_button.clicked.connect(self.stop_clicked)
        self.open_button.clicked.connect(self.open_clicked)
        self.select_path_button.clicked.connect(self.select_path_clicked)
        self.load_project_button.clicked.connect(self.load_project_clicked)

        # Layout and add button
        layout = QVBoxLayout()
        layout.addWidget(self.select_path_button)
        layout.addWidget(self.load_project_button)
        layout.addWidget(self.start_button)
        layout.addWidget(self.stop_button)
        layout.addWidget(self.open_button)

        self.path_label = QLabel(self)
        layout.addWidget(self.path_label)

        self.setLayout(layout)

        # 창 크기 및 제목 설정
        self.setGeometry(300, 300, 400, 200)
        self.setWindowTitle('CarMaker 12.0.1')

    def select_path_clicked(self):
        # 폴더 대화 상자를 통해 경로 선택
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        selected_folder = QFileDialog.getExistingDirectory(self, "프로젝트 폴더 선택", options=options)

        if selected_folder:
            # 선택된 폴더 경로를 변수에 저장
            self.project_path = pathlib.Path(selected_folder)

            # 선택된 경로를 레이블에 표시
            self.path_label.setText(f'선택된 프로젝트 경로: {str(self.project_path)}')

    def load_project_clicked(self):
        if self.project_path:
            try:
                # 프로젝트 로드
                cmapi.Project.load(self.project_path)
            except Exception as e:
                print(f'프로젝트를 불러오는 중 오류 발생: {e}')
        else:
            print('프로젝트 경로가 선택되지 않았습니다.')

    def start_clicked(self):

        print('Start Simulation')

    def stop_clicked(self):
        print('Stop Simulation')

    def open_clicked(self):
        file_path = r'C:\IPG\carmaker\win64-12.0.1\bin\CM.exe'
        
        try:
            subprocess.run([file_path], check=True)
        except subprocess.CalledProcessError as e:
            print(f'Error: {e}')

        print('Run CarMaker')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = SimpleGUI()
    gui.show()
    cmapi.Task.run_main_task(main())
    sys.exit(app.exec_())
