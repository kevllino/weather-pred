# -*- coding: utf-8 -*-
from pyspark import SparkContext
from pyspark.rdd import RDD
import os, sys
import numpy as np
from pyspark.mllib.regression import LabeledPoint
from pyspark.mllib.regression import LinearRegressionWithSGD
from pyspark.mllib.feature import Normalizer

# transform timestamps 
def transform_tsp(line):
    line[3] = line[3][:-4]
    return line 


# keep relevant featires for now
def extract_features(line):
    # the following indexes contian the relevant features: 0, 3, 4, 5, 22, 34; including 23 to deqal with N/A which can be
    # handled using other present values and 8 to map categorical features
    # NOTE: we group categorical and numerical features next to each other to make the task of creating feature vectors
    # easier later
    features = [line[0]] + [line[3]] + [line[8]] + line[4:6] + [line[26]] + line[22:24] + [line[34]]
    return features

# replace * with '' 
def transform_stars(line):
    import re
    for i in range(len(line)): 
        # line[i] = re.sub(r"(\*|\s)+","0",line[i])
        line[i] = re.sub(r"\*+",'',line[i])
    return line 


def replace_categ_data(line, maxi_key):
    if line[2] == '':
        line[2] =  maxi_key
    return line 

# handling numerical missing values 
def replace_numerical_data(line, average_values):
    for i in range(3, 8):
        if line[i] == '':
            line[i] =  average_values[i-3]
    return line  

# take (key, [[],.....[]]) <-- list of features
def numerical_data_averaging(line):
    values = []
    result = []
    for l in xrange(3, 9):
        value = [(float(line[1][j][l]) if line[1][j][l] else 0) for j in xrange(len(line[1]))]
        values.append(np.mean(value)) 
    result = line[1][0][0:3] + values
    return result

# binary-encoding of categorical features
def feature_mapping(rdd, index):
    return rdd.map(lambda fields: fields[index]).distinct().zipWithIndex().collectAsMap()

def create_key(line):
    return line[0] + "|" + line[1]

def get_features(line, categorical_length,mappage):
    categorical_vector = np.zeros(categorical_length)
    i = 0 
    offset = 0
    # access every categorical feature
    for field in line[0:3]:
        # access every dictionnaryy in overall mapping 
        map_dict = mappage[i]
        # get the index in dict which value is different than 0 
        index = map_dict[field]
        # assign the  value of 1 to the correcoping global index in categ_vector
        categorical_vector[index + offset] = 1
        # go to next dict and increase offest
        i = i + 1
        offset = offset + len(map_dict)
    
    # assign vector for numerical features by normalising them to fix scaling problems later
    normalizer = Normalizer()
    numerical_vector = normalizer.transform(np.array([float(val) for val in line[3:8]]))
    return np.concatenate((categorical_vector,numerical_vector))

def get_label(line):   
    return float(line[-1]) if line[-1] else 0 

# performance evaluation functions
def squarred_error(actual, pred):
    return (pred - actual)**2

def abs_error(actual, pred):
    return np.abs(pred - actual)

def squared_log_error(pred, actual):
    return (np.log(pred+1)-np.log(actual+1))**2

# tuning parameters using CV
def evaluate(train,test,iterations,step,regParam,regType,intercept):
    model = LinearRegressionWithSGD.train(train, iterations, step,regParam=regParam, regType=regType, intercept=intercept)
    tp = test.map(lambda p: (p.label, model.predict(p.features)))
    rmse = np.sqrt(tp.map(lambda (t,p): squarred_error(t,p)).mean())
    mae = np.sqrt(tp.map(lambda (t,p): abs_error(t,p)).mean())
    rmsle = np.sqrt(true_vs_predicted.map(lambda (t,p): squared_log_error(t,p)).mean())
    opt_metrics = [rmse,mae,rmsle] 
    return opt_metrics


