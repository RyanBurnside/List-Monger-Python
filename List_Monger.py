from Tkinter import *
import Pmw
import tkFileDialog
import tkMessageBox
import tkSimpleDialog
import tkColorChooser

import re
from collections import OrderedDict #dup removal
from FieldRadioDialog import *
from SetSelectorDialog import *

root = Tk()
root.title("List Monger")
menubar = Menu(root)
root.config(menu = menubar)

# Some config globals
TEXT_INSERTBACKGROUND = "Gray20"
TEXT_BACKGROUND = "Ivory"
TEXT_FOREGROUND = "Gray20"
TEXT_HIGHLIGHTCOLOR = "White" 
TEXT_SELECTBACKGROUND = "DeepSkyBlue"
TEXT_SELECTFOREGROUND = "White"

class Program:
    def __init__(self, master):
        self.frame = Frame(master)
        self.frame.pack(expand = 1, fill = BOTH)
        self.notebook = Pmw.NoteBook(self.frame,
                                     hull_width = 640,
                                     hull_height = 480)
        self.notebook.pack(expand = 1, fill = BOTH)
        self.status_text = StringVar()
        self.status = Entry(self.frame, 
                            textvar = self.status_text).pack(side = BOTTOM,
                                                             fill = X)
        self.pages_list = {} # Stores page widgets's ScrolledText by name
        
    def add_new_page(self, title = ""):
        # validate in keyword
        while title in self.pages_list:
            title += "+"

        tab_n = title
        if title == "":
             tab_n = "List " + str(len(self.notebook.pagenames()))
        self.notebook.add(tab_n)
        self.pages_list[tab_n] = Pmw.ScrolledText(self.notebook.page(tab_n),
                                                  text_insertbackground = 
                                                  TEXT_INSERTBACKGROUND,
                                                  text_background = 
                                                  TEXT_BACKGROUND,
                                                  text_foreground = 
                                                  TEXT_FOREGROUND,
                                                  text_highlightcolor = 
                                                  TEXT_HIGHLIGHTCOLOR,
                                                  text_selectbackground = 
                                                  TEXT_SELECTBACKGROUND,
                                                  text_selectforeground = 
                                                  TEXT_SELECTFOREGROUND,
                                                  text_undo = 1,
                                                  text_maxundo = 30,
                                                  text_wrap = NONE)
        self.pages_list[tab_n].pack(expand = 1, fill = BOTH)
        self.notebook.selectpage(tab_n)

    def delete_page(self, tab_name):
        # This should ALWAYS be used to remove a tab, it clears the list too
        self.notebook.delete(tab_name)
        del self.pages_list[tab_name]

# Make our program instance
a = Program(root)
a.add_new_page()

file_menu = Menu(menubar, tearoff = 1)
operations_menu = Menu(menubar, tearoff = 1)
compare_menu = Menu(menubar, tearoff = 1)

# Functions
def add_a_tab(title = ""):
    global a
    a.add_new_page(title)

def del_a_tab(title = ""):
    global a        
    current = a.notebook.getcurselection()
    a.delete_page(current)

def open_file():
    # TODO doesn't handle filenames with '_'
    # TODO cancel breaks
    file = tkFileDialog.askopenfilename()
    if file != "":
        global a
        f = open(file)
        a.add_new_page(file.replace("_","?"))
        current = a.notebook.getcurselection()
        a.pages_list[current].settext(f.read())

def insert_file():
    # TODO doesn't handle filenames with '_'
    # TODO cancel breaks
    global a
    if len(a.pages_list) > 0:
        file = tkFileDialog.askopenfilename()
        if file != "":
            f = open(file)
            current = a.notebook.getcurselection()
            orig = a.pages_list[current].settext(
                a.pages_list[current].getvalue() +
                f.read())

def save_file():
    # TODO doesn't handle filenames with '_'
    # TODO cancel breaks
    global a
    if len(a.pages_list) > 0:
        file = tkFileDialog.asksaveasfilename(defaultextension = ".txt")
        if file != "":
            f = open(file, "w")
            current = a.notebook.getcurselection()
            f.write(a.pages_list[current].getvalue())


def warn_not_implimented():
    tkMessageBox.showinfo("Warning", "This functionality is not implimented")

def end_program():
    global root
    root.quit()

def find():
    global a
    current = a.notebook.getcurselection()
    
