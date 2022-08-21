import time


poly_coef = [] #decreasing degree ending with the constant
for i in range(1, 40):
	poly_coef.append(i)
x_0 = 10**100000



def polynomial(x, coef):
	degree = len(coef) - 1
	poly = coef[0] * (x**degree)
	for i in range(degree):
		poly += coef[i+1] * (x**(degree-1-i))
	return poly


def nested_polynomial(x, coef):
	degree = len(coef) - 1
	poly = coef[0]*x + coef[1]
	for i in range(degree - 1):
		poly = poly*x + coef[i+2]
	return poly


t_0 = time.time()
polynomial(x_0, poly_coef)
print(time.time()-t_0)
t_1 = time.time()
nested_polynomial(x_0, poly_coef)
print(time.time()-t_1)