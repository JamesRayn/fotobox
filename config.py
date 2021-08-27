fotoboxCfg = {}

fotoboxCfg['footer']          = 'Fotoboxparty'

fotoboxCfg['window-width']    = 1280
fotoboxCfg['window-height']   = 1024

# Depending on the camera used previews might got smaller than set here
fotoboxCfg['cam-p-width']     = 906
fotoboxCfg['cam-p-height']    = 680
fotoboxCfg['cam-p-x']         = 28
fotoboxCfg['cam-p-y']         = 205
fotoboxCfg['cam-p-hflip']     = True # False = Like a camera, True = Like a mirror

# PiCam v1: 2592x1944, v2: 3280x2464, HQ: 4056x3040
fotoboxCfg['cam-c-width']     = 3280
fotoboxCfg['cam-c-height']    = 2464
fotoboxCfg['cam-c-hflip']     = False # False = Like a camera, True = Like a mirror

fotoboxCfg['nopi']            = False # True = Skip rasperry specific modules

fotoboxCfg['temp']            = '/tmp/fotobox/'
fotoboxCfg['save']            = '/home/pi/UberGallery-v2.4.8/gallery-images'

fotoboxCfg['countdown']       = 3   # Seconds countdown to take the picture
fotoboxCfg['timeout1']        = 60  # Seconds timeout on the review screen
fotoboxCfg['timeout2']        = 180 # Seconds timeout on the viewer screen

fotoboxText = {}

fotoboxText['info-home']    = '<span style="line-height: 1.8">Hallo und willkommen an der Fotobox!<br>Drücke einfach auf "Aufnahme" und los geht\'s!</span>'
fotoboxText['info-count']   = '<span style="font-size: 150%">Los geht\'s!</span><hr><span style="font-size: 350%; font-weight: bolder;">${countdown}</span>'
fotoboxText['info-capture'] = '<span style="font-size: 200%; font-weight: bolder;">Bitte lächeln!</span>'
fotoboxText['info-review']  = '<span style="font-size: 75%">Alles OK?<br>Wenn ja, kannst du gleich noch ein Bild machen oder mit "Fertig" den Vorgang abschließen. War die Grimasse doch zu schlimm? Dann kannst du das Bild auch wieder löschen.</span>'
fotoboxText['info-view']    = '<span style="font-size: 85%">Hier kannst du dir die Fotos der Veranstaltung direkt anschauen. Mit "Nächstes" und "Vorheriges" kannst du zwischen den Bildern wechseln. Mit "Zurück" geht\'s wieder zur Kamera.</span>'

fotoboxText['btn-capture']  = 'Aufnahme ▶'
fotoboxText['btn-view']     = 'Gallerie ▶'
fotoboxText['btn-recapture'] = '<span style="font-size: 80%">Gleich Nochmal</span> ▶'
fotoboxText['btn-save']     = 'Fertig ▶'
fotoboxText['btn-cancel']   = 'Löschen ▶'
fotoboxText['btn-next']     = 'Nächstes ▶'
fotoboxText['btn-previous'] = 'Vorheriges ▶'
fotoboxText['btn-back']     = 'Zurück ▶'
fotoboxText['btn-empty']    = ''
