from PIL import Image
import pytesseract

image = Image.open('file/test5.jpg')
text = pytesseract.image_to_string(image, lang='chi_sim')
print(text.replace(' ', ''))

image = Image.open('file/test3.png')
text = pytesseract.image_to_string(image)
print('ooxx:', text)

image = Image.open('file/test4.png')
text = pytesseract.image_to_string(image)
print('eng:', text)

image = Image.open('file/test6.png')
text = pytesseract.image_to_string(image, lang='chi_sim')
print('复杂中文:', text)

