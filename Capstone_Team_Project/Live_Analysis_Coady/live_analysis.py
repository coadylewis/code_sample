from asyncore import write
from collections import deque
import matplotlib.pyplot as plt
import numpy as np
from math import sin, cos, sqrt, pi, floor
from muselsl import stream, record, list_muses
from muselsl.muse import Muse
from datetime import datetime
import os
import csv, sys, time, threading
sys.path.append("..")
from itertools import combinations
import ML_Models.KSVM as KSVM
import ML_Models.ANN as ANN
import ML_Models.RCNN as RCNN
import ML_Models.RNN as RNN
import queue
from multiprocessing import Pipe
import pickle


def read_arg():
	try:
		filename = sys.argv[1]
	except:
		print('\n\nEnter a muse csv file name as an argument\n\n')
		exit()


	# check file extension
	if(filename[len(filename)-4:] != '.csv'):
		print('\n\nEnter a muse csv file name as an argument\n\n')
		exit()
	return filename


# Writes Data from list in the format above, 
# i.e. data must be [[header,x1,x2,...,xn],[header,x1,x2,...,xn],[header,x1,x2,...,xn],[header,x1,x2,...,xn],[header,x1,x2,...,xn]]
def muse_writefile(fn, data):
	with open(fn, 'w',newline='') as csvfile:
		w = csv.writer(csvfile)
		check_min=[]
		for k in range(len(data)):
			check_min.append(len(data[k]))
		for i in range(min(check_min)):
			row = []
			for j in range(len(data)):
				row.append(data[j][i])
			w.writerow(row)


def muse_readfile_from_line(filename, start_line = 1): # LINE INDEX STARTS AT ONE
	data = [[],[],[],[],[]]
	current_line = 1
	with open(filename) as csvfile:
		dataset = csv.reader(csvfile)
		header = (start_line == 1)
		while(current_line < start_line): # skip ahead in the file until current_line == start_line
			current_line += 1
			next(csvfile)
		for row in dataset:	
			if(header): # The header will be kept as strings
				for i in range(5):
					try: # if calling row[i] gives an out-of-range exception, file is not muse data
						data[i].append(row[i])
					except:
						print('\n\nData Is Not Formatted Correctly\n\n')
						exit()
			else:
				for i in range(5): # if calling row[i] gives an out-of-range exception, file is not muse data
					try:
						data[i].append(float(row[i]))
					except:
						print('\n\nData Is Not Formatted Correctly\n\n')
						exit()
			header = False # ensures that only the header elements are kept as strings
			current_line += 1
	return [data, current_line]	


def ft_mag(signal, electrode, N_initial, N_final):
	# FOURIER TRANSFORM MAGNITUDE
	#
	E = electrode # electrode to use
	N_i = N_initial # index of initial signal point (skip header at N_i=0)
	N_f = N_final # index of final signal point
	#freq = frequencies # frequencies to plot
	#plot_vals = [] # will store |F{x(t)}|(w) here
	sg = np.fft.rfft(signal[E+1][int(N_i):int(N_f+1)])
	freq = np.fft.rfftfreq(2*len(sg)-1,d=(1/256))	
	# return 2d array of freq and |F{x(t)}|(2*pi*freq)  
	return [freq, np.abs(sg)]


def bandlimited_avg_power(signal, electrode, N_initial, N_final, F_lower, F_upper):
	mag = ft_mag(signal,electrode,N_initial,N_final)
	ap = 0
	num = 0
	for i in range(len(mag[0])):
		# # ASSUMES THE FREQUENCY ARRAY IS SORTED; can work faster with large number of points
		# if(F_lower>=mag[0][i]):
		# 	continue
		# if(F_upper<mag[0][i]):
		# 	break
		# ap += mag[1][i]**2
		# num += 1
		if(F_lower<mag[0][i] and mag[0][i]<=F_upper):
			ap += mag[1][i]**2
			num += 1		
	try:
		ap /= num
		return ap
	except:
		return float("NaN")


