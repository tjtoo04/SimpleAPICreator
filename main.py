#Useful Links:
#Cheat Sheet: https://www.geeksforgeeks.org/tkinter-cheat-sheet/
#Element Positioning Cheat Sheet: https://stackoverflow.com/questions/28089942/difference-between-fill-and-expand-options-for-tkinter-pack-method
#Tutorial: https://realpython.com/python-gui-tkinter/
#App layouts: https://github.com/TomSchimansky/CustomTkinter/wiki/App-structure-and-layout

from threading import Thread
from fastapi import HTTPException, Response
from pathlib import Path
import subprocess
import requests
from pydantic import BaseModel, ValidationError, create_model
import customtkinter as ctk
from tkinter.messagebox import showinfo


def change_page():
    management_page_div.tkraise()

def start_API_server():
    global base_model
    change_page()
    base_model = create_base_model()
    path = Path(__file__).parent.absolute()
    cmd = f'cd {path.as_posix()}' + '/src' + ' && uvicorn conn:app --reload'
    subprocess.run(cmd, shell=True)

#Run uvicorn in another thread
def threading():
    thread = Thread(target=start_API_server)
    thread.start()

def on_quit():
    root.destroy()
    requests.get("http://127.0.0.1:8000/shutdown")

#Used for creating a base model to do type checking for user inputs
def create_base_model():
    global value_datatype, optional1_datatype, optional2_datatype, optional3_datatype
    
    value_datatype = int if value_datatype_var.get() == "Integer" else float if value_datatype_var.get() == "Float" else str
    optional1_datatype = str if optional1_datatype_var.get() =="String" else int if optional1_datatype_var.get() == "Integer" else float if optional1_datatype_var.get() == 'Float' else None 
    optional2_datatype = str if optional2_datatype_var.get() =="String" else int if optional2_datatype_var.get() == "Integer" else float if optional2_datatype_var.get() == 'Float' else None
    optional3_datatype = str if optional3_datatype_var.get() =="String" else int if optional3_datatype_var.get() == "Integer" else float if optional3_datatype_var.get() == 'Float' else None

    new_base_model = create_model(f"Base model", id=(int, ...), category=(str, ...), value=(value_datatype, ...))
    return new_base_model

def show_values():
    value_datatype = value_datatype_var.get()
    optional1_datatype = optional1_datatype_var.get()
    optional2_datatype = optional2_datatype_var.get()
    optional3_datatype = optional3_datatype_var.get()

def on_focus_out(entry):
    if entry.get() == '': 
        entry.insert('0', 'Enter optional fields')

def get_data():
    data = requests.get(f"http://127.0.0.1:8000/").json()
    result_label.configure(text=data)

def update_data():
    if change_value_var.get() != "" and item_id_var.get() != "":
        id = int(item_id_var.get())
        change = change_value_var.get()
        update = requests.put(f"http://127.0.0.1:8000/items/{id}?value={change}")
        if update.status_code == 404:
            showinfo("Invalid Item ID", "Item ID does not exist!")
        else:
            showinfo("Successful", "Updated Successfully")
    else:
        showinfo("Invalid Parameters", "No parameters entered")

def delete_data():
    if deletion_id_var.get() != '':
        deletion_id = int(deletion_id_var.get())
        delete = requests.delete(f"http://127.0.0.1:8000/items/{deletion_id}")
        if delete.status_code == 404:
            showinfo("Invalid Item ID", "Item ID does not exist!")
        else:
            showinfo("Successful", "Deleted Successfully")
            print("Deleted")
    else:
        showinfo("Invalid Item ID", "No Item ID entered")

def upload_data():
    try:
        new_id = int(list(requests.get(f"http://127.0.0.1:8000/").json()['result'].keys())[-1]) + 1
        new_category = new_category_var.get()
        new_data = value_datatype(new_data_var.get())
        verified_data = dict(base_model(id=new_id, category=new_category, value = new_data))
        requests.post(f"http://127.0.0.1:8000/", json=verified_data).json()
        showinfo("Successful", "Uploaded Successfully")
    except ValueError:
        showinfo("Type Error", "Invalid data type!")

ctk.set_appearance_mode('Dark')
ctk.set_default_color_theme('dark-blue')

#Initialization
root = ctk.CTk()
root.geometry("1080x900")
root.grid_rowconfigure((0,1,2,3,4), weight=0)
root.grid_columnconfigure((0,1,2), weight=1)


