from flask import Flask, render_template, request, url_for, redirect
from pymongo import MongoClient
from services.i2c_manager import I2CManager
app = Flask(__name__, static_folder='templates/assets')

client = MongoClient('localhost', 27017)
db = client.io_pear

if __name__ == "main":
		app.run(debug=True)

# host frontend
@app.route('/', methods=('GET', 'POST'))
def index():
	return render_template('index.html')

i2c_manager = I2CManager()