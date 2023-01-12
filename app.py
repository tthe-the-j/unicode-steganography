from flask import Flask, render_template

app = Flask(__name__)

@app.route("/encode")
def encode():
    return render_template("unicode_hider_template.html", method="encode")

@app.route("/decode")
def encode():
    return render_template("unicode_hider_template.html", method="decode")

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)