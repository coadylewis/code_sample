import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import tensorflow as tf
import time
import random
import pickle

from tensorflow.keras import Sequential, callbacks, models
from tensorflow.keras.layers import Dense, Dropout, Conv2D, MaxPooling2D, Flatten, LSTM, TimeDistributed, Input, BatchNormalization, Activation
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
LOG_DIR = f"RNN_hp/{int(time.time())}"
SEED = 17

### FUNCTIONS ###
def get_name():
    return "RNN"

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
    # needs modification for continuous
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
    y_pred = (y_pred > 0.5) # Need to comment out for continuous
    
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


#create sequences of data for RNN
def create_sequences(df: pd.DataFrame, seq_len: int, timestamps: bool, balance: bool=True):
    random.seed(SEED)
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
        single_seq.append(sample[idx_start:-1])
        if len(single_seq) == seq_len:
            sequence_data.append([np.array(single_seq), sample[-1]])
            if balance:
                for i in range(int(seq_len / 2)):
                    single_seq.popleft()
                #single_seq.clear()
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
#x_data should have 1 + seq_len lists, 1 for column names, seq_len for sequential set of values
def model_predict(model, norm_param, data, seq_len):
    #error-checking
    if len(data[1]) != seq_len:
        print("Error: data of sequence size %d entered, expected size %d", len(data[1]), seq_len)
        return

	#convert data into DataFrame
    columns = data[0]
    x_data = data[1]
    df = pd.DataFrame(x_data, columns=columns)

	#PREPROCESSING
	#removing timestamps
    df.drop(columns=df.columns[0], axis=1, inplace=True)

	#normalization
    for col in df.columns:
        min = norm_param[col][0]
        max = norm_param[col][1]
        df[col] = (df[col] - min) / (max - min)
    
    #reshape into (1, seq_len, 60)
    data_np = df.to_numpy()
    #print(data_np.shape)
    data_np = data_np.reshape(1, seq_len, 60)
    #print(data_np.shape)

    #PREDICTION
    #predict with trained model
    #input shape: (seq_len, 60)
    y_pred = model.predict(data_np)
    #print(y_pred)
    output = "drowsy" if y_pred >= 0.5 else "awake"
    #print(output)
    return y_pred


def build_model(hp):
    model = Sequential()
    #Input
    model.add(Input(shape=(12, 60)))

    #LSTM Layers
    model.add(LSTM(units=hp.Int("LSTM0_units", 16, 256, 16), activation='tanh', return_sequences=True)) # input LSTM layer (1)
    model.add(Dropout(0.2))
    model.add(LSTM(units=hp.Int("LSTM1_units", 16, 256, 16), activation='tanh')) # hidden LSTM layer (2)
    model.add(Dropout(0.2))

    #Dense Layers
    model.add(Dense(units=hp.Int("dense_units", 16, 256, 16), activation='relu'))  # hidden layer (3)
    model.add(Dropout(0.2))
    model.add(Dense(1, activation='sigmoid')) # output layer (4)

    model.compile(optimizer='adam',
            loss='binary_crossentropy',
            metrics=['accuracy'])
    
    return model

#best so far: 32 -> 48 -> 96
def RNN_hp(filedir: str, training_filename: str, testing_file: str=None, seq_len: int=5, features_per_electrode=15):
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
    print("Input shape:", input_shape) #should be seq_len, 60

    #60% training, 20% validation, 20% testing
    x_train, x_test, y_train, y_test = train_test_split(data_x, data_y, test_size=0.4, random_state=SEED)
    x_test, x_val, y_test, y_val = train_test_split(x_test, y_test, test_size=0.5, random_state=SEED)

    tuner = Hyperband(
        build_model,
        objective = "val_accuracy",
        max_epochs = 30,
        directory = LOG_DIR)

    earlystopping = callbacks.EarlyStopping(monitor ='val_loss', 
                                        mode ='min', patience = 5,
                                        restore_best_weights = True)
    
    tuner.search(x=x_train, y=y_train, 
        epochs=30, batch_size=32, validation_data=(x_val, y_val), callbacks=[earlystopping])
    
    with open(f"tuner_{int(time.time())}.pkl", "wb") as f:
        pickle.dump(tuner, f)
    
    print(tuner.get_best_hyperparameters()[0].values)
    print(tuner.results_summary())


