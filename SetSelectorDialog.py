from Tkinter import *

class SetSelectorDialog:
    # Creates a way to ask for a text value and also a boolean checkbox
    # text_var and check_value live inside the widget all GUI is temporary
    def __init__(self, label_text1, label_text2, selection):
        self.menu_value1 = StringVar()
        self.menu_value1.set(selection[0])
        self.menu_value2 = StringVar()
        self.menu_value2.set(selection[0])
        self.label_text1 = label_text1
        self.label_text2 = label_text2
        self.x_out = True #this is how we tell if a user x'd out
        self.selection = selection

    def ask(self):
        self.top = Toplevel()
        self.top.transient()
        self.top.minsize(240, 120)
        
        
        self.selector1 = OptionMenu(self.top, self.menu_value1, 
                                    *self.selection)

        self.selector2 = OptionMenu(self.top, self.menu_value2, 
                                    *self.selection)
        
        self.label = Label(self.top, text = self.label_text1).pack(side = TOP)
        self.selector1.pack(side = TOP, fill = X)
        self.label2 = Label(self.top, text = self.label_text2).pack(side = TOP)
        self.selector2.pack(side = TOP, fill = X)

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

def ask_compare(label_text1 = "Select First", label_text2 = "Select Second",  
                selection = ("")):
    temp = SetSelectorDialog(label_text1, label_text2, selection)
    temp.ask()
    if temp.x_out == False:
        return (temp.menu_value1.get(), temp.menu_value2.get())
    else:
        return ("", 0)
