from app import app
from flask import render_template, redirect, request, session, abort
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

@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        role = request.form["role"]
        if len(username) < 3 or len(username) > 20:
            return render_template("error.html", errormessage="Tunnuksen tulee olla vähintään 3 merkkiä ja enintään 20 merkkiä pitkä")
        if len(password) < 3 or len(password) > 100:
            return render_template("error.html", errormessage="Salasanan tulee olla vähintään 3 merkkiä ja enintään 100 merkkiä pitkä")
        if users.username_exists(username):
            return render_template("error.html", errormessage="Käyttäjätunnus on jo käytössä")
        users.register(username, password, role)
        return redirect("/")

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/create_topic", methods=["POST", "GET"])
def create_topic():
    users.role_required(2)

    if request.method == "GET":
        return render_template("create_topic.html")
    
    if request.method == "POST":
        users.check_csrf()
        topic = request.form["title"]
        topics.create_topic(topic)
        return redirect("/")

@app.route("/<topic_id>")
def topic(topic_id):
    try:
        if topics.topic_visible(topic_id).visible < 1:
            abort(404)
    except:
        abort(404)
    allthreads = threads.get_threads(topic_id)
    return render_template("threads.html", threads=allthreads, topic=topic_id)

@app.route("/<topic_id>/delete")
def topic_delete(topic_id):
    users.role_required(2)
    topics.delete_topic(topic_id)
    return redirect("/")

@app.route("/<topic_id>/create_thread", methods=["POST", "GET"])
def createthread(topic_id):
    users.role_required(1)

    if request.method == "GET":
        return render_template("create_thread.html", topic_id=topic_id)

    if request.method == "POST":
        users.check_csrf()
        user = session["user_id"]
        threadname = request.form["title"]
        if len(threadname) < 1 or len(threadname) > 50:
            return render_template("error.html", errormessage="Otsikon tulee olla vähintään 1 merkin ja enintään 50 merkin pituinen") 
        message = request.form["message"]
        if len(message) < 1 or len(message) > 5000:
            return render_template("error.html", errormessage="Viestin tulee olla vähintään 1 merkin ja enintään 5000 merkin pituinen")
        thread_id = threads.create_thread(topic_id, user, threadname)
        messages.send_message(thread_id.id, message, user)
        return redirect("/thread/"+str(thread_id.id))

@app.route("/thread/<thread_id>")
def thread(thread_id):
    if threads.thread_visible(thread_id).visible < 1:
        abort(404)
    allmessages = messages.get_messages(thread_id)
    threadinfo = threads.get_threadinfo(thread_id)
    topic_id = topics.get_topic_id(thread_id)
    return render_template("thread.html", messages=allmessages, info=threadinfo, topic_id=topic_id)

@app.route("/thread/<thread_id>/reply", methods=["POST", "GET"])
def reply(thread_id):
    users.role_required(1)
    
    if request.method == "GET":
        threadinfo = threads.get_threadinfo(thread_id)
        return render_template("reply.html", info=threadinfo)

    if request.method == "POST":
        users.check_csrf()
        content = request.form["content"]
        if len(content) < 1 or len(content) > 5000:
            return render_template("error.html", errormessage="Viestin tulee olla vähintään 1 merkin ja enintään 5000 merkin pituinen")
        user = session["user_id"]
        messages.send_message(thread_id, content, user)
        return redirect("/thread/"+str(thread_id))

@app.route("/edit/<message_id>", methods=["POST", "GET"])
def edit(message_id):
    users.allow_edit(message_id)
    
    if request.method == "GET":
        content = messages.get_content(message_id)
        thread_id = messages.get_thread_id(message_id)
        return render_template("edit.html", content=content, thread_id=thread_id)

    if request.method == "POST":
        users.check_csrf()
        content = request.form["content"]
        if len(content) < 1 or len(content) > 5000:
            return render_template("error.html", errormessage="Viestin tulee olla vähintään 1 merkin ja enintään 5000 merkin pituinen")
        messages.edit_message(message_id, content)
        thread_id = messages.get_thread_id(message_id)
        return redirect("/thread/"+str(thread_id.thread_id))

@app.route("/delete/<message_id>")
def delete_message(message_id):
    if users.role() > 1:
        pass
    else:
        users.allow_edit(message_id)
    thread_id = messages.get_thread_id(message_id)
    messages.delete_message(message_id)
    return redirect("/thread/"+str(thread_id.thread_id))

@app.route("/thread/<thread_id>/edit_title", methods=["POST", "GET"])
def edit_title(thread_id):
    users.allow_thread_edit(thread_id)
    
    if request.method == "GET":
        info = threads.get_threadinfo(thread_id)
        return render_template("edit_title.html", info = info)

    if request.method == "POST":
        users.check_csrf()
        title = request.form["title"]
        if len(title) < 1 or len(title) > 50:
            return render_template("error.html", errormessage="Otsikon tulee olla vähintään 1 merkin ja enintään 50 merkin pituinen")
        threads.edit_title(thread_id, title)
        return redirect("/thread/"+str(thread_id))

@app.route("/thread/<thread_id>/delete")
def delete_thread(thread_id):
    if users.role() > 1:
        pass
    else:
        users.allow_thread_edit(thread_id)
    topic_id = topics.get_topic_id(thread_id)
    threads.delete_thread(thread_id)
    return redirect("/"+str(topic_id.id))

@app.route("/<message_id>/upvote")
def upvote(message_id):
    thread_id = messages.get_thread_id(message_id)
    if messages.has_voted(message_id, session["user_id"]):
        pass
    elif not users.role():
        pass
    else:
        messages.vote(message_id, session["user_id"])
    return redirect("/thread/"+str(thread_id.thread_id))
