from flask import Flask, request, render_template 
from addClass import pisa

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
    if request.method == "POST":
        class_number = request.form['class_number']
        # password = request.form['password']
        # lang = request.form[' language']
        # C, conn = connection()
        className, meetingPlace, startDate, startTime, endTime, meetingDays, count = pisa(class_number)
        # print(className)
    
        # className, meetingPlace, startDate, startTime, endTime, meetingDays = 0, 0, 0, 0, 0, 0
        # pass
        if count > 0:
            gotData = True
        else:
            gotData = False
        return render_template('index.html', className = className, meetingPlace = meetingPlace, startDate=startDate, startTime=startTime, meetingDays=meetingDays, gotData=gotData)
    else:
        # GET 
        return render_template('index.html')

    


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

