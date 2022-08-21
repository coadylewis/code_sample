from math import *
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
# Coady Lewis Computer project
# 04-08-2021
# This Code implements the FDSOR method to find
# the potential distribution, and several parameters
# of a 2D cross-section microstrip transmission line


def calc_residual(pot,i,j,al=1,ep=1):
    # pot is the 2d potential array
    # constants
    c1 = 1/(2*(1+al**2))
    c2 = (2*(al**2))/(1+ep)
    if(j==0): # account for boundary
        return c1*(2*pot[i][1]+c2*(pot[i+1][0]+ep*pot[i-1][0]))-pot[i][j]
    else:
        return c1*(pot[i][j-1]+pot[i][j+1]+c2*(pot[i+1][j]+ep*pot[i-1][j]))-pot[i][j]


def rnd(val, d): # rounding
    if(val == None):
        return None
    return int(val*(10**d))/(10**d)


def capacitance(pot, sw, sh, al, ep=1, steps=1, finite=False):
    # pot is the 2d potential array
    # finite=True sets the strip width to 1 step
    # calculate capacitance using a rectangular contour integral
    # each sum represents a side of the rectangle
    sum1=0
    sum2=0
    sum3=0
    sum4=0
    # In each case below, the trapezoidal approximation is used
    for i in range(sw+1+steps+int(finite)):
        if(i==0 or i==(sw+steps+int(finite))):
            sum1+=0.5*al*ep*(pot[sh-steps-1][i]-pot[sh-steps+1][i])
            sum2+=0.5*al*(pot[sh+steps+1][i]-pot[sh+steps-1][i])
        else:
            sum1+=al*ep*(pot[sh-steps-1][i]-pot[sh-steps+1][i])
            sum2+=al*(pot[sh+steps+1][i]-pot[sh+steps-1][i])
    for i in range(sh-steps,sh+1):
        if(i==(sh-steps) or i==sh):
            sum3+=0.5*(1/al)*ep*(pot[i][sw+steps+1]-pot[i][sw+steps-1])
        else:
            sum3+=(1/al)*ep*(pot[i][sw+steps+1]-pot[i][sw+steps-1])
    for i in range(sh,sh+steps+1):
        if(i==sh or i==(sh+steps)):
            sum4+=0.5*(1/al)*(pot[i][sw+steps+1]-pot[i][sw+steps-1])
        else:
            sum4+=(1/al)*(pot[i][sw+steps+1]-pot[i][sw+steps-1])
    return (-1)*(sum1+sum2+sum3+sum4)


def plot(pot): # plots potential distribution from 2d list
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    # Construct data
    X = []
    Y = []
    for i in range(len(pot)):
        X.append(i)
    for i in range(len(pot[0])):
        Y.append(i)
    X,Y = np.meshgrid(Y,X)
    Z=np.array(pot)
    # Plot the surface.
    surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm, linewidth=0, antialiased=False)
    ax.set_zlim(0, 1)
    plt.show()


def printdist(x,dec=-1):
    #prints matrix with row 0 at the bottom
    for i in range(len(x)-1,-1,-1):
        print(x[i])



