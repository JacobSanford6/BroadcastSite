from flask import Flask, render_template, url_for, request
from waitress import serve
import json
import time
from PIL import Image
import random
import os

app = app = Flask(__name__)
broadcast = "None"

def handlePost():
    global broadcast

    if request.content_type=="application/json":
        data = json.loads(request.data)
        if data["broadcast"]:
            broadcast = data["broadcast"]
            return "{success:true}"
        else:
            return "{success:false}"
    elif len(request.files) > 0:
        localtime = time.localtime()
        timeNum = int( str( localtime.tm_hour+localtime.tm_min ) + str(localtime.tm_min) )

        if "secret-key" in request.form:
            if "broadcastImage" in request.files and request.form["secret-key"] == str(timeNum):
                print("saved new image")
                bimg = request.files["broadcastImage"]
                bimg.save("C:\\Users\\Jake\\chainReactionLinkSite\\static\\broadImage.jpg")
                return "{success:true}"
            else:
                print(request.form["secret-key"])
                print(str(timeNum))
                return "{success:false}"
    else:
        return"{success:false}"

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("index.html", broadcast=broadcast)
    elif request.method == "POST":
        return handlePost()

if __name__ == "__main__":
    print("Server Launched on Port 5000")
    serve(app, host="0.0.0.0", port="5000")