def relative_band_avg_power(signal, electrode, N_initial, N_final, FI_lower, FI_upper,FO_lower, FO_upper):
	apI = bandlimited_avg_power(signal, electrode, N_initial, N_final, FI_lower, FI_upper)
	apO = bandlimited_avg_power(signal, electrode, N_initial, N_final, FO_lower, FO_upper)
	try:
		return apI/apO
	except:
		return float("NaN")


def gen_default_freq_ranges(normalize_to_highest_band = True):
	freq_ranges = []
	if(normalize_to_highest_band):
		normalizing_band = [25,30]
		band_size = 0.5
		band_start = 4
		band_end = 17
		# construct freq_ranges
		for i in range(floor((band_end-band_start)/band_size)):
			freq_ranges.append([band_start+i*band_size,band_start+(i+1)*band_size])
		freq_ranges.append([17,20])
		freq_ranges.append([20,25])
		freq_ranges.append(normalizing_band)
	else:
		freq_ranges = [[4,6],[6,8],[8,10],[10,12],[12,21],[21,30]]
	return freq_ranges


def vector(raw_data=[],headers=[],timestamp=0,freq_ranges = [],normalize_to_highest_band = True,output_mode=[True,True]):
	#
	num_electrodes = 4
	output = []
	if(normalize_to_highest_band):
		normalizing_band = freq_ranges.pop() # normalize to highest input band
		n = len(freq_ranges)
		for i in range(num_electrodes*n+1):
			output.append([])

		# add headers
		output[0].append(headers[0])
		for i in range(1,num_electrodes+1):
			for j in range(n):
				output[n*i-(n-j-1)].append(headers[i]+'_'+str(j))
		
		if(output_mode[0] and (not output_mode[1])): # if only headers are needed
			return [col[0] for col in output]

		# timestamp will mark the beginning of interval
		output[0].append(timestamp)
		# add n values for all electrodes
		for i in range(1,num_electrodes+1):
			for j in range(n):
				output[n*i-(n-j-1)].append(relative_band_avg_power(raw_data, i-1, 0, len(raw_data[0])-1, freq_ranges[j][0], freq_ranges[j][1], normalizing_band[0], normalizing_band[1]))
	else:
		# construct combination array
		n = len(freq_ranges)
		k = 2
		test = []
		for i in range(n):
			test.append(i)
		comb = list(combinations(test,2))
		num_comb=len(comb)
		for i in range(num_electrodes*num_comb+1):
			output.append([])

		# add headers
		output[0].append(headers[0])
		for i in range(1,num_electrodes+1):
			for j in range(num_comb):
				output[num_comb*i-(num_comb-j-1)].append(headers[i]+'_'+str(j))

		if(output_mode[0] and (not output_mode[1])): # if only headers are needed
			return [col[0] for col in output]

		# timestamp will mark the beginning of interval
		output[0].append(timestamp)
		# add num_comb values for all electrodes
		for i in range(1,num_electrodes+1):
			for j in range(num_comb):
				output[num_comb*i-(num_comb-j-1)].append(relative_band_avg_power(raw_data, i-1, 0, len(raw_data[0])-1, freq_ranges[comb[j][0]][0], freq_ranges[comb[j][0]][1], freq_ranges[comb[j][1]][0], freq_ranges[comb[j][1]][1]))
	
	if((not output_mode[0]) and output_mode[1]): # if only vector vals are needed
		return [col[1] for col in output]

	return output


def transpose(input_matrix=[]):
	output_matrix=[]
	for i in range(len(input_matrix[0])):
		output_matrix.append([input_matrix[j][i] for j in range(len(input_matrix))])
	return output_matrix


#container to send to classify() function
# - type: "KSVM" or "ANN"
# - model: ML model object
# - norm_param: normalization parameters object
# - stream_filename: file with raw data currently being analyzed
# - model_filename: specifies ML model parameters
# - results_filename: file with classification output being written to
# - classification_count: list with [awake, drowsy] outputs
class ModelContainer:
	def __init__(self, type, model, norm_param, stream_filename, model_filename):
		self.type = type
		self.model = model
		self.norm_param = norm_param
		self.model_filename = model_filename

		self.results_filename = "live_analysis_results_" + type + ".csv"
		now = datetime.now()
		dt_string = now.strftime("%d/%m/%Y %H:%M:%S") # dd/mm/YY H:M:S
		with open(self.results_filename, 'a') as f:
			f.write('\n\n\n\n\n\n\n\n\nraw_data File: '+ stream_filename)
			f.write('\nModel Tested = '+ model_filename +'\n')
			f.write('Date: '+dt_string+'\n\n\n')

		self.classification_count = [0, 0]
		self.num_classifications = 0


