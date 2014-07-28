import XMLgetClass as XML
import tkinter
import threading
import time

x = XML.curveGet()
print(x.id[1])
print(x.month3[1])

class getCurveValues(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self._abort = False

	def run(self):
		#Things here:

		while not self._abort:
			next(self._nPhotos)

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

	def getCurve(self):
		self.worker = function(object)
		self.worker.start()
		while self.worker.isAlive(): # We wait for the worker to stop.
			time.sleep(1)





if __name__=="__main__":
	app = photosort_app(None) #Here parent is None because this is the 
							 #first GUI element created
	app.title("PhotoSorter")
	app.mainloop()

