from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPainter #, QPixmap
from PyQt5.QtWebKitWidgets import QWebView
#import os


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1280, 1024)
        Form.setStyleSheet("QWidget#Form {background-image: url(design/backdrop.png);}")

        # Header label
        self.l_header = QWebView(Form)
        self.l_header.setGeometry(50, 15, 860, 115)
        self.l_header.setStyleSheet("background: transparent")
        self.l_header.setObjectName("l_header")

        # MainPic viewer
        self.l_mainpic = QtWidgets.QLabel()
        self.l_mainpic.setObjectName("l_mainpic")

        self.w_mainpic = QtWidgets.QWidget(Form)
        self.w_mainpic.setGeometry(28, 205, 906, 680)
        self.w_mainpic.setObjectName("w_mainpic")

        self.w_mainpic_lay = QtWidgets.QGridLayout(self.w_mainpic)
        self.w_mainpic_lay.setContentsMargins(0, 0, 0, 0)
        self.w_mainpic_lay.setObjectName("w_mainpic_lay")
        self.w_mainpic_lay.addWidget(self.l_mainpic)#, 0, 0, 1, 1)

        # LastPic viewer
        self.w_picframe = QtWidgets.QWidget()
        self.w_picframe.setGeometry(0, 0, 350, 303)
        self.w_picframe.setStyleSheet("QWidget#w_picframe {background: transparent; background-image: url(design/picframe-s.png);}")
        self.w_picframe.setObjectName("w_picframe")

        self.l_lastpic = QtWidgets.QLabel(self.w_picframe)
        self.l_lastpic.setGeometry(12, 13, 320, 240)
        self.l_lastpic.setObjectName("l_lastpic")

        self.w_proxy = QtWidgets.QGraphicsProxyWidget()
        self.w_proxy.setWidget(self.w_picframe)
        self.w_proxy.setTransformOriginPoint(self.w_proxy.boundingRect().center())
        self.w_proxy.setRotation(15)
        self.w_graphicsview = QtWidgets.QGraphicsView()
        self.w_graphicsview.setRenderHints(QPainter.Antialiasing | QPainter.SmoothPixmapTransform)
        self.w_graphicsview.setStyleSheet("border-style: none;")
        self.w_scene = QtWidgets.QGraphicsScene(self.w_graphicsview)
        self.w_scene.addItem(self.w_proxy)
        self.w_graphicsview.setScene(self.w_scene)

        self.w_lastpic = QtWidgets.QWidget(Form)
        self.w_lastpic.setGeometry(934, -30, 417, 388) # x starting next to MainPic
        self.w_lastpic.setStyleSheet("background: transparent")
        self.w_lastpic.setObjectName("w_lastpic")

        self.w_lastpic_lay = QtWidgets.QGridLayout(self.w_lastpic)
        self.w_lastpic_lay.setContentsMargins(0, 0, 0, 0)
        self.w_lastpic_lay.setObjectName("w_lastpic_lay")
        self.w_lastpic_lay.addWidget(self.w_graphicsview)

        # Countdown label
        font = QtGui.QFont()
        font.setFamily("Kalam")
        font.setPixelSize(115)
        font.setBold(True)

        self.l_countdown = QtWidgets.QLabel(Form)
        self.l_countdown.setGeometry(830, 15, 80, 125)
        self.l_countdown.setFont(font)
        self.l_countdown.setAlignment(QtCore.Qt.AlignCenter)
        self.l_countdown.setObjectName("l_countdown")

        # Button labels
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

        # Footer label
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

        # Layer order
        self.l_header.raise_()
        self.l_countdown.raise_()
        self.l_btn1.raise_()
        self.l_btn2.raise_()
        self.l_btn3.raise_()
        self.l_footer.raise_()
        self.w_mainpic.raise_()
        self.w_lastpic.raise_()

        self.retranslateUi(Form)


    def retranslateUi(self, Form):
        Form.setWindowTitle("Fotobox UI")
        self.l_header.setHtml("<center><h1>UI-Test an der Fotobox</h1></center>")
        self.l_mainpic.setText("                              MainPic")
        self.l_lastpic.setText("                              LastPic")
        
        #pixmap = QPixmap(os.path.dirname(os.path.realpath(__file__)) + '/design/dummy.jpg')
        #self.l_lastpic.setPixmap(pixmap.scaledToWidth(320, QtCore.Qt.SmoothTransformation))
        #self.l_mainpic.setPixmap(pixmap.scaledToWidth(906, QtCore.Qt.SmoothTransformation))
        
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
