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
from collections import deque

#memory usage grows as model needs
gpus = tf.config.experimental.list_physical_devices('GPU')
if gpus:
  try:
    for gpu in gpus:
      tf.config.experimental.set_memory_growth(gpu, True)
  except RuntimeError as e:
    print("Error: " + e)

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
    
    data = data.dropna(axis='rows') #changed from columns to rows to just delete samples instead of entire features
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


#create sequences of data for CNN
def create_sequences(df: pd.DataFrame, seq_len: int, features_per_electrode: int, timestamps: bool, balance: bool=True):
    sequence_data = []  #list of sequences -> [sequence, label]
    single_seq = deque(maxlen=seq_len)

    prev_label = df["drowsy"].values[0] #should be 0
    prev_time = 0
    idx_start = 0
    if timestamps:
        prev_time = df["timestamps"].values[0]
        idx_start = 1
    for sample in df.values:
        if sample[-1] != prev_label or (timestamps and sample[0] < prev_time):
            single_seq.clear()
        
        #convert 1D feature vector into 2D electrode-feature vectors
        features_2D = []
        all_features = sample[idx_start:-1]
        electrode_features = []
        for feature in all_features:
            electrode_features.append(feature)
            if len(electrode_features) == features_per_electrode:
                features_2D.append(np.array(electrode_features))
                electrode_features.clear()

        single_seq.append(features_2D)
        if len(single_seq) == seq_len:
            sequence_data.append([np.array(single_seq), sample[-1]])
            # if balance:
            #     for i in range(int(seq_len)):
            #         single_seq.popleft()
        prev_label = sample[-1]
        prev_time = sample[0]
    print("Number of sequences: ", len(sequence_data))

    sequences = []

    if balance:
        #balance awake and drowsy data
        random.shuffle(sequence_data)
        awake = []
        drowsy = []
        for seq, label in sequence_data:
            if (label == 0):
                awake.append([seq, label])
            elif (label == 1):
                drowsy.append([seq, label])
        
        lower = min(len(awake), len(drowsy))
        awake = awake[:lower]
        drowsy = drowsy[:lower]
        print("Number of awake/drowsy sequences each: ", lower)

        #create x and y lists
        sequences = awake + drowsy
        random.shuffle(sequences)
    else:
        sequences = sequence_data

    x = []
    y = []
    for seq, label in sequences:
        x.append(seq)
        y.append(label)
    
    return np.array(x), np.array(y)

#use model to predict value for new data
#x_data is in format [[column names], [values], [values], ...]
#x_data should only have 2 lists, 1 for column names, 1 for 1 set of values
def model_predict(model, norm_param, data, seq_len):
	#convert data into DataFrame
	columns = data[0]
	x_data = data[1:(seq_len + 1)]
	df = pd.DataFrame(x_data, columns=columns)


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


def CNN(filedir: str, training_filename: str, seq_len: int, features_per_electrode: int, testing_file: str=None):
    training_file = filedir + training_filename
    data = pd.read_csv(training_file)
    data_len = data.shape[0]
    print("Number of training data samples:", data_len)

    testing_data = None
    if testing_file is not None:
        testing_data = pd.read_csv(testing_file)
        print("Number of testing data samples:", testing_data.shape[0])
        data = data.append(testing_data, ignore_index=True)
        print("Number of total data samples:", data.shape[0])
    
    data, norm_param = preprocess_data(data, True, False)
    print("Total_data shape after preprocessing:", data.shape)

    n_classes = len(np.unique(data[data.columns[-1]]))
    n_features = len(data.columns) - 1
    print("\nNumber of classes:", n_classes)
    print("Number of features:", n_features)
    
    if testing_file is not None:
        testing_data = data.iloc[data_len:, :]
    data = data.iloc[:data_len, :]
    print("\nTraining_data shape:", data.shape)

    data_x, data_y = create_sequences(data, seq_len, features_per_electrode, True)
    input_shape = data_x.shape[1:]
    print("Input shape:", input_shape)

    #60% training, 20% validation, 20% testing
    x_train, x_test, y_train, y_test = train_test_split(data_x, data_y, test_size=0.4, random_state=17)
    x_test, x_val, y_test, y_val = train_test_split(x_test, y_test, test_size=0.5, random_state=17)

    model = keras.Sequential([
        keras.layers.Conv2D(filters=64, kernel_size=(2, 2), activation='relu', input_shape=input_shape),
        keras.layers.Conv2D(filters=32, kernel_size=(2, 2), activation='relu'),
        keras.layers.Dropout(0.2),
        keras.layers.MaxPooling2D(pool_size=2),

        #keras.layers.Conv1D(filters=32, kernel_size=3, activation='relu'),
        #keras.layers.MaxPooling1D(pool_size=2),
        #keras.layers.Dropout(0.2),

        keras.layers.Flatten(),
        keras.layers.Dense(int(n_features / 2) + 1, activation='relu'),  # hidden layer (3/-2)
        keras.layers.Dropout(0.2),
        keras.layers.Dense(1, activation='sigmoid') # output layer (5)
    ])

    model.compile(optimizer='adam',
                loss='binary_crossentropy',
                metrics=['accuracy'])
    
    earlystopping = keras.callbacks.EarlyStopping(monitor ='val_loss', 
                                              mode ='min', patience = 5,
                                              restore_best_weights = True)


    #TRAINING
    model.fit(x_train, y_train, 
            epochs=50, 
            batch_size=32,
            validation_data = (x_val, y_val)
            , callbacks = [earlystopping]
            )
    
    #TESTING
    #test_loss, test_acc = model.evaluate(x_test, y_test, verbose=1)
    #print("Test accuracy: ", test_acc)
    test_model(model, x_test, y_test)
    
    if testing_file is not None:
        x_new_test, y_new_test = create_sequences(testing_data, seq_len, features_per_electrode, True, False)
        test_model(model, x_new_test, y_new_test)


if __name__ == "__main__":
    filedir = "../data/combined/processed/"
    try:
        CNN(filedir, "PS_w1280a1280.csv", seq_len=12, features_per_electrode=15, testing_file="../data/combined/raw/storage/processed/PS_w1280a1280.csv")
    except Exception as e:
        print("Error: ", e)
    input("Press enter to exit:")


def test():
    print("Successfully imported CNN-2D")