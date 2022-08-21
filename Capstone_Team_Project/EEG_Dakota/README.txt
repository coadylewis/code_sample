The main file for the arduino uno r3 is the Continuous_Run_of_DC1716 which is a modified version of Linear Technologies DC1716 file found on their website for the ADC
I have chosen for my circuit, the LTC2473. Using their library of files I was able to put together a simple sketch to continously run the sketch to take the analog
voltage from the circuit, convert it, and spit out the value in the python script labeled Python_serial_plotter.py.
