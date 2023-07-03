from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/template", methods=["GET","POST"])
def template():
    if request.method == "POST":
        pass
    else:
     return render_template("template.html")


if __name__ == '__main__':
    app.run()