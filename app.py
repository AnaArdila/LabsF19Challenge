from flask import Flask, render_template
import requests
from flask import escape

app = Flask(__name__)


@app.route('/', methods=['GET'])
def main():
	#return render_template('index.html')
	show_building('butler')
	
@app.route('/information/<building_name>')
def show_building(building_name):
	return 'Building is: %s' % escape(building_name)

if __name__ == '__main__':
	app.run()
