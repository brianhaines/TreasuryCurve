from tkinter import *
import XMLgetClass as XML

class App:


	def __init__(self, master):

		frame = Frame(master)
		frame.grid(column=0, row=0, columnspan=2, rowspan=12)

		self.button = Button(frame, text="CLOSE", fg="red", command=frame.quit)
		self.button.grid(row=13, column=0)

		#self.hi_there = Button(frame, text="Hello", command=self.say_hi)
		#self.hi_there.grid(row=13, column=1)

		#Get rates from the web
		self.xml = XML.curveGet()

		#Left Column
		Label(frame, text=self.xml.date[1][:10]).grid(row=0)
		Label(frame, text="TERM").grid(row=1)
		Label(frame, text="1 Month").grid(row=2)
		Label(frame, text="3 Month").grid(row=3)
		Label(frame, text="6 Month").grid(row=4)
		Label(frame, text="1 Year").grid(row=5)
		Label(frame, text="2 Year").grid(row=6)
		Label(frame, text="3 Year").grid(row=7)
		Label(frame, text="5 Year").grid(row=8)
		Label(frame, text="7 Year").grid(row=9)
		Label(frame, text="10 Year").grid(row=10)
		Label(frame, text="20 Year").grid(row=11)
		Label(frame, text="30 Year").grid(row=12)

		#Right Column
		Label(frame, text="RATE").grid(row=1, column=1)
		Label(frame, text=self.xml.month1[1]).grid(row=2, column=1)
		Label(frame, text=self.xml.month3[1]).grid(row=3, column=1)
		Label(frame, text=self.xml.month6[1]).grid(row=4, column=1)
		Label(frame, text=self.xml.year1[1]).grid(row=5, column=1)
		Label(frame, text=self.xml.year2[1]).grid(row=6, column=1)
		Label(frame, text=self.xml.year3[1]).grid(row=7, column=1)
		Label(frame, text=self.xml.year5[1]).grid(row=8, column=1)
		Label(frame, text=self.xml.year7[1]).grid(row=9, column=1)
		Label(frame, text=self.xml.year10[1]).grid(row=10, column=1)
		Label(frame, text=self.xml.year20[1]).grid(row=11, column=1)
		Label(frame, text=self.xml.year30[1]).grid(row=12, column=1)
    


	def say_hi(self):   
		self.v.set("Hellooooo!")
		self.s.set("Changed")

root = Tk()

app = App(root)

root.title("Treasury Yield Curve")
root.geometry('250x280')
root.mainloop()
root.destroy() # optional; see description below