#Frame
frame = ctk.CTkFrame(master=root)
frame.grid(row=0, column=1)

#Title
title = ctk.CTkLabel(master=frame, text="Simple API Creator")
title.grid(padx=10, pady=10)


#API Creation page
'''Need to get data type of value, optional fields'''

datatype_fill_div = ctk.CTkFrame(master=root)
datatype_fill_div.grid_rowconfigure((0,1,2,3,4,5,6), weight=0)
datatype_fill_div.grid_columnconfigure((0,1), weight=1)
datatype_fill_div.grid(row=1, column=1, padx=20, pady=20, sticky="nsew")


data_types = ['String', 'Integer', 'Float']
category_var = ctk.StringVar()
item_id_var = ctk.StringVar()
change_value_var = ctk.StringVar()
new_category_var = ctk.StringVar()
new_data_var = ctk.StringVar()
value_datatype_var = ctk.StringVar()
optional1_datatype_var = ctk.StringVar()
optional2_datatype_var = ctk.StringVar()
optional3_datatype_var = ctk.StringVar()
optional1_var = ctk.StringVar()
optional2_var = ctk.StringVar()
optional3_var = ctk.StringVar()
deletion_id_var = ctk.StringVar()


'''category_label = ctk.CTkLabel(master=datatype_fill_div, text="Category name: ", width=200, wraplength=200)
category_label.grid(row=2, column=0, padx=20, pady=20, sticky="ew")
category_entry = ctk.CTkEntry(master=datatype_fill_div, textvariable=category_var)
category_entry.grid(row=2, column=1, padx=20, pady=20, sticky="ew")'''

value_label = ctk.CTkLabel(master=datatype_fill_div, text="Choose data type of the data in the API (default String): ", width=200, wraplength=200)
value_label.grid(row=3, column=0, padx=20, pady=20, sticky="ew")
value_data_type_combobox = ctk.CTkComboBox(master=datatype_fill_div, variable=value_datatype_var, values = data_types)
value_data_type_combobox.grid(row=3, column=1, padx=20, pady=20, sticky="ew")

optional_entry1 = ctk.CTkEntry(master=datatype_fill_div, justify='center', textvariable=optional1_var)
optional_entry1.grid(row=4, column=0, padx=20, pady=20, sticky="ew")
optional1_data_type_combobox = ctk.CTkComboBox(master=datatype_fill_div, variable=optional1_datatype_var, values = data_types + ["None"])
optional1_data_type_combobox.grid(row=4, column=1, padx=20, pady=20, sticky="ew")

optional_entry2 = ctk.CTkEntry(master=datatype_fill_div, justify='center', textvariable=optional2_var)
optional_entry2.grid(row=5, column=0, padx=20, pady=20, sticky="ew")
optional2_data_type_combobox = ctk.CTkComboBox(master=datatype_fill_div, variable=optional2_datatype_var, values = data_types + ["None"])
optional2_data_type_combobox.grid(row=5, column=1, padx=20, pady=20, sticky="ew")


optional_entry3 = ctk.CTkEntry(master=datatype_fill_div, justify='center', textvariable=optional3_datatype_var)
optional_entry3.grid(row=6, column=0, padx=20, pady=20, sticky="ew")
optional3_data_type_combobox = ctk.CTkComboBox(master=datatype_fill_div, variable=optional3_var, values = data_types + ["None"])
optional3_data_type_combobox.grid(row=6, column=1, padx=20, pady=20, sticky="ew")

#Placeholder
optional_entry1.insert(0, "Enter optional field 1")
optional_entry1.bind("<FocusIn>", lambda args: optional_entry1.delete('0', 'end'))
optional_entry1.bind("<FocusOut>", lambda args: on_focus_out(optional_entry1))

optional_entry2.insert(0, "Enter optional field 2")
optional_entry2.bind("<FocusIn>", lambda args: optional_entry2.delete('0', 'end'))
optional_entry2.bind("<FocusOut>", lambda args: on_focus_out(optional_entry2))

optional_entry3.insert(0, "Enter optional field 3")
optional_entry3.bind("<FocusIn>", lambda args: optional_entry3.delete('0', 'end'))
optional_entry3.bind("<FocusOut>", lambda args: on_focus_out(optional_entry3))


next_button = ctk.CTkButton(master=datatype_fill_div, text='Next', command=threading)
next_button.grid(row=6, column=1, padx=20, pady=20, sticky="ew")

#API Management Page


