from PIL import Image
from numpy import zeros, log2, array
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



# load the image

image = Image.open(input_image_path)

# convert image to numpy array

data = array(image)


# # modify image with basic channel
# t1=time()
# for i in range(len(data)):
# 	for j in range(len(data[i])):
# 		for k in range(len(data[i][j])):
# 			data[i][j][k] = bin_8bit_to_int(received(int_to_bin_8bit(data[i][j][k])))
# print(time()-t1)
# Image.fromarray(data).save("basic.jpg")


# modify image with repetition encoded channel
rep = 7
t1=time()
for i in range(len(data)):
	for j in range(len(data[i])):
		for k in range(len(data[i][j])):
			data[i][j][k] = bin_8bit_to_int(repetition_decoder(received(repetition_encoder(int_to_bin_8bit(data[i][j][k]), rep)), rep))
print(time()-t1)
Image.fromarray(data).save("repetition_encoding.jpg")

