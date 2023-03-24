from flask import Flask, render_template, url_for, request
import json

app = Flask(__name__)

broadcast = "None"
action = 0
img = None


def handlePost():
    global broadcast
    data = json.loads(request.data)
    print(data['broadcast'])

    
    if data['broadcast']:
        broadcast = data['broadcast']
        
        return json.dumps({'success':True})
    else:
        return "{success:false}"



@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        print(broadcast)
        return render_template("index.html", broadcast=broadcast, action=action, img=img)
    elif request.method == 'POST':
        return handlePost()


if __name__ == "__main__":
    app.run(debug=True)
