from flask import Flask, render_template, request, url_for, redirect
app = Flask(__name__, static_folder='templates/assets')

if __name__ == "main":
        app.run(debug=True)

@app.route('/', methods=('GET', 'POST'))
def index():
    return render_template('index.html')