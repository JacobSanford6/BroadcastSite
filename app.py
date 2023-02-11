from flask import Flask, render_template, url_for, request
from flask_socketio import *

app = Flask(__name__)

broadcast = "black"
action = 0
img = None


def handlePost():
    global broadcast
    bc = request.args.get('broadcast')
    print(bc.strip())
    if bc.strip() != "":
        broadcast = bc.strip()
    return "<p>Thank you</p>"


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        print(broadcast)
        return render_template("index.html", broadcast=broadcast, action=action, img=img)
    elif request.method == 'POST':
        return handlePost()


if __name__ == "__main__":
    socketio.run(debug=True)
