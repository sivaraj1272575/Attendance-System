from pymongo import MongoClient
import face_recognition as fc
import cv2
import numpy as np
from datetime import date
from flask_mail import Mail,Message

url = 'mongodb+srv://siva:siva@cluster0.qwujv.mongodb.net/?retryWrites=true&w=majority'
conn = MongoClient(url)

def verify(d):
    db = conn['admins']
    col = db['admin']
    x = col.find_one({'username':d['username'],'password':d['password']})
    if(x):
        return True
    else:
        return False
        
def load_image(name,image):
    db = conn['workers']
    col = db['worker']
    d = [{'name':name,'image':image}]
    col.insert_many(d)
    print('inserted')

def already_in(id):
    db = conn['workers']
    col = db['worker']
    x = col.find_one({'id':id})
    return (x==None)

def get_enc(file):
    img = cv2.imread('static/photo/'+file)
    temp = fc.face_encodings(img)
    if len(temp)>0:
        enc = fc.face_encodings(img)[0]
        lst = enc.tolist()
        return lst
    else:
        return False

def add_worker(form,img):
    db = conn['workers']
    enc = get_enc(img)
    if(enc == False):
        return False
    data = {'id':form['id'], 'fname':form['fname'], 'lname':form['lname'], 'dob':form['dob'], 'post':form['post'], 'mobile': form['mobile'], 'email':form['email'] , 'photo':img,}
    encdata = {'id':form['id'],'image':enc}
    col1 = db['worker']
    col1.insert_one(data)
    col2 = db['encoding']
    col2.insert_one(encdata)
    print(data,encdata)

def get_workers():
    db = conn['workers']
    col = db['worker']
    workers = list()
    for i in col.find():
        workers.append(i)
    return workers

def fetch_emp(id):
    db = conn['workers']
    col = db['worker']
    x = col.find_one({'id':id})
    return x

def update_details(id,form):
    db = conn['workers']
    col = db['worker']
    newvals = {'$set':{'fname':form['fname'],'lname':form['lname'],'dob':form['dob'],'post':form['post'],'mobile':form['mobile'],'email':form['mobile']}}
    col.update_one({'id':id},newvals)

def delete_emp(id):
    db = conn['workers']
    col = db['worker']
    col.delete_one({'id':id})
    col = db['encoding']
    col.delete_one({'id':id})
    return True

def createdate():
    db = conn['workers']
    col = db['worker']
    x = date.today()
    s = x.strftime('%Y-%m-%d')
    col.insert_one({'date':s,'members':[]})

def get_details(id,dob):
    db = conn['workers']
    col = db['worker']
    a = col.find({'id':id,'dob':dob})
    count = 0
    for i in a:
        count+=1
    if count>0:
        return True
    else:
        return False

def get_attendance(id):
    db = conn['workers']
    col = db['attendance']
    a = col.find({})
    x = []
    for i in a:
        flag = 0
        for j in i['members']:
            if j['id'] == id:
                x.append({'Date':i['date'],'time':j['time']})
                flag=1
        if flag == 0:
            x.append({'Date':i['date'],'time':'Absent'})
    return x

def get_html(l):
    s= "<div>"
    for i in l:
        for j in i:
            s += "<strong>"+j+":  </strong>  "
            s += i[j]
        s+= "<br>"
    s+="</div>"
    return s

def get_attendance_all():
    lst = []
    x = get_workers()
    for i in x:
        lst.append({'id':i['id'],'name':i['fname']+' '+i['lname'],'attendance':get_attendance(i['id'])})
    return lst