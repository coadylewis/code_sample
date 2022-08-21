import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import tensorflow as tf
import time
import random
import pickle

from tensorflow import keras
from scipy import stats
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, f1_score


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


def remove_outliers(data):
    #removes all outliers from data to get more normally distributed data
    data = data[(np.abs(stats.zscore(data)) < 3).all(axis=1)]
    return data


#preprocess the data (collected data) by:
# - removing timestamp column
# - replacing nan values in each column with the column's mean
# - normalizing each column to be between [0, 1]
def preprocess_data(data, classes_in, drop_time=True):
    if drop_time:
        data.drop("timestamps", axis=1, inplace=True)
    
    data = data.dropna(axis='columns')
    #data = remove_outliers(data)
    data, norm_param = normalize_data(data, classes_in, drop_time)
    return data, norm_param


def print_accuracy(y_true, y_pred):
    print(confusion_matrix(y_true, y_pred))
    print(f1_score(y_true, y_pred, average=None))
    print("Total accuracy: ", f1_score(y_true, y_pred, average='weighted'))


#train model on training set
def train_model(model, x_train, y_train):
	model.fit(x_train, y_train)


#test model on testing set/new data
def test_model(model, x_test, y_test):
    prediction_time = time.time()
    y_pred = model.predict(x_test)
    y_pred = (y_pred > 0.5)
    
    prediction_time = time.time() - prediction_time
    print("Time to predict: ", prediction_time)
    print_accuracy(y_test, y_pred)


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


#save Neural Network for later use
def save_NN(model, filename):
    filepath = model_filedir + filename
    model.save(filepath)


#load Neural Network
def load_model(filename):
    filepath = model_filedir + filename
    return keras.models.load_model(filepath)


#save object for later use
# - normalizaton parameters
def save_object(object, filename):
	filepath = model_filedir + filename
	pickle.dump(object, open(filepath, 'wb'))


#load saved object
def load_object(filename):
	obj_filepath = model_filedir + filename
	return pickle.load(open(obj_filepath, 'rb'))


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
	output = "drowsy" if y_pred >= 0.5 else "awake"
	#print(output)
	return y_pred


#takes aggregate labeled processed data, preprocesses it, splits it into training
# and testing set, trains the model, then tests the model
def ANN(filedir, filename):
    file = filedir + filename
    data = pd.read_csv(file)
    data, norm_param = preprocess_data(data, True)

    n_classes = len(np.unique(data[data.columns[-1]]))
    n_features = len(data.columns) - 1
    print("Number of classes: ", n_classes)
    print("Number of features: ", n_features)

    #split up data into training and testing
    train, test = train_test_split(data, test_size=0.4, shuffle=True, random_state=27)
    x_train = train.iloc[:,:-1] # all rows, columns up until last(target)
    y_train = train.iloc[:, -1] # all rows, only target column
    x_test_full = test.iloc[:, :-1]
    y_test_full = test.iloc[:, -1]


    #NEURAL NETWORK ARCHITECTURE
    #hidden layers in a pyramid fashion, less neurons at the outer layers
    #regularization: kernel_regularizer=keras.regularizers.l2(0.01)
    #hidden layer activation: relu(o), sigmoid, tanh
    #output layer activation: linear, sigmoid, softmax(o)
    model = keras.Sequential([
        keras.layers.Dense(n_features + 1, input_dim=n_features),  # input layer (1)
        keras.layers.Dense(int(n_features / 2) + 1, activation='relu'),  # hidden layer (2)
        keras.layers.Dropout(0.2),
        #keras.layers.Dense(int(n_features / 4) + 1, activation='relu'), # hidden layer (3)
        #keras.layers.Dropout(0.2),
        #keras.layers.Dense(32, activation='relu', kernel_regularizer=keras.regularizers.l2(0.001)), # hidden layer (4)
        #keras.layers.Dropout(0.2),
        keras.layers.Dense(1, activation='sigmoid') # output layer (5)
    ])

    model.compile(optimizer='adam',
                loss='binary_crossentropy',
                metrics=['accuracy'])
    
    earlystopping = keras.callbacks.EarlyStopping(monitor ="val_loss", 
                                              mode ="min", patience = 5,
                                              restore_best_weights = True)

    partition = int(test.shape[0]/2)
    print(partition)
    x_val = x_test_full[:partition]
    y_val = y_test_full[:partition]

    x_test = x_test_full[partition:]
    y_test = y_test_full[partition:]


    #TRAINING
    model.fit(x_train, y_train, 
            epochs=100, 
            batch_size=32,
            validation_data = (x_val, y_val),
            callbacks = [earlystopping])
    
    test_loss, test_acc = model.evaluate(x_test, y_test, verbose=1)
    print("Test accuracy: ", test_acc)


    #SAVING MODEL
    #save model
    model_filename = "ANN_" + filename[:-4]
    save_NN(model, model_filename)

    #save normalization parameters
    norm_filename = "ANN_norm_param_" + filename[:-4]
    save_object(norm_param, norm_filename)


    #LOADING MODEL
    #load model
    loaded_model = load_model(model_filename)

    #load normalization parameters
    loaded_norm_param = load_object(norm_filename)


    #TESTING
    test_model(loaded_model, x_test, y_test)
    #y_pred = model.predict(x_test)


if __name__ == "__main__":
    #file = "../data/404_data/coady_power_3_ratios_test.csv"
    #file = "../data/404_data/coady_power_15_ratios_test.csv"
    filedir = "../data/403_data/processed/"
    filename = "PS_w1280a100.csv"
    ANN(filedir, filename)


def test():
    print("Successfully imported ANN")