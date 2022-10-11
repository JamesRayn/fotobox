fotoboxCfg = {}

# Footer text
fotoboxCfg['footer']          = 'Fotoboxparty'

# Screen settings
## all layout and resolution settings are located at layout.py

# Common camera settings
fotoboxCfg['cam-vflip']       = False # False = normal operation, True = camera upside down mounting

# Camera preview settings
fotoboxCfg['cam-p-width']     = 906
fotoboxCfg['cam-p-height']    = 680
fotoboxCfg['cam-p-x']         = 28
fotoboxCfg['cam-p-y']         = 205
fotoboxCfg['cam-p-hflip']     = True  # False = Like a camera, True = Like a mirror

# Camera image settings
###fotoboxCfg['cam-c-res']       = ''    # default empty = full resolution, otherwise enter '"size": (2028, 1520)'
fotoboxCfg['cam-c-hflip']     = False # False = Like a camera, True = Like a mirror

# Hardware settings
fotoboxCfg['nopi']            = False # True = Skip raspberry specific modules
fotoboxCfg['light-pwm']       = True  # True = Uses the RPi-Hardware-PWM Lib to control a foto light, False = No foto light

# File settings
fotoboxCfg['temp']            = '/tmp/fotobox/'
fotoboxCfg['save']            = '/home/pi/ubergallery/gallery-images'

# Timing settings
fotoboxCfg['countdown']       = 4   # Seconds countdown to take the picture
fotoboxCfg['timeout1']        = 45  # Seconds timeout on the review screen
fotoboxCfg['timeout2']        = 180 # Seconds timeout on the viewer screen


fotoboxText = {}

fotoboxText['defbody']        = '<body style="padding: 0; margin: 0; font-family: \'Kalam\'; line-height: 1.2; position: fixed; width: 860px; height: 115px; font-size: 33px; text-align: center; display: flex; align-items: center; justify-content: center; overflow: hidden">'

fotoboxText['info-home']      = fotoboxText['defbody'] + '<span style="line-height: 1.8">Hallo und willkommen an der Fotobox!<br>Drücke einfach auf "Aufnahme" und los geht\'s!</span></body>'
fotoboxText['info-prepair']   = fotoboxText['defbody'] + '<span style="font-size: 50px">aufwärmen...</span></body>'
fotoboxText['info-count']     = fotoboxText['defbody'] + '<span style="font-size: 50px">Los geht\'s!</span><hr></body>'
fotoboxText['info-capture']   = fotoboxText['defbody'] + '<span style="font-size: 66px; font-weight: bold">Bitte lächeln!</span></body>'
fotoboxText['info-wait']      = fotoboxText['defbody'] + '<span style="font-size: 50px">Bitte warten...</span></body>'
fotoboxText['info-review']    = fotoboxText['defbody'] + '<span style="font-size: 25px">Alles OK?<br>Wenn ja, kannst du gleich noch ein Bild machen oder mit "Fertig" den Vorgang abschließen. War die Grimasse doch zu schlimm? Dann kannst du das Bild auch wieder löschen.</span></body>'
fotoboxText['info-view']      = fotoboxText['defbody'] + '<span style="font-size: 28px">Hier kannst du dir die Fotos der Veranstaltung direkt anschauen. Mit "Nächstes" und "Vorheriges" kannst du zwischen den Bildern wechseln. Mit "Zurück" geht\'s wieder zur Kamera.</span></body>'

fotoboxText['btn-capture']    = 'Aufnahme ▶'
fotoboxText['btn-view']       = 'Galerie ▶'
fotoboxText['btn-recapture']  = '<span style="font-size: 37px">Gleich nochmal</span> ▶'
fotoboxText['btn-save']       = 'Fertig ▶'
fotoboxText['btn-cancel']     = 'Löschen ▶'
fotoboxText['btn-next']       = 'Nächstes ▶'
fotoboxText['btn-previous']   = 'Vorheriges ▶'
fotoboxText['btn-back']       = 'Zurück ▶'
fotoboxText['btn-empty']      = ''
