import sys

import Thread_pars
from gui.qt_core import *
from Utils.style import *


class Ui_MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(Ui_MainWindow, self).__init__(parent)

        self.setupUi(self)

        self.btn_start.clicked.connect(self.start_check_button)

        self.btn_select_file.clicked.connect(self.select_file)

        self.pars_thread = Thread_pars.Thread_pars(mainwindow=self)


    def setupUi(self, MainWindow):

        MainWindow.resize(1200, 700)
        MainWindow.setStyleSheet(u"background: #1C1C1E;")
        self.centralwidget = QWidget(MainWindow)

        self.btn_frame = QFrame(self.centralwidget)
        self.btn_frame.setGeometry(QRect(0, 0, 1200, 50))
        self.btn_frame.setStyleSheet(u"QFrame { border-bottom: 1px solid #404042; background: #1C1C1E; }")

        self.main_frame_proccess = QFrame(self.centralwidget)
        self.main_frame_proccess.setGeometry(QRect(0, 50, 1200, 650))
        self.main_frame_proccess.setStyleSheet(u"QFrame { background: #1C1C1E; }")

        self.btn_select_file = QPushButton(self.btn_frame)
        self.btn_select_file.setGeometry(QRect(0, 0, 110, 49))
        self.btn_select_file.setStyleSheet(btn_style)
        self.btn_select_file.setText("Select file")

        self.btn_start = QPushButton(self.btn_frame)
        self.btn_start.setGeometry(QRect(111, 0, 110, 49))
        self.btn_start.setStyleSheet(btn_style)
        self.btn_start.setText("Start")

        self.label_version = QLabel(self.btn_frame)
        self.label_version.setGeometry(QRect(950, 16, 240, 20))
        self.label_version.setStyleSheet("font-family: 'Inter';font-style: normal;font-weight: 400;font-size: 16px;line-height: 19px;color: #404042; border: none;")
        self.label_version.setText("CryptoWallets checker     v1.0.0")

        self.label_selected_file = QLabel(self.main_frame_proccess)
        self.label_selected_file.setGeometry(QRect(10, 20, 100, 20))
        self.label_selected_file.setStyleSheet("font-family: 'Inter';font-style: normal;font-weight: 400;font-size: 16px;line-height: 19px;color: #4374B1; background: none;")
        self.label_selected_file.setText("Selected file:")

        self.label_file_name = QLabel(self.main_frame_proccess)
        self.label_file_name.setGeometry(QRect(120, 20, 500, 20))
        self.label_file_name.setStyleSheet("font-family: 'Inter';font-style: normal;font-weight: 400;font-size: 16px;line-height: 19px;color: #4374B1;")
        self.label_file_name.setText("None")

        self.label_state = QLabel(self.main_frame_proccess)
        self.label_state.setGeometry(QRect(1000, 40, 300, 20))
        self.label_state.setStyleSheet("font-family: 'Inter';font-style: normal;font-weight: 400;font-size: 16px;line-height: 19px;color: #77A7D6;")
        self.label_state.setText("The script is not running")


        self.list_widget = QListWidget(self.main_frame_proccess)
        self.list_widget.setGeometry(QRect(10, 65, 1180, 575))
        self.list_widget.setStyleSheet(u"QListWidget { background: #1C1C1E; border: 2px solid #404042; border-radius: 8px; padding-left: 15px; padding-top: 15px; padding-bottom: 15px; color: #51A764;}")
        self.list_widget.setLineWidth(1)
        self.list_widget.setMidLineWidth(0)
        self.list_widget.setAutoScroll(True)
        self.list_widget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.list_widget.setSpacing(2)

        MainWindow.setCentralWidget(self.centralwidget)


    def select_file(self):
        self.file = QFileDialog.getOpenFileName()[0]
        self.label_file_name.setText(self.file)

    def start_check_button(self):
        print("start")
        self.pars_thread.start()
        self.label_state.setText("Script is working")  # TODO Remove the label after the script runs


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Ui_MainWindow()
    window.show()
    sys.exit(app.exec())

