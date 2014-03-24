from Tkinter import *

class SearchDialog:
    # Creates a way to ask for a text value and also a boolean checkbox
    # text_var and use_regex_check live inside the widget all GUI is temporary
    def __init__(self, label_text = ""):
        self.text_value = StringVar()
        self.text_value.set("")
        self.use_regex_check = IntVar()
        self.use_regex_check.set(0)
        self.match_case = IntVar()
        self.match_case.set(1)
        self.match_whole_word = IntVar()
        self.match_whole_word.set(0)
        self.wrap_around = IntVar()
        self.wrap_around.set(1)
        self.direction_var = IntVar()
        self.direction_var.set(1)

        self.label_text = label_text
        self.x_out = True #this is how we tell if a user x'd out

    def ask(self):
        self.top = Toplevel()
        self.top.transient()
        #self.top.geometry('300x128+320+120')
        self.label = Label(self.top, text = self.label_text).pack(side = TOP)
        self.entry = Entry(self.top, textvariable = self.text_value)
        self.entry.pack(side = TOP, fill = X)
        self.use_regex_check.set(0)
        self.check = Checkbutton(self.top,
                                 variable = self.use_regex_check,
                                 text = "Use Regex")
        self.check.pack(side = TOP, expand = 0, anchor = NW, fill = NONE)

        self.match_case_check = Checkbutton(self.top,
                                            variable = self.match_case,
                                            text = "Match Case")
        self.match_case_check.pack(side = TOP, expand = 0, 
                                   anchor = NW, fill = NONE)
        
        self.match_word_check = Checkbutton(self.top,
                                            variable = self.match_whole_word,
                                            text = "Match Whole Word")
        self.match_word_check.pack(side = TOP, expand = 0, 
                                   anchor = NW, fill = NONE)
        
        
        self.wrap_around_check = Checkbutton(self.top,
                                            variable = self.wrap_around,
                                            text = "Wrap Around")
        self.wrap_around_check.pack(side = TOP, expand = 0, 
                                   anchor = NW, fill = NONE)

        self.search_frame = LabelFrame(self.top, text = "Search Direction",
                                       padx = 5, pady = 5)

        self.search_frame.pack(side = TOP, expand = 1, 
                               anchor = NW, fill = X)

        self.direction_beginning = Radiobutton(self.search_frame, 
                                               text = "From Beginning",
                                               variable = self.direction_var,
                                               value = 0)
        self.direction_beginning.pack(side = TOP, expand = 0, 
                                   anchor = NW, fill = NONE)

        self.direction_up = Radiobutton(self.search_frame, text = "Search Up",
                                        variable = self.direction_var,
                                        value = 1)

        self.direction_up.pack(side = TOP, expand = 0, 
                                   anchor = NW, fill = NONE)

        self.direction_down = Radiobutton(self.search_frame,
                                          text = "Search Down",
                                          variable = self.direction_var,
                                          value = 2)

        self.direction_down.pack(side = TOP, expand = 0, 
                                   anchor = NW, fill = NONE)

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

def ask_search(label_text = ""):
    temp = SearchDialog("Enter Search term: ")
    temp.ask()
    if temp.x_out == False:
        # Returns term, regular expression, case, word, wrap, direction
        return (temp.text_value.get(), temp.use_regex_check.get(),
                temp.match_case, temp.match_whole_word, temp.wrap_around,
                temp.direction_var)
    else:
        return False
