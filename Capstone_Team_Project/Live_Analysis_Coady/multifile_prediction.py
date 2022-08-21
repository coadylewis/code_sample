import subprocess
from time import time
from output_trimmer import output_trimmer
from live_analysis import eeg_live_analysis_from_updating_file
from os import walk
import sys
sys.path.append("..")
import ML_Models.RCNN as RCNN
import ML_Models.RNN as RNN
import pandas as pd
import numpy as np
from collections import deque
import csv

def multifile_live_analysis():
    filedir = "../data/long_session/Ali/"
    raw_files = []
    for (dirpath, dirnames, filenames) in walk(filedir):
        raw_files = filenames

        #remove non-".csv" files
        for file in raw_files:
            #print(file[-3:])
            if file[-3:] != "csv":
                raw_files.remove(file)
        break

    print("Raw EEG Files:")
    for file in raw_files:
        print(" - " + file)
    print("")

    normalize_to_highest_band = False
    #model = "PS_w1280a1280" 
    model = "PS_w1280a1280_ratio_offset320combined_orig"
    seq_len = 12

    for file in raw_files:
        print("Processing " + file + "...")

        print("Starting muse writing process...")
        muse_writing = subprocess.Popen([sys.executable, "test_live_analysis.py", filedir + file, "15"])
        #muse_writing = Process(target=test_single_file, args=(filedir + raw_files[0], True))
        #muse_writing.start()

        print("Starting live analysis...")
        eeg_live_analysis_from_updating_file("live_analysis_testcase.csv", normalize_to_highest_band, model_filename=model, seq_len=seq_len, duration=80)
        muse_writing.terminate()

        #muse_writing.join()
    output_trimmer("Outputs/RCNN_" + model + "_L1Ali_output.csv")


def multifile_processed(ML_module, model_filename: str, seq_len: int, testing_file: str, output_filename: str, write=False):
    full_output_filepath = "Outputs/" + ML_module.get_name() + "s" + str(seq_len) + "_" + model_filename + "_" + output_filename

    print("Model: %s" % (ML_module.get_name() + "s" + str(seq_len) + "_" + model_filename))
    print("Testing file: %s\n" % testing_file)

    data = pd.read_csv(testing_file)
    model = ML_module.load_model(ML_module.get_name() + "s" + str(seq_len) + '_'+ model_filename + '.h5')
    norm_param = ML_module.load_object(ML_module.get_name() + "s" + str(seq_len) + '_norm_param_'+ model_filename)

    single_seq = deque(maxlen=seq_len)
    columns = np.array(data.columns[:-1])
    num_rows = data.shape[0]
    vector_data = None
    prev_timestamp = 0
    num_awake = 0
    num_drowsy = 0
    num_outputs = 0
    section = 1
    row_idx = 0

    print('\n')
    for row in data.values:
        timestamp = row[0]
        if timestamp < prev_timestamp or row_idx == num_rows - 1:
            single_seq.clear()
            print("SECTION: %d" % section)
            print(" - Awake Fraction: %.3f" % (num_awake / num_outputs))
            print(" - Drowsy Fraction: %.3f\n" % (num_drowsy / num_outputs))
            num_awake = 0
            num_drowsy = 0
            num_outputs = 0
            section += 1
        
        single_seq.append(np.array(row[:-1]))
        if len(single_seq) == seq_len:
            vector_data = [columns, np.array(single_seq)]
            y_pred_orig = ML_module.model_predict(model, norm_param, vector_data, seq_len)[0][0]
            y_pred = y_pred_orig > 0.5
            if y_pred == 1:
                num_drowsy += 1
            else:
                num_awake += 1
            num_outputs += 1
            if write:
                with open(full_output_filepath, 'a+', newline='') as f:
                    writer = csv.writer(f)
                    if f.tell() == 0: 	#file newly created
                        writer.writerow(["classification", "true_output", "binary_output"])	#append header
                    new_row = [num_outputs, y_pred_orig, int(y_pred)]
                    writer.writerow(new_row)
                    f.close()
        prev_timestamp = timestamp
        row_idx += 1

    if write:
        print("Classification outputs written to:", full_output_filepath)
        print("Trimming...")
        output_trimmer(full_output_filepath)
        print("done")


if __name__ == "__main__":
    ML_module = RCNN
    model_filename = "PS_w1280a1280"
    seq_len = 12
    testing_file = "../data/long_session/Coady/processed/PS_w1280a1280.csv"
    output_filename = "L1Coady_output.csv"
    try:
        #multifile_live_analysis()
        multifile_processed(ML_module, model_filename, seq_len, testing_file, output_filename)
    except Exception as e:
        print("Error:", e)
    input("Press enter to exit:")