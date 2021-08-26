from flask import Flask, request, render_template, redirect, session, url_for
import pywhatkit as kit
from urllib.parse import quote
from selenium import webdriver
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
import pyrebase
import urllib, hashlib
from flask_session import Session
from datetime import date
import csv


app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


config = {
  "apiKey": "AIzaSyARJHP1fE9QkiPzk8NGzll-jh9mvbQc2IM",
  "authDomain": "whato-7a8ed.firebaseapp.com",
  "projectId": "whato-7a8ed",
  "storageBucket": "whato-7a8ed.appspot.com",
  "messagingSenderId": "918836431687",
  "appId": "1:918836431687:web:11cd51524b100085939a62",
  "measurementId": "G-LW200LFV7E",
  "databaseURL": "https://whato-7a8ed-default-rtdb.asia-southeast1.firebasedatabase.app/",

};

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

@app.route('/', methods=['POST'])
def home():
    
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if (request.method == 'POST'):
            email = request.form['username']
            password = request.form['password']
            
            try:
                print("i am invoked")
                user = auth.sign_in_with_email_and_password(email, password)
                cc = auth.get_account_info(user['idToken'])
                usr  = cc['users'][0]['localId']
                session["user"] = usr
                return redirect('/dashboard')
                # return render_template('dashboard.html')
            except:
                unsuccessful = 'Please check your credentials'
                return render_template('login.html', umessage=unsuccessful)
    return render_template('login.html')

@app.route('/forgotpassword', methods=['GET', 'POST'])
def forgotpassword():
    if (request.method == 'POST'):
            email = request.form['username']
            auth.send_password_reset_email(email)
            return render_template('login.html')
          
    return render_template('forgot.html')