def count_lines():
    global a
    current = a.notebook.getcurselection()
    mod_list = a.pages_list[current].get().split('\n')
    num_valid_lines = 0
    for i in mod_list:
        if i != "":
            num_valid_lines += 1
    num_newlines = a.pages_list[current].get()
    num_newlines = num_newlines.count("\n")
    message_string = ("There are " + str(num_valid_lines) +
                      " valid items \n in " + 
                      str(num_newlines) + 
                      " total lines.") 
    tkMessageBox.showinfo(message = message_string)

def list_to_line():
    seperator = tkSimpleDialog.askstring("", "Enter seperator:")
    if seperator != "":
        global a
        current = a.notebook.getcurselection()
        mod_list = a.pages_list[current].get().split('\n')
        for i in xrange(len(mod_list)):
            if mod_list[i] != "\n" and mod_list[i] != "":
                mod_list[i] = mod_list[i] + seperator
        a.pages_list[current].settext("".join(mod_list))

def line_to_list():
    seperator = tkSimpleDialog.askstring("", "Enter seperator:")
    if seperator != "":
        global a
        current = a.notebook.getcurselection()
        mod_list = a.pages_list[current].get().split(seperator)
        new_list = []
        for i in xrange(len(mod_list)):
            if mod_list[i] != "\n" and mod_list[i] != "":
                new_list.append(mod_list[i])
        a.pages_list[current].settext("\n".join(new_list))

def trim_whitespace():
    global a
    current = a.notebook.getcurselection()
    mod_list = a.pages_list[current].get().split('\n')
    final_list = []
    for i in mod_list:
        if i != "":
            final_list.append(i.strip())
    a.pages_list[current].settext("\n".join(final_list))

def sort_lines():
    global a
    current = a.notebook.getcurselection()
    mod_list = a.pages_list[current].get().split('\n')
    final_list = []
    mod_list.sort()
    for i in mod_list:
        if i != "":
            final_list.append(i)
    a.pages_list[current].settext("\n".join(final_list))

def reverse_lines():
    global a
    current = a.notebook.getcurselection()
    mod_list = a.pages_list[current].get().split('\n')
    final_list = []
    for i in mod_list:
        if i != "":
            final_list.append(i)
    final_list.reverse()
    a.pages_list[current].settext("\n".join(final_list))

def remove_duplicate_lines():
    global a
    current = a.notebook.getcurselection()
    mod_list = a.pages_list[current].get().split('\n')
    mod_list = list(OrderedDict.fromkeys(mod_list))
    final_list = []
    for i in mod_list:
        if i != "":
            final_list.append(i)
    a.pages_list[current].settext("\n".join(final_list))

def remove_containing():
    result = ask_with_option("Enter term to match: ", "Use Regex")
    search = result[0]
    use_regex = result[1]
    if search != "":
        global a
        current = a.notebook.getcurselection()
        mod_list = a.pages_list[current].get().split('\n')
        final_list = []
        for i in xrange(len(mod_list)):
            if mod_list[i] != "\n" and mod_list[i] != "":
                if use_regex == 0: # Normal Search
                    if not search in mod_list[i]:
                        final_list.append(mod_list[i])
                else: # Regex search
                    if not re.search(search, mod_list[i]):
                        final_list.append(mod_list[i])                
        a.pages_list[current].settext("\n".join(final_list))

def keep_containing():
    result = ask_with_option("Enter term to match: ", "Use Regex")
    search = result[0]
    use_regex = result[1]
    if search != "":
        global a
        current = a.notebook.getcurselection()
        mod_list = a.pages_list[current].get().split('\n')
        final_list = []
        for i in xrange(len(mod_list)):
            if mod_list[i] != "\n" and mod_list[i] != "":
                if use_regex == 0: # Normal Search
                    if search in mod_list[i]:
                        final_list.append(mod_list[i])
                else: # Regex search
                    if re.search(search, mod_list[i]):
                        final_list.append(mod_list[i])                
        a.pages_list[current].settext("\n".join(final_list))

def uppercase_lines():
    global a
    current = a.notebook.getcurselection()
    mod_string = a.pages_list[current].get().upper()
    a.pages_list[current].settext(mod_string.rstrip())

def lowercase_lines():
    global a
    current = a.notebook.getcurselection()
    mod_string = a.pages_list[current].get().lower()
    a.pages_list[current].settext(mod_string.rstrip())

