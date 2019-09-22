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
	parent_id = ""
	counter = 0
	while counter < dict_num and is_name == False:
		current_dict = list_of_dicts[counter]
		if current_dict.get('parent_name') == query.replace('_', ' ').title():
			is_name = True
			parent_id = str(current_dict.get('parent_id'))
		counter += 1
	if is_name == True:
		return show_building(parent_id)
	else:
		return show_number(int(query))


def show_building(parent_id):

	key = "-VsZgGinNEOP9UZyeYhElGo6EpdmeMQq6lpJRfZYhO4vh0SH56NLQo54p0oh7Qh_"
	auth = {'auth_token' : key}
	r = requests.get('https://density.adicu.com/latest/building/' + parent_id, params=auth)	
	data =  json.loads(r.text)
	list_of_strings = []
	list_of_dicts = data.get('data')
	num_groups = len(list_of_dicts)
	key1 = 'group_name'
	key2 = 'percent_full'
	for x in range(num_groups):
		dict = list_of_dicts[x]
		line = dict.get(key1) + ' is ' + str(dict.get(key2)) + '% full'
		list_of_strings.append(line)
	return json.dumps(list_of_strings)


def show_number(num_groups):

	key = "-VsZgGinNEOP9UZyeYhElGo6EpdmeMQq6lpJRfZYhO4vh0SH56NLQo54p0oh7Qh_"
	auth = {'auth_token' : key}
	r = requests.get('https://density.adicu.com/latest', params=auth)
	data = json.loads(r.text)
	list_of_dicts = data.get('data')
	list_of_strings = []
	new_list = sorted(list_of_dicts, key = lambda i: i['percent_full'])
	
	key1 = 'group_name'
	key2 = 'percent_full'
	for x in range(num_groups):
		dict = new_list[x]
		line = dict.get(key1) + ' is ' + str(dict.get(key2)) + '% full'
		list_of_strings.append(line)		

	return json.dumps(list_of_strings)



if __name__ == '__main__':
	app.run()
