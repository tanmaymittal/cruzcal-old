from flask import Flask, request, render_template, send_file, session
from addClass import pisa
from Calendar import iCalendar
import time
from settings import *
from random import randint
import gc
import datetime
from Util import *

ical = iCalendar()
app = Flask(__name__) 
last_gc = datetime.datetime.min

def garbageCollection():
    # run garbage collection
    c, conn = connection()
    c.execute("SELECT uid FROM session WHERE ftime < NOW() - INTERVAL 30 DAY")
    dataset = [row for row in c]
    c.close()
    conn.close() 
    deletion_queue = [row[0] for row in dataset]
    clear_files(deletion_queue)
    # handles removal of records from database
    sqlarg = 'DELETE FROM session WHERE '
    for i in range(len(dataset)):
        if i == (len(dataset) - 1):
            sqlarg += 'uid = {}'.format(dataset[i][0])
        else:
            sqlarg += 'uid = {} AND '.format(dataset[i][0])
    c, conn = connection()
    c.execute(sqlarg)
    c.close()
    conn.close()
    return True

@app.route('/', methods =["GET", "POST"])
def piso():
    count = 0
    cal = False
    if request.method == "POST":
        # 1 Garbage collection per 24 hours
        curr_time = datetime.datetime.now()
        if (curr_time - last_gc).days > 0:
            last_gc = curr_time
            garbageCollection()
        while True:
            # generate unique session ID
            session['uid'] = randint(100000, 999999)
            # check if such session ID exists
            c, conn = connection()
            c.execute("SELECT * FROM session WHERE uid = {}".format(session['uid']))
            dataset = [row for row in c]
            #garbage collection and closing connnection
            c.close()
            conn.close()
            if len(dataset) == 0: break
        ical.clear(session['uid'])
        class_number = request.form['class_number']
        class_number_two = request.form['class_number_two']
        class_number_three = request.form['class_number_three']
        class_number_four = request.form['class_number_four']
        class_number_five = request.form['class_number_four']
        className, meetingPlace, startDate, startTime, endTime, meetingDays, count, class_number = pisa(class_number)
        c1 = pisa(class_number)
        c2 = pisa(class_number_two)
        c3 = pisa(class_number_three)
        c4 = pisa(class_number_four)
        c5 = pisa(class_number_five)

        class_dict = {
            'className' : [], 
            'startDate' : []
        }
        class_carry = []
        gotData = False
        
        class_list = [c1, c2, c3, c4, c5]
        for x in class_list:
            if x is not None:
                if ical.addCourse(x[-1]):
                    cal = True
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
        ical.export()
        return render_template('index.html', class_carry = class_carry,  gotData=gotData)
    else:
        return render_template('index.html')

    
@app.route('/download')
def download():
    uid = request.args.get('uid')
    #under the following logic, the system will return the file for 
    if ('uid' not in session) and (uid == None):
        return redirect(url_for('piso'))
    elif uid == None:
        uid = session[uid]
    #determine if uid exists
    c, conn = connection()
    c.execute("SELECT uid FROM session WHERE uid = {}".format(uid))
    dataset = [row for row in c]
    c.close()
    conn.close() 
    if len(dataset) == 0: return redirect(url_for('piso'))
    time.sleep(2)
    return send_file('{}.ics'.format(uid), as_attachment=True)

@app.route("/downloadfile/calendar.ics", methods = ['GET'])
def download_file(filename):
    return render_template('download.html',value=filename)
