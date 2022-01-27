from flask import Flask, request, render_template 
from addClass import pisa

# Flask constructor
app = Flask(__name__) 

@app.route('/', methods =["GET", "POST"])
def piso():
    # Gonna have to import function from different file 
    # Look into making API 
    return render_template('index.html', passObjectsLikeThis = False)
