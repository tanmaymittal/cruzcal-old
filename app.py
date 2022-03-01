from flask import Flask, request, render_template, send_file, session, redirect, url_for
from addClass import pisa
from Calendar import iCalendar
import time
from settings import *
from random import randint
import gc
import datetime
from Util import *
import os
import sys
import logging
import pathlib

app = Flask(__name__) 
if 'DYNO' in os.environ:
    app.logger.addHandler(logging.StreamHandler(sys.stdout))
    app.logger.setLevel(logging.ERROR)

app.secret_key = 'asdasdasdasd'
# app.debug = True
app.config['DEBUG'] = True

last_gc = datetime.datetime.min
ical = iCalendar()

def garbageCollection():
    # run garbage collection
    c, conn = connection()
    c.execute("SELECT uid FROM sessions WHERE ftime < TIMESTAMP(DATE_SUB(NOW(), INTERVAL 30 day))")
    dataset = [row for row in c]
    c.close()
    conn.close() 
    deletion_queue = [row[0] for row in dataset]
    clear_files(deletion_queue)
    # handles removal of records from database
    sqlarg = 'DELETE FROM sessions WHERE '
    if len(deletion_queue) == 0: return True
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
    global ical
    global last_gc
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
            c.execute("SELECT * FROM sessions WHERE uid = {}".format(session['uid']))
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
                        print("hi",i)
                    elif num == 2:
                        class_dict['startDate'] = i
                    elif num == 5:
                        class_dict['meetingDays'] = i
                gotData = True
                class_carry.append(class_dict)
                pass
        ical.export()
        # return render_template('indexv2.html', class_carry = class_carry,  gotData=gotData, uid = session['uid'])
        return redirect(url_for('download'))
    else:
        return render_template('indexv2.html')

    
@app.route('/download')
def download():
    uid = request.args.get('uid')
    #under the following logic, the system will return the file for 
    if ('uid' not in session) and (uid == None):
        return redirect(url_for('piso'))
    elif uid == None:
        uid = session['uid']
    #determine if uid exists
    c, conn = connection()
    c.execute("SELECT uid FROM sessions WHERE uid = {}".format(uid))
    dataset = [row for row in c]
    c.close()
    conn.close() 
    if len(dataset) == 0: return redirect(url_for('piso'))
    time.sleep(2)
    return send_file('{}/user_requests/{}.ics'.format(pathlib.Path.cwd(), uid), as_attachment=True)
