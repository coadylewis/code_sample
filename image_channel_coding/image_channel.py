from PIL import Image
from numpy import zeros, log2, array, concatenate, split
from math import floor
from random import random
from time import time


input_image_path='test.jpg'
f = 0.3 # flip probability of binary symmetric channel
# store bit vectors as boolean arrays, convert other types to this format


def received(transmitted):
	lt = len(transmitted)
	received = zeros((lt), dtype=int)
	for i in range(lt):
		flip = random() < f
		if(flip):
			received[i] = (int(not transmitted[i]))
		else:
			received[i] = (int(transmitted[i]))
	return received


def int_to_bin_8bit(x):
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
	x_len=len(x)
	output = zeros((x_len*n), dtype=int)
	for i in range(x_len):
		for j in range(n):
			output[i*n+j]=x[i]
	return output


def repetition_decoder(x, n):
	x_len=len(x)
	output = zeros((x_len//n), dtype=int)
	for i in range(x_len//n):
		for j in range(n):
			output[i]+=x[i*n+j]
		output[i]=int((n/2) < output[i])
	return output


def is_power_2(x):
	check = round(log2(x),5)
	return check.is_integer()


def list_2d_to_bin_list(data): # convert 2d array of ints to a single binary list
	output=int_to_bin_8bit(data[0][0][0])
	#print(output)
	for i in range(len(data)): #row
		for j in range(len(data[i])): #column
			for k in range(len(data[i][j])):
				if(i==0 and j==0 and k==0):
					continue
				#print(int_to_bin_8bit(data[i][j][k]))
				output=concatenate((output,int_to_bin_8bit(data[i][j][k])))
	print('successful')
	return output


def list_to_bin_2d_list(x,num_bits,width,height): # inverse of above function
	data_1d = split(x,len(x)//num_bits)
	data = []
	for i in range(height):
		data.append([])
		for j in range(width):
			data[i].append([])#i*j+j)
			for k in range(3):
				data[i][j].append(bin_8bit_to_int(data_1d[i*width*3+j*3+k]))
	return data


def hamming_encoder(x, num_blocks): 
	k=len(x) # num information bits
	# soln. here





# load the image

image = Image.open(input_image_path)

# convert image to numpy array

data = array(image)

bits = 8


# # test transform to 1d list and back
# w=10
# h=10
# data_subset=data[:w][:h]
# t1=time()
# data_subset_transformed = list_to_bin_2d_list(list_2d_to_bin_list(data_subset),bits,w,h)
# print(time()-t1)
# # for i in range(len(data_subset)):
# # 	for j in range(len(data_subset[i])):
# # 		for k in range(len(data_subset[i][j])):
# # 			print(data_subset[i][j][k]-data_subset_transformed[i][j][k])
# # 			data_subset[i][j][k]-=data_subset_transformed[i][j][k]
# print(data_subset)
# print(array(data_subset_transformed))
# #Image.fromarray(data).save("basic.jpg")





# # # modify image with basic channel
# # t1=time()
# # for i in range(len(data)):
# # 	for j in range(len(data[i])):
# # 		for k in range(len(data[i][j])):
# # 			data[i][j][k] = bin_8bit_to_int(received(int_to_bin_8bit(data[i][j][k])))
# # print(time()-t1)
# # Image.fromarray(data).save("basic.jpg")





# # modify image with repetition encoded channel
# rep = 7
# t1=time()
# for i in range(len(data)):
# 	for j in range(len(data[i])):
# 		for k in range(len(data[i][j])):
# 			data[i][j][k] = bin_8bit_to_int(repetition_decoder(received(repetition_encoder(int_to_bin_8bit(data[i][j][k]), rep)), rep))
# print(time()-t1)
# Image.fromarray(data).save("repetition_encoding.jpg")

