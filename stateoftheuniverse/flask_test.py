from flask import Flask, render_template
from main import main

app = Flask(__name__)
text = main()
print(text)
text = {"consts": text}
print(text)
@app.route("/")
def home():
	return render_template("base.html", dictionary=text) #"Hello, World!"

if __name__ == "__main__":
	app.run(debug=True)
