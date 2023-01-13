from flask import Flask, render_template, redirect

app = Flask(__name__)


@app.route("/")
def redirect_to_hide():
    return redirect("hide")


@app.route("/hide")
def hide():
    return render_template("unicode_hider_template.html", method="hide")


@app.route("/unhide")
def unhide():
    return render_template("unicode_hider_template.html", method="unhide")


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
