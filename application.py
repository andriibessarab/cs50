import os
import sys

from flask import Flask, render_template, redirect, request, jsonify
from flask_socketio import SocketIO, emit
from PIL import Image

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)

channels = {}
users = []
imageID = 0
allImages = []

# MAIN
@app.route("/", methods=["GET", "POST"])
def main():
    return render_template("main.html")


# OTHER

# ADD USER
@app.route("/add_user", methods=["POST"])
def add_user():
    global users
    username = request.form.get("username")
    if username in users:
        return jsonify({"valid": False})
    else:
        users.append(username)
        return jsonify({"valid": True})

# CREATE CHANNEL
@app.route("/create_channel", methods=["POST"])
def create_channel():
    global channels
    channel_name = request.form.get("channel_name")
    for channel in channels:
        if channel_name == channel:
            return jsonify({"valid": False})
    channels[channel_name] = []
    return jsonify({"valid": True})

# GET CHANNELS
@app.route("/get_channels", methods=["POST"])
def get_channels():
    return jsonify({"channels": channels})

# GET MESSAGES
@app.route("/get_messages", methods=["POST"])
def get_messages():
    channel = request.form.get("channel")
    return jsonify({"channel": channel, "messages": channels[channel]})

# ADD MESSAGE
@app.route("/add_message", methods=["GET", "POST"])
def add_message():
    global channels, imageID, allImages
    if request.form.get("type") == "11":
        message = request.form.get("message")
        image = request.files["image"]
        channel = request.form.get("channel")
        author = request.form.get("author")
        date = request.form.get("date")
        time = request.form.get("time")
        need_to_delete = request.form.get("need_to_delete")
        image_name = str(imageID) + image.filename
        if image_name in allImages:
            image_name = str(imageID) + "copy(" + \
                str(imageID) + ")" + image.filename
        image.save("./static/files/" + image_name)
        imageID += 1
        allImages.append(image_name)
        if need_to_delete == True:
            del channels[channel][0]
        channels[channel].append(
            ["11", message, image_name, author, date, time])
    if request.form.get("type") == "10":
        message = request.form.get("message")
        channel = request.form.get("channel")
        author = request.form.get("author")
        date = request.form.get("date")
        time = request.form.get("time")
        need_to_delete = request.form.get("need_to_delete")
        if need_to_delete == True:
            del channels[channel][0]
        channels[channel].append(["10", message, author, date, time])
    if request.form.get("type") == "01":
        image = request.files["image"]
        channel = request.form.get("channel")
        author = request.form.get("author")
        date = request.form.get("date")
        time = request.form.get("time")
        need_to_delete = request.form.get("need_to_delete")
        image_name = str(imageID) + image.filename
        if image_name in allImages:
            image_name = str(imageID) + "copy(" + \
                str(imageID) + ")" + image.filename
        image.save("./static/files/" + image_name)
        imageID += 1
        allImages.append(image_name)
        if need_to_delete == True:
            del channels[channel][0]
        channels[channel].append(["01", image_name, author, date, time])
    return jsonify({"done": True})


# SOCKETIO

# NEW CHANNEL ADDED
@socketio.on("new channel added")
def new_channel_added():
    emit("refresh channels", broadcast=True)

# NEW MESSAGE ADDED
@socketio.on("new message added")
def new_message_added(data):
    for channel in channels:
        if channel == data["channel"]:
            emit("refresh channel", {"channel": channel}, broadcast=True)
