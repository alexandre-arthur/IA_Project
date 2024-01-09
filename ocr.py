#!/usr/bin/env python3

import pdf2image
import pytesseract
import cv2
import numpy as np
from PIL import Image
import sys

# Works only on Linux
# pip3 install opencv-contrib-python==4.6.0.66
# pip3 install meson
# pip3 install PILLOW
# sudo apt install ninja-build
# sudo apt-get install libpoppler-cpp-dev
# pip3 install python-poppler
# pip3 install pdf2image
# sudo apt install tesseract-ocr
# pip3 install pytesseract

if __name__ != "__main__": raise ; exit(1)

try:
    pdf_path = sys.argv[1]
except IndexError:
    pdf_path = 'Tarragoni.pdf'


def __add__(x, y): return x+y
def fold(l, f, x): res = x; [res := f(res, y) for y in l]; return res

txt_path = fold(pdf_path.split('.')[:-1], __add__, '') + '.txt'
images = pdf2image.convert_from_path(pdf_path)

print(txt_path)

with open(txt_path, "w") as f:
    f.write('')

for i in range(len(images)):

    image = np.array(images[i])
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray_image, 127, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    cv2.imwrite(f"output/{i}.png", thresh)

    with open(txt_path, "a") as f:
        text = pytesseract.image_to_string(Image.fromarray(thresh), lang='fra')
        # text = f"Text {i} : " + pytesseract.image_to_string(Image.open(f'output/{i}.png'), lang='fra')
        f.write(text)