@app.route('/contactus', methods=['GET', 'POST'])
def contactus():
    if (request.method == 'POST'):
            name = request.form['name']
            email = request.form['email']
            phone = request.form['phone']
            look = request.form['look']
            message = 'Hey,\nI am' + str(name) + '\n*My Email* : '  + str(email) + '\nMy Phone : ' + str(phone) + '\nI am here for : ' + str(look) + '\nThanks.'
            message = quote(message)
            url = 'https://web.whatsapp.com/send?phone=+917598308018&text=' + message
            return redirect(url, code=302)
           
    return render_template('contact.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if (request.method == 'POST'):
            name = request.form['name']
            email = request.form['email']
            phone = request.form['phone']
            password = request.form['password']
            user = auth.create_user_with_email_and_password(email, password)
            cc = auth.get_account_info(user['idToken'])
            ukey = cc['users'][0]['localId']
            result = hashlib.md5(email.encode("utf-8")).hexdigest()
            gravatar_url = "https://www.gravatar.com/avatar/" + str(result)
            
            data = {
                "name": name,
                "email": email,
                "phone": phone,
                "profileURL" : gravatar_url,
                "pack" : "1000"

                }

            
            db.child("users").child(ukey).set(data)
            db.child("users").child(ukey).child("campaigns")


           
    return render_template('register.html')

@app.route("/logout")
def logout():
    session["user"] = None
    return redirect("/dashboard")

    
@app.route("/dashboard")
def dashboard():
    if not session.get("user"):
        return redirect("/login")
    else:
        onUser = session['user']
        onUser = str(onUser)
        userData = db.child("users").child(onUser).get()
        userData = userData.val()
        return  render_template('dashboard.html' , currentUser=userData)

    return render_template('dashboard.html' , currentUser=userData)


#campaigns 

@app.route('/messagecampaign' , methods=['GET', 'POST'])
def messagecampaign():
    if not session.get("user"):
        return redirect("/login")
    else:
        today = date.today()
        today = str(today)
        onUser = session['user']
        onUser = str(onUser)
        userData = db.child("users").child(onUser).get()
        userData = userData.val()
        if (request.method == 'POST'):
            name = request.form['name']
            tagline = request.form['tagline']
            message = request.form['message']
            excel = request.form['excel'] 

            datas = {
               
                    "name": name,
                    "location": excel,
                    "date": today,
                    "tagline" : tagline,
                    "analysis" : "100",
                    "status"    : "Active",
                    "number"    : "",
                    "success"   : "",
                    "failed"    : "",
                    "type"      : "Message",
                    "message"   : message,
                    "path"      : "/message"
                
                
                }        
        
            db.child("users").child(onUser).child("campaign").push(datas)
        
        return  render_template('messagecampaign.html')

    return render_template('messagecampaign.html' , currentUser=userData)

@app.route('/mediacampaign')
def mediacampaign():
    if not session.get("user"):
        return redirect("/login")
    else:
        onUser = session['user']
        onUser = str(onUser)
        userData = db.child("users").child(onUser).get()
        userData = userData.val()
        return  render_template('mediacampaign.html' , currentUser=userData)

    return render_template('mediacampaign.html' , currentUser=userData)

@app.route('/videocampaign')
def videocampaign():
    if not session.get("user"):
        return redirect("/login")
    else:
        onUser = session['user']
        onUser = str(onUser)
        userData = db.child("users").child(onUser).get()
        userData = userData.val()
        return  render_template('videocampaign.html' , currentUser=userData)

    return render_template('videocampaign.html' , currentUser=userData)

@app.route('/reportcampaign')
def reportcampaign():
    if not session.get("user"):
        return redirect("/login")
    else:
        onUser = session['user']
        onUser = str(onUser)
        userData = db.child("users").child(onUser).get()
        userData = userData.val()
        return  render_template('reportcampaign.html' , currentUser=userData)

    return render_template('reportcampaign.html' , currentUser=userData)

@app.route('/dynamiccampaign')
def dynamiccampaign():
    if not session.get("user"):
        return redirect("/login")
    else:
        onUser = session['user']
        onUser = str(onUser)
        userData = db.child("users").child(onUser).get()
        userData = userData.val()
        return  render_template('dynamiccampaign.html' , currentUser=userData)

    return render_template('dynamiccampaign.html' , currentUser=userData)

@app.route('/insights')
def insights():
    if (request.method == 'POST'):
            email = request.form['name']
            password = request.form['password']
            try:
                auth.sign_in_with_email_and_password(email, password)
                #user_id = auth.get_account_info(user['idToken'])
                #session['usr'] = user_id
                return render_template('contact.html')
            except:
                unsuccessful = 'Please check your credentials'
                return render_template('index.html', umessage=unsuccessful)
    return render_template('graphs.html')


@app.route('/message/<id>')
def image(id):
    onUser = session['user']
    onUser = str(onUser)
    userData = db.child("users").child(onUser).child("campaign").child(id).get()
    userData = userData.val()
    message = userData['message']
    message = str(message)
    path = userData['location']
    path = str(path)
    numbers = []
    f = open('C:/Users/ManishDev/Desktop/numbers.txt', encoding='UTF8')


    f = open("C:/Users/ManishDev/Desktop/numbers.txt", "r")
    for line in f.read().splitlines():
        if line != "":
            numbers.append(line)
    f.close()
    total_number=len(numbers)
    count = 1;
    for idx, number in enumerate(numbers):
        number = number.strip()
        if number == "":
                continue
        try:
                kit.sendwhats_image(phone_no = number, img_path = path, caption = message, tab_close = True)

        except Exception as e:
                print('Failed to send message to ' + number + str(e))

    return "messages sent"

@app.route('/documents')
def documents():
    driver = webdriver.Chrome('D:/whatsapp/Whato/whato/venv/chromedriver')
    driver.get('https://web.whatsapp.com/')
    url = 'https://web.whatsapp.com/send?phone=+919943073083&text=hellomanish'
    driver.get(url)
    sleep(10)
    button = driver.find_element_by_class_name('_2jitM')
    button.click()
    sleep(1)
    doc = driver.find_element_by_xpath('//input[@accept="*"]')
    doc.send_keys("D:/whatsapp/Whato/whato/venv/RF_DECK.pptx")
    sleep(1)
    final = driver.find_element_by_class_name('_1w1m1')
    final.click()
    sleep(10)


@app.route('/video')
def video():
    driver = webdriver.Chrome('D:/whatsapp/Whato/whato/venv/chromedriver')
    driver.get('https://web.whatsapp.com/')
    url = 'https://web.whatsapp.com/send?phone=+919943073083&text=forimagesandvideo'
    driver.get(url)
    sleep(20)
    button = driver.find_element_by_class_name('_2jitM')
    button.click()
    sleep(1)
    doc = driver.find_element_by_xpath('//input[@accept="image/*,video/mp4,video/3gpp,video/quicktime"]')
    doc.send_keys("D:/whatsapp/Whato/whato/venv/cc.mp4")
    sleep(10)
    final = driver.find_element_by_class_name('_1w1m1')
    final.click()
    sleep(20)

@app.route('/images')
def images():
    driver = webdriver.Chrome('D:/whatsapp/Whato/whato/venv/chromedriver')
    driver.get('https://web.whatsapp.com/')
    url = 'https://web.whatsapp.com/send?phone=+919025363428&text=Automated'
    driver.get(url)
    sleep(20)
    button = driver.find_element_by_class_name('_2jitM')
    button.click()
    sleep(1)
    doc = driver.find_element_by_xpath('//input[@accept="image/*,video/mp4,video/3gpp,video/quicktime"]')
    doc.send_keys("D:/whatsapp/Whato/whato/venv/maxresdefault.jpg")
    sleep(10)
    final = driver.find_element_by_class_name('_1w1m1')
    final.click()
    sleep(20)


if __name__ == '__main__':
   app.run(host='0.0.0.0',port=8080)