def classify(vect, model_cont: ModelContainer, seq_len=None, write_results=False, show_save_output=True):
	filename = "D4H1Ali_output.csv"
	y_pred_orig = 0
	y_pred = 0
	if show_save_output:
		model_cont.num_classifications += 1
	if model_cont.type == "KSVM":
		y_pred_orig = KSVM.model_predict(model_cont.model, model_cont.norm_param, vect)
		y_pred = y_pred_orig
		if write_results:
			with open("Outputs/KSVM_" + filename, 'a', newline='') as f:
				writer = csv.writer(f)
				new_row = [model_cont.num_classifications, int(y_pred)]
				writer.writerow(new_row)
				f.close()
	elif model_cont.type == "ANN":
		y_pred_orig = ANN.model_predict(model_cont.model, model_cont.norm_param, vect)
		y_pred = y_pred_orig > 0.5
	elif model_cont.type == "RCNN":
		y_pred_orig = RCNN.model_predict(model_cont.model, model_cont.norm_param, vect, seq_len)
		y_pred = y_pred_orig > 0.5
		if write_results:
			with open("Outputs/RCNN_" + model_cont.model_filename + "_" + filename, 'a+', newline='') as f:
				writer = csv.writer(f)
				if f.tell() == 0: 	#file newly created
					writer.writerow(["classification", "true_output", "bin_output"])	#append header
				new_row = [model_cont.num_classifications, y_pred_orig[0][0], int(y_pred[0][0])]
				writer.writerow(new_row)
				f.close()
	elif model_cont.type == "RNN":
		y_pred_orig = RNN.model_predict(model_cont.model, model_cont.norm_param, vect, seq_len)
		y_pred = y_pred_orig > 0.5
		if write_results:
			with open("Outputs/RNN_" + filename, 'a+', newline='') as f:
				writer = csv.writer(f)
				new_row = [model_cont.num_classifications, y_pred_orig[0][0], int(y_pred[0][0])]
				writer.writerow(new_row)
				f.close()

	if show_save_output:
		if (y_pred == 1):
			model_cont.classification_count[1] += 1
		else:
			model_cont.classification_count[0] += 1

		with open(model_cont.results_filename, 'a') as f:
			f.write(str(y_pred)+'\n')
			output = "drowsy" if y_pred == 1 else "awake"
			f.write(output)
			num_outputs = model_cont.classification_count[0]+model_cont.classification_count[1]
			f.write('\nDrowsy Fraction = '+str(model_cont.classification_count[1]/num_outputs))
			f.write('\nAwake Fraction = '+str(model_cont.classification_count[0]/num_outputs))
			f.write('\nOutput Count = '+str(num_outputs))
			f.write('\n\n\n')
		
		print('\n')
		print('\nDrowsy Fraction = '+str(model_cont.classification_count[1]/num_outputs))
		print('\nAwake Fraction = '+str(model_cont.classification_count[0]/num_outputs))
		print('\nOutput Count = '+str(num_outputs))
	return y_pred_orig