management_page_div = ctk.CTkFrame(master=root)
management_page_div.grid_rowconfigure((0,1,2,3,4), weight=0)
management_page_div.grid_columnconfigure((0,1,2), weight=1)
management_page_div.grid(row=1, column=1, padx=20, pady=20, sticky="nsew")

label = ctk.CTkLabel(master=management_page_div, text="API Management Page", font = ('Helvetica', 18, 'bold'))
label.grid(row=0, column=0, pady=10, padx=20, sticky="w")

#Get Requests
get_req_label = ctk.CTkLabel(master=management_page_div, text="GET Request", font = ('Helvetica', 12, 'bold'))
get_req_label.grid(row=1, column=0, padx=20, pady=10, sticky="w")

result_text_label = ctk.CTkLabel(master=management_page_div, text="Result:")
result_text_label.grid(row=2, column=0, padx=20, sticky="w")

get_data_btn = ctk.CTkButton(master=management_page_div, text='Get data', command=get_data)
get_data_btn.grid(row=1, column=1, pady=10, padx=10, sticky="ew")

result_label = ctk.CTkLabel(master=management_page_div, text="", wraplength=200)
result_label.grid(row=2, column=1, pady=10, padx=10, sticky="ew")

#Update Requests
update_req_label = ctk.CTkLabel(master=management_page_div, text="Update Request", font = ('Helvetica', 12, 'bold'))
update_req_label.grid(row=3, column=0, padx=20, pady=10, sticky="w")

item_id_label = ctk.CTkLabel(master=management_page_div, text="ID of item you want to change:")
item_id_label.grid(row=4, column=0, padx=20, sticky="w")

wanted_change_label = ctk.CTkLabel(master=management_page_div, text="Change of value:")
wanted_change_label.grid(row=5, column=0, padx=20, sticky="w")

item_id = ctk.CTkEntry(master=management_page_div, justify='center', textvariable=item_id_var)
item_id.grid(row=4, column=1, padx=20, pady=20, sticky="ew")

change_value = ctk.CTkEntry(master=management_page_div, justify='center', textvariable=change_value_var)
change_value.grid(row=5, column=1, padx=20, pady=20, sticky="ew")

update_data_btn = ctk.CTkButton(master=management_page_div, text='Update data', command=update_data)
update_data_btn.grid(row=6, column=1, pady=10, padx=10, sticky="ew")

#Post Requests
post_req_label = ctk.CTkLabel(master=management_page_div, text="Post Request", font = ('Helvetica', 12, 'bold'))
post_req_label.grid(row=7, column=0, padx=20, pady=10, sticky="w")

new_category_label = ctk.CTkLabel(master=management_page_div, text="Category of new data:")
new_category_label.grid(row=8, column=0, padx=20, sticky="w")

new_data_label = ctk.CTkLabel(master=management_page_div, text="Values:")
new_data_label.grid(row=9, column=0, padx=20, sticky="w")

category_value = ctk.CTkEntry(master=management_page_div, justify='center', textvariable=new_category_var)
category_value.grid(row=8, column=1, padx=20, pady=20, sticky="ew")

data_value = ctk.CTkEntry(master=management_page_div, justify='center', textvariable=new_data_var)
data_value.grid(row=9, column=1, padx=20, pady=20, sticky="ew")

submit_data_btn = ctk.CTkButton(master=management_page_div, text='Submit data', command=upload_data)
submit_data_btn.grid(row=10, column=1, pady=10, padx=10, sticky="ew")

#Delete Requests
delete_req_label = ctk.CTkLabel(master=management_page_div, text="Delete Request", font = ('Helvetica', 12, 'bold'))
delete_req_label.grid(row=11, column=0, padx=20, pady=10, sticky="w")

deletion_id_label = ctk.CTkLabel(master=management_page_div, text="ID of item you want to delete:")
deletion_id_label.grid(row=12, column=0, padx=20, sticky="w")

deletion_id_entry = ctk.CTkEntry(master=management_page_div, justify='center', textvariable=deletion_id_var)
deletion_id_entry.grid(row=12, column=1, padx=20, pady=20, sticky="ew")

delete_data_btn = ctk.CTkButton(master=management_page_div, text='Delete data', command=delete_data)
delete_data_btn.grid(row=13, column=1, pady=10, padx=10, sticky="ew")

if __name__ == '__main__':
    datatype_fill_div.tkraise()
    root.protocol("WM_DELETE_WINDOW", on_quit)
    root.mainloop()