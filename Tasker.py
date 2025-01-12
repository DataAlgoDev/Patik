import customtkinter
import json

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("green")

app = customtkinter.CTk()

app.title("Tasker")
app.geometry("800x600")

title = customtkinter.CTkLabel(master=app, text="Project 1", font=customtkinter.CTkFont(size=30, weight="bold"))
title.place(relx="0.1", rely="0.1")

# delete_btn = customtkinter.CTkButton(master=app, text="Delete", width=80)
# delete_btn.place(relx="0.8", rely="0.05")


# Task adding box
textbox = customtkinter.CTkEntry(master=app, width=200, placeholder_text="Add new task")

textbox.place(relx="0.1", rely="0.2")

# Function to add new task
def add_new_task():
    new_data = textbox.get()
    with open("data.json", 'r') as file:
        data = json.load(file)
        if new_data:
            data[new_data] = 0
            textbox.delete(first_index=0, last_index=30)
    with open("data.json", "w") as file:
        json.dump(data, file, indent=4)
    task_maker()
        
# Clear all data
def clear_all_data():
    data = {}
    with open("data.json", "w") as file:
        json.dump(data, file, indent=4)
    for obj in checkbox_set:
        obj.destroy()   

add_btn = customtkinter.CTkButton(master=app, text="+ Add", width=80, command=add_new_task)
add_btn.place(relx="0.4", rely="0.2")

add_btn = customtkinter.CTkButton(master=app, text="Clear All", width=80, fg_color="Crimson", command=clear_all_data)
add_btn.place(relx="0.6", rely="0.2")

#Checkbox

# Event checker

checkbox_set = set()

def checkbox_event():
    for obj in checkbox_set:
        task = obj.cget("text")
        value = obj.get()
        # print(f"Check box {task} is now :", value)
        with open("data.json", 'r') as file:
            data = json.load(file)
            data[task] = value
        with open("data.json", "w+") as file:
            json.dump(data, file, indent=4)


def task_maker():
    y = 0.5
    i = 0
    with open('data.json', 'r') as file:
        data = json.load(file)
    # print(data)
    for task, value in data.items():
        obj = customtkinter.CTkCheckBox(master=app, text=f"{task}", font=customtkinter.CTkFont(size=15, weight="bold"), onvalue=1, offvalue=0, command=checkbox_event)
        obj.select() if value else obj.deselect()
        obj.place(relx="0.1", rely=str(y))
        checkbox_set.add(obj)
        y += 0.1
        i += 1
# checkbox_event()
# checkbox = customtkinter.CTkCheckBox(master=app, text=f"{textt}", font=customtkinter.CTkFont(size=15, weight="bold"), onvalue=1, offvalue=0, command=checkbox_event,)
task_maker()
app.mainloop()
