from PIL import Image
from numpy import zeros, log2, array, concatenate, split, uint8, all
from math import floor
from random import random
from time import time
import csv


input_image_path='test.jpg'
f = 0.2 # flip probability of binary symmetric channel
# store bit vectors as boolean arrays, convert other types to this format


def received(transmitted):
	print('transmitting over binary symmetric channel ...')
	t1=time()
	lt = len(transmitted)
	received = zeros((lt), dtype=int)
	for i in range(lt):
		flip = random() < f
		if(flip):
			received[i] = (int(not transmitted[i]))
		else:
			received[i] = (int(transmitted[i]))
	print(time()-t1)
	print('received\n\n\n')
	return received


def int_to_bin_8bit(x): # scales horribly, better to flatten image array and use one_dim_int_list_to_bin_array
	output = zeros((8), dtype=int)
	while (x!=0):
		ex = floor(log2(x))
		output[-1-ex] = 1
		x -= 2**ex
	return output


def bin_8bit_to_int(x):
	output = 0
	for i in range(len(x)):
		output += x[-1-i] * (2**i)
	return output


def repetition_encoder(x, n):
	print('encoding with n='+str(n),'repetition ...')
	t1=time()
	x_len=len(x)
	output = zeros((x_len*n), dtype=int)
	for i in range(x_len):
		if(x[i]):
			for j in range(n):
				output[i*n+j]=x[i]
		else:
			continue
	print(time()-t1)
	print('encoded\n\n\n')
	return output


