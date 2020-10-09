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
from TwoFieldDialog import *
from SearchDialog import *

# Some config globals
TEXT_INSERTBACKGROUND = "Gray10"
TEXT_BACKGROUND = "Lavender"#"Ivory"
TEXT_FOREGROUND = "Gray10"
TEXT_HIGHLIGHTCOLOR = "White" 
TEXT_SELECTBACKGROUND = "Steel Blue"#"DeepSkyBlue"
TEXT_SELECTFOREGROUND = "White"
VERSION = .9

root = Tk()
root.title("List Monger " + str(VERSION))
menubar = Menu(root, activebackground = TEXT_BACKGROUND)
root.config(menu = menubar)

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
        self.next_tab_number = 0
    def add_new_page(self):
        # validate in keyword
        self.next_tab_number += 1
        tab_n = "List " + str(self.next_tab_number)

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
        for title in self.pages_list:
            print title

# Make our program instance
a = Program(root)
a.add_new_page()

file_menu = Menu(menubar, tearoff = 1, activebackground = TEXT_BACKGROUND,
                 activeforeground = TEXT_FOREGROUND)
operations_menu = Menu(menubar, tearoff = 1, activebackground = TEXT_BACKGROUND,
                       activeforeground = TEXT_FOREGROUND)
compare_menu = Menu(menubar, tearoff = 1, activebackground = TEXT_BACKGROUND,
                    activeforeground = TEXT_FOREGROUND)
help_menu = Menu(menubar, tearoff = 1, activebackground = TEXT_BACKGROUND,
                 activeforeground = TEXT_FOREGROUND)

# Functions
def add_a_tab():
    global a
    a.add_new_page()

def del_a_tab():
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
        a.add_new_page()
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

def about():
    tkMessageBox.showinfo("Warning", "Ryan Burnside's List Monger version " +
                          str(VERSION) +
                          "\nReleased under GPL version 4")

def end_program():
    global root
    root.quit()

def get_current_tab():
    #Gets the current tab in the global notebook
    global a
    return a.notebook.getcurselection()

def get_current_tab_text_widget():
    # Gets the text widget associated with the current tab
    global a
    return a.pages_list[get_current_tab()]
    
def get_current_tab_text():
    # Gets the text associated with the current tab in the current notebook
    return get_current_tab_text_widget().get()

def get_list_from_current_tab():
    # Gets a list of lines from the current notebook tab
    return get_current_tab_text().splitlines()

def set_current_tab_text(text):
    get_current_tab_text_widget().settext(text)

def set_current_tab_list(l):
    if l:
        return set_current_tab_text("\n".join(str(n) for n in l))

def find():
    result = ask_with_option("Search Forward: ", "Use Regex")
    count = StringVar()
    count.set(0)
    box = get_current_tab_text_widget()
    index = box.search(result[0], INSERT, "end", regexp = (result[1] == 1),
                       count = count)
    
    if index != "":
        box.mark_set("insert", index)
        box.see(index)
        
def count_lines():
    mod_list = get_list_from_current_tab()
    tkMessageBox.showinfo(message="""There are {} non-blank items. 
    and {} lines.""".format(sum(0 if i == "" else 1 for i in mod_list),
                            len(mod_list) - 1))

def list_to_line():
    seperator = tkSimpleDialog.askstring("", "Enter seperator:")
    result = get_current_tab_text().replace("\n", seperator)
    set_current_tab_text(result)

def line_to_list():
    seperator = tkSimpleDialog.askstring("", "Enter seperator:")
    result = get_current_tab_text().replace(seperator, "\n")
    set_current_tab_text(result)

def trim_whitespace():
    set_current_tab_list([i.strip() for i in get_list_from_current_tab()])

def natural_sort(l): 
    """ Sort the given iterable in the way that humans expect-Mark Byers"""
    convert = lambda text: int(text) if text.isdigit() else text 
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)] 
    return sorted(l, key = alphanum_key)

def natural_sort_lines():
    set_current_tab_list(natural_sort(get_list_from_current_tab()))

def sort_lines():
    set_current_tab_list(sorted(get_list_from_current_tab()))
    
def reverse_lines():
    set_current_tab_list(get_list_from_current_tab()[::-1])

def remove_duplicate_lines():
    set_current_tab_list(list(OrderedDict.fromkeys(get_list_from_current_tab())))
    
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
    set_current_tab_list([i.upper() for i in get_list_from_current_tab()])

def lowercase_lines():
    set_current_tab_list([i.lower() for i in get_list_from_current_tab()])

def capitalize_lines():
    set_current_tab_list([i.capitalize() for i in get_list_from_current_tab()])

