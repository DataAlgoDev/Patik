# import tkinter
from tkinter import messagebox
import customtkinter
import json

with open("data.json") as file:
    data = json.load(file)
    
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("green")

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        # self.wm_attributes("-transparentcolor", "white")  # Set the transparency color
        self.wm_attributes("-alpha", 0.9) 
        # Window structure
        self.title("Patik")
        self.geometry("700x600")
        self.resizable(height=True, width=True)

        # #############################
        # Configuring app grid pattern: root/main app window [4x4 grid : (0,0),(0,1),(1.0),(1,1)]
        # #############################

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1,weight=1)
        self.grid_rowconfigure(0,weight=0)

        # ###############
        # Creating frames
        # ###############

        # Sidebar frame
        self.frame1 = customtkinter.CTkFrame(self, corner_radius=10, width=220)
        # Sidebar frame => Progress bar frame
        self.progressbar_frame = customtkinter.CTkFrame(self.frame1, corner_radius=10, fg_color="transparent", height=50, width=300)
        # Sidebar frame => Progress bar frame => left
        self.progressbar_frame_left = customtkinter.CTkFrame(self.progressbar_frame, width=200, corner_radius=10, fg_color="transparent")
        # Sidebar frame => Progress bar frame => right
        self.progressbar_frame_right = customtkinter.CTkFrame(
                                                            self.progressbar_frame, corner_radius=10, fg_color="transparent", 
                                                            border_width=4, border_color="black")
        # Top frame
        self.frame2 = customtkinter.CTkFrame(self, height=50, corner_radius=0, fg_color="transparent")
        # Top frame => Project Title
        self.project_title = customtkinter.CTkLabel(self.frame2, text="Project 1", font=("Terminal", 50))
        # Bottom frame
        self.frame3 = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent", border_width=0)
        # Bottom frame => Inserter frame
        self.inserter_frame = customtkinter.CTkFrame(self.frame3, height=100, corner_radius=10, fg_color="black")

        # ######################################################
        # Grid configuration(Frames and Subframes) and placement
        # ######################################################

        # Sidebar frame
        self.frame1.rowconfigure((0,1), weight=1)
        # self.frame1.columnconfigure()
        self.frame1.grid(row=0, column=0, rowspan=2, padx=(5,2.5), pady=(5,2.5), sticky="nsew")
        # Progress bar grid configure
        self.progressbar_frame.rowconfigure((0,1), weight=0)
        self.progressbar_frame.columnconfigure((0,1), weight=0)
        # Progress bar frame placement
        self.progressbar_frame.grid(row=1,padx=(0,0), pady=(0,0), sticky="s")
        # Progress bar frame 'left' grid configure
        self.progressbar_frame_left.grid(row=1, column=0, sticky="s")
        # Progress text
        self.progress_text = customtkinter.CTkLabel(self.progressbar_frame_left, font=("Terminal", 10))
        self.progress_text.grid(padx=(5,5), pady=(0,0), sticky="sw")
        # Progress bar frame 'right' grid configure
        self.progressbar_frame_right.grid(row=1, column=1, sticky="s", pady=(5,5))
        self.progressbar = customtkinter.CTkProgressBar(self.progressbar_frame_right, width=160)
        # Progress bar placement
        self.progressbar.grid(padx=(5,5), pady=(5,5), sticky="se")

        # Top frame
        self.frame2.rowconfigure(0, weight=1)
        self.frame2.columnconfigure(0, weight=1)
        self.frame2.grid(row=0, column=1, padx=(2.5,5), pady=(5,25), sticky="nsew")
        # Top frame => Project title
        self.project_title.grid(padx=(10,0), sticky="w")

        # Bottom frame [4x4 grid]
        self.frame3.grid_rowconfigure(0, weight=0)
        self.frame3.grid_rowconfigure(1, weight=1)
        self.frame3.grid_columnconfigure((0,1), weight=1)
        self.frame3.grid(row=1, column=1, padx=(2.5,5), pady=(2.5,5), sticky="nsew")
        # Bottom frame => Inserter frame
        self.inserter_frame.rowconfigure(0, weight=0)
        self.inserter_frame.columnconfigure(0, weight=0)
        self.inserter_frame.columnconfigure((1,2), weight=1)
        self.inserter_frame.grid(row=0, columnspan=3, pady=(0,5), sticky="nsew")
        # Bottom frame => Inserter frame => Text box
        self.textbox = customtkinter.CTkEntry(self.inserter_frame, width=250, placeholder_text="Add new task", font=("Calibri",15, "bold"))
        self.textbox.bind("<Return>", lambda event : self.add_new_task())
        # Text box Placement
        self.textbox.grid(row=0, column=0, padx=(10, 0), pady=(10, 10), sticky="w")
        # Bottom frame => Inserter frame => Insert button
        self.insert_button = customtkinter.CTkButton(
                                                    self.inserter_frame, text="+ Add ", width=70, font=("Calibri",15, "bold"), 
                                                    command=self.add_new_task)
        # Insert button placement
        self.insert_button.grid(row=0, column=1, padx=(30, 0), pady=(10, 10), sticky="w")
        # Bottom frame => Inserter frame => Delete Button
        self.delete_button = customtkinter.CTkButton(
                                                    self.inserter_frame, text="Clear", width=80, fg_color="Crimson", 
                                                    font=("Calibri",15, "bold"), command=self.clear_all_tasks)
        # Delete Button placement
        self.delete_button.grid(row=0, column=2, padx=(0, 10), pady=(10, 10), sticky="e")
        # frame3 => task_display_frame
        self.task_display_frame = customtkinter.CTkScrollableFrame(
                                                                    self.frame3, corner_radius=10, fg_color="transparent", 
                                                                    scrollbar_button_color="black")
        # Bottom frame => Task display frame
        self.task_display_frame.rowconfigure(1, weight=0)
        self.task_display_frame.columnconfigure((0,1), weight=1)
        self.task_display_frame.grid(row=1, columnspan=2, pady=(5,0), sticky="nsew")

        # ########################
        # Functions and attributes
        # ########################

        # All Projects data from local file
        self.temp_data = globals()["data"]
        # List of taskbar key-value pair
        self.temp_data_list = self.temp_data["task_data"]
        # List for storing taskbar objects
        self.objects_list = list()

    # Appends a new task at the end
    def add_new_task(self):
        new_task = self.textbox.get()
        if new_task:
            self.temp_data_list.append({new_task: 0})
            row_number = len(self.temp_data_list) - 1
            self.task_maker(row_number)
            self.textbox.delete(first_index=0, last_index=30)
            self.progress_maker()

    # Removes selected task
    def remove_task(self, obj):
        object_row_number = obj.row_number

        del_obj = self.objects_list[object_row_number]
        del_obj.destruct()

        del self.temp_data_list[object_row_number]
        del self.objects_list[object_row_number]
        
        for index in range(object_row_number, len(self.objects_list)):
            obj = self.objects_list[index]
            self.forget_taskbar(obj)
            self.place_taskbar(obj, index)
        self.progress_maker()

    # Deletes all the taskbars in task_display_frame
    def clear_all_tasks(self):
        if not self.objects_list:
            return
        self.temp_data_list.clear()
        for obj in self.objects_list:
            obj.destruct()            
        self.objects_list.clear()
        self.progress_maker()

    # Checks the status of checkboxes
    def mark_checker(self, obj):
        for task, value in self.temp_data_list[obj.row_number].items():
            task, value = task, value
        if value:
            self.temp_data_list[obj.row_number][task], obj.value = 0, 0
        else:
            self.temp_data_list[obj.row_number][task], obj.value = 1, 1
        self.progress_maker()
            
    # Function to keep track of the progress
    def progress_maker(self):
        total_task_count = len(self.temp_data_list)
        completed_task_count = 0
        for item in self.temp_data_list:
            for value in item.values():
                completed_task_count += value
        if total_task_count:
            status = completed_task_count / total_task_count
        else:
            status = 0
        self.progressbar.set(value=status) # 0 to 1

        if status == 1:
            self.progressbar.configure(progress_color="lightgreen")
        elif 0.6 <= status < 1:
            self.progressbar.configure(progress_color="yellow")
        elif 0.25 <= status < 0.6:
            self.progressbar.configure(progress_color="orange")
        elif status < 0.25:
            self.progressbar.configure(progress_color="red")

        self.progress_text.configure(text=f"{completed_task_count}/{total_task_count}")

    # Task maker method : Creates task based on data from the local file
    def task_maker(self, row_number=None):
        if row_number:
            for task, value in self.temp_data_list[-1].items():
                task, value = task, value
                obj = Taskbar(self.task_display_frame, row_number, task, value)
                self.place_taskbar(obj, row_number)
                self.objects_list.append(obj)
        else:
            for row_number, dixnry in enumerate(self.temp_data_list):
                for task, value in dixnry.items():
                    task, value = task, value 

                obj = Taskbar(self.task_display_frame, row_number, task, value)
                self.place_taskbar(obj, row_number)
                self.objects_list.append(obj)

        self.progress_maker()

    # Releases the grid dependancies of a taskbar object
    def forget_taskbar(self, obj):
        obj.checkbox_frame.grid_forget()
        obj.checkbox.grid_forget()
        obj.task_del_button.grid_forget()

    # Places the taskbar object in frame
    def place_taskbar(self, obj, row_number):
        obj.row_number = row_number
        obj.checkbox_frame.grid(row=row_number, columnspan=2, padx=(0,10), pady=(5,0), sticky="nsew")
        obj.checkbox.grid(row=row_number, column=0, padx=(10, 0), pady=(10, 10), sticky="w")
        obj.task_del_button.grid(row=row_number, column=1, padx=(0, 10), pady=(0,0), sticky="e")
        
