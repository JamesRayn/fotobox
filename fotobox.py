import sys
import os
import subprocess

from config import fotoboxText, fotoboxCfg

from datetime import datetime, date, time
from time import sleep

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTime, QTimer, QUrl
from PyQt5.QtGui import QIcon, QPixmap, QCursor
from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5.QtWebKitWidgets import QWebView
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow

if not fotoboxCfg['nopi']:
  try:
    from picamera import PiCamera
  except ImportError:
    print("PiCamera not found - operating in simulation mode")
    fotoboxCfg['nopi']            = True
  
  try:
    import RPi.GPIO as GPIO
  except ImportError:
    print("RPi GPIO not found - operating in simulation mode")
    fotoboxCfg['nopi']            = True
  
  try:
    from rpi_hardware_pwm import HardwarePWM
  except ImportError:
    print("rpi-hardware-pwm not found - operating in simulation mode")
    fotoboxCfg['nopi']            = True

from shutil import copyfile, move
from stat import S_ISREG, ST_MTIME, ST_MODE

class Ui_Form_mod(object):
  def setupUi(self, Form):
    Form.setObjectName("Form")
    Form.setWindowTitle("Fotobox")
    Form.resize(fotoboxCfg['window-width'], fotoboxCfg['window-height'])
    Form.setMinimumSize(QtCore.QSize(fotoboxCfg['window-width'], fotoboxCfg['window-height']))
    Form.setMaximumSize(QtCore.QSize(fotoboxCfg['window-width'], fotoboxCfg['window-height']))
    Form.setHtml("Initializing...")
    self.countdownTime = fotoboxCfg['countdown']
    self.entries = None
    self.tplFooterOrg = fotoboxCfg['footer']
    self.tplImage = "init.png"
    self.tplImage2 = "dummy.jpg"
    self.tplFooter = self.tplFooterOrg
    self.tplInstruct = "Instruction placeholder"
    self.tplBtn1 = "Button 1"
    self.tplBtn2 = "Button 2"
    self.tplBtn3 = "Button 3"
    with open('design/template.html', 'r') as myfile:
      self.template=myfile.read().replace('\n', '')

    if fotoboxCfg['nopi']:
      self.tplFooterOrg = "Demo simulation mode"

  def initSystem(self, Form):
    #Camera + Button LED
    if not fotoboxCfg['nopi']:
      GPIO.setmode(GPIO.BCM)
      self.pwm = HardwarePWM(0, hz=600)
      self.pwm.start(10)
      GPIO.setup(18, GPIO.OUT)
      GPIO.setup(23, GPIO.OUT)
      GPIO.setup(24, GPIO.OUT)
      self.camera = PiCamera()
      self.camera.hflip = fotoboxCfg['cam-c-hflip']
      if(fotoboxCfg['cam-p-hflip'] == fotoboxCfg['cam-c-hflip']):
        fotoboxCfg['cam-p-hflip'] = False
    self.isLive = False

    #Countdown Updater
    self.timerCnt = QTimer(Form)
    self.timerCnt.timeout.connect(self.updateCountdown)
    self.timerCnt.setSingleShot(True)
    
    #Timeout review screen
    self.tout1Cnt = QTimer(Form)
    self.tout1Cnt.timeout.connect(self.timeout1)
    self.tout1Cnt.setSingleShot(True)

    #Timeout viewer screen
    self.tout2Cnt = QTimer(Form)
    self.tout2Cnt.timeout.connect(self.timeout2)
    self.tout2Cnt.setSingleShot(True)

    #Blank dummy image
    self.blankImage = QPixmap(1,1)

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

  def updateHtml(self, Form):
    data = self.template
    data = data.replace('${btn1}', self.tplBtn1, 1)
    data = data.replace('${btn2}', self.tplBtn2, 1)
    data = data.replace('${btn3}', self.tplBtn3, 1)
    data = data.replace('${info}', self.tplInstruct, 1)
    data = data.replace('${status}', self.tplFooter, 1)
    data = data.replace('${image}', self.tplImage, 1)
    data = data.replace('${image2}', self.tplImage2, 1)
    Form.setHtml(data, QUrl('file://'+os.path.dirname(os.path.realpath(__file__))+'/design/.'))

  def screenMain(self, Form):
    self.screen = 1
    
    self.tout1Cnt.stop()
    self.tout2Cnt.stop()

    self.tplInstruct = fotoboxText['info-home']
    self.tplBtn1 = fotoboxText['btn-capture']
    self.tplBtn2 = fotoboxText['btn-view']
    self.tplBtn3 = fotoboxText['btn-empty']
    if not fotoboxCfg['nopi']:
      GPIO.output(18, GPIO.HIGH)
      GPIO.output(23, GPIO.HIGH)
      GPIO.output(24, GPIO.LOW)

    if not self.isLive:
      self.tplImage = "liveBack.png"
      if not fotoboxCfg['nopi']:
        self.camera.start_preview(fullscreen=False, window = (fotoboxCfg['cam-p-x'], fotoboxCfg['cam-p-y'], fotoboxCfg['cam-p-width'], fotoboxCfg['cam-p-height']), hflip=fotoboxCfg['cam-p-hflip'])
        print("Enabling camera preview")
      self.isLive = True

    self.tplFooter = self.tplFooterOrg

    self.updateHtml(Form)

  def screenCapture(self, Form):
    self.screen = 2

    self.tplBtn1 = fotoboxText['btn-empty']
    self.tplBtn2 = fotoboxText['btn-empty']
    self.tplBtn3 = fotoboxText['btn-empty']
    if not fotoboxCfg['nopi']:
      GPIO.output(18, GPIO.LOW)
      GPIO.output(23, GPIO.LOW)
      GPIO.output(24, GPIO.LOW)
      self.pwm.change_duty_cycle(50)

    if not self.isLive:
      self.tplImage = "liveBack.png"
      if not fotoboxCfg['nopi']:
        self.camera.start_preview(fullscreen=False, window = (fotoboxCfg['cam-p-x'], fotoboxCfg['cam-p-y'], fotoboxCfg['cam-p-width'], fotoboxCfg['cam-p-height']), hflip=fotoboxCfg['cam-p-hflip'])
        print("Enabling camera preview")
      self.isLive = True

    self.tplFooter = self.tplFooterOrg

    self.updateHtml(Form)

    #start countdown
    self.countdownTime = fotoboxCfg['countdown']
    self.updateCountdown()

  def updateCountdown(self):
    Form = window

    self.tplInstruct = fotoboxText['info-count']
    self.tplInstruct = self.tplInstruct.replace('${countdown}', str(self.countdownTime), 1)
    self.updateHtml(Form)

    self.countdownTime-=1

    if(self.countdownTime > 0):
      self.timerCnt.start(1000)
    elif self.countdownTime == 0:
      self.timerCnt.start(750)
    elif self.countdownTime == -1:
      #We already switch it here because photoTake seems to freeze the GPU briefly
      #and the updated HTML will not be ready in time
      self.tplInstruct = fotoboxText['info-capture']
      self.tplImage = "capturing.png"
      self.tplFooter = "Aufnahme..." #Capturing...
      self.updateHtml(Form)
      self.timerCnt.start(250)
    else:
      self.photoTake(Form)

  def photoTake(self, Form):
    if(self.isLive):
      self.isLive=False
      if not fotoboxCfg['nopi']:
        self.camera.stop_preview()
        print("Disabling camera preview")

    self.lastPhoto = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".jpg"
    if not fotoboxCfg['nopi']:
      self.pwm.change_duty_cycle(100)
      self.camera.resolution = (fotoboxCfg['cam-c-width'], fotoboxCfg['cam-c-height'])
      self.camera.capture(self.temp+self.lastPhoto)
      self.pwm.change_duty_cycle(10)
    else:
      copyfile(os.path.dirname(os.path.realpath(__file__)) + '/design/dummy.jpg', self.temp+self.lastPhoto)

    self.screenReview(Form)

  def screenReview(self, Form):
    self.screen = 3

    self.tplInstruct = fotoboxText['info-review']
    self.tplBtn1 = fotoboxText['btn-recapture']
    self.tplBtn2 = fotoboxText['btn-save']
    self.tplBtn3 = fotoboxText['btn-cancel']
    if not fotoboxCfg['nopi']:
      GPIO.output(18, GPIO.HIGH)
      GPIO.output(23, GPIO.HIGH)
      GPIO.output(24, GPIO.HIGH)
    self.tplImage = self.temp+self.lastPhoto
    self.tplFooter = "Foto: " + self.lastPhoto

    self.updateHtml(Form)
    
    #start timeout
    self.tout1Cnt.start(fotoboxCfg['timeout1']*1000)

  def timeout1(self):
    Form = window
    self.doConfirm(Form)

  def tempDel(self):
    if self.lastPhoto != "" and os.path.isfile(self.temp+self.lastPhoto):
      os.remove(self.temp+self.lastPhoto)
      self.lastPhoto = ""

  def noConfirm(self, Form):
    self.tout1Cnt.stop()
    self.tempDel()
    self.screenMain(window)

  def doConfirm(self, Form):
    self.tout1Cnt.stop()
    move(self.temp+self.lastPhoto, self.save+self.lastPhoto)
    self.tplImage2 = self.save+self.lastPhoto
    print("Saved " + self.save+self.lastPhoto)
    self.screenMain(window)

  def retry(self, Form):
    self.tout1Cnt.stop()
    move(self.temp+self.lastPhoto, self.save+self.lastPhoto)
    self.tplImage2 = self.save+self.lastPhoto
    print("Saved " + self.save+self.lastPhoto)
    self.screenCapture(window)

  def startViewer(self, Form):
    self.screen = 4

    if(self.isLive):
      self.isLive=False
      self.tplImage = "init.png"
      if not fotoboxCfg['nopi']:
        self.camera.stop_preview()

    self.entries = None
    self.entries = (os.path.join(self.save, fn) for fn in os.listdir(self.save))
    self.entries = ((os.stat(path), path) for path in self.entries)
    self.entries = ((stat[ST_MTIME], path)
      for stat, path in self.entries if S_ISREG(stat[ST_MODE]))
    self.entries = list(self.entries)

    if(len(self.entries) > 0):
      self.viewerIndex = (len(self.entries)-1) #0
      self.screenViewer(Form)
    else:
      print("No images to show")
      self.screenMain(Form)

  def screenViewer(self, Form):
    self.tplInstruct = fotoboxText['info-view']

    if(self.viewerIndex < (len(self.entries)-1)):
      self.tplBtn1 = fotoboxText['btn-next']
      if not fotoboxCfg['nopi']:
        GPIO.output(18, GPIO.HIGH)
    else:
      self.tplBtn1 = fotoboxText['btn-empty']
      if not fotoboxCfg['nopi']:
        GPIO.output(18, GPIO.LOW)
    
    if(self.viewerIndex > 0):
      self.tplBtn2 = fotoboxText['btn-previous']
      if not fotoboxCfg['nopi']:
        GPIO.output(23, GPIO.HIGH)
    else:
      self.tplBtn2 = fotoboxText['btn-empty']
      if not fotoboxCfg['nopi']:
        GPIO.output(23, GPIO.LOW)

    self.tplBtn3 = fotoboxText['btn-back']
    if not fotoboxCfg['nopi']:
      GPIO.output(24, GPIO.HIGH)
    self.tplImage = self.entries[self.viewerIndex][1]
    self.tplFooter = "Foto " + str(self.viewerIndex+1) + \
      ' von ' + str(len(self.entries)) + \
      " · " + str(os.path.basename(self.entries[self.viewerIndex][1]))
    
    self.updateHtml(Form)
    
    #start timeout
    self.tout2Cnt.start(fotoboxCfg['timeout2']*1000)

  def timeout2(self):
    Form = window
    self.screenMain(Form)

  def viewPrev(self, Form):
    if(self.viewerIndex > 0):
      self.viewerIndex -= 1
    self.screenViewer(Form)

  def viewNext(self, Form):
    if(self.viewerIndex < (len(self.entries)-1)):
      self.viewerIndex += 1
    self.screenViewer(Form)

class QWebView_mod(QWebView):
  def __init__(self):
    super(QWebView, self).__init__()
    self.ui = Ui_Form_mod()
    self.ui.setupUi(self)
    self.ui.initSystem(self)
    self.ui.screenMain(self)
    self.setCursor(QtGui.QCursor(QtCore.Qt.BlankCursor))

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

    self.showFullScreen()

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
    print("Button Event: " + str(btn))
    if(self.ui.screen == 1):
      if(btn == 1):
        self.ui.screenCapture(self)
      elif(btn == 2):
        self.ui.startViewer(self)
    elif(self.ui.screen == 3):
      if(btn == 1):
        self.ui.retry(self)
      elif(btn == 2):
        self.ui.doConfirm(self)
      elif(btn == 3):
        self.ui.noConfirm(self)
    elif(self.ui.screen == 4):
      if(btn == 1):
        self.ui.viewNext(self)
      elif(btn == 2):
        self.ui.viewPrev(self)
      elif(btn == 3):
        self.ui.screenMain(self)

  def keyPressEvent(self, e):
    if e.key() == QtCore.Qt.Key_Escape:
      GPIO.cleanup()
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
window = QWebView_mod()

sys.exit(app.exec_())
