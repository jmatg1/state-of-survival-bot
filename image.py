import pytesseract
import cv2


pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'

print(pytesseract.image_to_string(r'C:\Users\Roman\Desktop\Bot\State of Survival\attack2.png', lang='rus'))
#
#
# img = cv2.imread(r'C:\Users\Roman\Desktop\Bot\State of Survival\attack2.png')
#
# custom_config = '-l rus'
# # C:\Users\Roman\Desktop\Bot\State of Survival\attack2.png
# text = pytesseract.image_to_string(r'C:\Users\Roman\Desktop\Bot\State of Survival\attack2.png', config=custom_config)

# print(text)