def y_reshape(y, sequence_timesteps): # makes sequence label equal to the mean of the individual labels
    # takes in a pd dataframe, returns a np array
    output_y = []
    for i in range(y.shape[0]//sequence_timesteps):
        output_y.append(round(y.iloc[i*sequence_timesteps:(i+1)*sequence_timesteps].mean()))
    return np.array(output_y)


#takes aggregate labeled processed data, preprocesses it, splits it into training
# and testing set, trains the model, then tests the model
def RNN(filedir, training_filename, testing_file, sequence_timesteps):
    training_file = filedir + training_filename
    testing_file = filedir + testing_filename
    train = pd.read_csv(training_file)
    test= pd.read_csv(testing_file)
    train, norm_param = preprocess_data(train, True, False)
    
    #PREPROCESSING TEST DATA***********************
    #removing timestamps
    #test.drop("timestamps", axis=1, inplace=True)
    #drop NaN
    test = test.dropna(axis='columns')
    #normalization
    for col in test.columns:
        min = norm_param[col][0]
        max = norm_param[col][1]
        test[col] = (test[col] - min) / (max - min)
    #**********************************************

    n_classes = len(np.unique(train[train.columns[-1]]))
    n_features = len(train.columns) - 1
    print("Number of classes: ", n_classes)
    print("Number of features: ", n_features)

    x_train = train.iloc[:,:-1] # all rows, columns up until last(target)
    y_train = train.iloc[:, -1] # all rows, only target column
    x_test_full = test.iloc[:, :-1]
    y_test_full = test.iloc[:, -1]

    # Reshape dataframes into numpy arrays with dim [sample][timestep][feature]
    num_train_samples = x_train.shape[0]//sequence_timesteps # integer division, so
    num_test_samples = x_test_full.shape[0]//sequence_timesteps # drop extras that don't make a full sequence
    x_train = x_train.iloc[:num_train_samples*sequence_timesteps,:].to_numpy().reshape(num_train_samples,sequence_timesteps,n_features)
    x_test_full = x_test_full.iloc[:num_test_samples*sequence_timesteps,:].to_numpy().reshape(num_test_samples,sequence_timesteps,n_features)
    y_train = y_reshape(y_train, sequence_timesteps)
    y_test_full = y_reshape(y_test_full, sequence_timesteps)


    #RECURRENT NEURAL NETWORK ARCHITECTURE
    #hidden layers in a pyramid fashion, less neurons at the outer layers
    #regularization: kernel_regularizer=keras.regularizers.l2(0.01)
    #hidden layer activation: relu(o), sigmoid, tanh
    #output layer activation: linear, sigmoid, softmax(o)
    #node about input:
    # - input should be such that x_train[0].shape is a 2D-list
    # - 2D list should look like the following:
        # t1: f1 f2 ... fn
        # t2: f1 f2 ... fn
        # ... .. .. ... ..
        # tn: f1 f2 ... fn
    # - f represents feature with fn # of featuress
    # - t represents sequential data with tn # of sequential data points
    # - t itself is not a feature, so x_train[0].shape should be (fn, tn), not (fn + 1, tn)
    model = keras.Sequential([
        keras.layers.CuDNNLSTM(128, input_shape=(sequence_timesteps,n_features), return_sequences=True), # input LSTM layer (1)
        keras.layers.Dropout(0.2),
        keras.layers.CuDNNLSTM(128), # hidden LSTM layer (2)
        keras.layers.Dropout(0.2),
        #keras.layers.Dense(n_features + 1, input_dim=n_features),  # input layer (-1)
        keras.layers.Dense(int(n_features / 2) + 1, activation='relu'),  # hidden layer (3/-2)
        keras.layers.Dropout(0.2),
        #keras.layers.Dense(int(n_features / 4) + 1, activation='relu'), # hidden layer (-3)
        #keras.layers.Dropout(0.2),
        #keras.layers.Dense(32, activation='relu', kernel_regularizer=keras.regularizers.l2(0.001)), # hidden layer (4)
        #keras.layers.Dropout(0.2),
        keras.layers.Dense(1, activation='sigmoid') # output layer (5)
    ])

    model.compile(optimizer='adam',
                loss='binary_crossentropy',
                metrics=['accuracy'])
    
    earlystopping = keras.callbacks.EarlyStopping(monitor ='val_loss', 
                                              mode ='min', patience = 5,
                                              restore_best_weights = True)

    partition = int(x_test_full.shape[0]/2)
    print(partition)
    x_val = x_test_full[:partition]
    y_val = y_test_full[:partition]

    x_test = x_test_full[partition:]
    y_test = y_test_full[partition:]


    #TRAINING
    model.fit(x_train, y_train, 
            epochs=30, 
            # batch_size=32,
            validation_data = (x_val, y_val)
            #, callbacks = [earlystopping]
            )
    
    test_loss, test_acc = model.evaluate(x_test, y_test, verbose=1)
    print("\n\nTest accuracy: ", test_acc)


    #SAVING MODEL
    #save model
    model_filename = "RNN_" + training_filename[:-4]
    save_NN(model, model_filename+'.h5')

    #save normalization parameters
    norm_filename = "RNN_norm_param_" + training_filename[:-4]
    save_object(norm_param, norm_filename)


    #LOADING MODEL
    #load model
    loaded_model = load_model(model_filename+'.h5')

    #load normalization parameters
    loaded_norm_param = load_object(norm_filename)


    #TESTING
    test_model(loaded_model, x_test, y_test)
    # continuous not supported error
    # test_model(model, x_test, y_test)
    #y_pred = model.predict(x_test)


def RNN_new(filedir: str, training_filename: str, testing_file: str=None, seq_len: int=5, save_model=False, file_append=""):
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

    data_x, data_y = create_sequences(data, seq_len, True)
    input_shape = data_x.shape[1:]
    print("Input shape:", input_shape)

    #60% training, 20% validation, 20% testing
    x_train, x_test, y_train, y_test = train_test_split(data_x, data_y, test_size=0.4, random_state=17)
    x_test, x_val, y_test, y_val = train_test_split(x_test, y_test, test_size=0.5, random_state=17)

    model = Sequential([
        LSTM(160, input_shape=input_shape, activation='tanh', return_sequences=True), # input LSTM layer (1)
        Dropout(0.2),
        LSTM(96, activation='tanh'), # hidden LSTM layer (2)
        Dropout(0.2),
        #keras.layers.Dense(n_features + 1, input_dim=n_features),  # input layer (-1)
        Dense(240, activation='relu'),  # hidden layer (3/-2)
        Dropout(0.2),
        #Dense(int(n_features / 4) + 1, activation='relu'), # hidden layer (-3)
        Dropout(0.2),
        #keras.layers.Dense(32, activation='relu', kernel_regularizer=keras.regularizers.l2(0.001)), # hidden layer (4)
        #keras.layers.Dropout(0.2),
        Dense(1, activation='sigmoid') # output layer (5)
    ])

    model.compile(optimizer='adam',
                loss='binary_crossentropy',
                metrics=['accuracy'])
    
    print(model.summary())
    
    earlystopping = callbacks.EarlyStopping(monitor ='val_loss', 
                                            mode ='min', patience = 5,
                                            restore_best_weights = True)


    #TRAINING
    model.fit(x_train, y_train, 
            epochs=50, 
            batch_size=32,
            validation_data = (x_val, y_val),
            callbacks = [earlystopping]
            )
    
    #TESTING
    #test_loss, test_acc = model.evaluate(x_test, y_test, verbose=1)
    #print("Test accuracy: ", test_acc)
    test_model(model, x_test, y_test)
    
    if testing_file is not None:
        x_new_test, y_new_test = create_sequences(testing_data, seq_len, True, False)
        test_model(model, x_new_test, y_new_test)

    if save_model:
        #SAVING MODEL
        #save model
        model_filename = "RNNs" + str(seq_len) + "_" + training_filename[:-4] + file_append
        print("Saving model to:", model_filename)
        save_NN(model, model_filename)

        #save normalization parameters
        norm_filename = "RNNs" + str(seq_len) + "_norm_param_" + training_filename[:-4] + file_append
        print("Saving normalization parameters to:", norm_filename)
        save_object(norm_param, norm_filename)


if __name__ == "__main__":
    #file = "../data/404_data/coady_power_3_ratios_test.csv"
    #file = "../data/404_data/coady_power_15_ratios_test.csv"
    filedir = "../data/403_data/processed/"
    # split_file = True
    # if(not split_file):
    train_filename = "256_256_normal_30_10_6_4_training_seq.csv"
    test_filename = "256_256_normal_30_10_6_4_testing_seq.csv"
    # else:
    # train_filename = "test1_training_seq.csv"
    # test_filename = "test1_testing_seq.csv"       

    RNN(filedir, train_filename, test_filename, 10)


def test():
    print("Successfully imported RNN")