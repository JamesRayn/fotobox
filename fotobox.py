import sys
import os
import subprocess

from config import fotoboxText, fotoboxCfg
from layout import Ui_Form

from datetime import datetime

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTime, QTimer, QUrl
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5.QtWebKitWidgets import QWebView

from PIL import Image

if not fotoboxCfg['nopi']:
  try:
    from libcamera import Transform
    from picamera2 import Picamera2
    from picamera2.previews.qt import QGlPicamera2
  except ImportError:
    print("PiCamera2 or libcamera not found - operating in simulation mode")
    fotoboxCfg['nopi']            = True
  
  try:
    import RPi.GPIO as GPIO
  except ImportError:
    print("RPi GPIO not found - operating in simulation mode")
    fotoboxCfg['nopi']            = True
  
  if fotoboxCfg['light-pwm']:
    try:
      from rpi_hardware_pwm import HardwarePWM
    except ImportError:
      print("RPi-Hardware-PWM not found - operating without foto light")
      fotoboxCfg['light-pwm']     = False

from shutil import copyfile, move
from stat import S_ISREG, ST_MTIME, ST_MODE

class Ui_Form_mod(Ui_Form):
  def initSystem(self, Form):
    #Blank dummy image
    self.blankImage = QPixmap(1,1)
    self.waiting = QPixmap(os.path.dirname(os.path.realpath(__file__)) + '/design/waiting.png').scaledToWidth(fotoboxCfg['cam-p-width'], QtCore.Qt.SmoothTransformation)
    self.l_lastpic.setPixmap(QPixmap(os.path.dirname(os.path.realpath(__file__)) + '/design/dummy.jpg').scaledToWidth(320, QtCore.Qt.SmoothTransformation))
    self.countdownTime = fotoboxCfg['countdown']
    self.tplFooterOrg = fotoboxCfg['footer']

    if fotoboxCfg['nopi']:
      self.l_footer.setText("Demo simulation mode")

    #Camera + Button LED
    if not fotoboxCfg['nopi']:
      GPIO.setmode(GPIO.BCM)
      GPIO.setup(18, GPIO.OUT)
      GPIO.setup(23, GPIO.OUT)
      GPIO.setup(24, GPIO.OUT)
      if fotoboxCfg['light-pwm']:
        self.pwm = HardwarePWM(0, hz=1000)
        self.pwm.start(10)

      self.camera = Picamera2()
      if fotoboxCfg['cam-p-hflip'] == fotoboxCfg['cam-c-hflip']:
        fotoboxCfg['cam-p-hflip'] = False
      elif fotoboxCfg['cam-c-hflip']:
        if not fotoboxCfg['cam-p-hflip']:
          fotoboxCfg['cam-p-hflip'] = True
      if fotoboxCfg['cam-vflip']:
        fotoboxCfg['cam-c-hflip'] = not fotoboxCfg['cam-c-hflip']

      main_stream = {}
      lores_stream = {"size": (fotoboxCfg['cam-p-width'], fotoboxCfg['cam-p-height'])}
      self.my_config = self.camera.create_still_configuration(main_stream, lores_stream, display="lores", buffer_count=2, transform=Transform(hflip=fotoboxCfg['cam-c-hflip'], vflip=fotoboxCfg['cam-vflip']))

      self.camera.configure(self.my_config)
      self.qpicamera2 = QGlPicamera2(self.camera, width=fotoboxCfg['cam-p-width'], height=fotoboxCfg['cam-p-height'], keep_ar=False, transform=Transform(hflip=fotoboxCfg['cam-p-hflip']))
      self.camera.start()
      self.w_mainpic_lay.addWidget(self.qpicamera2)
      self.qpicamera2.setVisible(False)

    self.isLive = False

    #Countdown Updater
    self.timerCnt = QTimer(Form)
    self.timerCnt.timeout.connect(self.updateCountdown)
    self.timerCnt.setSingleShot(True)

    #Timeout review screen
    self.tout1Cnt = QTimer(Form)
    self.tout1Cnt.timeout.connect(self.doConfirm)
    self.tout1Cnt.setSingleShot(True)

    #Timeout viewer screen
    self.tout2Cnt = QTimer(Form)
    self.tout2Cnt.timeout.connect(self.screenMain)
    self.tout2Cnt.setSingleShot(True)

    self.lastPhoto = ""
    self.screen = ""
    self.temp = fotoboxCfg['temp']
    self.save = fotoboxCfg['save']

    if not self.temp.endswith('/'):
      self.temp += '/'
    if not self.save.endswith('/'):
      self.save += '/'

    if not os.path.exists(self.temp):
      try:
        os.makedirs(self.temp)
      except:
        print("Could not set up temp path")
        self.tplFooterOrg = "Could not set up temp path"
    if not os.path.exists(self.save):
      try:
        os.makedirs(self.save)
      except:
        print("Could not set up save path")
        self.tplFooterOrg = "Could not set up save path"

  def patchDesign(self, Form):
    Form.setWindowTitle("Fotobox")
    Form.showFullScreen()

  def screenMain(self):
    self.screen = 1

    self.tout1Cnt.stop()
    self.tout2Cnt.stop()

    self.l_header.setHtml(fotoboxText['info-home'])
    self.l_btn1.setText(fotoboxText['btn-capture'])
    self.l_btn2.setText(fotoboxText['btn-view'])
    self.l_btn3.setText(fotoboxText['btn-empty'])
    if not fotoboxCfg['nopi']:
      GPIO.output(18, GPIO.HIGH)
      GPIO.output(23, GPIO.HIGH)
      GPIO.output(24, GPIO.LOW)

    if not self.isLive:
      self.l_mainpic.setVisible(False)
      self.l_mainpic.setPixmap(self.blankImage)
      if not fotoboxCfg['nopi']:
        self.qpicamera2.setVisible(True)
        print("Enabling camera preview")
      self.isLive = True

    self.l_footer.setText(self.tplFooterOrg)

  def screenCapture(self):
    self.screen = 2

    self.l_btn1.setText(fotoboxText['btn-empty'])
    self.l_btn2.setText(fotoboxText['btn-empty'])
    self.l_btn3.setText(fotoboxText['btn-empty'])
    if not fotoboxCfg['nopi']:
      GPIO.output(18, GPIO.LOW)
      GPIO.output(23, GPIO.LOW)
      GPIO.output(24, GPIO.LOW)
      if fotoboxCfg['light-pwm']:
        self.pwm.change_duty_cycle(60)

    if not self.isLive:
      self.l_mainpic.setVisible(False)
      self.l_mainpic.setPixmap(self.blankImage)
      if not fotoboxCfg['nopi']:
        self.qpicamera2.setVisible(True)
        print("Enabling camera preview")
      self.isLive = True

    self.l_footer.setText(self.tplFooterOrg)

    #start countdown
    self.countdownTime = fotoboxCfg['countdown'] + 1

    self.updateCountdown()

  def updateCountdown(self):

    if self.countdownTime == fotoboxCfg['countdown'] + 1:
      self.l_header.setHtml(fotoboxText['info-count'])


    self.countdownTime-=1

    if(self.countdownTime > 1):
      self.l_countdown.setText(str(self.countdownTime))
      self.timerCnt.start(1000)
    elif self.countdownTime == 1:
      self.l_header.setHtml(fotoboxText['info-capture'])
      self.l_countdown.setText(str(self.countdownTime))
      if fotoboxCfg['light-pwm']:
        self.pwm.change_duty_cycle(100)
      self.timerCnt.start(1000)
    elif self.countdownTime == 0:

      self.l_countdown.setText("")
      if(self.isLive):
        if not fotoboxCfg['nopi']:
          self.qpicamera2.setVisible(False)
          print("Disabling camera preview", datetime.now())
        self.l_mainpic.setVisible(True)
        self.isLive=False
        self.l_header.setHtml(fotoboxText['info-wait'])
        self.l_mainpic.setPixmap(self.waiting)
        self.l_footer.setText("verarbeite...")
      self.timerCnt.start(1)
    else:
      self.photoTake()

  def photoTake(self):

    self.lastPhoto = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".jpg"
    print("take picture", datetime.now())
    if not fotoboxCfg['nopi']:
      self.camera.capture_file(self.temp+self.lastPhoto)

      if fotoboxCfg['light-pwm']:
        self.pwm.change_duty_cycle(10)
    else:
      copyfile(os.path.dirname(os.path.realpath(__file__)) + '/design/dummy.jpg', self.temp+self.lastPhoto)

    self.screenReview()

  def screenReview(self):
    self.screen = 3

    print("screenReview", datetime.now())
    self.l_header.setHtml(fotoboxText['info-review'])
    self.l_btn1.setText(fotoboxText['btn-recapture'])
    self.l_btn2.setText(fotoboxText['btn-save'])
    self.l_btn3.setText(fotoboxText['btn-cancel'])
    if not fotoboxCfg['nopi']:
      GPIO.output(18, GPIO.HIGH)
      GPIO.output(23, GPIO.HIGH)
      GPIO.output(24, GPIO.HIGH)
    self.lastpic = QPixmap(self.temp+self.lastPhoto)
    self.l_mainpic.setPixmap(self.lastpic.scaledToWidth(fotoboxCfg['cam-p-width'], QtCore.Qt.SmoothTransformation))
    self.l_footer.setText("Foto: " + self.lastPhoto)
    self.lastpic = self.lastpic.scaledToWidth(320, QtCore.Qt.SmoothTransformation)
    
    #start timeout
    self.tout1Cnt.start(fotoboxCfg['timeout1']*1000)

  def tempDel(self):
    if self.lastPhoto != "" and os.path.isfile(self.temp+self.lastPhoto):
      os.remove(self.temp+self.lastPhoto)
      self.lastPhoto = ""

  def noConfirm(self):
    self.tout1Cnt.stop()
    self.tempDel()
    self.screenMain()

  def doConfirm(self):
    self.tout1Cnt.stop()
    move(self.temp+self.lastPhoto, self.save+self.lastPhoto)
    self.tplImage2 = self.save+self.lastPhoto
    self.l_lastpic.setPixmap(self.lastpic)
    print("Saved " + self.save+self.lastPhoto)
    self.screenMain()

  def another(self):
    self.tout1Cnt.stop()
    move(self.temp+self.lastPhoto, self.save+self.lastPhoto)
    self.tplImage2 = self.save+self.lastPhoto
    self.l_lastpic.setPixmap(self.lastpic)
    print("Saved " + self.save+self.lastPhoto)
    self.screenCapture()

  def startViewer(self):
    self.screen = 4

    if(self.isLive):
      if not fotoboxCfg['nopi']:
        self.qpicamera2.setVisible(False)
      self.l_mainpic.setVisible(True)
      self.isLive=False

    self.entries = None
    self.entries = (os.path.join(self.save, fn) for fn in os.listdir(self.save))
    self.entries = ((os.stat(path), path) for path in self.entries)
    self.entries = ((stat[ST_MTIME], path)
      for stat, path in self.entries if S_ISREG(stat[ST_MODE]))
    self.entries = list(self.entries)

    if(len(self.entries) > 0):
      self.viewerIndex = (len(self.entries)-1) #0
      self.screenViewer()
    else:
      print("No images to show")
      self.screenMain()

  def screenViewer(self):
    self.l_header.setHtml(fotoboxText['info-view'])

    if(self.viewerIndex < (len(self.entries)-1)):
      self.l_btn1.setText(fotoboxText['btn-next'])
      if not fotoboxCfg['nopi']:
        GPIO.output(18, GPIO.HIGH)
    else:
      self.l_btn1.setText(fotoboxText['btn-empty'])
      if not fotoboxCfg['nopi']:
        GPIO.output(18, GPIO.LOW)
    
    if(self.viewerIndex > 0):
      self.l_btn2.setText(fotoboxText['btn-previous'])
      if not fotoboxCfg['nopi']:
        GPIO.output(23, GPIO.HIGH)
    else:
      self.l_btn2.setText(fotoboxText['btn-empty'])
      if not fotoboxCfg['nopi']:
        GPIO.output(23, GPIO.LOW)

    self.l_btn3.setText(fotoboxText['btn-back'])
    if not fotoboxCfg['nopi']:
      GPIO.output(24, GPIO.HIGH)
    pixmap = QPixmap(str(self.entries[self.viewerIndex][1]))
    self.l_mainpic.setPixmap(pixmap.scaledToWidth(fotoboxCfg['cam-p-width'], QtCore.Qt.SmoothTransformation))
    self.l_footer.setText("Foto " + str(self.viewerIndex+1) + \
      ' von ' + str(len(self.entries)) + \
      " · " + str(os.path.basename(self.entries[self.viewerIndex][1])))
    
    #start timeout
    self.tout2Cnt.start(fotoboxCfg['timeout2']*1000)

  def viewPrev(self):
    if(self.viewerIndex > 0):
      self.viewerIndex -= 1
    self.screenViewer()

  def viewNext(self):
    if(self.viewerIndex < (len(self.entries)-1)):
      self.viewerIndex += 1
    self.screenViewer()

