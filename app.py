from flask import Flask, request, render_template 
from addClass import pisa

# Flask constructor
app = Flask(__name__) 

@app.route('/', methods =["GET", "POST"])
def piso():
    # Gonna have to import function from different file 
    # Look into making API 
    error = request.args.get('error')
    message = request.args.get ('message')
    try:
        if request.method =="POST":
            class_number = request.form['class_number']
            # password = request.form['password']
            # lang = request.form[' language']
            # C, conn = connection()
    except:
        pass
    className, meetingPlace, startDate, startTime, endTime, meetingDays, count = pisa(class_number)
    print(className)
    if count > 0:
        gotData = True
    else:
        gotData = False

    return render_template('index.html', className = className, meetingPlace = meetingPlace,
    startDate=startDate, startTime=startTime, meetingDays=meetingDays, gotData=gotData)

@app.route('/login/', methods=[ 'GET', 'POST'])
def login():
    error = request.args.get('error')
    message = request.args.get ('message')
    try:
        if request.method =="POST":
            email = request.form['email']
            password = request.form['password']
            lang = request.form[' language']
            # C, conn = connection()
    except:
        pass
