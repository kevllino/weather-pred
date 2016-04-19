import simplejson as json
import pandas as pd
import pandas.io.sql as psql
from pyhive import hive


def db_query_month(city_name, date_value):
	cursor = hive.connect('localhost').cursor()
	#conn = pymysql.connect(sql_host, sql_usr, paswrd, db)
	query = r"SELECT * FROM weather_data WHERE location LIKE '%" + city_name + "%' AND temp_dat LIKE '%" + date_value[:6] + "%'"
	cursor.execute(query)
	all_data = cursor.fetchall()
	df = pd.DataFrame([[ij for ij in i] for i in all_data])
	df.columns = ["location", "temp_date", "act_temp", "pred_temp"]
	datafr = df.reset_index().to_json(orient='records')
	return datafr


def db_query_date(city_name, date_value):
	cursor = hive.connect('localhost').cursor()
	query = r"SELECT * FROM weather_data WHERE location LIKE '%" + city_name + "%' AND temp_dat LIKE '%" + date_value + "%'"
	cursor.execute(query)
	all_data = cursor.fetchall()
	df = pd.DataFrame([[ij for ij in i] for i in all_data])
	df.columns = ["location", "temp_date", "act_temp", "pred_temp"]
	datafr = df.reset_index().to_json(orient='records')
	return datafr