class QDialog_mod(QDialog):
  def __init__(self):
    super(QDialog, self).__init__()
    self.ui = Ui_Form_mod()
    self.ui.setupUi(self)
    self.ui.initSystem(self)
    self.ui.patchDesign(self)
    self.ui.screenMain()

    if not fotoboxCfg['nopi']:
      GPIO.setmode(GPIO.BCM)

      GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
      GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)
      GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)

      self.btnC1 = GPIO.HIGH
      self.btnC2 = GPIO.HIGH
      self.btnC3 = GPIO.HIGH

    #Key Poller
    self.timerKey = QTimer(self)
    self.timerKey.timeout.connect(self.buttonCheck)
    self.timerKey.start(25)
    self.btnB  = 1

    #self.showFullScreen()
    self.setVisible(True)

  def buttonCheck(self):
    if not fotoboxCfg['nopi']:
      if self.btnB == 0:
        if GPIO.input(17) != self.btnC1:
          self.btnB = 3
          if GPIO.input(17) == GPIO.LOW:
            self.buttonPress(1)
          self.btnC1 = GPIO.input(17)
        if GPIO.input(27) != self.btnC2:
          self.btnB = 3
          if GPIO.input(27) == GPIO.LOW:
            self.buttonPress(2)
          self.btnC2 = GPIO.input(27)
        if GPIO.input(22) != self.btnC3:
          self.btnB = 3
          if GPIO.input(22) == GPIO.LOW:
            self.buttonPress(3)
          self.btnC3 = GPIO.input(22)
      else:
        self.btnB -= 1

  #keyHandling
  def buttonPress(self, btn):
    print("Button Event: " + str(btn), datetime.now())
    if(self.ui.screen == 1):
      if(btn == 1):
        self.ui.screenCapture()
      elif(btn == 2):
        self.ui.startViewer()
    elif(self.ui.screen == 3):
      if(btn == 1):
        self.ui.another()
      elif(btn == 2):
        self.ui.doConfirm()
      elif(btn == 3):
        self.ui.noConfirm()
    elif(self.ui.screen == 4):
      if(btn == 1):
        self.ui.viewNext()
      elif(btn == 2):
        self.ui.viewPrev()
      elif(btn == 3):
        self.ui.screenMain()

  def keyPressEvent(self, e):
    if e.key() == QtCore.Qt.Key_Escape:
      if not fotoboxCfg['nopi']:
        GPIO.cleanup()
        if fotoboxCfg['light-pwm']:
          self.ui.pwm.stop()
      self.close()
    elif e.key() == QtCore.Qt.Key_1:
      self.buttonPress(1)
    elif e.key() == QtCore.Qt.Key_2:
      self.buttonPress(2)
    elif e.key() == QtCore.Qt.Key_3:
      self.buttonPress(3)
    elif e.key() == QtCore.Qt.Key_0:
      os.system('sudo shutdown -h now')

app = QApplication(sys.argv)
window = QDialog_mod()

sys.exit(app.exec_())