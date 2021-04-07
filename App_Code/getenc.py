from pymongo import MongoClient
import numpy as np
from datetime import date
from datetime import datetime
from gtts import gTTS
from playsound import playsound

url = 'mongodb+srv://siva:siva@cluster0.qwujv.mongodb.net/?retryWrites=true&w=majority'
conn = MongoClient(url)

def encodings():
    db = conn['workers']
    col = db['encoding']
    x = list()
    for i in col.find():
        x.append(i)
    t = list()
    for i in x:
        t.append(i)
    for i in range(len(t)):
        t[i]['image'] = np.array(t[i]['image'])
    print(t)
    return t

def put_attendance(id):
    db = conn['workers']
    col = db['attendance']
    x = date.today()
    s = x.strftime('%Y-%m-%d')
    t = col.find({'date':s,'members':{'$elemMatch':{'id':id}}})
    n = 0
    for i in t:
        n+=1
    if n == 0:
        now = datetime.now()
        now = now.strftime("%H:%M:%S")
        col.update_one({'date':s},{'$addToSet':{'members':{'id':id,'time':now}}})
        col2 = db['worker']
        s = col2.find_one({'id':id})
        name = s['fname']+s['lname']
        tts = gTTS('Hello,'+name+'. Your Attendance has been recorded. Have a nice day')
        tts.save('hello.mp3')
        playsound('hello.mp3')