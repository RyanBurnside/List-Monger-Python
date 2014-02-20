from Tkinter import *

root = Tk()
Text(root).pack()
top = Toplevel()
top.transient(root)
top.grab_set()
top.mainloop()
