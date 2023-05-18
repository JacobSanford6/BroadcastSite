from flask import Flask, render_template, url_for, request
from waitress import serve
import json
import time

app = app = Flask(__name__)
broadcast = "None"
imageNum = 0
imgPath = "static/broadImage"

# Handles post requests recieved from clients
# Returns json success data to client
def handlePost():
    global broadcast

    if request.content_type=="application/json":
        data = json.loads(request.data)
        if data["broadcast"]:
            broadcast = data["broadcast"]
            return "{success:true}"
        else:
            return "{success:false}"
    # If a file was sent...
    elif len(request.files) > 0:
        # Create server side secret key
        localtime = time.localtime()
        timeNum = int( str( localtime.tm_hour+localtime.tm_min ) + str(localtime.tm_min) )
        global imageNum

        #check to make sure secret keys match
        if "secret-key" in request.form:
            if "broadcastImage" in request.files and request.form["secret-key"] == str(timeNum):
                bimg = request.files["broadcastImage"]
                # Switch image name every other time, so laptop knows when to update site
                bimg.save(imgPath + str(imageNum)+".jpg")
                if imageNum == 0:
                    imageNum = 1
                else:
                    imageNum = 0
                return "{success:true}"
            else:
                return "{success:false}"
    else:
        return"{success:false}"

# GET and POST requests handler
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        # Determine what image to show when website is requeted
        if imageNum == 1:
            return render_template("index.html", broadcast=broadcast, bimg=imgPath+"0.jpg")
        else:
            return render_template("index.html", broadcast=broadcast, bimg=imgPath+"1.jpg")
    elif request.method == "POST":
        return handlePost()

if __name__ == "__main__":
    print("Server Launched on Port 5000")
    serve(app, host="0.0.0.0", port="5000")