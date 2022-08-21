import matplotlib
matplotlib.use('TKAgg')
import matplotlib.pyplot as plt
from matplotlib import animation
import time
import random
from multiprocessing import Process

FONT_SIZE = 20

#class for live analysis graph
# - mode: either 'KSVM' or 'NN'
# - max_points_shown: maximum number of points shown on graph at any moment
class LAGraph:
    def __init__(self, mode="KSVM", max_points_shown=10):
        #class variables
        if "NN" in mode:
            self.mode = "NN"
        else:
            self.mode = mode
        self.max_points_shown = max_points_shown
        self.x_time = []    #time
        self.y_labels = []  #true label from model output
        self.y_bin = []     #binary label from NN
        self.fig = plt.figure()
        self.ax = plt.axes(xlim=(1, max_points_shown), ylim=(-0.02, 1.02))

        #configure graph labels
        self.ax.invert_yaxis()
        self.ax.set_yticks([0, 1])
        self.ax.set_yticklabels(["awake (0)", "drowsy (1)"])
        self.ax.set_xlabel("Classification #", fontsize=FONT_SIZE)
        self.ax.set_title(mode, fontsize=FONT_SIZE)

        #configure figure size
        self.fig.set_figwidth(12)
        self.fig.set_figheight(6)
        
        #configure font sizes
        plt.rcParams['font.size'] = FONT_SIZE
        for label in (self.ax.get_xticklabels() + self.ax.get_yticklabels()):
            label.set_fontsize(FONT_SIZE)
        
        #change graph color to black
        self.ax.set_facecolor('k')

        self.line, = self.ax.plot([], [], marker='o', lw=2)
        self.line_bin = None
        if self.mode == "NN":
            self.line_bin, = self.ax.plot([], [], marker='o', lw=2)
    
    #initializes empty graph
    def line_init(self):
        self.line.set_data([], [])
        if self.mode == "NN":
            self.line_bin.set_data([], [])
            self.ax.legend([self.line, self.line_bin], ["true output", "binary output"])
            return self.line, self.line_bin
        return self.line,

    
    def update(self, new_value):
        #graph plots all points in x_time and y_labels, so pop the oldest values when limit is reached
        if len(self.x_time) == self.max_points_shown:
            self.x_time.pop(0)
            self.y_labels.pop(0)
            self.mode == "NN" and self.y_bin.pop(0)
        self.x_time.append(new_value[0])
        self.y_labels.append(new_value[1])

        #set x-axis bounds to smallest and largest values in x_time list
        self.ax.set_xlim(min(self.x_time), max(max(self.x_time), self.max_points_shown))
        self.line.set_data(self.x_time, self.y_labels)
        if self.mode == "NN":
            self.y_bin.append(new_value[1] > 0.5)
            self.line_bin.set_data(self.x_time, self.y_bin)
            return self.line, self.line_bin
        return self.line,


#generator used to send values to FuncAnimation
class AddValues(object):
    def __init__(self):
        self.time = 0
        self.label = 0

    def __call__(self):
        time.sleep(0.5)
        self.time += 1
        self.label = random.randint(0, 1)
        return [self.time, self.label]


def plot_live_analysis(pipe_reader, mode="KSVM", max_points_shown=10):
    #add_values = AddValues()
    def frames():
        while True:
            #yield add_values()
            yield pipe_reader()

    graph = LAGraph(mode, max_points_shown)
    anim = animation.FuncAnimation(graph.fig, graph.update, init_func=graph.line_init, frames=frames)
    plt.show()


def other_program():
    for i in range(20):
        time.sleep(0.5)
        print(i)


if __name__ == "__main__":
    la_graph = Process(target=plot_live_analysis)
    la_graph.start()
    other_program()
    la_graph.join()