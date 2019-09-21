from flask import Flask, render_template
import requests
from flask import escape
import json
from ast import literal_eval
app = Flask(__name__)


@app.route('/', methods=['GET'])
def main():
	return render_template('index.html')
	
@app.route('/information/<building_name>')
def show_building(building_name):

	key = "-VsZgGinNEOP9UZyeYhElGo6EpdmeMQq6lpJRfZYhO4vh0SH56NLQo54p0oh7Qh_"

	auth = {'auth_token' : key}
	r = requests.get('https://density.adicu.com/latest/building/124', params=auth)	
	data =  json.loads(r.text)
	percent_full = data.get('data')[0].get('percent_full')
	return '%s is %s%% full' % (escape(building_name), percent_full)



if __name__ == '__main__':
	app.run()
