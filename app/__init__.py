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

@app.route('/loganswork/')
def loganwork():
    return render_template('loganwork.html')

@app.route('/royswork/')
def roywork():
    return render_template('roywork.html')

if __name__ ==  "__main__":
    app.run()