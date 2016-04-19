from flask import Flask
from flask import render_template, request
from query import db_query_date
from query import db_query_month

import jinja2
import json

app = Flask(__name__)


#return the initial page with parameter request
@app.route("/")
def index_page():
	return render_template("index.html")


@app.route("/", methods=['POST'])
def index_post():


	#Get elements from html form
	city_name = request.form['location']
	city_name = city_name.upper()
	time_data1 = request.form['date']
	time_data = time_data1.replace("-", "")

	#Return data for the full month
	act_temp = []
	pred_temp = []
	my_var = db_query_month(city_name, time_data)
	rdata = json.loads(my_var, parse_float=float)
	for d in rdata:
		act_temp.append(d['act_temp'])
		pred_temp.append(d['pred_temp'])

	#Rerutn the data for the date requested
	single_act_temp = []
	single_pred_temp = []
	data_query = db_query_date(city_name, time_data)
	Sdata = json.loads(data_query, parse_float=float)
	for item in Sdata:
		single_pred_temp.append(d['pred_temp'])
	


	return render_template("index.html",  JSlocation = city_name,
		JSsingle_date = time_data1,
		JSsingle_pred_temp = single_pred_temp,
		JSact_temp = act_temp,
		JSpred_temp = pred_temp, 
		check_data_flask = "0")


if __name__=="__main__":
	app.run(host = '0.0.0.0', port=5000, debug=True)

