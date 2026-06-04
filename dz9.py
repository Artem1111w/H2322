import cv2
from PIL import Image


IMAGE_PATH = 'man.jpg'
man_face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')

image = cv2.imread(IMAGE_PATH)
man_face = man_face_cascade.detectMultiScale(image)

print(man_face)

man = Image.open(IMAGE_PATH).convert('RGBA')
glasses =Image.open('glasses.png').convert('RGBA')

for x,y,w,h in man_face:
    # cv2.rectangle(image,(x,y),(x+w, y+h),(0,0,255), 3)
    glasses = glasses.resize((w, h//3))
    man.paste(glasses, (x, int(y + h / 4)), glasses)

man.save('new_man.png')

new_image = cv2.imread('new_man.png')
cv2.imshow('Man', new_image)
cv2.waitKey()
