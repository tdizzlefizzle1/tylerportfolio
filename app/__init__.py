import os
from flask import Flask, render_template, request
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', title="Picturesque", url=os.getenv("URL"))

@app.route('/tylerswork/')
def tylerwork():
    return render_template('tylerwork.html')
    
@app.route('/tylershobbies/')
def tylerhobby():
    return render_template('tylerhobby.html')

@app.route('/loganswork/')
def loganwork():
    return render_template('loganwork.html')

@app.route('/loganshobbies/')
def loganhobby():
    return render_template('loganhobby.html')

@app.route('/royswork/')
def roywork():
    return render_template('roywork.html')

@app.route('/royshobbies/')
def royhobby():
    return render_template('royhobby.html')

if __name__ ==  "__main__":
    app.run()