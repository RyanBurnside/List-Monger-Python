from Tkinter import *

class TwoFieldDialog:
    # Creates a way to ask for a text value and also a boolean checkbox
    # text_var and check_value live inside the widget all GUI is temporary
    def __init__(self, label_text = "", label_text2 = "",
                 initial_value1 = "", initial_value2 = ""):
        self.text_value = StringVar()
        self.text_value.set(initial_value1)
        self.text_value2 = StringVar()
        self.text_value2.set(initial_value2)
        self.label_text = label_text
        self.label_text2 = label_text2
        self.x_out = True #this is how we tell if a user x'd out

    def ask(self):
        self.top = Toplevel()
        self.top.transient()
        self.top.geometry('300x128+320+120')
        self.label = Label(self.top, text = self.label_text).pack(side = TOP)
        self.entry = Entry(self.top, textvariable = self.text_value)
        self.entry.pack(side = TOP, fill = X)
        self.label2 = Label(self.top, text = self.label_text2).pack(side = TOP)
        self.entry2 = Entry(self.top, textvariable = self.text_value2)
        self.entry2.pack(side = TOP, fill = X)
        self.ok = Button(self.top, text = "OK", command = self.p_ok)
        self.ok.pack(side = LEFT, anchor = SW)
        self.cancel = Button(self.top, text = "Cancel", 
                             command = self.p_cancel)
        self.cancel.pack(side = RIGHT, anchor = SE)
        self.top.wait_window()

    def p_ok(self):
        self.x_out = False
        self.top.destroy()

    def p_cancel(self):
        self.x_out = True
        self.top.destroy()

def ask_two_values(label_text = "", label_text2 = "", 
                   initial_value1 = "", initial_value2 = ""):
    temp = TwoFieldDialog(label_text, label_text2, 
                          initial_value1, initial_value2)
    temp.ask()
    if temp.x_out == False:
        return (temp.text_value.get(), temp.text_value2.get())
    else:
        return False