def repetition_decoder(x, n):
	print('decoding n='+str(n),'repetition ...')
	t1=time()
	x_len=len(x)
	output = zeros((x_len//n), dtype=int)
	for i in range(x_len//n):
		for j in range(n):
			output[i]+=x[i*n+j]
		output[i]=int((n/2) < output[i])
	print(time()-t1)
	print('decoded\n\n\n')
	return output


def is_power_2(x):
	check = round(log2(x),5)
	return check.is_integer()


def image_int_array_to_1d_int_list(data): # convert image array of ints to a 1d list
	t1=time()
	print('image_int_array_to_1d_int_list')
	height=len(data)
	width=len(data[0])
	output=[[],height,width]
	for row in data:
		for pixel in row:
			for color in pixel:
				output[0].append(color)
	print(time()-t1)
	print('\n\n\n')
	return output


def one_dim_int_list_to_image_int_array(data): # inverse of image_int_array_to_1d_int_list()
	t1=time()
	print('one_dim_int_list_to_image_int_array')
	output=[]
	for i in range(data[1]):
		output.append([])
		for j in range(data[2]):
			output[i].append([])
			for k in range(3):
				output[i][j].append(data[0][((i)*data[2]*3) + ((j)*3) + k])
	print(time()-t1)
	print('\n\n\n')
	return array(output)


def one_dim_int_list_to_bin_array(data):
	t1=time()
	print('one_dim_int_list_to_bin_array')
	# # first implementation; extremely slow; like first repetition encoder
	# output=int_to_bin_8bit(data[0])
	# for i in range(1,len(data)):
	# 	output = concatenate((output,int_to_bin_8bit(data[i])))

	# second implementation; allocate single np array; used to improve first repetition encoder
	output=zeros((8*len(data)),dtype=int)
	for i in range(len(data)):
		while (data[i]!=0):
			ex = floor(log2(data[i]))
			output[8*(i+1)-1-ex] = 1
			data[i] -= 2**ex
	print(time()-t1)
	print((time()-t1)/(len(data)))
	print('\n\n\n')
	return output


def bin_array_to_1d_int_list(data): #inverse of one_dim_int_list_to_bin_array() assuming 8 bit
	t1=time()
	print('bin_array_to_1d_int_list')
	output=[]
	for i in range(len(data)//8):
		output.append(bin_8bit_to_int(data[i*8:(i+1)*8]))
	# output=zeros((len(data)//8), dtype=int)
	# for i in range(len(output)):
	# 	for j in range(8):
	# 		output[i] += data[8*(i+1)-1-j] * (2**j)

	print(time()-t1)
	print((time()-t1)/(len(data)//8))
	print('\n\n\n')
	return output

	





def hamming_encoder(x, num_blocks): 
	k=len(x) # num information bits
	# soln. here

















# access saved test data if available
use_saved_test_data = True
save_data = True
save_cpy_of_loaded_image_data = False
filename = "binary_test_data.csv"
if(not use_saved_test_data):
	# load the image

	image = Image.open(input_image_path)

	# convert image to numpy array

	data = array(image)
	bits = 8
	w=len(data[0])
	h=len(data)
	data_subset=data[:h,:w]
	data_subset_orig=data_subset
	print('Res =',str(h),'x',str(w)+'\n\n\n')

	# flatten image array into binary string; slowest part of process; best to use saved binary test string for repeated testing of large images

	data_subset_flat = image_int_array_to_1d_int_list(data_subset)
	data_subset_flat_bin = one_dim_int_list_to_bin_array(data_subset_flat[0])

	if(save_data):
		with open(filename, 'w',newline='') as csvfile:
			wri = csv.writer(csvfile)
			wri.writerow([h,w])
			wri.writerow(data_subset_flat_bin)
else: # load from csv
	t1=time()
	print('loading binary image data')
	with open(filename) as csvfile:
		readdata = csv.reader(csvfile)
		h, w = [int(elem) for elem in next(readdata)]
		data_subset_flat_bin = array([int(elem) for elem in next(readdata)])
	print(time()-t1)
	print('\n\n\n')
	# save copy of unmodified image
	if(save_cpy_of_loaded_image_data):
		t1=time()
		print('loading binary image data')
		print('\n')
		data_subset_flat_loaded = bin_array_to_1d_int_list(data_subset_flat_bin)
		data_subset_loaded = one_dim_int_list_to_image_int_array([data_subset_flat_loaded,h,w])
		Image.fromarray(data_subset_loaded.astype(uint8)).save("loaded.jpg")
		print('\n')
		print(time()-t1)
		print('\n\n\n')






# # test transform to 1d list and back**********************************************************************************************
# #print(data_subset)
# t1=time()
# d1_list_full=image_int_array_to_1d_int_list(data_subset)
# #print(d1_list_full)
# d1_list=one_dim_int_list_to_bin_array(d1_list_full[0])

# data_subset_transformed = one_dim_int_list_to_image_int_array([bin_array_to_1d_int_list(d1_list),d1_list_full[1],d1_list_full[2]])
# # print(data_subset)
# # print(data_subset_transformed)
# print(all(data_subset==data_subset_transformed))
# #print(time()-t1)
# Image.fromarray(data_subset_transformed.astype(uint8)).save("basic_1d.jpg")


# print(d1_list)
# print(time()-t1)
# print(bin_array_to_1d_int_list(d1_list))

# save unmodified image*************************************************************************************************************



# modify image with basic binary symmetric channel**********************************************************************************
# # first method; elementwise; very slow
# for i in range(len(data)):
#     for j in range(len(data[i])):
#         for k in range(len(data[i][j])):
#             data[i][j][k] = bin_8bit_to_int(received(int_to_bin_8bit(data[i][j][k])))
# second method

# data_subset_flat_bin_received = received(data_subset_flat_bin)
# data_subset_flat_received = bin_array_to_1d_int_list(data_subset_flat_bin_received)
# data_subset_received = one_dim_int_list_to_image_int_array([data_subset_flat_received,h,w])
# print('image modified with basic binary symmetric channel**********************************************')
# Image.fromarray(data_subset_received.astype(uint8)).save("basic.jpg")





# modify image with repetition encoded binary symmetric channel*********************************************************************
rep = 3
# # first method; elementwise; very slow
# for i in range(len(data)):
#   for j in range(len(data[i])):
#       for k in range(len(data[i][j])):
#           data[i][j][k] = bin_8bit_to_int(repetition_decoder(received(repetition_encoder(int_to_bin_8bit(data[i][j][k]), rep)), rep))
# second method

data_subset_flat_bin_encoded = repetition_encoder(data_subset_flat_bin,rep)
data_subset_flat_bin_received_encoded = received(data_subset_flat_bin_encoded)
data_subset_flat_bin_received_decoded = repetition_decoder(data_subset_flat_bin_received_encoded,rep)
data_subset_flat_received_decoded = bin_array_to_1d_int_list(data_subset_flat_bin_received_decoded)
data_subset_received_decoded = one_dim_int_list_to_image_int_array([data_subset_flat_received_decoded,h,w])
print('image modified with repetition encoded binary symmetric channel*********************************')
Image.fromarray(data_subset_received_decoded.astype(uint8)).save("repetition_encoding.jpg")