def SQL_lines():
    global a
    current = a.notebook.getcurselection()
    mod_list = a.pages_list[current].get().split('\n')
    for i in xrange(len(mod_list)):
        if mod_list[i] != "\n" and mod_list[i] != "":
            mod_list[i] = "'" + mod_list[i] + "',"
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
    # Try a compilation to ensure the regex is valid
    if use_regex != 0:
        try:
            compiled_regex = re.compile(search)
        except:
            return

    if search != "":
        global a
        current = a.notebook.getcurselection()
        mod_list = a.pages_list[current].get().split('\n')
        final_list = []
        compiled_regex = ""
        if use_regex != 0:
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
    # Try a compilation to ensure the regex is valid
    if use_regex != 0:
        try:
            compiled_regex = re.compile(search)
        except:
            return

    if search != "":
        global a
        current = a.notebook.getcurselection()
        mod_list = a.pages_list[current].get().split('\n')
        final_list = []
        compiled_regex = ""
        if use_regex != 0:
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

def slice_lines():
    global a
    collected = ask_two_values("First character position\n(blank and 0 are first index) ", 
                               "First ignored position \n(blank is end of line)", 
                               "", "")
    if collected:
        try: 
            collected = (int(collected[0]), collected[1])
        except ValueError:
            collected = (None, collected[1])

        try: 
            collected = (collected[0], int(collected[1]))
        except ValueError:
            collected = (collected[0], None)

        current = a.notebook.getcurselection()
        mod_list = a.pages_list[current].get().split('\n')
        final_list = []
        for i in mod_list:
            if i != "":
                final_list.append(i[collected[0]:collected[1]])
        a.pages_list[current].settext("\n".join(final_list))    

def find_intersection():
    global a
    temp = ask_compare("List 1", "List 2", a.pages_list.keys())
    if temp[0] == "":
        return
    else:
        set_a = set(a.pages_list[temp[0]].get().split('\n'))
        set_b = set(a.pages_list[temp[1]].get().split('\n'))
        a.add_new_page()
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
        a.add_new_page()
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
        a.add_new_page()
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
        a.add_new_page()
        current = a.notebook.getcurselection()
        a.pages_list[current].settext("\n".join(set_a.union(set_b)))
        trim_whitespace()

file_menu.add_command(label = "New List", command = add_a_tab)
file_menu.add_command(label = "Destroy Current List", command = del_a_tab)
file_menu.add_separator()
file_menu.add_command(label = "Open File", command = open_file)
file_menu.add_command(label = "Insert File", command = insert_file)
file_menu.add_command(label = "Export File", command = save_file)
file_menu.add_command(label = "Quit", command = end_program)
operations_menu.add_command(label = "Find", 
                            command = find)
operations_menu.add_command(label = "Replace", 
                            command = warn_not_implimented)
operations_menu.add_command(label = "Count List", command = count_lines)
operations_menu.add_separator()
operations_menu.add_command(label = "List to Line", command = list_to_line)
operations_menu.add_command(label = "Line to List", command = line_to_list)
operations_menu.add_separator()
operations_menu.add_command(label = "Trim Whitespace", 
                            command = trim_whitespace)
operations_menu.add_command(label = "Natural Sort", 
                            command = natural_sort_lines)
operations_menu.add_command(label = "ASCII Sort", command = sort_lines)
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
operations_menu.add_command(label = "SQL String List", command = SQL_lines)
operations_menu.add_command(label = "Quote", command = quote_lines)
operations_menu.add_command(label = "Add Prefix", command = prefix_lines)
operations_menu.add_command(label = "Add Suffix", command = suffix_lines)
operations_menu.add_command(label = "Remove Prefix", command = strip_prefix)
operations_menu.add_command(label = "Remove Suffix", command = strip_suffix)
operations_menu.add_separator()
operations_menu.add_command(label = "Keep Slice", 
                            command = slice_lines)

compare_menu.add_command(label = "Find Intersection", 
                            command = find_intersection)
compare_menu.add_command(label = "Find Symmetric Difference", 
                            command = find_symmetric_difference)
compare_menu.add_command(label = "Find Compliment", 
                            command = find_compliment)
compare_menu.add_command(label = "Find Union", 
                            command = find_union)

help_menu.add_command(label = "About",
                      command = about)

help_menu.add_command(label = "Concepts")

menubar.add_cascade(label = "File", menu = file_menu)
menubar.add_cascade(label = "Operations", menu = operations_menu)
menubar.add_cascade(label = "Compare", menu = compare_menu)
menubar.add_cascade(label = "Help", menu = help_menu)

root.mainloop()
