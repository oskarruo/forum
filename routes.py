from app import app
from flask import render_template, redirect, request, session
import topics, threads, messages, users

@app.route("/")
def index():
    alltopics = topics.get_topics()
    return render_template("index.html", topics=alltopics)

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    if not users.login(username, password):
        return render_template("error.html", errormessage="Käyttäjätunnus tai salasana on väärä!")
    return redirect("/")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/registration", methods=["POST"])
def registration():
    username = request.form["username"]
    password = request.form["password"]
    if len(username) < 3 or len(username) > 20:
        return render_template("error.html", errormessage="Tunnuksen tulee olla vähintään 3 merkkiä ja enintään 20 merkkiä pitkä")
    if len(password) < 3 or len(password) > 100:
        return render_template("error.html", errormessage="Salasanan tulee olla vähintään 3 merkkiä ja enintään 100 merkkiä pitkä")
    if users.username_exists(username):
        return render_template("error.html", errormessage="Käyttäjätunnus on jo käytössä")
    users.register(username, password)
    return redirect("/")

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/<topic>")
def topic(topic):
    allthreads = threads.get_threads(topic)
    return render_template("threads.html", threads=allthreads, topic=topic)

@app.route("/<topic>/createthread")
def createthread(topic):
    users.islogged()
    return render_template("create_thread.html", topic=topic)

@app.route("/<topic>/create", methods=["POST"])
def create(topic):
    users.islogged()
    user = session["user_id"]
    threadname = request.form["title"]
    if len(threadname) < 1 or len(threadname) > 50:
        return render_template("error.html", errormessage="Otsikon tulee olla vähintään 1 merkin ja enintään 50 merkin pituinen") 
    message = request.form["message"]
    if len(message) < 1 or len(message) > 5000:
        return render_template("error.html", errormessage="Viestin tulee olla vähintään 1 merkin ja enintään 5000 merkin pituinen")
    topic_id = topics.get_topicid(topic)
    thread_id = threads.create_thread(topic_id.id, user, threadname)
    messages.send_message(thread_id.id, message, user)
    return redirect("/")

@app.route("/thread/<thread_id>")
def thread(thread_id):
    allmessages = messages.get_messages(thread_id)
    threadinfo = threads.get_threadinfo(thread_id)
    return render_template("thread.html", messages=allmessages, info=threadinfo)

@app.route("/thread/<thread_id>/reply")
def reply(thread_id):
    users.islogged()
    threadinfo = threads.get_threadinfo(thread_id)
    return render_template("reply.html", info=threadinfo)

@app.route("/thread/<thread_id>/send", methods=["POST"])
def send(thread_id):
    users.islogged()
    content = request.form["content"]
    if len(content) < 1 or len(content) > 5000:
        return render_template("error.html", errormessage="Viestin tulee olla vähintään 1 merkin ja enintään 5000 merkin pituinen")
    user = session["user_id"]
    messages.send_message(thread_id, content, user)
    return redirect("/")