#conns - optional parameter with list of shared pipe connections to live analysis graph process
def eeg_live_analysis_from_updating_file(filename="current_stream_data.csv", nhb=True, duration=1800, mean_time_interval=5, model_filename='PS_w1280a100', conns=None, seq_len=None):
	#print(filename)
	#print(nhb)
	#print(duration)
	#print(mean_time_interval)
	#print(model_filename)
	#print(conns)
	#print(seq_len)
	# run for duration (seconds)
	# checks for updated data file every check_for_update_interval (seconds)
	# if raw data file has no update, check again after check_for_update_interval (seconds)
	# if raw data file has an update, add it to the data array
	# 
	start_time = time.time() # used for determining when to end function
	print('\n')

	
	normalize_to_highest_band = nhb
	freq_ranges = gen_default_freq_ranges(normalize_to_highest_band)
	feature_headers=[]

	# mean_window_samples = int(mean_time_interval * 256) # avg number of samples in window
	num_electrodes = 4 # number of device electrodes, the muse has 4

	first = True # add header on first run, then set to false
	update_times = []
	raw_data = []
	feature_data = []
	computation_times = []
	feature_savefile_tag = ''

	# load KSVM model and normalization parameters
	#model_ksvm=KSVM.load_object('KSVM_'+model_filename)
	#norm_ksvm=KSVM.load_object('KSVM_norm_param_'+model_filename)

	# load NN model and normalization parameters
	#model_ann=ANN.load_model('ANN_'+ model_filename)
	#norm_ann=ANN.load_object('ANN_norm_param_'+ model_filename)

	# load RNN model and normalization parameters
	#model_rnn=RNN.load_model('RNNs' + str(seq_len) + '_'+ model_filename + '.h5')
	#norm_rnn=RNN.load_object('RNNs' + str(seq_len) + '_norm_param_'+ model_filename)

	print("Initializing model...")

	# load RCNN model and normalization parameters
	model_rcnn=RCNN.load_model('RCNNs' + str(seq_len) + '_'+ model_filename + '.h5')
	norm_rcnn=RCNN.load_object('RCNNs' + str(seq_len) + '_norm_param_'+ model_filename)

	#ksvm_cont = ModelContainer("KSVM", model_ksvm, norm_ksvm, filename, model_filename)
	#ann_cont = ModelContainer("ANN", model_ann, norm_ann, filename, model_filename)
	#rnn_cont = ModelContainer("RNN", model_rnn, norm_rnn, filename, model_filename)
	rcnn_cont = ModelContainer("RCNN", model_rcnn, norm_rcnn, filename, model_filename)
	vector_data = pickle.load(open("RCNN_predict_init.p", 'rb'))
	#print("Initializing model predict function...")
	classify(vector_data, rcnn_cont, seq_len, show_save_output=False)	#initializes model predict() function
	#classify(vector_data, rnn_cont, seq_len, show_save_output=False)
	print("Model initialized")
	sequenced_data = deque(maxlen=seq_len)

	try:
		timestamp_start = 0
		N_i = 1
		N_f = 1
		line = 1
		startline = 0
		last_update_time = os.path.getmtime(filename) # gives the last time the file was modified
		while ((time.time()-start_time) < duration): # main body of function runs in this loop
			check_update_time = os.path.getmtime(filename) # keeps checking the 'modified' time
			if(abs(last_update_time - check_update_time) >= 0.1): # if True, an update to the file occured
				time.sleep(0.1) # gives time for file to be closed after update before accessing again
				read_data = muse_readfile_from_line(filename,line)

				line = read_data[1] # get next line to start from in the csv file
				update_times.append(time.time()-check_update_time)
				if(first): # ignore first sample and all negative timestamps, just initialize
					first = False # forces code to else block next time
					timestamp_start = check_update_time
					# add raw_data headers
					for column in read_data[0]:
						raw_data.append([column[0]])
					# get feature_data headers 
					feature_headers = vector([col[1:] for col in raw_data],[col[0] for col in raw_data],timestamp_start,freq_ranges,normalize_to_highest_band,[True,False])
					# add feature_data headers
					for header in feature_headers:
						feature_data.append([header])
					# save file name modifier
					if(normalize_to_highest_band):
						savefile_tag = '_normalized_power_live.csv'
					else:
						savefile_tag = '_ratio_power_live.csv'

				else: # all runs after the first are executed in this block	
					num_samples = len(raw_data[0])
					if(num_samples != 0):
						N_i = num_samples # get start of interval for power calculation
					for i in range(len(raw_data)): # updates all 5 columns of the raw_data array
						raw_data[i].extend(read_data[0][i])
					N_f = len(raw_data[0])-1 # get end of interval for power calculation

					comp_start = time.time()
					if(startline==0):
						startline = N_i

					# # SYNC CHECKING
					# if(abs((N_f-N_i+1)-mean_window_samples)>10 or abs((check_update_time-last_update_time)-mean_time_interval) > (0.02*mean_time_interval)):
					# 	print('\n\n\nERROR: SYNC LOST\n\nCHECK INPUT STREAM\n\n\nEXITING...\n\n\n')
					# 	exit()

					print('Samples in Interval = '+str(N_f-N_i+1))
					with open("live_analysis_results.txt", 'a') as f:
						f.write('\nSamples in Interval = '+str(N_f-N_i+1)+'\n'+'Start = '+str(N_i)+'\nEnd = '+str(N_f)+'\n')
					
					# get feature_update for all 4 electrodes
					feature_update = vector(read_data[0],[col[0] for col in raw_data],update_times[-1],freq_ranges,normalize_to_highest_band)
					# add feature_data
					for i in range(len(feature_update)):
						feature_data[i].append(feature_update[i][1])
					

					print('timestamp = '+str(feature_data[0][len(feature_data[0])-1])+' s\n', end='')
					#for model_cont in [ksvm_cont, ann_cont]:
					for model_cont in [rcnn_cont]:
						with open(model_cont.results_filename, 'a') as f:
							f.write('timestamp = '+str(feature_data[0][len(feature_data[0])-1])+' s'+'\n')
					print('\n')
					#
					#
					#
					# classify vector, print output, and log classification data
					transposed_features = transpose(feature_update)
					sequenced_data.append(transposed_features[1])
					#y_pred_ksvm = classify(transposed_features, ksvm_cont)
					#y_pred_ann_orig = classify(transposed_features, ann_cont)
					y_pred_rcnn_orig = 0
					if len(sequenced_data) == seq_len:
						vector_data = [transposed_features[0], np.array(sequenced_data)]
						#pickle.dump(vector_data, open("RCNN_predict_init.p", "wb"))
						y_pred_rcnn_orig = classify(vector_data, rcnn_cont, seq_len, write_results=True)
						#classify(vector_data, rnn_cont, seq_len, write_results=True)
						if conns is not None:
							conns.get("RCNN") is not None and conns.get("RCNN").send(y_pred_rcnn_orig)

					# send output to live analysis graph process(es)
					if conns is not None:
						conns.get("KSVM") is not None and conns.get("KSVM").send(y_pred_ksvm)
						conns.get("ANN") is not None and conns.get("ANN").send(y_pred_ann_orig)
						#conns.get("RCNN") is not None and conns.get("RCNN").send(y_pred_rcnn_orig)

					comp_end = time.time()
					computation_times.append(comp_end-comp_start)
					print('\nComputation Time = '+str(comp_end-comp_start)+' s\n\n\n\n\n\n')

				last_update_time = check_update_time # change this at the end of every update

		if conns is not None:
			conns.get("KSVM") is not None and conns.get("KSVM").close()
			conns.get("ANN") is not None and conns.get("ANN").close()
			conns.get("RCNN") is not None and conns.get("RCNN").close()

		# save power raw_data when done
		muse_writefile((filename[:len(filename)-4]+savefile_tag),feature_data)
		return [raw_data, feature_data, startline, computation_times]
		
	except KeyboardInterrupt:
		if conns is not None:
			conns.get("KSVM") is not None and conns.get("KSVM").close()
			conns.get("ANN") is not None and conns.get("ANN").close()
			conns.get("RCNN") is not None and conns.get("RCNN").close()
		muse_writefile((filename[:len(filename)-4]+savefile_tag),feature_data)		
		return [raw_data, feature_data, startline, computation_times]

if __name__ == "__main__":
	normalize_to_highest_band = False
	model = 'PS_w1280a1280'
	seq_len = 12
	try:
		dataset = eeg_live_analysis_from_updating_file('live_analysis_testcase.csv',normalize_to_highest_band,model_filename=model,seq_len=seq_len)
	except Exception as e:
		print("Error:", e)
	input("Press enter to exit:")