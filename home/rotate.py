import cv2 
import numpy 
import pytesseract
import re
from PIL import Image
import os

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
)

check = []
rotPer=0
def detecttext(img):
    img = cv2.imread(str(img))
    img = cv2.resize(img, None, fx=1.2, fy=1, interpolation=cv2.INTER_CUBIC)
    fltxt = pytesseract.image_to_string(img, lang='fra',
                                        config='--psm 11')
    
    lstt = fltxt.split('\n')
    CIN = re.compile("^[A-Z]+[0-9]{3,}$")
    MAROC = re.compile("[A-Z]+\s[A-Z]+\sMAROC$")
    for i in lstt:
        if(CIN.match(i)):
            check.append(i)
    for i in lstt:
        if(MAROC.match(i)):
            check.append(i)
    if len(check)>0:
        return True
    else:
        return False

imag="static/images/cardid/scanImage.jpg"
while True:
    imgg = Image.open(imag)
    p=detecttext(imag)
    if p == True:
        break
    elif p == False:
        transposed  =imgg.transpose(Image.ROTATE_90)
        os.remove('static/images/cardid/scanImage.jpg')
        transposed.save('static/images/cardid/scanImage.jpg')
        rotPer +=90
print(rotPer)
