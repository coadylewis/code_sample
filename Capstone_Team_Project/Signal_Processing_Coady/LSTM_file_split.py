import Signal_Processing.raw_conversion_overlap_tab_ratios as SP
import time
from SPML_train_test import SP_all
from os.path import exists
import random,csv,time
import matplotlib.pyplot as plt



def readfile(fn): #reads csv data in feature format
    # file vars
    file = [] # no shorthand, memory assignment issue
    filename = fn


    # store file data in 2d list file[tag_index][n] where n is the data point
    with open(filename) as csvfile:
        dataset = csv.reader(csvfile)
        hold = True
        for row in dataset: 
            if(hold):       
                for element in row:
                    file.append([element])
            else:
                for i in range(len(row)):
                    # if calling row[i] gives an out-of-range exception, file is not muse data
                    file[i].append(float(row[i]))
            hold = False
    return file



# Writes Data from list in the format above, 
# i.e. data must be [[header,x1,x2,...,xn],[header,x1,x2,...,xn],[header,x1,x2,...,xn],[header,x1,x2,...,xn],[header,x1,x2,...,xn]]
def muse_writefile(fn, data):
    n = len(data[0])
    with open(fn, 'w',newline='') as csvfile:
        w = csv.writer(csvfile)
        prog = 0
        print('\n\n'+fn+' Progress: ')
        for i in range(len(data[0])):
            if(prog<int(100*i/n)):
                prog = int(100*i/n)
                print(str(prog)+'%')
            row = []
            for j in range(len(data)):
                row.append(data[j][i])
            w.writerow(row)


def split_drowsy_awake(data=[]):
    headers = [col.pop(0) for col in data]
    drowsy_points=[[] for i in range(len(headers))]
    awake_points = [[] for i in range(len(headers))]
    for i in range(len(data[0])):
        if(bool(data[-1][i])): # drowsy
            for j in range(len(data)): # keep timestamps
                drowsy_points[j].append(data[j][i])
        else: # awake
            for j in range(len(data)): # keep timestamps
                awake_points[j].append(data[j][i])

    return [headers, drowsy_points, awake_points]


def generate_training_testing_sequences(output_filename='default.csv',headers=[],drowsy_points=[],awake_points=[],write=True):
    print('\n\n\n\nGenerating Sequences\n')
    training_sequence=[[header] for header in headers]
    testing_sequence=[[header] for header in headers]
    split = 0.80
    for i in range(len(drowsy_points[0])):
        if(i < int(split*len(drowsy_points[0]))): # place in training
            for j in range(len(training_sequence)):
                training_sequence[j].append(drowsy_points[j][i])
        else: # place in testing
            for j in range(len(testing_sequence)):
                testing_sequence[j].append(drowsy_points[j][i])
    for i in range(len(awake_points[0])):
        if(i < int(split*len(awake_points[0]))): # place in training
            for j in range(len(training_sequence)):
                training_sequence[j].append(awake_points[j][i])
        else: # place in testing
            for j in range(len(testing_sequence)):
                testing_sequence[j].append(awake_points[j][i])


    print('done\n\n\n')

    # save sequences
    if(write):
        print('\n\n\nWriting\n')
        muse_writefile(output_filename[:-4]+'_training_seq.csv', training_sequence)
        muse_writefile(output_filename[:-4]+'_testing_seq.csv', testing_sequence)
        print('done\n')
    return [training_sequence,testing_sequence]


if __name__ == "__main__":
    window = 1920
    advance = 100
    normalize_to_highest_band = False
    sequence_timesteps=10
    n_tag = ''
    if(normalize_to_highest_band):
        n_tag = 'normal'
    else:
        n_tag = 'ratio'



    file_dir = "data/403_data/raw/"

    if(normalize_to_highest_band):
        ps_filename = "PS_w" + str(window) + "a" + str(advance) + "_normal.csv"
    else:
        ps_filename = "PS_w" + str(window) + "a" + str(advance) + "_ratio.csv"

    ps_filepath = file_dir + "../processed/" + ps_filename

    

    if(not exists(ps_filepath)): # if data hasn't been processed yet
        print('\nprocessing data\n')
        start_pro = time.time()
        paths = SP_all(file_dir,window,advance)
        print('\ndone\n')
        print('Processing Delay: '+str(time.time()-start_pro))
        
    start_gen = time.time()
    
    data = readfile(ps_filepath)
    headers, drowsy_points, awake_points = split_drowsy_awake(data)
    outfile = 'test1.csv'
    generate_training_testing_sequences(outfile,headers,drowsy_points,awake_points,True)