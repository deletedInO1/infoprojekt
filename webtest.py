from flask import Flask

app = Flask(__name__)

@app.route("/")
def site():
    return "hi"

app.run("localhost", 3000, debug=False)