def capitalize_lines():
    global a
    current = a.notebook.getcurselection()
    mod_list = a.pages_list[current].get().split('\n')
    for i in xrange(len(mod_list)):
        mod_list[i] = mod_list[i].capitalize()
    a.pages_list[current].settext("\n".join(mod_list).rstrip())

def quote_lines():
    quote = tkSimpleDialog.askstring("", "Enter quote mark: ")
    if quote != "":
        global a
        current = a.notebook.getcurselection()
        mod_list = a.pages_list[current].get().split('\n')
        for i in xrange(len(mod_list)):
            if mod_list[i] != "\n" and mod_list[i] != "":
                mod_list[i] = quote + mod_list[i] + quote
        a.pages_list[current].settext("\n".join(mod_list).rstrip())

def prefix_lines():
    prefix = tkSimpleDialog.askstring("", "Enter prefix: ")
    if prefix != "":
        global a
        current = a.notebook.getcurselection()
        mod_list = a.pages_list[current].get().split('\n')
        for i in xrange(len(mod_list)):
            if mod_list[i] != "\n" and mod_list[i] != "":
                mod_list[i] = prefix + mod_list[i]
        a.pages_list[current].settext("\n".join(mod_list).rstrip())

def suffix_lines():
    suffix = tkSimpleDialog.askstring("", "Enter suffix: ")
    if suffix != "":
        global a
        current = a.notebook.getcurselection()
        mod_list = a.pages_list[current].get().split('\n')
        final_list = []
        for i in xrange(len(mod_list)):
            if mod_list[i] != "\n" and mod_list[i] != "":
                final_list.append(mod_list[i] + suffix)
                
        a.pages_list[current].settext("\n".join(final_list).rstrip())

def strip_prefix():
    result = ask_with_option("Enter term to match: ", "Use Regex")
    search = result[0]
    use_regex = result[1]
    if search != "":
        global a
        current = a.notebook.getcurselection()
        mod_list = a.pages_list[current].get().split('\n')
        final_list = []
        compiled_regex = re.compile(search)
        for i in xrange(len(mod_list)):
            if mod_list[i] != "\n" and mod_list[i] != "":
                if use_regex == 0: # Normal Search
                    if mod_list[i].startswith(search):
                        new_value = mod_list[i][len(search):]
                        final_list.append(new_value)
                    else:
                        final_list.append(mod_list[i])
                else: # Regex search
                    match = compiled_regex.match(mod_list[i])
                    if match:
                        temp = match.group(0)
                        if mod_list[i].startswith(temp):
                            new_value = mod_list[i][len(temp):]
                            final_list.append(new_value)
                    else:
                        final_list.append(mod_list[i])
        a.pages_list[current].settext("\n".join(final_list))


def strip_suffix():
    result = ask_with_option("Enter term to match: ", "Use Regex")
    search = result[0]
    use_regex = result[1]
    if search != "":
        global a
        current = a.notebook.getcurselection()
        mod_list = a.pages_list[current].get().split('\n')
        final_list = []
        compiled_regex = re.compile(search)
        for i in xrange(len(mod_list)):
            if mod_list[i] != "\n" and mod_list[i] != "":
                if use_regex == 0: # Normal Search
                    if mod_list[i].endswith(search):
                        keep_length = len(mod_list[i]) - len(search)
                        new_value = mod_list[i][:keep_length]
                        final_list.append(new_value)
                    else:
                        final_list.append(mod_list[i])
                else: # Regex search
                    match = compiled_regex.findall(mod_list[i])
                    if len(match) > 0:
                        temp = match[-1]
                        if mod_list[i].endswith(temp):
                            keep_length = len(mod_list[i]) - len(temp)
                            new_value = mod_list[i][:keep_length]
                            final_list.append(new_value)
                        else:
                            final_list.append(mod_list[i])
                    else:
                        final_list.append(mod_list[i])
        a.pages_list[current].settext("\n".join(final_list))

def find_intersection():
    global a
    temp = ask_compare("List 1", "List 2", a.pages_list.keys())
    if temp[0] == "":
        return
    else:
        set_a = set(a.pages_list[temp[0]].get().split('\n'))
        set_b = set(a.pages_list[temp[1]].get().split('\n'))
        a.add_new_page("(" + temp[0] + " Intrsct " + temp[1] + ")")
        current = a.notebook.getcurselection()
        a.pages_list[current].settext("\n".join(set_a.intersection(set_b)))
        trim_whitespace()

