from flask import Flask, render_template
import requests
from flask import escape
import json
from ast import literal_eval
app = Flask(__name__)


@app.route('/', methods=['GET'])
def main():
	return render_template('index.html')
	
@app.route('/information/<query>')
def decide_query_type(query):
	r = requests.get('https://density.adicu.com/docs/building_info')
	data = json.loads(r.text)
	list_of_dicts = data.get('data')
	dict_num = len(list_of_dicts)
	is_name = False
	counter = 0
	while counter < dict_num and is_name == False:
		current_dict = list_of_dicts[counter]
		if current_dict.get('parent_name') == query.capitalize():
			is_name = True
	if is_name == True:
		return show_building(query.capitalize())
	else:
		return showing_number(query)




def show_building(building_name):

	key = "-VsZgGinNEOP9UZyeYhElGo6EpdmeMQq6lpJRfZYhO4vh0SH56NLQo54p0oh7Qh_"

	auth = {'auth_token' : key}
	r = requests.get('https://density.adicu.com/latest/building/124', params=auth)	
	data =  json.loads(r.text)
	percent_full = data.get('data')[0].get('percent_full')
	return '%s is %s%% full' % (escape(building_name), percent_full)

def show_number(num_groups):
	return '%s' % escape(num_groups)

if __name__ == '__main__':
	app.run()
