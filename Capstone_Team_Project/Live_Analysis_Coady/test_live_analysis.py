import numpy as np
import csv, sys, time, os

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
def muse_writefile_a(fn, data, start, end):
	with open(fn, 'a',newline='') as csvfile:
		w = csv.writer(csvfile)
		for i in range(start, end):
			row = [data[0][i],data[1][i],data[2][i],data[3][i],data[4][i]]
			w.writerow(row)


def muse_writefile(fn, data, end):
	with open(fn, 'w',newline='') as csvfile:
		w = csv.writer(csvfile)
		for i in range(end):
			row = [data[0][i],data[1][i],data[2][i],data[3][i],data[4][i]]
			w.writerow(row)


def test_single_file(data_file: str, duration=80, sleep=None):
	sleep is not None and time.sleep(sleep)
	print("Testing " + data_file + "...")
	filename='live_analysis_testcase.csv'
	#data = muse_readfile('../data/404_data/raw/Ali_near_awake_15min_a1.csv')
	#data = muse_readfile('../../../ECEN403/MuseData/Ali_L1h1-6.csv')
	#data = muse_readfile("../data/new_person/Dakota/raw/Dakota_L1h3_drowsy_10min.csv")
	#data = muse_readfile("../data/long_session/Coady/Coady_L1h6_drowsy_10min.csv")
	data = muse_readfile(data_file)

	start_time = time.time()
	iteration = 1
	frames = 1284
	timestep = frames / 256
	timestep = 0.5
	while ((time.time()-start_time) < duration):
		if(abs(time.time()-start_time-timestep*iteration)<=0.01):
			t1=time.time()
			if(iteration == 1):
				muse_writefile(filename,data,1+iteration*frames)
			else:
				muse_writefile_a(filename,data,1+(iteration-1)*frames,1+iteration*frames)
			iteration += 1
			print(time.time()-t1)#os.path.getmtime(filename))


if __name__ == "__main__":
	#test_single_file("../data/long_session/Ali/Ali_L1h2_awake_10min.csv")
	test_single_file(sys.argv[1], sleep=int(sys.argv[2]))
