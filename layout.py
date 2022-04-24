from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWebKitWidgets import QWebView


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1280, 1024)

        self.l_header = QWebView(Form)
        self.l_header.setGeometry(50, 15, 860, 115)
        self.l_header.setStyleSheet("background:transparent")
        self.l_header.setObjectName("l_header")


        #self.l_header = QtWidgets.QLabel(Form)
        #self.l_header.setGeometry(50, 15, 860, 115)
        #self.l_header.setFont(font)
        #self.l_header.setAlignment(QtCore.Qt.AlignCenter)
        #self.l_header.setWordWrap(True)
        #self.l_header.setObjectName("l_header")

        # zur Positionierung benötigt
        self.p_mountpoint = QtWidgets.QWidget(Form)
        self.p_mountpoint.setGeometry(28, 205, 906, 680)
        self.p_mountpoint.setObjectName("p_mountpoint")

        # mount point für Kamera und Bildbetrachter
        self.w_viewpoint = QtWidgets.QGridLayout(self.p_mountpoint)
        self.w_viewpoint.setContentsMargins(0, 0, 0, 0)
        self.w_viewpoint.setObjectName("w_viewpoint")

        # Bildbetrachter
        self.l_image = QtWidgets.QLabel(self.p_mountpoint)
        self.l_image.setObjectName("l_image")

        self.w_viewpoint.addWidget(self.l_image, 0, 0, 1, 1)

        # Hintergrund + letztem Bild
        self.bg_lastpic = QWebView(Form)
        self.bg_lastpic.setGeometry(0, 0, 1280, 1024)
        self.bg_lastpic.setObjectName("bg_lastpic")

        font = QtGui.QFont()
        font.setFamily("Kalam")
        font.setPixelSize(115)
        font.setBold(True)

        self.l_countdown = QtWidgets.QLabel(Form)
        self.l_countdown.setGeometry(830, 15, 80, 125)
        self.l_countdown.setFont(font)
        self.l_countdown.setAlignment(QtCore.Qt.AlignCenter)
        self.l_countdown.setObjectName("l_countdown")

        font = QtGui.QFont()
        font.setFamily("Kalam")
        font.setPixelSize(45)

        self.l_btn1 = QtWidgets.QLabel(Form)
        self.l_btn1.setGeometry(965, 552, 300, 90)
        self.l_btn1.setFont(font)
        self.l_btn1.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
        self.l_btn1.setObjectName("l_btn1")

        self.l_btn2 = QtWidgets.QLabel(Form)
        self.l_btn2.setGeometry(965, 702, 300, 90)
        self.l_btn2.setFont(font)
        self.l_btn2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
        self.l_btn2.setObjectName("l_btn2")

        self.l_btn3 = QtWidgets.QLabel(Form)
        self.l_btn3.setGeometry(965, 852, 300, 90)
        self.l_btn3.setFont(font)
        self.l_btn3.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
        self.l_btn3.setObjectName("l_btn3")

        font = QtGui.QFont()
        font.setFamily("Kalam")
        font.setPixelSize(33)

        self.l_footer = QtWidgets.QLabel(Form)
        self.l_footer.setGeometry(28, 900, 906, 95)
        self.l_footer.setFont(font)
        self.l_footer.setStyleSheet("color: #7a7a7a;")
        self.l_footer.setAlignment(QtCore.Qt.AlignCenter)
        self.l_footer.setWordWrap(True)
        self.l_footer.setObjectName("l_footer")

        # Ebenensortierung
        self.bg_lastpic.raise_()
        self.l_header.raise_()
        self.l_countdown.raise_()
        self.l_btn1.raise_()
        self.l_btn2.raise_()
        self.l_btn3.raise_()
        self.l_footer.raise_()
        self.p_mountpoint.raise_()

        self.retranslateUi(Form)


    def retranslateUi(self, Form):
        Form.setWindowTitle("Fotobox UI")
        #self.l_header.setText("Willkommen an der Fotobox")
        self.l_header.setHtml("Willkommen an der Fotobox")
        self.bg_lastpic.setHtml("<body style=\"background-color: #bed4ed;\"><div id=\"LastPic\" style=\"position: fixed; right: 50px; top: 50px; transform: rotate(15deg);\">LastPic</div>"
            "<div id=\"MainPic\" style=\"position: fixed; left: 450px; top: 500px;\">MainPic</div></body>")
        self.l_btn1.setText("Button 1 ▶")
        self.l_btn2.setText("Button 2 ▶")
        self.l_btn3.setText("Button 3 ▶")
        self.l_footer.setText("Fotobox-Party")


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
