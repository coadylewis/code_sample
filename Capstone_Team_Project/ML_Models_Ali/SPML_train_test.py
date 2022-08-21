#integration of Signal Processor (Coady Lewis) and ML Models (Ali Imran)

#import programs
import ML_Models.ANN as ANN
import ML_Models.KSVM as KSVM
import Signal_Processing.raw_conversion_overlap_tab_ratios as SP

from os import walk
import time

#process all raw EEG files within the specified directory
def SP_all(file_dir, window, advance):
    raw_files = []
    num_awake = 0
    num_drowsy = 0

    #system goes inside directory and walks through each object
    for (dirpath, dirnames, filenames) in walk(file_dir):
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

    all_output = []
    for i in range(13):
        all_output.append([])

    #process each raw EEG file, add labels, and combine into single output
    first_file_processed = False
    for file in raw_files:
        print("Processing " + file + "...")
        file_path = file_dir + file
        output = SP.convert_raw_to_n_ratio_bandpower(file_path, window, advance, False)

        #adding labels depending on name of file
        if "awake" in file:
            label_list = ['drowsy'] + [0] * (len(output[0]) - 1)
            output.append(label_list)
            num_awake += 1
        elif "drowsy" in file:
            label_list = ['drowsy'] + [1] * (len(output[0]) - 1)
            output.append(label_list)
            num_drowsy += 1
        
        #all_output gets extended when the first file has been processed
        if first_file_processed:
            for i in range(len(output)):
                #remove column names when adding data
                all_output[i].extend(output[i][1:])
        else:
            first_file_processed = True
            all_output = output
        print("done")
    
    ps_filename = "PS_w" + str(window) + "a" + str(advance) + ".csv"
    ps_filepath = file_dir + "../processed/" + ps_filename
    print("Writing processed signal file to " + ps_filepath)
    SP.muse_writefile(ps_filepath, all_output)

    #write file info in same directory
    ps_info_filepath = ps_filepath[:-4] + "_info.txt"
    f = open(ps_info_filepath, "w")
    f.write("Raw EEG Files:\n")
    for file in raw_files:
        f.write(" - " + file + "\n")
    f.write("Number of awake: " + str(num_awake) + "\n")
    f.write("Number of drowsy: " + str(num_drowsy) + "\n")
    f.close()

    return ps_filepath


def automated_testing():
    windows = [2560,1920,1280,640]
    advancements = [2560,1920,1280,640,320]
    for win in windows:
        for adv in advancements:
            start = time.time()
            if (win<adv):
                continue
            paths = SP_all(file_dir,win,adv)
            KSVM.KSVM(paths[0], paths[1],win,adv)
            with open("train_test_results.txt", 'a') as f:
                f.write('Full Computation Time = '+str(time.time()-start)+'\n\n\n')


if __name__ == "__main__":
    ANN.test()
    KSVM.test()
    SP.test()
    #file_dir = "data/combined/raw/storage/raw/"
    file_dir = "data/long_session/Coady/raw/"
    ps_filepath = SP_all(file_dir, 1280, 1280)