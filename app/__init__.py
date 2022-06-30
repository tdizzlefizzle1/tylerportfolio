from asyncio.windows_events import NULL
import os
from flask import Flask, render_template, request
from dotenv import load_dotenv
from peewee import *
import datetime
import werkzeug

from playhouse.shortcuts import model_to_dict

PORTFOLIO_DIR = os.path.dirname(os.path.realpath(__file__))
CURRENT_DIR = os.path.join(PORTFOLIO_DIR, "app")
STATIC_DIR = os.path.join(PORTFOLIO_DIR, "static")
IMG_DIR = os.path.join(STATIC_DIR, "img")
KEYBOARD_DIR = os.path.join(IMG_DIR, "keyboard")
KEYBOARD_LIST = os.listdir(KEYBOARD_DIR)
RELATIVE = os.path.relpath(KEYBOARD_DIR, CURRENT_DIR)

load_dotenv()
app = Flask(__name__)

# If we set a env variable called TESTING to true, run through in-memory db
if os.getenv("TESTING") == "true":
    print("Running in test mode...")
    mydb = SqliteDatabase("file:memory?mode=memory&cache=shared", uri=True)

else:
    mydb = MySQLDatabase(
        os.getenv("MYSQL_DATABASE"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        host=os.getenv("MYSQL_HOST"),
        port=3306,
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


def keyboard_images():
    keyboards = []
    for file in KEYBOARD_LIST:
        IMAGE_NAME = os.path.join(RELATIVE, file)
        keyboards += [IMAGE_NAME]
    return keyboards


@app.route("/")
def tylerwork():
    return render_template("tylerwork.html", title="Tyler's Work", url=os.getenv("URL"))


@app.route("/hobbies")
def tylerhobby():
    keyboards = keyboard_images()
    return render_template("tylerhobby.html", title="Tyler's Hobbies", images=keyboards)


@app.route("/timeline")
def timeline():
    posts = TimelinePost.select().order_by(TimelinePost.created_at.desc())
    return render_template("timeline.html", title="Timeline", timeline=posts)


@app.route("/api/timeline_post", methods=["POST"])
def post_time_line_post():
        name = request.form["name"]
        email = request.form["email"]
        content = request.form["content"]

        if content == "":
            return "Invalid content", 400
        elif "@" not in email:
            return "Invalid email", 400
        else:
            post = TimelinePost.create(name=name, email=email, content=content)
            return model_to_dict(post)
   

@app.route("/api/timeline_post", methods=["GET"])
def get_time_line_post():
    return {
        "timeline_posts": [
            model_to_dict(p)
            for p in TimelinePost.select().order_by(TimelinePost.created_at.desc())
        ]
    }


@app.route("/api/timeline_post", methods=["DELETE"])
def delete_time_line_post():

    post_id = request.form["id"]
    TimelinePost.delete_by_id(post_id)
    return "deleted post\n"

# this endpoint handles bad requests (400 only), and returns a string depending on which parameter is missing from the bad request.
# this does not cover many of the end cases, but you are using bootstrap forms on the frontend which already cover your input validation, so these backend checks are redundant
@app.errorhandler(werkzeug.exceptions.BadRequest)
def handle_bad_request(e):

    # at this point, the request is bad, now we check if a parameter is missing to determine the err msg
    req = request
    if 'name' not in req.form:
        return "Invalid name", 400
    elif 'email' not in req.form:
        return "Invalid email", 400
    elif ('content' not in req.form):
        return "Invalid content", 400
    else:
        return "Invalid format, try again"


if __name__ == "__main__":
    app.run()
