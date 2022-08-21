from stat import filemode
#from xml.etree.ElementInclude import DEFAULT_MAX_INCLUSION_DEPTH
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import time
import random
from scipy import stats

from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, f1_score
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score

import pickle


#model_filedir = "C:\\Users\\coady\\Desktop\\DDDS_ECEN404-master\\DDDS_ECEN404-master\\ML_Models\\trained_models\\"
model_filedir = "../ML_Models/trained_models/"

### FUNCTIONS ###
#convert the data in each feature column to be [0, 1]
def normalize_data(data, classes_in, drop_time=True):
	#normalized_data = (data - data.min()) / (data.max() - data.min())
	normalize_param = {}
	
	normalized_data = data.copy()
	for col in data.columns:
		min = data[col].min()
		max = data[col].max()
		if (min == max):
			normalized_data.drop(col, axis=1, inplace=True)
		else:
			normalized_data[col] = (data[col] - min) / (max - min)

			#save normalization parameters (min and max) into set for each column
			normalize_param[col] = [min, max]
		
		if (not drop_time and col == "timestamps"):
			normalized_data[col] *= (max - min)
	
	#don't normalize last label indicating classes
	if (classes_in == True):
		normalized_data[normalized_data.columns[-1]] = data[data.columns[-1]]
		
	return normalized_data, normalize_param


#removes all outliers from data to get more normally distributed data
def remove_outliers(data):
	#anything that is outside of 3 degrees of standard deviation gets clipped
	#print("original size: " + str(data.shape[0]))
	#print(data["drowsy"].value_counts(normalize=True))
	#data_clipped = data[(np.abs(stats.zscore(data)) >= 3).all(axis=1)]
	#data_clipped.to_csv("clipped.csv", index=False)
	data = data[(np.abs(stats.zscore(data)) < 3).all(axis=1)]
	#print("clipped size: " + str(data.shape[0]))
	#print(data["drowsy"].value_counts(normalize=True))
	return data


#preprocess the data (collected data) by:
# - removing timestamp column
# - replacing nan values in each column with the column's mean
# - normalizing each column to be between [0, 1]
def preprocess_data(data, classes_in, drop_time=True):
	if drop_time:
		data.drop("timestamps", axis=1, inplace=True)
	
	data = data.dropna(axis='rows')
	#data = remove_outliers(data)
	data, norm_param = normalize_data(data, classes_in, drop_time)
	return data, norm_param


def print_accuracy(y_true, y_pred, window=0, advance=0, test_output="test_results.txt"):
	# with open(test_output, 'a') as f:
	# 	f.write('\n\n\nWindow = '+str(window)+' Advancement = '+str(advance)+' Results'+'\n')
	# 	f.write(str(confusion_matrix(y_true, y_pred))+'\n')
	# 	f.write(str(f1_score(y_true, y_pred, average=None))+'\n')
	# 	f.write("Total accuracy:  "+ str(f1_score(y_true, y_pred, average='weighted'))+'\n\n\n')
	print(confusion_matrix(y_true, y_pred))
	print(f1_score(y_true, y_pred, average=None))
	print("Total accuracy: ", f1_score(y_true, y_pred, average='weighted'))


#trains the model over different sets of data and compares the accuracues
def cross_validation(data):
	# prepare the cross-validation procedure
	cv = KFold(n_splits=10, random_state=1, shuffle=True)
	data_x = data.iloc[:,:-1]
	data_y = data.iloc[:, -1]
	# evaluate model
	model = svm.SVC(kernel = 'rbf', random_state = 0)
	scores = cross_val_score(model, data_x, data_y, scoring='accuracy', cv=cv, n_jobs=-1)

	print(scores)
	print("Accuracy:\n mean - %.3f\nstdev - %.3f" % (np.mean(scores), np.std(scores)))


#train model on training set
def train_model(model, x_train, y_train):
	model.fit(x_train, y_train)


#test model on testing set/new data
def test_model(model, x_test, y_test, window=0, advance=0):
	prediction_time = time.time()
	y_pred = model.predict(x_test)
	
	prediction_time = time.time() - prediction_time
	print("Time to predict: ", prediction_time)
	print_accuracy(y_test, y_pred, window, advance)


