from live_analysis import eeg_live_analysis_from_updating_file
import LAGraph as lag
from multiprocessing import Pipe, Process


#reads values from shared pipe and sends values to FuncAnimation
class PipeReader(object):
    def __init__(self, conn):
        self.time = 0
        self.conn = conn

    def __call__(self):
        self.time += 1
        label = self.conn.recv()
        return [self.time, label]


if __name__ == "__main__":
    #create pipe between eeg live analysis process and live analysis graph process
    # la_send_conn_ksvm, lag_recv_conn_ksvm = Pipe()
    # pipe_reader_ksvm = PipeReader(lag_recv_conn_ksvm)
    # lag_process_ksvm = Process(target=lag.plot_live_analysis, args=(pipe_reader_ksvm, "KSVM", 50,))
    # lag_process_ksvm.start()

    # la_send_conn_nn, lag_recv_conn_nn = Pipe()
    # pipe_reader_nn = PipeReader(lag_recv_conn_nn)
    # lag_process_nn = Process(target=lag.plot_live_analysis, args=(pipe_reader_nn, "ANN", 50,))
    # lag_process_nn.start()

    la_send_conn_rcnn, lag_recv_conn_rcnn = Pipe()
    pipe_reader_rcnn = PipeReader(lag_recv_conn_rcnn)
    lag_process_rcnn = Process(target=lag.plot_live_analysis, args=(pipe_reader_rcnn, "RCNN", 12,))
    print("--starting RCNN graph process--")
    lag_process_rcnn.start()

    # conns = {"KSVM" : la_send_conn_ksvm, 
    #          "ANN"  : la_send_conn_nn}

    conns = {"RCNN": la_send_conn_rcnn}

    eeg_live_analysis_from_updating_file(conns=conns, filename="DemoDay1.csv", nhb=False, model_filename='PS_w1280a1280', seq_len=12)
    #lag_process_ksvm.join()
    #lag_process_nn.join()
    lag_process_rcnn.join()
    #lag_process_rcnn.close()