def getUserInput():
    # This function gets the problem's parameters from the user
    # and ensures the inputs are of the correct type to proceed
    # without stopping the program.
    out = []
    #
    # Get w/d
    print('\n\nEnter w/d as a ratio of integers')
    while (True):
        try:
            hold = int(input('\n\nEnter the numerator: '))
            while (hold < 1):
                print('\n\nERROR: Input must be positive')
                hold = int(input('\n\nEnter the numerator: '))
            out.append(hold)
            break
        except ValueError:
            print('\n\nERROR: Input must be an integer')
    while (True):
        try:
            hold = int(input('\n\nEnter the denominator: '))
            while (hold < 1):
                print('\n\nERROR: Input must be positive')
                hold = int(input('\n\nEnter the denominator: '))
            out.append(hold)
            break
        except ValueError:
            print('\n\nERROR: Input must be an integer')
    #
    # Get b/d and check that b > d
    print('\n\nEnter b/d as a ratio of integers')
    while (True):
        try:
            hold = int(input('\n\nEnter the numerator: '))
            while (hold < 2):
                # conflict of boundary conditions
                print('\n\nERROR: Input must be at least 2')
                hold = int(input('\n\nEnter the numerator: '))
            out.append(hold)
            break
        except ValueError:
            print('\n\nERROR: Input must be an integer')
    while (True):
        try:
            hold = int(input('\n\nEnter the denominator: '))
            while (hold < 1 or hold >= out[2]):
                print('\n\nERROR: Input must be positive and less than the numerator')
                hold = int(input('\n\nEnter the denominator: '))
            out.append(hold)
            break
        except ValueError:
            print('\n\nERROR: Input must be an integer')
    #
    # Get a/w and check that a > w
    print('\n\nEnter a/w as a ratio of integers')
    while (True):
        try:
            hold = int(input('\n\nEnter the numerator: '))
            while (hold < 2):
                # conflict of boundary conditions
                print('\n\nERROR: Input must be at least 2')
                hold = int(input('\n\nEnter the numerator: '))
            out.append(hold)
            break
        except ValueError:
            print('\n\nERROR: Input must be an integer')
    while (True):
        try:
            hold = int(input('\n\nEnter the denominator: '))
            while (hold < 1 or hold >= out[4]):
                print('\n\nERROR: Input must be positive and less than the numerator')
                hold = int(input('\n\nEnter the denominator: '))
            out.append(hold)
            break
        except ValueError:
            print('\n\nERROR: Input must be an integer')
    #
    # Get n_a
    while (True):
    # To position the strip in the mesh, (w/a)*n_a must be an integer
    # check that (w*n_a)%a == 0
        try:
            hold = int(input('\n\nEnter n_a: '))
            while ((hold * out[5]) % out[4] != 0):
                print('\n\nERROR: Entered n_a does not place the end of the strip at a mesh point')
                hold = int(input('\n\nEnter n_a: '))
            while (hold < 1):
                print('\n\nERROR: n_a must be positive')
                hold = int(input('\n\nEnter n_a: '))
            out.append(hold)
            break
        except ValueError:
            print('\n\nERROR: n_a must be an integer')
    #
    # Get n_b
    while (True):
    # To position the strip in the mesh, (d/b)*n_b must be an integer
    # check that (d*n_b)%b == 0
        try:
            hold = int(input('\n\nEnter n_b: '))
            while ((hold * out[3]) % out[2] != 0):
                print('\n\nERROR: Entered n_b does not place the strip in the mesh')
                hold = int(input('\n\nEnter n_b: '))
            while (hold < 1):
                print('\n\nERROR: n_b must be positive')
                hold = int(input('\n\nEnter n_b: '))
            out.append(hold)
            break
        except ValueError:
            print('\n\nERROR: n_b must be an integer')
    #
    # Get epsilon_r
    while (True):
        try:
            hold = float(input('\n\nEnter epsilon_r: '))
            while (hold <= 0):
                print('\n\nERROR: epsilon_r must be positive')
                hold = float(input('\n\nEnter epsilon_r: '))
            out.append(hold)
            break
        except ValueError:
            print('\n\nERROR: epsilon_r must be a number')
    #
    # Check if a 3d plot is to be generated
    hold = input('\n\nWould you like to to generate and display a 3-D plot of the potential distribution on the specified grid? (y/n): ')
    while (hold != 'Y' and hold != 'y' and hold != 'N' and hold != 'n'):
        print('\n\nERROR: Please answer (y/n)')
        hold = input('\n\nWould you like to to generate and display a 3-D plot of the potential distribution on the specified grid? (y/n): ')
    if hold == 'Y' or hold == 'y':
        out.append(True)
    else:
        out.append(False)
    #
    # Check if the strip is to have finite thickness k.
    hold = input('\n\nWould you like to model a strip of finite thickness k? (y/n): ')
    while (hold != 'Y' and hold != 'y' and hold != 'N' and hold != 'n'):
        print('\n\nERROR: Please answer (y/n)')
        hold = input('\n\nWould you like to model a strip of finite thickness k? (y/n): ')
    if hold == 'Y' or hold == 'y':
        out.append(True)
    else:
        out.append(False)
    print('\n\n')
    #
    return out


# main (comment out the test cases when using user input)
#para = getUserInput()
#test cases
para = [3,1,2,1,3,1,60,60,1,True,False]
#para = [3,1,2,1,3,1,120,120,1,False,False]
#para = [3,1,2,1,3,1,240,240,1,False,False]
#para = [3,1,2,1,3,1,480,480,1,False,False]
#Line2
#para = [3,1,10,1,3,1,60,60,1,True,False]
#para = [3,1,10,1,3,1,120,120,1,False,False]
#para = [3,1,10,1,3,1,240,240,1,False,False]
#para = [3,1,10,1,3,1,480,480,1,False,False]
#Line3
#para = [3,1,10,1,3,1,60,60,10,True,False]
#para = [3,1,10,1,3,1,120,120,10,False,False]
#para = [3,1,10,1,3,1,240,240,10,False,False]
#para = [3,1,10,1,3,1,480,480,10,False,False]
#Bonus Finite
#para = [5,12,25,12,10,1,50,25,2.3,True, True]
#para = [5,12,25,12,10,1,50,25,1,False, True]


f=para[10]
alpha = (para[7]/para[6])*(para[4]/para[5])*(para[0]/para[1])*(para[3]/para[2])
n_a = para[6]
n_b = para[7]
omega_opt = 2 * (1-(pi/sqrt(2))*sqrt((1/(n_a**2))+(1/(n_b**2))))
tol = 10**(-5)
strip_height = (para[3]*n_b)//para[2]
strip_width = (para[5]*n_a)//para[4]
# indexing: [row][column] with row 0 at the lower boundary in the
# substrate region and column zero at the left side of the cutout
potential = []
for i in range(n_b+1):
    potential.append([])
    for j in range(n_a+1):
        potential[i].append(0)
        if((i == strip_height and j <= strip_width) or (i == (strip_height+int(f)) and j <= strip_width)):
            potential[i][j] = 1
residual = []
for i in range(n_b+1):
    residual.append([])
    for j in range(n_a+1):
        residual[i].append(None)


#iteration
rmax=1
iterations=0
while(rmax > tol):
    rmax=0
    if(iterations==1000):
        break
    for i in range(1,len(potential)-1):
        for j in range(len(potential[i])-1):
            if((i == strip_height and j <= strip_width) or (i == (strip_height+int(f)) and j <= strip_width)):
                continue
            if(i == strip_height):
                residual[i][j]=calc_residual(potential,i,j,alpha,para[8])
            else:
                residual[i][j]=calc_residual(potential,i,j,alpha)
            if(abs(residual[i][j])>rmax):
                rmax=abs(residual[i][j])
            potential[i][j] += omega_opt*residual[i][j]
    iterations+=1
print('\n\n')
print('Final Maximum Residual: '+str(rmax))
print('\n\n')
print('Total Iterations: '+str(iterations))
print('\n\n')
print('Calculated Capacitance: '+str(capacitance(potential,strip_width,strip_height,alpha,para[8])))
print('\n\n')
print('Omega_opt: '+str(omega_opt))
print('\n\n')
if(para[9]):
    plot(potential)
