from flask import Flask, render_template, url_for, request
from waitress import serve
import json
import time
from PIL import Image
import random
import os
import openpyxl
from pathlib import Path

app = app = Flask(__name__)
broadcast = "None"
imageNum = 0
imgPath = "static/broadImage"

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
        global imageNum

        if "secret-key" in request.form:
            if "broadcastImage" in request.files and request.form["secret-key"] == str(timeNum):
                bimg = request.files["broadcastImage"]
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

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        if imageNum == 1:
            return render_template("index.html", broadcast=broadcast, bimg=imgPath+"0.jpg")
        else:
            return render_template("index.html", broadcast=broadcast, bimg=imgPath+"1.jpg")
    elif request.method == "POST":
        return handlePost()
    if request.method == "GET":
        nDict = {}

        nArr =readXlsx()
        
        nDict["days"] = nArr[0]
        
        for row in nArr[1::]:
            name = row[0].split(" ")[0]
            if name.strip() == "":
                name = row[0].split(" ")[1]
            if name.strip() == "":
                name = "err"
            if name != "err":
                nDict[name] = row[1::]

        return json.dumps(nDict)
    else:
        return "{test:'No'}"

if __name__ == "__main__":
    print("Server Launched on Port 5000")
    serve(app, host="0.0.0.0", port="5000")