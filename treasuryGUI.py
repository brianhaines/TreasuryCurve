import XMLgetClass as XML
import tkinter
import threading
import time

#x = XML.curveGet()
#print(x.id[1])
#print(x.month3[1])

class getCurveValues(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self._abort = False

	def run(self):
		#Things here:

		#while not self._abort:

			

	def abort(self):
		self._abort = True


class showTreasuryCurve(tkinter.Tk):
	"""
	"""
	def __init__(self, parent):
		tkinter.Tk.__init__(self, parent)
		self.parent = parent
		self.initialize()

	def initialize(self):
		self.grid()

		self.source_string = tkinter.StringVar()

		#Define the text box where the source folder path is displayed
		self.source = tkinter.Label(self, textvariable="1month or more if possible", anchor='w', fg='white', bg='blue')
		self.source.grid(row = 0, column = 0, sticky = 'W')
		self.source_string.set("1month")

		#Source button
		source_button = tkinter.Button(self, text="Retrieve Curve", command=self.getCurve())
		source_button.grid(row = 4, column = 1, sticky = 'W')

	def getCurve(self):
		self.worker = getCurveValues()
		self.worker.start()
		while self.worker.isAlive(): # We wait for the worker to stop.
			time.sleep(1)



if __name__=="__main__":
	app = showTreasuryCurve(None) #Here parent is None because this is the 
							 #first GUI element created
	app.title("Treasury Curve")
	app.mainloop()

