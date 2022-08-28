from flask import Flask, render_template, make_response

app = Flask(__name__)

menu = [{"title": "main page", "url": "/"},
        {"title": "Add article", "url": "/add_post"}
        ]

@app.route("/")
def index():
    content = render_template("index.html", menu=menu, posts=[])
    res = make_response(content)
    res.headers['Content-type'] = 'text/plain'
    res.headers['Server'] = 'flasksite'
    return res

if __name__ == "__main__":
    app.run(Debug=True)
