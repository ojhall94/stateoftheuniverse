from flask import Flask, render_template
from main import main

app = Flask(__name__)
data = main()

@app.route("/")
def home():
    return render_template("base.html", dictionary=data)  # "Hello, World!"


if __name__ == "__main__":
    app.run(debug=True)
