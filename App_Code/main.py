import getenc
import face_recognition as fc
import cv2

def check(encodings,face):
    for i in encodings:
        if fc.compare_faces(face,i['image'])==[True]:
            getenc.put_attendance(i['id'])
            

data = getenc.encodings()

cam = cv2.VideoCapture(0)
cv2.namedWindow('Attendance System')
imgcounter = 0
enc = []
while True:
    ret,fram = cam.read()
    if not ret:
        print('Failed to Grab')
        break
    loc = fc.face_locations(fram,model='hog')
    if len(loc)>0:
        enc = fc.face_encodings(fram,loc)
    for i in enc:
        check(data,[i])

    cv2.imshow('Attendance System',fram)
    k = cv2.waitKey(1)
    if k%256 == 27:
        print('Exit')
        break

cam.release()
cv2.destroyAllWindows()
