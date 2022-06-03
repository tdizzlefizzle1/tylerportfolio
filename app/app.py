from flask import Flask, render_template

app = Flask(__name___)

@app.route('/')
def portfolio():
    return render_template("index.html")