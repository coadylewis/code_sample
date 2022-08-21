from msilib import sequence
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import tensorflow as tf
import time
import random
import pickle

from tensorflow.keras import Sequential, callbacks, models
from tensorflow.keras.layers import Dense, Dropout, Conv2D, MaxPooling2D, AveragePooling2D, Flatten, LSTM, TimeDistributed, Input, BatchNormalization, Activation
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.optimizers.schedules import ExponentialDecay
from scipy import stats
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, f1_score
from collections import deque

#default to CPU usage
#import os
#os.environ['CUDA_VISIBLE_DEVICES'] = '-1'

import os
os.environ['TF_FORCE_GPU_ALLOW_GROWTH'] = 'true'

#memory usage grows as model needs
gpus = tf.config.experimental.list_physical_devices('GPU')
if gpus:
  try:
    for gpu in gpus:
      tf.config.experimental.set_memory_growth(gpu, True)
  except RuntimeError as e:
    print("Error: " + e)

model_filedir = "../ML_Models/trained_models/"
LOG_DIR = f"RCNN_hp/{int(time.time())}"
SEED = 17

### FUNCTIONS ###
def get_name():
    return "RCNN"

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
    filepath = model_filedir + filename + ".h5"
    model.save(filepath)


#load Neural Network
def load_model(filename):
    filepath = model_filedir + filename
    return models.load_model(filepath)


#save object for later use
# - normalizaton parameters
def save_object(object, filename):
	filepath = model_filedir + filename
	pickle.dump(object, open(filepath, 'wb'))


#load saved object
def load_object(filename):
	obj_filepath = model_filedir + filename
	return pickle.load(open(obj_filepath, 'rb'))


#electrodes are TP9, AF7, AF8, TP10
#convolutional comparisons are made across TP9-AF7, AF7-AF8, AF8-TP10
#need comparison across TP10-TP9, so append TP9 to the end of the electrode dimension
def append_TP9_electrode(data: np.array):
    #data should be in shape (seq, electrode, feature, 1) (seq_len, 4, 15, 1)
    seq_len = data.shape[0]
    n_electrodes = data.shape[1]
    n_features_per_electrode = data.shape[2]
    data_appended = np.empty([seq_len, n_electrodes + 1, n_features_per_electrode, 1])
    for i in range(seq_len):
        sample = data[i]
        electrode_TP9 = sample[0].reshape(1, n_features_per_electrode, 1)
        #print(seq.shape) #expecting (4, 15, 1)
        #print(electrode.shape)
        data_appended[i] = np.append(sample, electrode_TP9, axis=0)
        #print(data_appended[i].shape) #expecting (5, 15, 1)
    #print("\nAPPENDED DATA")
    #print(data_appended)
    return data_appended


#create sequences of data for RNN
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
            electrode_features.append([feature])
            if len(electrode_features) == features_per_electrode:
                features_2D.append(np.array(electrode_features))
                electrode_features.clear()

        single_seq.append(features_2D)
        if len(single_seq) == seq_len:
            #appended_TP9_seq = append_TP9_electrode(np.array(single_seq))
            #sequence_data.append([appended_TP9_seq, sample[-1]])
            sequence_data.append([np.array(single_seq), sample[-1]])
            if balance:
                for i in range(int(seq_len / 2)):
                    single_seq.popleft()
            # if balance:
            #     single_seq.clear()
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
#x_data is in format [[column names], [[values], [values], ...]]
#x_data should have 1 + [seq_len] lists, 1 for column names, [seq_len] for sequential set of values
def model_predict(model, norm_param, data, seq_len):
    #error-checking
    if len(data[1]) != seq_len:
        print("Error: data of sequence size %d entered, expected size %d", len(data[1]), seq_len)
        return

	#convert data into DataFrame
    columns = data[0]
    x_data = data[1]
    df = pd.DataFrame(x_data, columns=columns)

    #print(df.head(3))


	#PREPROCESSING
	#removing timestamps
    df.drop(columns=df.columns[0], axis=1, inplace=True)

	#normalization
    for col in df.columns:
        min = norm_param[col][0]
        max = norm_param[col][1]
        df[col] = (df[col] - min) / (max - min)
    
    #df.add(df.columns[1])
    

    #reshape into (seq_len, 4, 15, 1)
    data_np = df.to_numpy()
    #print(data_np.shape)
    data_np = data_np.reshape(1, seq_len, 4, 15, 1)
    #print(data_np.shape)

    #PREDICTION
    #predict with trained model
    #input shape: (seq_len, 4, 15, 1)
    y_pred = model.predict(data_np)
    #print(y_pred)
    output = "drowsy" if y_pred >= 0.5 else "awake"
    #print(output)
    return y_pred


def build_model(hp):
    model = Sequential()
    model.add(Input(shape=(12, 4, 15, 1)))

    #2D CNN Layers
    model.add(TimeDistributed(Conv2D(filters=hp.Int("C0_filters", 16, 128, 16), kernel_size=(2, 2), activation='relu')))
    model.add(TimeDistributed(Conv2D(filters=hp.Int("C1_filters", 16, 128, 16), kernel_size=(2, 2), activation='relu')))
    model.add(TimeDistributed(Dropout(0.2)))
    
    model.add(TimeDistributed(MaxPooling2D(pool_size=2)))
    model.add(TimeDistributed(Flatten()))

    #LSTM Layers
    model.add(LSTM(160, activation='tanh', return_sequences=True)) # input LSTM layer (1)
    model.add(Dropout(0.2))
    model.add(LSTM(96, activation='tanh')) # hidden LSTM layer (2)
    model.add(Dropout(0.2))
    model.add(Dense(units=240, activation='relu'))  # hidden layer (3/-2)
    model.add(Dropout(0.2))
    model.add(Dense(1, activation='sigmoid')) # output layer (5)

    model.compile(optimizer='adam',
            loss='binary_crossentropy',
            metrics=['accuracy'])
    
    return model

