# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/Users/rl/PycharmProjects/SimleyBudding/form.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QGraphicsObject
import cv2
import requests


class Ui_Form(QGraphicsObject):

    def setupUi(self, Form):

        Form.setObjectName("Form")
        Form.resize(563, 413)
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(200, 230, 114, 32))
        self.pushButton.setObjectName("pushButton")


        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.pushButton.setText(_translate("Form", "Smile!"))
        self.pushButton.clicked.connect(self.printMessageEvent)

    def printMessageEvent(self):
        """
        Signal means that I can send signal to another worker
        To receive a signal, I need to be connected.
        :return:
        """
        self.print_thread = TestThread()
        self.print_thread.finished.connect(self.button_done)
        self.print_thread.sig.connect(self.emit_callback)
        self.pushButton.setEnabled(False)
        self.print_thread.start()

    def button_done(self):
        self.pushButton.setEnabled(True)

    def emit_callback(self, message):
        print(message)




class TestThread(QThread):

    sig = pyqtSignal(list)

    def __init__(self):
        QThread.__init__(self)
        self.msg = None

    def __del__(self):
        self.wait()

    def run(self):

        cap = cv2.VideoCapture(0)

        # Capture frame-by-frame
        ret, frame = cap.read()

        # Our operations on the frame come here
        # gray = cv2.cvtColor(frame, cv2.COLOR_BAYER_BG2BGR)

        # Display the resulting frame
        cv2.imshow('frame', frame)
        cv2.imwrite('img.JPEG', frame)
        # When everything done, release the capture
        cap.release()
        cv2.destroyAllWindows()

        subscription_key = "9c2a662ceba54c96902f6b78430f01bb"

        emotion_recognition_url = "https://eastus.api.cognitive.microsoft.com/face/v1.0/detect"

        image_path = "img.JPEG"
        params = {
            'returnFaceId': 'true',
            'returnFaceLandmarks': 'false',
            'returnFaceAttributes': 'emotion'
        }

        with open('img.JPEG', 'rb') as f:
            image_data = f.read()

        headers = {'Ocp-Apim-Subscription-Key': subscription_key, "Content-Type": "application/octet-stream"}
        response = requests.post(emotion_recognition_url, headers=headers, params=params, data=image_data)
        response.raise_for_status()
        analysis = response.json()

        self.sig.emit(analysis)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

#