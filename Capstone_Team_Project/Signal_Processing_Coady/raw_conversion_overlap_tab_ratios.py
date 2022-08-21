import numpy as np
import csv, sys, time
from itertools import combinations
from math import floor

#ASSUMES MUSE FILES AND 256 HZ
#Reads raw data from argument and outputs the alpha/beta relative power
#as a csv in the same format with name = input_filename + "_power"


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


#outputs a 2d list from a muse format csv input
#file = [['timestamp',x1,x2,...,xn],['tp9',x1,x2,...,xn],['af7',x1,x2,...,xn],['af8',x1,x2,...,xn],['tp10',x1,x2,...,xn]]
# where x1-xn are the float data vals under the given header
def muse_readfile(fn):
	# file vars
	file = [[],[],[],[],[]] # no shorthand, memory assignment issue
	filename = fn


	# store file data in 2d list file[tag_index][n] where n is the data point
	with open(filename) as csvfile:
		dataset = csv.reader(csvfile)
		hold = True
		for row in dataset:	
			if(hold):		
				for i in range(5):
					# if calling row[i] gives an out-of-range exception, file is not muse data
					try:
						file[i].append(row[i])
					except:
						print('\n\nEnter a muse csv file name as an argument\n\n')
						exit()
			else:
				for i in range(5):
					# if calling row[i] gives an out-of-range exception, file is not muse data
					try:
						file[i].append(float(row[i]))
					except:
						print('\n\nEnter a muse csv file name as an argument\n\n')
						exit()
			hold = False
	return file


# Writes Data from list in the format above, 
# i.e. data must be [[header,x1,x2,...,xn],[header,x1,x2,...,xn],[header,x1,x2,...,xn],[header,x1,x2,...,xn],[header,x1,x2,...,xn]]
def muse_writefile(fn, data):
	with open(fn, 'w',newline='') as csvfile:
		w = csv.writer(csvfile)
		for i in range(len(data[0])):
			row = []
			for j in range(len(data)):
				row.append(data[j][i])
			w.writerow(row)


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


def convert_raw_to_n_ratio_bandpower(filename,frames_per_seg=2560, advancement = 2560, write=True): #default 10s with 256 hz
	dataset = muse_readfile(filename)
	freq_ranges = [[4,6],[6,8],[8,10],[10,12],[12,15],[15,21],[21,30]]
	num_electrodes = 4
	# construct combination array
	n = len(freq_ranges)
	k = 2
	test = []
	for i in range(n):
		test.append(i)
	comb = list(combinations(test,2))
	num_comb=len(comb)
	output = []
	for i in range(num_electrodes*num_comb+1):
		output.append([])
	# add headers
	output[0].append(dataset[0][0])
	for i in range(1,num_electrodes+1):
		for j in range(num_comb):
			output[num_comb*i-(num_comb-j-1)].append(dataset[i][0]+'_'+str(j))
	current_win_end = frames_per_seg
	current_win_start = 1
	while(current_win_end < len(dataset[0])):
		# timestamp will mark the beginning of interval
		output[0].append((current_win_start-1)/256)
		# add num_comb values for all electrodes

		for i in range(1,num_electrodes+1):
			for j in range(num_comb):
				output[num_comb*i-(num_comb-j-1)].append(relative_band_avg_power(dataset, i-1, current_win_start, current_win_end, freq_ranges[comb[j][0]][0], freq_ranges[comb[j][0]][1], freq_ranges[comb[j][1]][0], freq_ranges[comb[j][1]][1]))

		current_win_start += advancement
		current_win_end += advancement
	if write:
		muse_writefile((filename[:len(filename)-4]+'_power_n_ratios.csv'),output)
	return output


# For CNN?
def convert_raw_to_n_bandpower(filename,frames_per_seg=2560, advancement = 2560, write=True, only_headers=False): #default 10s with 256 hz
	dataset = muse_readfile(filename)
	normalizing_band = [25,30]
	band_size = 0.5
	band_start = 4
	band_end = 17
	freq_ranges = []
	# construct freq_ranges
	for i in range(floor((band_end-band_start)/band_size)):
		freq_ranges.append([band_start+i*band_size,band_start+(i+1)*band_size])
	freq_ranges.append([17,20])
	freq_ranges.append([20,25])
	#
	num_electrodes = 4
	n = len(freq_ranges)
	output = []
	for i in range(num_electrodes*n+1):
		output.append([])
	# add headers
	output[0].append(dataset[0][0])
	for i in range(1,num_electrodes+1):
		for j in range(n):
			output[n*i-(n-j-1)].append(dataset[i][0]+'_'+str(j))
	current_win_end = frames_per_seg
	current_win_start = 1
	while(current_win_end < len(dataset[0])):
		# timestamp will mark the beginning of interval
		output[0].append((current_win_start-1)/256)
		# add n values for all electrodes

		for i in range(1,num_electrodes+1):
			for j in range(n):
				output[n*i-(n-j-1)].append(relative_band_avg_power(dataset, i-1, current_win_start, current_win_end, freq_ranges[j][0], freq_ranges[j][1], normalizing_band[0], normalizing_band[1]))

		current_win_start += advancement
		current_win_end += advancement
	if write:
		muse_writefile((filename[:len(filename)-4]+'_power_n_normalized.csv'),output)
	if(only_headers):
		return [col[0] for col in output]
	else:
		return output


if __name__ == "__main__":
	#Final val is list formatted in the muse format
	#also saves as a new csv
	#
	start = time.time()
	# alpha_to_beta = convert_raw_to_rel_bandpower(read_arg(),8,12,12,30,1280,100,True)
	# theta_alpha_beta = convert_raw_to_tab_bandpower(read_arg(),1280,100,True)
	output = convert_raw_to_n_ratio_bandpower(read_arg(),1920,1920,True)
	print('Delay = '+str(time.time()-start))

	
def test():
	print("Successfully imported Signal Processor")