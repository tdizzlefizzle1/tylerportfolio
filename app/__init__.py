import os
from unicodedata import name

from requests import post

from flask import Flask, render_template, request
from dotenv import load_dotenv
from peewee import *
import datetime
from playhouse.shortcuts import model_to_dict

load_dotenv()
app = Flask(__name__)
mydb = MySQLDatabase(os.getenv("MYSQL_DATABASE"),
    user = os.getenv("MYSQL_USER"),
    password = os.getenv("MYSQL_PASSWORD"),
    host = os.getenv("MYSQL_HOST"),
    port = 3306
)

print(mydb)

class TimelinePost(Model):
    name = CharField()
    email = CharField()
    content = TextField()
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = mydb
mydb.connect()
mydb.create_tables([TimelinePost])

@app.route('/')
def index():
    return render_template('index.html', title="Tyler's Portfolio", url=os.getenv("URL"))

@app.route('/tylerswork/')
def tylerwork():
    return render_template('tylerwork.html', title="Tyler'sWork")
    
@app.route('/tylershobbies/')
def tylerhobby():
    return render_template('tylerhobby.html', title="Tyler's Hobbies")

@app.route('/timeline')
def timeline():
    posts = TimelinePost.select().order_by(TimelinePost.created_at.desc())
    return render_template('timeline.html', title="Timeline", timeline=posts)

@app.route('/api/timeline_post', methods=['POST'])
def post_time_line_post():
    name = request.form['name']
    email = request.form['email']
    content = request.form['content']
    post = TimelinePost.create(name=name, email=email, content=content)
    return model_to_dict(post)

@app.route('/api/timeline_post', methods=['GET'])
def get_time_line_post():
    return{
        'timeline_posts': [
            model_to_dict(p)
            for p in TimelinePost.select().order_by(TimelinePost.created_at.desc())
        ]
    }
@app.route('/api/timeline_post', methods=['DELETE'])
def delete_time_line_post():

    post_id = request.form["id"]
    TimelinePost.delete_by_id(post_id)
    return "deleted post\n"

if __name__ ==  "__main__":
    app.run()