#use model to predict value for new data
#x_data is in format [[column names], [values], [values], ...]
#x_data should only have 2 lists, 1 for column names, 1 for 1 set of values
def model_predict(model, norm_param, data):
	#convert data into DataFrame
	columns = data[0]
	x_data = data[1]
	df = pd.DataFrame([x_data], columns=columns)


	#PREPROCESSING
	#removing timestamps
	df.drop("timestamps", axis=1, inplace=True)

	#normalization
	for col in df.columns:
		min = norm_param[col][0]
		max = norm_param[col][1]
		df[col] = (df[col] - min) / (max - min)


	#PREDICTION
	#predict with trained model
	y_pred = model.predict(df)
	#print(y_pred)
	output = "drowsy" if y_pred == 1 else "awake"
	#print(output)
	return y_pred


#save object for later use
# - ML model
# - normalizaton parameters
def save_object(object, filename):
	filepath = model_filedir + filename
	pickle.dump(object, open(filepath, 'wb'))


#load saved object
def load_object(filename):
	obj_filepath = model_filedir + filename
	return pickle.load(open(obj_filepath, 'rb'))


#takes aggregate labeled processed data, preprocesses it, splits it into training
# and testing set, trains the model, then tests the model
def KSVM(filedir: str, training_filename: str, window=0, advance=0, testing_file: str=None, save_model=False):
	file = filedir + filename
	data = pd.read_csv(file)
	data_len = data.shape[0]
	print("Number of training data samples:", data_len)

	testing_data = None
	if testing_file is not None:
		testing_data = pd.read_csv(testing_file)
		print("Number of testing data samples:", testing_data.shape[0])
		data = data.append(testing_data, ignore_index=True)
		print("Number of total data samples:", data.shape[0])

	data, norm_param = preprocess_data(data, True)
	print("Total_data shape after preprocessing:", data.shape)

	n_classes = len(np.unique(data[data.columns[-1]]))
	n_features = len(data.columns) - 1
	print("Number of classes:", n_classes)
	print("Number of features:", n_features)

	if testing_file is not None:
		testing_data = data.iloc[data_len:, :]
	data = data.iloc[:data_len, :]
	print("\nTraining_data shape:", data.shape)

	#split up data into training and testing
	train, test = train_test_split(data, test_size=0.2, random_state=17)
	x_train = train.iloc[:,:-1] # all rows, columns up until last(target)
	y_train = train.iloc[:, -1] # all rows, only target column
	x_test = test.iloc[:, :-1]
	y_test = test.iloc[:, -1]
	#K-FOLD CROSS VALIDATION
	#cross_validation(data)

	model = svm.SVC(kernel = 'rbf', random_state = 1)

	#TRAINING
	train_model(model, x_train, y_train)

	#TESTING
	test_model(model, x_test, y_test, window, advance)

	#TRAIN WITH TESTING DATA
	train_model(model, x_test, y_test)

	if testing_file is not None:
		print(testing_data.shape)
		x_new_test = testing_data.iloc[:,:-1]
		y_new_test = testing_data.iloc[:, -1]
		test_model(model, x_new_test, y_new_test)

	#SAVING MODEL
	if save_model:
		model_filename = "KSVM_" + filename[:-4]
		save_object(model, model_filename)
		norm_filename = "KSVM_norm_param_" + filename[:-4]
		save_object(norm_param, norm_filename)

	#LOADING MODEL
	#loaded_model = load_object(model_filename)
	#loaded_norm_param = load_object(norm_filename)



def prediction_test(filename):
	file = filedir + filename
	data = pd.read_csv(file)

	#LOADING MODEL
	model_filename = "KSVM_" + filename[:-4]
	norm_param_filename = "KSVM_norm_param_" + filename[:-4]
	loaded_model = load_object(model_filename)
	loaded_norm_param = load_object(norm_param_filename)

	#PREDICTING
	for i in range(10000, 11000):
		test_data = [list(data.columns[:-1]), [list(data.iloc[i, :-1].values)]]
		model_predict(loaded_model, loaded_norm_param, test_data)


### MAIN ###
if __name__ == "__main__":
	#file = "../data/403_data/Combined_tab_ratios_C1-4_A1-4.csv"
	#file = "../data/404_data/coady_power_3_ratios_test.csv"
	#file = "../data/403_data/processed/PS_w1280a100.csv"
	filedir = "../data/combined/processed/"
	filename = "PS_w1280a320.csv"
	try:
		KSVM(filedir, filename, testing_file="../data/combined/raw/storage/processed/PS_w1280a320.csv", save_model=True)
	except Exception as e:
		print("Error: ", e)
	input("Press enter to exit:")
	#prediction_test(filename)


#used when this file is imported from outside
def test():
	print("Successfully imported KSVM")
