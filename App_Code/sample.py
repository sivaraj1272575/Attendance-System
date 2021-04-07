import face_recognition as fc
import cv2
import numpy as np

img1 = cv2.imread('/home/sivaraj/Downloads/emma.jpg')
img2 = cv2.imread('/home/sivaraj/Downloads/emma2.jpeg')

enc1 = fc.face_encodings(img1)
enc2 = fc.face_encodings(img2)

print(enc1,enc2)


print (fc.compare_faces(enc1,enc2[0]))

cv2.imshow('Attendance System',img1)
k = cv2.waitKey(0)
cv2.destroyAllWindows()
