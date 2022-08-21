import random
from numpy import log2,array,zeros
from math import floor

f = 0.1

# store bit vectors as boolean arrays, convert other types to this format
t_test = [1,0,0,1,1]



def received(transmitted):
	received = []
	for bit in transmitted:
		
		flip = random.random() < f
		if(flip):
			received.append(int(not bit))
		else:
			received.append(int(bit))
	return array(received)


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


#print(received(t_test))

def int_to_bin_8bit(x):
	output = [0,0,0,0,0,0,0,0]
	while (x!=0):
		ex = floor(log2(x))
		output[-1-ex] = 1
		x -= 2**ex
	return array(output)


def bin_8bit_to_int(x):
	output = 0
	for i in range(len(x)):
		output += x[-1-i] * (2**i)
	return output


def all_true(x):
	at = True
	for var in x:
		if(not var):
			at = False
	return at


def bin_equal(a,b):
	check_arr = []
	if(len(a) != len(b)):
		return False
	for i in range(len(a)):
		check_arr.append(a[i]==b[i])
	return all_true(check_arr)


# print(all_true([True,True,True]))
# print(all_true([True,False,True]))
# print(all_true([False,True,True]))
# print(all_true([True,True,False]))

test_arr = []
for i in range(256):
	b = int_to_bin_8bit(i)
	b_enc= repetition_encoder(b,3)
	print(b_enc)
	print(b)
	b_dec=repetition_decoder(b_enc,3)
	print(b_dec)
	integer = bin_8bit_to_int(b_dec)
	print(integer)
	print('\n\n\n')
	test_arr.append(bin_equal(b,b_dec))
print(all_true(test_arr))




