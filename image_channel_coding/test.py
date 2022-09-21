from numpy import array,zeros,all,sum,concatenate,eye,dot,any
from math import floor, log2, ceil
from time import time

x=array([0,0,0,0,0,1,0,1,0,0,1,1,1,0,0,1,0,1,1,1,0,1,1,1])
x5=array([i for i in range(32)])
#print(x5)


def repetition_decoder_0(x, n):
	x_len=len(x)
	output = zeros((x_len//n), dtype=int)
	for i in range(x_len//n):
		for j in range(n):
			output[i]+=x[i*n+j]
		output[i]=int((n/2) < output[i])
	return output


def repetition_decoder(x, n):
	print('decoding n='+str(n),'repetition ...')
	t1=time()
	x_len=len(x)
	output = zeros((x_len//n), dtype=int)
	for i in range(x_len//n):
		output[i]=int((n/2) < sum(x[i*n:(i+1)*n]))
		# output[i]= majority_rule(x[i*n:(i+1)*n])
		# # if(x[i*n]):

		# # 	output[i]=int(x[i*n+1] or x[i*n+2])
		# # else:
		# # 	output[i]=int(x[i*n+1] and x[i*n+2])
	print(time()-t1)
	print('decoded\n\n\n')
	return output

def majority_rule(x):
	lx = len(x)
	if(lx>3):
		return  majority_rule(array([majority_rule(x[i:i+3]) for i in range(lx-2)]))
	else:
		if(x[0]):
			return int(x[1] or x[2])
		else:
			return int(x[1] and x[2])	


#print(majority_rule(array([1,1,1,0,0])))

def one_dim_int_list_to_bin_array(data,bits):
	t1=time()
	print('one_dim_int_list_to_bin_array')
	# # first implementation; extremely slow; like first repetition encoder
	# output=int_to_bin_8bit(data[0])
	# for i in range(1,len(data)):
	# 	output = concatenate((output,int_to_bin_8bit(data[i])))

	# second implementation; allocate single np array; used to improve first repetition encoder
	output=zeros((bits*len(data)),dtype=int)
	for i in range(len(data)):
		while (data[i]!=0):
			ex = floor(log2(data[i]))
			output[bits*(i+1)-1-ex] = 1
			data[i] -= 2**ex
	print(time()-t1)
	print((time()-t1)/(len(data)))
	print('\n\n\n')
	return output

bin_arr = one_dim_int_list_to_bin_array(x5,5)
# print(repetition_decoder(bin_arr,5))
# print(repetition_decoder_0(bin_arr,5))
# print(repetition_decoder(bin_arr,5)==repetition_decoder_0(bin_arr,5))
# print(all(repetition_decoder(bin_arr,5)==repetition_decoder_0(bin_arr,5)))
# #print(repetition_decoder(x,3))

def int_to_bin(x, b):
	output = zeros((b), dtype=int)
	while (x!=0):
		ex = floor(log2(x))
		output[-1-ex] = 1
		x -= 2**ex
	return output

def is_power_2(x):
	check = round(log2(x),5)
	return check.is_integer()


def generate_hamming_matrices(r):
	block_len = 2**r -1
	message_len = 2**r - r - 1
	# construct A
	A = []
	for i in range(block_len):
		if(not is_power_2(i+1)):
			A.append(i+1)
	bits=ceil(log2(max(A))) # works bc max(A) can't be a power of 2
	for i in range(len(A)):
		A[i] = int_to_bin(A[i], bits)
	A = array(A).T
	H = concatenate((A, eye(block_len-message_len, dtype=int)), axis=1)
	G = concatenate((eye(message_len, dtype=int), A.T), axis=1)
	return H, G



def hamming_encoder(x, r): 
	k=len(x) # num information bits
	block_len = 2**r -1
	message_len = 2**r - r - 1
	num_blocks=int(ceil(k/message_len))
	# must pad zeros to get to whole number of blocks
	data = concatenate((x ,zeros((block_len - (k%block_len)),dtype=int)))
	output = zeros((num_blocks*block_len),dtype=int) 
	print(num_blocks*block_len)
	print(k)
	H, G = generate_hamming_matrices(r)
	for i in range(num_blocks):
		output[i*block_len:(i+1)*block_len] = (data[i*message_len:(i+1)*message_len].dot(G)%2 + array([0,0,0,0,0,0,0])) % 2
	return output


def hamming_decoder(x, r):
	k=len(x) # num information bits
	block_len = 2**r -1
	message_len = 2**r - r - 1
	num_blocks=int(k/block_len)
	#print(num_blocks)
	output = zeros((num_blocks*message_len),dtype=int) 
	H, G = generate_hamming_matrices(r)
	for i in range(num_blocks):
		#print(x[i*block_len:(i+1)*block_len].T)
		syndrome = H.dot(x[i*block_len:(i+1)*block_len].T)%2
		# Error Case
		if(any(syndrome)): # executes when at least one value in the vector is non zero
			for j in range(block_len):
				if(all(syndrome == H[:,j])): # check syndrome against each column
					x[i*block_len + j] = (x[i*block_len + j] + 1) % 2 # correct error
		output[i*message_len:(i+1)*message_len] = x[i*block_len:i*block_len + message_len]
	return output

print(bin_arr)
print('\n')
sent = hamming_encoder(bin_arr, 3)
print(sent)
print('\n')
decoded = hamming_decoder(sent, 3)
print(decoded)
print('\n')
print(all(decoded[:len(bin_arr)]==bin_arr))