import os
from flask import Flask, abort, render_template, request
from dotenv import load_dotenv
import json
from peewee import *
import datetime
from playhouse.shortcuts import model_to_dict
import re

load_dotenv()
app = Flask(__name__)

if os.getenv("TESTING") == "true":
    print("Running in test mode")
    mydb = SqliteDatabase('file:memory?mode=memory&cache=shared', uri=True)
else:
    mydb = MySQLDatabase(os.getenv("MYSQL_DATABASE"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        host=os.getenv("MYSQL_HOST"),
        port=3306,
        charset='utf8mb4',
        use_unicode=True
    )

class TimelinePost(Model):
    name = CharField()
    email = CharField()
    content = TextField()
    created_at = DateTimeField(default=datetime.datetime.now)
    
    class Meta:
        database = mydb

mydb.connect()
mydb.create_tables([TimelinePost], safe=True)

@app.route('/api/timeline_post', methods=['POST'])
def create_time_line_post():
    name = request.form.get('name', '')
    email = request.form.get('email', '')
    content = request.form.get('content', '')

    # Validate input
    if not name:
        return "Invalid name", 400
    if not email or not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email):
        return "Invalid email", 400
    if not content:
        return "Invalid content", 400


    timeline_post = TimelinePost.create(name=name, email=email, content=content)
     
    return model_to_dict(timeline_post)

@app.route('/api/timeline_post', methods=['GET'])
def get_time_line_posts():
    return {
        'timeline_posts': [model_to_dict(post) for post in TimelinePost.select().order_by(TimelinePost.created_at.desc())]
    }

@app.route('/api/timeline_post/<int:post_id>', methods=['DELETE'])
def delete_time_line_post(post_id):
    try:
        post = TimelinePost.get(TimelinePost.id == post_id)
        post.delete_instance()
        return {'status': 'success', 'message': 'Post deleted successfully.'}
    except TimelinePost.DoesNotExist:
        abort(404, description="Post not found.")

@app.route('/timeline')
def timeline():
    try:
        timeline_posts = [model_to_dict(post) for post in TimelinePost.select().order_by(TimelinePost.created_at.desc())]
        print(timeline_posts)
        return render_template('timeline.html', title="Timeline", timeline_posts=timeline_posts, url=os.getenv("URL"))
    except Exception as e:
        abort(500, description=f"An error occurred while fetching timeline posts: {str(e)}")


def load_json_file(filename):
    path = os.path.join(app.root_path, 'data', filename)
    with open(path, 'r') as file:
        return json.load(file)

# Make footer_data accesable globally
@app.context_processor
def inject_footer_data():
    try:
        footer_data = load_json_file('footer.json')
        return dict(footer_data=footer_data)
    except FileNotFoundError:
            abort(404, description="Footer data not found.")

@app.route('/')
def index():
    try:
        about = load_json_file('about.json')
        return render_template('index.html', title="Portfolio Site", about =about, url=os.getenv("URL"))
    except FileNotFoundError:
        abort(404, description="About data not found.")

@app.route('/profile')
def profile():
    try:
        profile = load_json_file('profile.json')
        return render_template('profile.html', title="Profile", profile=profile, url=os.getenv("URL"))
    except FileNotFoundError:
        abort(404, description="Profile data not found.")
    
@app.route('/map')
def travel_map():
    try:
        API_KEY = os.getenv("API_KEY")
        places = load_json_file('map.json')
        return render_template('map.html', title="My Travel Map", places=places, API_KEY=API_KEY, url=os.getenv("URL"))
    except FileNotFoundError:
        abort(404, description="Map data not found.")

@app.route('/hobbies')
def hobbies():
    try:
        hobbies = load_json_file('hobbies.json')
        return render_template('hobbies.html', title="Hobbies", hobbies=hobbies, url=os.getenv("URL"))
    except FileNotFoundError:
        abort(404, description="Hobbies data not found.")