if __name__ == "__main__":
	sc = SparkContext()

	# load the data 
	clean_data = sc.textFile("s3n://usweatherdata/big_file3.txt")

	# split every line of records and cache 
	wea_recs = clean_data.map(lambda line: line.split())
	wea_recs.cache()

	# format the timestamps to just keep the minutes
	wea_recs1 = wea_recs.map(lambda fields: transform_tsp(fields))

	# keep complete features
	wea_recs2 = wea_recs1.map(lambda line: extract_features(line))

	# replace * characters
	wea_recs3 = wea_recs2.map(lambda fields: transform_stars(fields))
	wea_recs3_bis = wea_recs2.map(lambda fields: transform_stars(fields))
	firstone = wea_recs3.first()

	# get rid of line of records with only 3 features recorded and the rest filled with N/As
	wea_recs3 = wea_recs3.filter(lambda line: len([features for features in line if features != '']) > 3)

	# we handle missing sky_over recorded by replacing any missing values with the one having the largest occurence
	# first we get average, e.g. DEWP 
	sky_cover = wea_recs3_bis.map(lambda fields: (fields[2], 1)).reduceByKey(lambda x, y: x+y).collectAsMap()
	sky_cover_not_null_keys = [k for (k,v) in sky_cover.items() if k != '' ] 
	maxi_val = np.max([sky_cover[k] for k in sky_cover_not_null_keys])
	maxi_key = [k for (k,v) in sky_cover.items() if v == maxi_val][0]


	wea_recs3 = wea_recs3.map(lambda line:  replace_categ_data(line, maxi_key))

	# Handling numerical missing values by replacing them with the average of the feature values 
	wea_recs3bis1 = wea_recs3.map(lambda line: line)
	wea_recs3bis2 = wea_recs3.map(lambda line: line)
	wea_recs3bis3 = wea_recs3.map(lambda line: line)
	wea_recs3bis4 = wea_recs3.map(lambda line: line)
	wea_recs3bis5 = wea_recs3.map(lambda line: line)
	average_wind_direction = wea_recs3bis1.map(lambda fields: float(fields[3]) if fields[3] else 0 ).collect()
	average_wind_speed = wea_recs3bis2.map(lambda fields: float(fields[4]) if fields[4] else 0 ).collect()
	sea_level_pressure= wea_recs3bis3.map(lambda fields: float(fields[5]) if fields[5] else 0 ).collect()
	average_temperature = wea_recs3bis4.map(lambda fields: float(fields[6]) if fields[6] else 0 ).collect()
	average_dewp = wea_recs3bis5.map(lambda fields: float(fields[7]) if fields[7] else 0 ).collect()
	average_values = [ np.mean(val) for val in [average_wind_direction, average_wind_speed, sea_level_pressure, average_temperature, average_dewp] ] 
	wea_recs4 = wea_recs3.map(lambda line: replace_numerical_data(line,average_values))

	# convert the pyspark iterable to a list 
	temp_wea =  wea_recs4.map(lambda line: (create_key(line),line)).groupByKey()
	temp_wea1 = temp_wea.map(lambda fields: (fields[0],list(fields[1])))
	temp_wea2 = temp_wea1.map(lambda line: numerical_data_averaging(line))


	# binary-encoding of categorical features
	mappage = [feature_mapping(wea_recs3, i) for i in range(0,3)]
	categorical_length = sum(map(len, mappage))
	numerical_length= len(firstone[3:8])
	total_length = categorical_length + numerical_length

	# building the feature vectors 
	feature_vectors = temp_wea2.map(lambda line: LabeledPoint(get_label(line),get_features(line, categorical_length,mappage)))
	feature_vectors1 = temp_wea2.map(lambda line: (line[0],line[1],LabeledPoint(get_label(line),get_features(line, categorical_length,mappage))))

	# train the model 
	linear_model = LinearRegressionWithSGD.train(feature_vectors, iterations=10,step=0.1,intercept=False)
	true_vs_predicted = feature_vectors.map(lambda p: (p.label,linear_model.predict(p.features)))
	true_vs_predicted1 = feature_vectors1.map(lambda p: (p[0],p[1],p[2].label,linear_model.predict(p[2].features)))

	# save the output as (LOC,TSP,actual_temp,predicted_temp)
	true_vs_predicted1.saveAsTextFile("s3n://usweatherdata/weather_predictions1")

	# Evaluate performance
	# print 'Linear modelmse predictions: ' + str(true_vs_predicted.take(5))
	rmse = np.sqrt(true_vs_predicted.map(lambda (t,p): squarred_error(t,p)).mean())
	mae = true_vs_predicted.map(lambda (t,p): abs_error(t,p)).mean()
	rmsle = np.sqrt(true_vs_predicted.map(lambda (t,p): squared_log_error(t,p)).mean())

	# Tuning parameters using cross validation 
	# we operate on the index keys
	indexed_feature_vectors = feature_vectors.zipWithIndex().map(lambda (k,v): (v,k))

	# randomly splitting training and testing data
	test = indexed_feature_vectors.sample(False,0.2)
	train = indexed_feature_vectors.subtractByKey(test)
	train_data = train.map(lambda (index, p): p)
	test_data = test.map(lambda (index, p): p)
	train_size = train_data.count()

	# Optimal number of iterations 
	params = [1,5,10,20,50,100]
	metrics = [evaluate(train_data,test_data,param,0.01,0.0,'l2',False) for param in params]
	optimal_niter = params[metrics.index(min(metrics))]

	# Optimal learning rate
	paramss = [0.01,0.025,0.05,0.1,0.25,0.5]
	metrics2 = [evaluate(train_data,test_data,100,param,0.0,'l2',False) for param in paramss]
	optimal_step = paramss[metrics2.index(min(metrics2))]
	opt_metrics = evaluate(train_data,test_data,optimal_niter,optimal_step,0.0,'l2',False) 
	rmse_opt = opt_metrics[0]
	mae_opt = opt_metrics[1]
	rmsle_opt = opt_metrics[2]	

	
	# use the tuned hyperparameters to optimise the regression model, get better predictions and finally save those results to S3
	linear_model2 = LinearRegressionWithSGD.train(feature_vectors, 	iterations=optimal_niter,step=optimal_step,intercept=False)
	true_vs_predicted2 = feature_vectors1.map(lambda p: (p[0],p[1],p[2].label,linear_model2.predict(p[2].features)))
	true_vs_predicted2.saveAsTextFile("s3n://usweatherdata/weather_predictions3")	

	print "\n<<<<<<<<<<<EVALUATION PERFORMANCE REPORT>>>>>>>>>>>>"
	print "Linear Model - Before optimizing the hyperparameters:"
	print "Root Mean Squared Error: %2.4f " % rmse
	print "Mean Absolute Error: %2.4f " % mae
	print "Root Mean Squared Log Error: %2.4f " % rmsle
	print "\n"
	print "Optimal Linear Model - After tuning the parameters:"
	print "Root Mean Squared Error: %2.4f " % rmse_opt
	print "Mean Absolute Error: %2.4f " % mae_opt
	print "Root Mean Squared Log Error: %2.4f " % rmsle_opt
	print "<<<<<<<<<<<<<<<<<<END OF REPORT>>>>>>>>>>>>>>>>>>>>>\n"


	sc.stop()
