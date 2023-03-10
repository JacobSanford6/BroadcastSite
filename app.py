from flask import Flask, render_template, url_for, request


app = Flask(__name__)

broadcast = "test"
action = 0
img = None


def handlePost():
    print("recieved post")
    global broadcast
    bc = request.args.get('broadcast')
    print(bc.strip())
    if bc.strip() != "":
        broadcast = bc.strip()
    return "{id:12}"


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        print(broadcast)
        return render_template("index.html", broadcast=broadcast, action=action, img=img)
    elif request.method == 'POST':
        return handlePost()


if __name__ == "__main__":
    app.run(debug=True)
