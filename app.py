from flask import Flask, render_template, url_for, request
from waitress import serve
import json
import time

app = Flask(__name__)

broadcast = "None"
action = 0
broadcastImageHtml = "<p></p>"

def handlePost():
    global broadcast
    global broadcastImageHtml

    if request.content_type=="application/json":
        data = json.loads(request.data)
        print(data['broadcast'])

        
        if data['broadcast']:
            broadcast = data['broadcast']
            
            return json.dumps({'success':True})
        else:
            return "{success:false}"
    elif request.content_type.split(";")[0] == "multipart/form-data":
        data = request.form
        

        print(data.keys())
        
        if data["broadcastImage"]:
            print(type(data["broadcastImage"]))
            print("Printing image binary data in 2 seconds")
            time.sleep(2)
            print(data["broadcastImage"])
        
        return "{success:false}"



@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        print(broadcast)
        return render_template("index.html", broadcast=broadcast, action=action, broadcastImage=broadcastImageHtml)
    elif request.method == 'POST':
        return handlePost()


if __name__ == "__main__":
    print("Server Launched on Port 5000")
    serve(app, host="0.0.0.0", port="5000")