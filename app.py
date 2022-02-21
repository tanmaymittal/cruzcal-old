from flask import Flask, request, render_template, send_file
from addClass import pisa
from pathlib import Path
from Calendar import iCalendar
import time


ical = iCalendar()
# Flask constructor
app = Flask(__name__) 

@app.route('/', methods =["GET", "POST"])
def piso():
    # Gonna have to import function from different file 
    # Look into making API 
    # error = request.args.get('error')
    # message = request.args.get ('message')
    count = 0
    # try:
    cal = False
    if request.method == "POST":
        class_number = request.form['class_number']
        class_number_two = request.form['class_number_two']
        class_number_three = request.form['class_number_three']
        class_number_four = request.form['class_number_four']
        class_number_five = request.form['class_number_four']
        # password = request.form['password']
        # lang = request.form[' language']
        # C, conn = connection()
        className, meetingPlace, startDate, startTime, endTime, meetingDays, count, class_number = pisa(class_number)
        c1 = pisa(class_number)
        c2 = pisa(class_number_two)
        c3 = pisa(class_number_three)
        c4 = pisa(class_number_four)
        c5 = pisa(class_number_five)
        # print(className)
        # print(c5)
        class_dict = {
            'className' : [], 
            'startDate' : []
        }
        class_carry = []
        gotData = False
        
        class_list = [c1, c2, c3, c4, c5]
        for x in class_list:
            if x is not None:
                # print(x[-1])
                # cn = int(x)
                if ical.addCourse(x[-1]):
                    cal = True
                # then do something here 
                # add to dictionary of classes 
                class_dict = {
                    # 'className' : [], 
                    # 'startDate' : []
                }
                for num, i in enumerate(x):
                    if num == 0:
                        class_dict['className'] = i
                    elif num == 2:
                        class_dict['startDate'] = i
                    elif num == 5:
                        class_dict['meetingDays'] = i
                gotData = True
                class_carry.append(class_dict)
                pass
        # print(gotData)
        # print(class_dict)
        # print(cal)
        # print(class_carry)
        # className, meetingPlace, startDate, startTime, endTime, meetingDays = 0, 0, 0, 0, 0, 0
        # pass
        # if count > 0:
        #     gotData = True
        # else:
        #     gotData = False
        # return render_template('index.html', className = className, meetingPlace = meetingPlace, startDate=startDate, startTime=startTime, meetingDays=meetingDays, gotData=gotData)
        return render_template('index.html', class_carry = class_carry,  gotData=gotData)
        # return redirect('/downloadfile/'+ filename)
    else:
        # GET 
        return render_template('index.html')

    
@app.route('/download')
def download():
    file_path = str(Path.cwd())
    ical.export(file_path)
    time.sleep(2)
    return send_file('calendar.ics', as_attachment=True)

@app.route("/downloadfile/calendar.ics", methods = ['GET'])
def download_file(filename):
    return render_template('download.html',value=filename)

# @app.route('/login/', methods=[ 'GET', 'POST'])
# def login():
#     error = request.args.get('error')
#     message = request.args.get ('message')
#     try:
#         if request.method =="POST":
#             email = request.form['email']
#             password = request.form['password']
#             lang = request.form[' language']
#             # C, conn = connection()
#     except:
#         pass

# if __name__ == '__main__':
#     app.debug = True
#     app.run()