# For creating taskbar objects
class Taskbar():
    def __init__(self, task_display_frame,row_number, task, value):
        
        self.row_number = row_number
        self.task = task
        self.value = value

        self.checkbox_frame = customtkinter.CTkFrame(
                                                    task_display_frame, corner_radius=10, border_color="darkgray", 
                                                    border_width=1, fg_color="transparent")

        self.checkbox_frame.rowconfigure(0, weight=0)
        self.checkbox_frame.columnconfigure((0,1), weight=1)

        self.checkbox = customtkinter.CTkCheckBox(
                                                self.checkbox_frame, text=f"{task}", font=("Consolas", 18, "bold"), onvalue=1, offvalue=0, 
                                                command=lambda:app.mark_checker(self),checkbox_height=22, checkbox_width=22, 
                                                corner_radius=5, border_width=3, variable=customtkinter.IntVar(value=value))

        self.task_del_button = customtkinter.CTkButton(
                                                        self.checkbox_frame, text="-", width=10, font=("Calibri",15, "bold"), fg_color="black", 
                                                        corner_radius=10, command=lambda:app.remove_task(self), hover_color="crimson")
        
    # Destroys the taskbar frame and all child widgets
    def destruct(self):
        self.checkbox_frame.destroy()


if __name__ == "__main__":

    app = App()
    app.task_maker()

    def on_closing():
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            # save and close the file
            data["task_data"] = app.temp_data_list
            with open("data.json", "w") as file:
                json.dump(data, file, indent=4)

            app.destroy()  # Close the window
    app.protocol("WM_DELETE_WINDOW", on_closing)
    
    app.mainloop()