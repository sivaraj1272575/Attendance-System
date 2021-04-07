import cv2


def video():
    s = cv2.VideoCapture(0)
    while True:
        ret,frame = s.read()
        if not ret:
            break
        
        ac, buff = cv2.imencode('.jpg',frame)
        frame = buff.tobytes()
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

def photo():
    img = cv2.imread('/home/sivaraj/Downloads/sample2.jpg')
    ret,buffer = cv2.imencode('.jpg',img)
    frame = buffer.tobytes()
    yield(b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
