from flask import Flask, render_template, url_for, request

app = Flask(__name__)

def handlePost():
    print(request.args.get('broadcast'))
    
    return "<p>Test Get<p>"


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template("index.html")
    elif request.method == 'POST':
        return handlePost()


if __name__ == "__main__":
    app.run(debug=True)