#best so far: 32 -> 48 -> 96
def RCNN_hp(filedir: str, training_filename: str, testing_file: str=None, seq_len: int=5, features_per_electrode=15):
    from kerastuner.tuners import RandomSearch, Hyperband
    from kerastuner.engine.hyperparameters import HyperParameters

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
    print("Input shape:", input_shape) #should be seq_len, 4, 15

    #60% training, 20% validation, 20% testing
    x_train, x_test, y_train, y_test = train_test_split(data_x, data_y, test_size=0.4, random_state=SEED)
    x_test, x_val, y_test, y_val = train_test_split(x_test, y_test, test_size=0.5, random_state=SEED)

    tuner = Hyperband(
        build_model,
        objective = "val_accuracy",
        max_epochs = 40,
        directory = LOG_DIR)

    earlystopping = callbacks.EarlyStopping(monitor ='val_loss', 
                                        mode ='min', patience = 5,
                                        restore_best_weights = True)
    
    tuner.search(x=x_train, y=y_train, 
        epochs=30, batch_size=16, validation_data=(x_val, y_val), callbacks=[earlystopping])
    
    with open(f"tuner_{int(time.time())}.pkl", "wb") as f:
        pickle.dump(tuner, f)
    
    print(tuner.get_best_hyperparameters()[0].values)
    print(tuner.results_summary())



def RCNN(filedir: str, training_filename: str, testing_file: str=None, seq_len: int=5, features_per_electrode=15, save_model=False, file_append = ""):
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
    print("Input shape:", input_shape) #should be seq_len, 4, 15

    #60% training, 20% validation, 20% testing
    x_train, x_test, y_train, y_test = train_test_split(data_x, data_y, test_size=0.4, random_state=17)
    x_test, x_val, y_test, y_val = train_test_split(x_test, y_test, test_size=0.5, random_state=17)

    model = Sequential([
        Input(shape=(seq_len, 4, 15, 1)), 

        #2D CNN Layers
        TimeDistributed(Conv2D(filters=64, kernel_size=(2, 2), activation='relu')), # input Conv layer (1)
        TimeDistributed(Conv2D(filters=32, kernel_size=(2, 2), activation='relu')), # hidden Conv layer (2)
        TimeDistributed(Dropout(0.2)), 

        TimeDistributed(MaxPooling2D(pool_size=(2, 2))),
        TimeDistributed(Flatten()),

        #LSTM Layers
        LSTM(128, activation='tanh', return_sequences=True), # hidden LSTM layer (3)
        Dropout(0.2),
        LSTM(128, activation='tanh'), # hidden LSTM layer (4)
        Dropout(0.2),
        Dense(31, activation='relu'),  # hidden layer (5)
        Dropout(0.2),
        #Dense(32, activation='relu'),  # hidden layer
        #Dropout(0.2),
        Dense(1, activation='sigmoid') # output layer (6)
    ])

    print(model.summary())

    #learning rate with exponential decay
    #lr_decay = ExponentialDecay(0.9, 10000, 0.9)
    #opt = Adam(learning_rate = lr_decay)

    model.compile(optimizer='adam',
                loss='binary_crossentropy',
                metrics=['accuracy'])
    
    earlystopping = callbacks.EarlyStopping(monitor ='val_loss', 
                                            mode ='min', patience = 5,
                                            restore_best_weights = True)


    #TRAINING
    model.fit(x_train, y_train, 
            epochs=50, 
            batch_size=16,
            validation_data = (x_val, y_val),
            callbacks = [earlystopping]
            )
    
    #TESTING
    #test_loss, test_acc = model.evaluate(x_test, y_test, verbose=1)
    #print("Test accuracy: ", test_acc)
    test_model(model, x_test, y_test)
    
    if testing_file is not None:
        x_new_test, y_new_test = create_sequences(testing_data, seq_len, features_per_electrode, timestamps=True, balance=False)
        test_model(model, x_new_test, y_new_test)
    

    if save_model:
        #SAVING MODEL
        #save model
        model_filename = "RCNNs" + str(seq_len) + "_" + training_filename[:-4] + file_append
        print("Saving model to:", model_filename)
        save_NN(model, model_filename)

        #save normalization parameters
        norm_filename = "RCNNs" + str(seq_len) + "_norm_param_" + training_filename[:-4] + file_append
        print("Saving normalization parameters to:", norm_filename)
        save_object(norm_param, norm_filename)


if __name__ == "__main__":
    random.seed(SEED)
    filedir = "../data/combined/processed/"
    filename = "PS_w1280a1280_extra.csv"
    #testing_file="../data/combined/raw/storage/processed/PS_w1280a1280.csv", 
    try:
        RCNN(filedir, filename, seq_len=12, save_model=True)
        #RCNN_hp(filedir, "PS_w1280a1280.csv", seq_len=12)
    except Exception as e:
        print("Error: ", e)
    input("Press enter to exit:")


def test():
    print("Successfully imported RCNN")