from Tkinter import *

class FieldRadioDialog:
    # Creates a way to ask for a text value and also a boolean checkbox
    # text_var and check_value live inside the widget all GUI is temporary
    def __init__(self, label_text = "", check_label = ""):
        self.text_value = StringVar()
        self.text_value.set("")
        self.check_value = IntVar()
        self.check_value.set(0)
        self.label_text = label_text
        self.check_label = check_label
        self.x_out = True #this is how we tell if a user x'd out

    def ask(self):
        self.top = Toplevel()
        self.top.transient()

        self.label = Label(self.top, text = self.label_text).pack(side = TOP)
        self.entry = Entry(self.top, textvariable = self.text_value)
        self.entry.pack(side = TOP, fill = X)
        self.check_value.set(0)
        self.check = Checkbutton(self.top,
                                 variable = self.check_value,
                                 text = self.check_label)
        self.check.pack(side = TOP, expand = 0, anchor = NW, fill = NONE)
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
        self.x_out = False
        self.top.destroy()

def ask_with_option(label_text = "", check_label = ""):
    temp = FieldRadioDialog("Enter term: ", check_label)
    temp.ask()
    if temp.x_out == False:
        return (temp.text_value.get(), temp.check_value.get())
    else:
        return ("", 0)
