from muselsl import record
import os
import winsound

def muse_record(d): # Duration in seconds
	try:
		if __name__ == "__main__":
			# Note: stream must be active
			filename = os.path.join(os.getcwd(), "Demo1_Coady_h7.csv")
			record(duration=d, filename=filename)#,filename='current_rawdata.csv')
			# Note: will not execute until recording is finished
			print('Recording has ended')
	except:
		print('\n\nOof: Recording Failed\n\nCheck current_rawdata.csv to salvage any data\n\nGoodbye\n\n')
		exit()	


muse_record(600)
winsound.MessageBeep(-1)