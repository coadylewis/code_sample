import Signal_Processing.raw_conversion_overlap_tab_ratios as SP
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
    headers.pop(0) # don't need timestamps
    drowsy_points=[[] for i in range(len(headers))]
    awake_points = [[] for i in range(len(headers))]
    for i in range(len(data[0])):
        if(bool(data[-1][i])): # drowsy
            for j in range(1, len(data)): # drop timestamps
                drowsy_points[j-1].append(data[j][i])
        else: # awake
            for j in range(1, len(data)): # drop timestamps
                awake_points[j-1].append(data[j][i])

    return [headers, drowsy_points, awake_points]



def all_same_bool(arr):
    if(arr[0]):
        for i in range(len(arr)):
            if(not arr[i]):
                return False
        return True
    else:
        for i in range(len(arr)):
            if(arr[i]):
                return False
        return True


# 
# need to tune lambda based on both minimum_windows_before_state_change
# and num_windows_in_augmented_dataset to try to target a uniform dist
# for the state change density over many construct_drowsy_awake_list outputs
def construct_drowsy_awake_list(num_windows_in_augmented_dataset = 10, minimum_windows_before_state_change = 3, lamb = 4, iterations=1):
    print('\n\n\n\nGenerating Random Structure\n')
    full_drowsy_sequence = []
    for z in range(iterations):
        drowsy = [bool(random.randint(0,1))]
        # drowsy[i]=T gets a drowsy chunk
        # drowsy[i]=F gets an awake chunk   

        exp_var = 1
        while(exp_var >= 1 or exp_var == 0):
            exp_var = random.expovariate(lamb)

        threshold = 1-exp_var # fraction of times to hold state
        for i in range(num_windows_in_augmented_dataset - 1):
            if(len(drowsy) >= minimum_windows_before_state_change):
                if(all_same_bool(drowsy[-minimum_windows_before_state_change:])): # eligible for state change
                    # We want a state change to be less likely,
                    # otherwise there will be very few output 
                    # sequences with few state changes.
                    # 
                    # Ideally, the number of state changes should
                    # be uniformly distributed for many outputs.
                    # 
                    # This can be tested for various lambda 
                    # with plot_state_change_density()
                    # but perfectly uniform is impossible
                    # with this setup.
                    # 
                    #
                    hold_state = (random.random() < threshold)
                    if(hold_state): # hold state
                        drowsy.append(drowsy[i])
                    else: # change state
                        drowsy.append(not drowsy[i])
                else:
                    drowsy.append(drowsy[i])

            else: # get to minimum windows before considering any state changes
                drowsy.append(drowsy[i])
        full_drowsy_sequence.extend(drowsy)
    print('done\n\n\n')
    return full_drowsy_sequence


# should look kinda uniform with chosen parameters
def plot_state_change_density(num_datasets = 10000, num_windows_in_augmented_dataset = 10, minimum_windows_before_state_change = 3, lamb = 4):
    maximum_state_changes = num_windows_in_augmented_dataset//minimum_windows_before_state_change - 1
    sc=[i for i in range(0,maximum_state_changes+1)]
    sc_count=[0]*len(sc)
    for i in range(num_datasets):
        d_indices = construct_drowsy_awake_list(num_windows_in_augmented_dataset,minimum_windows_before_state_change)
        num_state_changes = 0
        for i in range(len(d_indices)-1):
            if(d_indices[i]!=d_indices[i+1]):
                num_state_changes += 1
        sc_count[sc.index(num_state_changes)] += 1
    plt.plot(sc,sc_count)
    plt.ylim([0,1.1*max(sc_count)])
    plt.show()



def generate_training_testing_sequences(output_filename='default.csv',headers=[],drowsy_points=[],awake_points=[],bool_seq=[],write=True):
    print('\n\n\n\nGenerating Sequences\n')
    training_sequence=[[header] for header in headers]
    testing_sequence=[[header] for header in headers]
    split = 0.80
    for i in range(len(bool_seq)):
        if(i < int(split*len(bool_seq))): # place in training
            if(bool_seq[i]): # choose drowsy point
                choice = random.randint(0,len(drowsy_points[0])-1)
                for j in range(len(training_sequence)):
                    training_sequence[j].append(drowsy_points[j][choice])
            else: # choose awake point
                choice = random.randint(0,len(awake_points[0])-1)
                for j in range(len(training_sequence)):
                    training_sequence[j].append(awake_points[j][choice])
        else: # place in testing
            if(bool_seq[i]): # choose drowsy point
                choice = random.randint(0,len(drowsy_points[0])-1)
                for j in range(len(testing_sequence)):
                    testing_sequence[j].append(drowsy_points[j][choice])
            else: # choose awake point
                choice = random.randint(0,len(awake_points[0])-1)
                for j in range(len(testing_sequence)):
                    testing_sequence[j].append(awake_points[j][choice])
    print('done\n\n\n')

    # save sequences
    if(write):
        print('\n\n\nWriting\n')
        muse_writefile(output_filename[:-4]+'_training_seq.csv', training_sequence)
        muse_writefile(output_filename[:-4]+'_testing_seq.csv', testing_sequence)
        print('done\n')
    return [training_sequence,testing_sequence]







if __name__ == "__main__":
    window = 1280
    advance = 640
    normalize_to_highest_band = True
    n_tag = ''
    if(normalize_to_highest_band):
        n_tag = 'normal'
    else:
        n_tag = 'ratio'

    single_augmented_dataset_duration_min = 30
    single_augmented_dataset_duration = single_augmented_dataset_duration_min * 60
    num_augmented_datasets = 1000 # 1000 --> 500 hours with these parameters
    sampling_rate = 256
    num_samples_in_augmented_dataset = single_augmented_dataset_duration * sampling_rate # 256 Hz * 60s * 30 = 30 min of data
    num_windows_in_augmented_dataset = num_samples_in_augmented_dataset//window
    minimum_windows_before_state_change = 6
    lamb = 4


    file_dir = "data/403_data/raw/"

    if(normalize_to_highest_band):
        ps_filename = "PS_w" + str(window) + "a" + str(advance) + "_normal.csv"
    else:
        ps_filename = "PS_w" + str(window) + "a" + str(advance) + "_ratio.csv"

    ps_filepath = file_dir + "../processed/" + ps_filename

    

    if(not exists(ps_filepath)): # if data hasn't been processed yet
        print('\nprocessing data\n')
        start_pro = time.time()
        paths = SP_all(file_dir,win,adv)
        print('\ndone\n')
        print('Processing Delay: '+str(time.time()-start_pro))
        
    start_gen = time.time()
    
    data = readfile(ps_filepath)
    headers, drowsy_points, awake_points = split_drowsy_awake(data)
    drowsy_bool_seq = construct_drowsy_awake_list(num_windows_in_augmented_dataset,minimum_windows_before_state_change,lamb,num_augmented_datasets)
    
    seq_name = str(window)+'_'+str(advance)+'_'+n_tag+'_'+str(single_augmented_dataset_duration_min)+'_'+str(num_augmented_datasets)+'_'+str(minimum_windows_before_state_change)+'_'+str(lamb)+'.csv'
    generate_training_testing_sequences(seq_name,headers,drowsy_points,awake_points,drowsy_bool_seq,True)
    
    print('Generation and Writing Delay: '+str(time.time()-start_gen))