def find_symmetric_difference():
    global a
    temp = ask_compare("List 1", "List 2", a.pages_list.keys())
    if temp[0] == "":
        return
    else:
        set_a = set(a.pages_list[temp[0]].get().split('\n'))
        set_b = set(a.pages_list[temp[1]].get().split('\n'))
        a.add_new_page("(" + temp[0] + " Sdif " + temp[1] + ")")
        current = a.notebook.getcurselection()
        a.pages_list[current].settext("\n".join(set_a.symmetric_difference(set_b)))
        trim_whitespace()

def find_compliment():
    global a
    temp = ask_compare("List 1", "List 2", a.pages_list.keys())
    if temp[0] == "":
        return
    else:
        set_a = set(a.pages_list[temp[0]].get().split('\n'))
        set_b = set(a.pages_list[temp[1]].get().split('\n'))
        a.add_new_page("(" + temp[0] + " Cmplmnt " + temp[1] + ")")
        current = a.notebook.getcurselection()
        a.pages_list[current].settext("\n".join(set_a.difference(set_b)))
        trim_whitespace()

def find_union():
    global a
    temp = ask_compare("List 1", "List 2", a.pages_list.keys())
    if temp[0] == "":
        return
    else:
        set_a = set(a.pages_list[temp[0]].get().split('\n'))
        set_b = set(a.pages_list[temp[1]].get().split('\n'))
        a.add_new_page("(" + temp[0] + " Unin" + temp[1] + ")")
        current = a.notebook.getcurselection()
        a.pages_list[current].settext("\n".join(set_a.union(set_b)))
        trim_whitespace()


file_menu.add_command(label = "New Tab", command = add_a_tab)
file_menu.add_command(label = "Destroy Selected Tab", command = del_a_tab)
file_menu.add_separator()
file_menu.add_command(label = "Open File", command = open_file)
file_menu.add_command(label = "Insert File", command = insert_file)
file_menu.add_command(label = "Export File", command = save_file)
file_menu.add_command(label = "Quit", command = end_program)
operations_menu.add_command(label = "Find", 
                            command = warn_not_implimented)
operations_menu.add_command(label = "Replace", 
                            command = warn_not_implimented)
operations_menu.add_command(label = "Count List", command = count_lines)
operations_menu.add_separator()
operations_menu.add_command(label = "List to Line", command = list_to_line)
operations_menu.add_command(label = "Line to List", command = line_to_list)
operations_menu.add_separator()
operations_menu.add_command(label = "Trim Whitespace", 
                            command = trim_whitespace)
operations_menu.add_command(label = "Sort", command = sort_lines)
operations_menu.add_command(label = "Reverse", command = reverse_lines)
operations_menu.add_separator()
operations_menu.add_command(label = "Remove Duplicates",
                            command = remove_duplicate_lines)
operations_menu.add_command(label = "Remove Containing",
                            command = remove_containing)
operations_menu.add_command(label = "Keep Containing", 
                            command = keep_containing)
operations_menu.add_separator()
operations_menu.add_command(label = "Uppercase", command = uppercase_lines)
operations_menu.add_command(label = "Lowercase", command = lowercase_lines)
operations_menu.add_command(label = "Capitalize", command = capitalize_lines)
operations_menu.add_separator()
operations_menu.add_command(label = "Quote", command = quote_lines)
operations_menu.add_command(label = "Add Prefix", command = prefix_lines)
operations_menu.add_command(label = "Add Suffix", command = suffix_lines)
operations_menu.add_command(label = "Remove Prefix", command = strip_prefix)
operations_menu.add_command(label = "Remove Suffix", command = strip_suffix)
operations_menu.add_separator()
operations_menu.add_command(label = "Slice Rectangle", 
                            command = warn_not_implimented)
operations_menu.add_command(label = "Keep Rectangle", 
                            command = warn_not_implimented)

compare_menu.add_command(label = "Find Intersection", 
                            command = find_intersection)
compare_menu.add_command(label = "Find Symmetric Difference", 
                            command = find_symmetric_difference)
compare_menu.add_command(label = "Find Compliment", 
                            command = find_compliment)
compare_menu.add_command(label = "Find Union", 
                            command = find_union)

menubar.add_cascade(label = "File", menu = file_menu)
menubar.add_cascade(label = "Operations", menu = operations_menu)
menubar.add_cascade(label = "Compare", menu = compare_menu)

root.mainloop()
