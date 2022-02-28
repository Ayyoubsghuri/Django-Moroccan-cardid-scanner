# from pyScanLib import pyScanLib
import cv2
import pytesseract
import re
import os
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
)

# loadScanner = pyScanLib()
# scanners = loadScanner.getScanners()
# loadScanner.setScanner(scanners[0])

# loadScanner.setDPI(300)
# loadScanner.setScanArea(width=512,height=512)
# loadScanner.setPixelType("color")

# PIL = loadScanner.scan()
# PIL.save("scanImage.jpg")
# loadScanner.closeScanner()
# loadScanner.close()


img = cv2.imread('static/images/cardid/scanImage.jpg')
img = cv2.resize(img, None, fx=1.2, fy=1, interpolation=cv2.INTER_CUBIC)

fltxt = pytesseract.image_to_string(img, lang='fra',
                                    config='--psm 11')

lstt = fltxt.split('\n')
b = []
etatCivil = re.compile("^[0-9]+\/+[0-9]+$")

for i in lstt:
    if(etatCivil.match(i)):
        b.append(i)

if len(b) > 0:
    if os.path.exists('static/images/cardid/back.jpg'):
        os.remove('static/images/cardid/back.jpg')
        os.rename('static/images/cardid/scanImage.jpg',
                      'static/images/cardid/back.jpg')
    else:
        os.rename('static/images/cardid/scanImage.jpg',
                      'static/images/cardid/back.jpg')
else:
    if os.path.exists('static/images/cardid/front.jpg'):
        os.remove('static/images/cardid/front.jpg')
        os.rename('static/images/cardid/scanImage.jpg',
                      'static/images/cardid/front.jpg')
    else:
        os.rename('static/images/cardid/scanImage.jpg',
                      'static/images/cardid/front.jpg')