from numpy import array,zeros,all,sum
from math import floor, log2
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


print(majority_rule(array([1,1,1,0,0])))

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
print(repetition_decoder(bin_arr,5))
print(repetition_decoder_0(bin_arr,5))
print(repetition_decoder(bin_arr,5)==repetition_decoder_0(bin_arr,5))
print(all(repetition_decoder(bin_arr,5)==repetition_decoder_0(bin_arr,5)))
#print(repetition_decoder(x,3))