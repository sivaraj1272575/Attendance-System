from flask import Flask,render_template,Response,request,redirect,session,flash,url_for
from apscheduler.schedulers.background import BackgroundScheduler
from contextlib import contextmanager

import os
import camera
import mongodb
from flask_mail import Mail,Message
import verify


app = Flask(__name__)
app.secret_key = 'Shhhhh'

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'test1372001@gmail.com'
app.config['MAIL_PASSWORD'] = 'Siva@1234'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)

@app.after_request
def add_header(response):
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Expires'] = '0'
    return response

def sendmail(id):
    global mail
    x  = mongodb.fetch_emp(id)
    email = x['email']
    s = Message('Your Attendance', sender='test@1372001@gmail.com',recipients=[email])
    l = mongodb.get_attendance(id)
    content = mongodb.get_html(l)
    s.html = content
    mail.send(s)

def createdate():
    mongodb.createdate()

sched = BackgroundScheduler()
#sched.add_job(sendmail,'cron',day_of_week='mon-sun', hour=9, minute=20, timezone='Asia/Kolkata')
#sched.add_job(createdate,'cron',day_of_week='mon-sat',hour=8, minute=30, timezone='Asia/Kolkata')
sched.start()



UPLOAD_FOLDER = '/home/sivaraj/Attendance/static/photo/'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(camera.video(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/admin')
def admin():
    return render_template('admin_login.html')

@app.route('/admin_home')
def admin_home():
    if session.get('username'):
        return render_template('admin_home.html')
    else:
        return redirect('/admin')

@app.route('/login',methods=['POST','GET'])
def login():
    if request.method == "POST":
        if mongodb.verify(request.form) == True:
            session['username'] = request.form['username']
            return redirect('/admin_home')
        else:
            flash('Invalid Username or Password','danger')
            return redirect('/admin')

@app.route('/worker')
def worker():
    if session.get('username'):
        x = mongodb.get_workers()
        print(x)
        return render_template('worker.html',workers=x)
    else:
        return redirect('/admin')

@app.route('/add_worker')
def add_worker():
    if session.get('username'):
        return render_template('addworker.html')
    else:
        return redirect('/admin')

@app.route('/add_worker1',methods=['POST','GET'])
def add_worker1():
    if request.method == 'POST':
        if mongodb.already_in(request.form['id']):
            if 'photo' not in request.files:
                flash('No File Selected', 'Danger')
                return redirect(request.url)
            else:
                #mongodb.add_worker(request.form,request.files['photo'])
                if(verify.check_format(request.files['photo'].filename)):
                    f = request.files['photo']
                    file_name = verify.get_file_name(request.form['id'],request.files['photo'].filename)
                    f.save('static/photo/'+file_name)
                    if mongodb.add_worker(request.form,file_name)==False:
                        flash('Try with Another Photo', 'danger')
                        return redirect('/add_worker')
                    else:
                        flash('Uploaded Successfully', 'success')
                        return redirect('/add_worker')
                else:
                    flash('Choose Proper Photo', 'danger')
                    return redirect('/add_worker')
                
        else:
            flash('The given Id Already Present', 'danger')
            return redirect('/add_worker')
    else:
        return 'Other Method'

@app.route('/open_employee/<id>')
def open_employee(id):
    if session.get('username'):
        det = mongodb.fetch_emp(id)
        return render_template('show_employee.html',emp = det,edit=False)
    else:
        return redirect('/')

@app.route('/delete_employee/<id>')
def delete_employee(id):
    if session.get('username'):
        if mongodb.delete_emp(id):
            flash('Employee Deleted Successfully', 'success')
            return redirect('/worker')
        else:
            flash('Error in Deleting Employee', 'danger')
            return redirect('/worker')
    else:
        return redirect('/')

@app.route('/edit_employee/<id>')
def edit_employee(id):
    if session.get('username'):
        print('Hello')
        det = mongodb.fetch_emp(id)
        return render_template('show_employee.html',emp = det,edit=True)
    else:
        return redirect('/')

@app.route('/edit_employee1/<id>',methods=['POST','GET'])
def edit_employee1(id):
    if session.get('username'):
        if request.method=="POST":
            mongodb.update_details(id,request.form)
            flash('Details Updated Successfully','success')
            return redirect('/worker')
    else:
        return redirect('/')

@app.route('/see_attendance')
def see_attendance():
    return render_template('see_attendance.html')

@app.route('/see_attendance1',methods=['POST','GET'])
def see_attendance1():
    if request.method == 'POST':
        if mongodb.get_details(request.form['id'],request.form['dob']):
            sendmail(request.form['id'])
            flash('Email sent successfully','success')
            return redirect('/')
        else:
            flash('Invalid Details','danger')
            return redirect('/')

@app.route('/admin_attendance')
def admin_attendance():
    if session.get('username'):
        s = mongodb.get_attendance_all()
        return render_template('admin_attendance.html',attendance = s)
    else:
        return('/')


@app.route('/logout')
def logout():
    session.pop('username',None)
    return redirect('/')


if __name__ == '__main__':
    app.run()