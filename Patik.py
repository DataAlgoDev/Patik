from tkinter import messagebox
import customtkinter
import json

# Setting environment variables
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("green")

# Main app
class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.wm_attributes("-alpha", 0.9) 
        # Window structure
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        width = 750
        height = 600
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.title("Patik")
        self.geometry(f"{width}x{height}+{x}+{y}")
        self.resizable(height=True, width=True)

        # #############################
        # Configuring app grid pattern: root/main app window [4x4 grid : (0,0),(0,1),(1.0),(1,1)]
        # #############################

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1,weight=1)
        self.grid_rowconfigure(0,weight=0)

        # ###########################################
        # Creating frames and placing them over grids
        # ###########################################

        # Sidebar frame
        self.frame1 = customtkinter.CTkFrame(self, corner_radius=10, width=300, fg_color="transparent")
        self.frame1.rowconfigure(2, weight=1)
        self.frame1.rowconfigure(1, weight=1, minsize=500)
        self.frame1.columnconfigure(0, weight=1, minsize=270)
        self.frame1.columnconfigure(1, weight=1)
        self.frame1.grid(row=0, column=0, rowspan=2, padx=(5,2.5), pady=(5,2.5), sticky="nsew")
        # Sidebar frame => New_project frame
        # New project button
        self.new_project_frame = customtkinter.CTkFrame(self.frame1, corner_radius=10, fg_color="transparent")
        self.new_project_frame.grid(row=0, sticky="nsew")
        self.new_project_frame.rowconfigure(0, weight=0)
        self.new_project_frame.columnconfigure(0, weight=1)
        self.new_project_button = customtkinter.CTkButton(
                                                    self.new_project_frame, text="New Project +", width=80, height=35, 
                                                    font=("Calibri",15, "bold"), command=self.create_helper, fg_color="transparent", border_color="darkgray", border_width=2)
        self.new_project_button.grid(row=0, padx=(10,10), pady=(20,10), sticky="news")
        self.input_box = None
        # Delete project button
        self.delete_project_button = customtkinter.CTkButton(
                                                    self.new_project_frame, text="Delete Project", width=80, height=35, 
                                                    font=("Calibri",15, "bold"), command=self.del_project, fg_color="transparent", border_color="darkgray", border_width=2, hover_color=("crimson"))
        self.delete_project_button.grid(row=1, padx=(10,10), pady=(10,20), sticky="nsew")
        self.deletion_window = None
        # Sidebar frame => Project_list frame
        self.project_list_frame = customtkinter.CTkScrollableFrame(self.frame1, corner_radius=10, fg_color="transparent", scrollbar_button_color="black")
        self.project_list_frame.rowconfigure(0, weight=1)
        self.project_list_frame.columnconfigure(0, weight=1)
        self.project_list_frame.grid(row=1, sticky="nsew")
        # Sidebar frame => Progress bar frame
        self.progressbar_frame = customtkinter.CTkFrame(self.frame1, corner_radius=0, fg_color="transparent", height=50, width=300)
        self.progressbar_frame.rowconfigure((0,1), weight=0)
        self.progressbar_frame.columnconfigure((0,1), weight=0)
        # Sidebar frame => Progress bar frame => left
        self.progressbar_frame_left = customtkinter.CTkFrame(self.progressbar_frame, width=200, corner_radius=10, fg_color="transparent")
        # Sidebar frame => Progress bar frame => right
        self.progressbar_frame_right = customtkinter.CTkFrame(
                                                            self.progressbar_frame, corner_radius=10, fg_color="transparent", 
                                                            border_width=4, border_color="black")
        # Progress text
        self.progress_text = customtkinter.CTkLabel(self.progressbar_frame_left, font=("Terminal", 10))
        self.progressbar = customtkinter.CTkProgressBar(self.progressbar_frame_right, width=160)
        # Top frame
        self.frame2 = customtkinter.CTkFrame(self, height=50, corner_radius=0, fg_color="transparent")
        self.frame2.rowconfigure(1, weight=0)
        self.frame2.columnconfigure(0, weight=0)
        self.frame2.grid(row=0, column=1, padx=(2.5,5), pady=(5,25), sticky="nsew")
        # Top frame => Project Title
        self.project_title = customtkinter.CTkLabel(self.frame2, text=None, font=("Terminal", 50))
        # Bottom frame
        self.frame3 = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent", border_width=0)
        self.frame3.grid_rowconfigure(0, weight=0)
        self.frame3.grid_rowconfigure(1, weight=1)
        self.frame3.grid_columnconfigure((0,1), weight=1)
        self.frame3.grid(row=1, column=1, padx=(2.5,5), pady=(2.5,5), sticky="nsew")
        # Bottom frame => Inserter frame
        self.inserter_frame = customtkinter.CTkFrame(self.frame3, height=100, corner_radius=10, fg_color="black")
        self.inserter_frame.rowconfigure(0, weight=0)
        self.inserter_frame.columnconfigure(0, weight=0)
        self.inserter_frame.columnconfigure((1,2), weight=1)
        self.inserter_frame.grid(row=0, columnspan=3, pady=(0,5), sticky="nsew")
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
        # Bottom frame => task_display_frame
        self.task_display_frame = customtkinter.CTkScrollableFrame(
                                                                    self.frame3, corner_radius=10, fg_color="transparent", 
                                                                    scrollbar_button_color="black")
        # Bottom frame => Task display frame
        self.task_display_frame.rowconfigure(1, weight=0)
        self.task_display_frame.columnconfigure((0,1), weight=1)
        self.task_display_frame.grid(row=1, columnspan=2, pady=(5,0), sticky="nsew")
        self.null_message = customtkinter.CTkLabel(self.task_display_frame, text="No tasks...", font=("Terminal", 20))

        # ######################
        # Methods and attributes
        # ######################
        # Main dictionary
        self.temp_data = globals()["data"]

    # Used during startup and on project deletion
    def full_init(self) -> None:
        # --------------
        # Main variables
        # --------------
        self.temp_project_names = list()
        for item in self.temp_data:
            self.temp_project_names.append(item)
        self.temp_data_list = list()
        # List for storing Project objects
        self.project_objects_list = list()
        # List for storing taskbar objects
        self.task_objects_list = list()

        self.curr_project_row = self.project_selector(len(self.temp_project_names) - 1)
        self.title_maker(self.curr_project)
        self.project_maker()
        self.task_maker()
        self.progress_bar_placer()

    # Used during project switching and when added new project
    def project_init(self, new_index : int) -> None:
        if not self.temp_project_names:
            return
        self.curr_project_row = self.project_selector(new_index)
        self.title_maker(self.curr_project)
        self.task_maker()
        self.progress_bar_placer()

    # To change title
    def title_maker(self, title : str = None) -> None:
        self.project_title.grid(padx=(10,0), sticky="w")
        if title:
            self.project_title.configure(text=title)
        else:
            self.project_title.configure(text="Begin...")

    def create_helper(self) -> None:
        if not self.input_box:
            self.input_box = CreateBox()
        self.input_box.update()
        self.input_box.focus()

    # Creates new project object
    def create_new_project(self, new_project : str) -> None:
        if new_project in self.temp_project_names:
            return
        self.temp_data[new_project] = []
        self.temp_project_names.append(new_project)
        new_row = len(self.temp_project_names) - 1
        if new_row == 0:
            self.full_init()
            return
        self.project_maker(new_row)
        new_proj_obj = self.project_objects_list[new_row]
        self.project_switch(new_proj_obj)

    # For making a project curr project. last project by default
    def project_selector(self, index : int) -> int:
        index = index
        if not self.temp_project_names:
            self.curr_project = None
            return
        # Currently selected project name
        self.curr_project = self.temp_project_names[index]
        # List of tasks inside the projects
        self.temp_data_list = self.temp_data[self.curr_project][:]
        return index
    
    # Creates delete dialogue window
    def del_project(self) -> None:
        if not self.deletion_window:
            self.deletion_window = DeleteBox()
        self.deletion_window.construct_optionmenu()
        self.deletion_window.update()
        self.deletion_window.focus()

    # Delete the selected project from options box
    def delete_selected_project(self, proj_name : str) -> None:
        # Modifying main dict
        del self.temp_data[proj_name]
        self.clear_all_tasks()
        self.null_message_forget()
        for obj in self.project_objects_list:
            obj.destruct()
        self.project_objects_list.clear()
        self.temp_project_names.clear()
        self.project_title.grid_forget()
        self.full_init()

    # Appends a new task at the end
    def add_new_task(self) -> None:
        new_task = self.textbox.get()
        if new_task:
            self.temp_data_list.append({new_task: 0})
            row_number = len(self.temp_data_list) - 1
            self.task_maker(row_number)
            self.textbox.delete(first_index=0, last_index=30)
            self.progress_maker()

    # Removes selected task
    def remove_task(self, obj) -> None:
        object_row_number = obj.row_number

        del_obj = self.task_objects_list[object_row_number]
        del_obj.destruct()

        del self.temp_data_list[object_row_number]
        del self.task_objects_list[object_row_number]
        
        for index in range(object_row_number, len(self.task_objects_list)):
            obj = self.task_objects_list[index]
            self.forget_taskbar(obj)
            self.place_taskbar(obj, index)

        self.progress_maker()
        if len(self.temp_data_list) == 0:
            self.null_message_placer()

    # Deletes all the taskbars in task_display_frame
    def clear_all_tasks(self) -> None:
        if not self.task_objects_list:
            return
        self.temp_data_list.clear()
        for obj in self.task_objects_list:
            obj.destruct()          
        self.task_objects_list.clear()
        self.progress_maker()
        self.null_message_placer()

    # Checks the status of checkboxes
    def mark_checker(self, obj) -> None:
        for task, value in self.temp_data_list[obj.row_number].items():
            task, value = task, value
        if value:
            self.temp_data_list[obj.row_number][task], obj.value = 0, 0
        else:
            self.temp_data_list[obj.row_number][task], obj.value = 1, 1
        self.progress_maker()
    
    # Progress bar maker
    def progress_bar_placer(self) -> None:
        # Progress bar frame placement
        self.progressbar_frame.grid(row=2,padx=(0,0), pady=(0,0), sticky="s")
        # Progress bar frame 'left' grid configure
        self.progressbar_frame_left.grid(row=1, column=0, sticky="s")
        # Progress bar frame 'right' grid configure
        self.progressbar_frame_right.grid(row=1, column=1, sticky="s", pady=(5,5))
        self.progress_text.grid(padx=(0,5), pady=(0,0), sticky="sw")
        self.progressbar.grid(padx=(5,5), pady=(5,5), sticky="se")

    # Function to keep track of the progress
    def progress_maker(self) -> None:
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

    def null_message_placer(self) -> None:
        self.null_message.grid(row=1, columnspan=2, sticky="nsew")

    def null_message_forget(self) -> None:
        self.null_message.grid_forget()

    # Task maker method : Creates task based on data from the local file
    def task_maker(self, row_number : int = None) -> None:
        if row_number is not None:
            if row_number == 0:
                self.null_message_forget()
            for task, value in self.temp_data_list[-1].items():
                task, value = task, value
                obj = TaskBar(self.task_display_frame, row_number, task, value)
                self.place_taskbar(obj, row_number)
                self.task_objects_list.append(obj)
        elif not self.temp_data_list:
            self.null_message_placer()
        else:
            for row_number, dixnry in enumerate(self.temp_data_list):
                for task, value in dixnry.items():
                    task, value = task, value 
                obj = TaskBar(self.task_display_frame, row_number, task, value)
                self.place_taskbar(obj, row_number)
                self.task_objects_list.append(obj)

        self.progress_maker()

    # Releases the grid dependancies of a taskbar object
    def forget_taskbar(self, obj) -> None:
        obj.checkbox_frame.grid_forget()
        obj.checkbox.grid_forget()
        obj.task_del_button.grid_forget()

    # Places the taskbar object in frame
    def place_taskbar(self, obj, row_number : int) -> None:
        obj.row_number = row_number
        obj.checkbox_frame.grid(row=row_number, columnspan=2, padx=(0,10), pady=(5,0), sticky="nsew")
        obj.checkbox.grid(row=row_number, column=0, padx=(10, 0), pady=(10, 10), sticky="w")
        obj.task_del_button.grid(row=row_number, column=1, padx=(0, 10), pady=(0,0), sticky="e")

    # Creates a new project
    def project_maker(self, proj_row : int = None) -> None:
        if proj_row is None:
            for proj_row, name in enumerate(self.temp_project_names):
                obj = ProjectBar(self.project_list_frame, proj_row, name)
                self.place_project_bar(obj, proj_row)
                self.project_objects_list.append(obj)
        else:
            name = self.temp_project_names[proj_row]
            obj = ProjectBar(self.project_list_frame, proj_row, name)
            self.place_project_bar(obj, proj_row)
            self.project_objects_list.append(obj) 

    def place_project_bar(self, proj_obj, proj_row : int) -> None:
        proj_obj.row_number = proj_row
        proj_obj.project_bar_frame.grid(row=proj_row, padx=(0, 5), pady=(5, 5), sticky="nsew")
        proj_obj.radio_button.grid(row=proj_row, padx=(10, 10), pady=(10, 10), sticky="nsew")

    # For switching between projects
    def project_switch(self, proj_obj) -> None:
        if self.curr_project_row is None:
            self.curr_project_row = 0
        curr_index = self.curr_project_row
        new_index = proj_obj.proj_row
        if new_index != curr_index:
            # turn off curr obj radio button
            self.project_objects_list[curr_index].toggle_radio(0)
            # write the tasks data to main dictionary
            self.temp_data[self.temp_project_names[curr_index]] = self.temp_data_list[:]
            # clear all temp lists
            self.clear_all_tasks()
            self.null_message_forget()
            # Select the current object
            self.project_selector(new_index)
            self.project_init(new_index)
            # turn that button on
            proj_obj.toggle_radio(1)

# For creating taskbar objects
class TaskBar():
    def __init__(self, task_display_frame, row_number, task, value):
        self.row_number = row_number
        self.task = task
        self.value = value
        self.checkbox_frame = customtkinter.CTkFrame(
                                                task_display_frame, corner_radius=10, border_color="darkgray", 
                                                border_width=1, fg_color="transparent")

        self.checkbox_frame.rowconfigure(0, weight=0)
        self.checkbox_frame.columnconfigure((0,1), weight=1)
        self.checkbox = customtkinter.CTkCheckBox(
                                                self.checkbox_frame, text=task, font=("Consolas", 18, "bold"), onvalue=1, offvalue=0, 
                                                command=lambda:app.mark_checker(self),checkbox_height=22, checkbox_width=22, 
                                                corner_radius=5, border_width=3, variable=customtkinter.IntVar(value=value))

        self.task_del_button = customtkinter.CTkButton(
                                                self.checkbox_frame, text="-", width=10, font=("Calibri",15, "bold"), fg_color="black", corner_radius=10, command=lambda:app.remove_task(self), hover_color="crimson")
        
    # Destroys the taskbar frame and all child widgets
    def destruct(self) -> None:
        self.checkbox_frame.destroy()

# For creating project bar widget
class ProjectBar():
    def __init__(self, project_list_frame, proj_row, project_name):
        self.proj_row = proj_row
        self.project_name = project_name
        self.text_color ="darkgray"
        self.radio_var = customtkinter.IntVar()                 
            
        self.project_bar_frame = customtkinter.CTkFrame(
                                                    project_list_frame, corner_radius=10, border_color=self.text_color, 
                                                    border_width=1, fg_color="black")
        
        self.project_bar_frame.rowconfigure(0, weight=1)
        self.project_bar_frame.columnconfigure(0, weight=1)
        self.radio_button = customtkinter.CTkRadioButton(
                                                    self.project_bar_frame, variable=self.radio_var, value=1, text=self.project_name, text_color=self.text_color, font=("Consolas",18, "bold"), border_color="darkgray", hover_color="#39C288", command=lambda:app.project_switch(self))
    
        if self.project_name == app.curr_project:
            self.toggle_radio(1)
        
    def destruct(self) -> None:
        self.project_bar_frame.destroy()

    # Turn on turn of  radio button
    def toggle_radio(self, button_val : int) -> None:
        if button_val:
            self.radio_var.set(1)
            self.radio_button.configure(text_color="#39C288")
            self.project_bar_frame.configure(border_color="#39C288")
        else:
            self.radio_var.set(0)
            self.radio_button.configure(text_color=self.text_color)
            self.project_bar_frame.configure(border_color=self.text_color)

    def destruct(self) -> None:
        self.project_bar_frame.destroy()

# Class for the new project dialogue box
class CreateBox(customtkinter.CTkToplevel):
    def __init__(self):
        super().__init__()
        # Window structure
        width = 350
        height = 200
        x = 750
        y = 500
        self.title("Create New Poject")
        self.geometry(f"{width}x{height}+{x}+{y}")
        self.rowconfigure((0,1,2), weight=0)
        self.columnconfigure((0,1), weight=1)
        
        self.label = customtkinter.CTkLabel(self, text="Create A New Project", font=("Consolas", 18, "bold"))
        self.label.grid(row=0, columnspan=2, padx=20, pady=20, sticky="nsew")

        self.textbox = customtkinter.CTkEntry(self, width=250, placeholder_text="Project Name", font=("Calibri",15, "bold"))
        self.textbox.bind("<Return>", lambda event : self.project_parse())
        # Text box Placement
        self.textbox.grid(row=1, columnspan=2, padx=(20, 20), pady=(10, 20), sticky="ns")

        self.ok_button = customtkinter.CTkButton(self, text="Ok", width=80, font=("Calibri",15, "bold"), command=self.project_parse)
        self.ok_button.grid(row=2, column=0, padx=20, pady=(10, 20), sticky="e")

        self.cancel_button = customtkinter.CTkButton(self, text="Cancel", width=80, fg_color="crimson", font=("Calibri",15, "bold"), command=self.reset)
        self.cancel_button.grid(row=2, column=1, padx=20, pady=(10, 20), sticky="w")

    # Sends newly entered project name 
    def project_parse(self) -> None:
            new_project = self.textbox.get()
            if new_project:
                app.create_new_project(new_project)
                self.textbox.delete(0,30)
                self.reset()

    def reset(self) -> None:
        self.destroy()
        app.input_box=None

# Class for delete project dialogue box
class DeleteBox(customtkinter.CTkToplevel):
    def __init__(self):
        super().__init__()
        # Window structure
        width = 350
        height = 200
        x = 750
        y = 500
        self.title("Delete Poject")
        self.geometry(f"{width}x{height}+{x}+{y}")
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=0)
        self.columnconfigure((0,1), weight=1)
        
        self.construct_optionmenu()

        self.label = customtkinter.CTkLabel(self, text="Select a project to delete", font=("Consolas", 18, "bold"))
        self.label.grid(row=0, columnspan=2, padx=20, pady=20, sticky="s")

        self.del_button = customtkinter.CTkButton(self, text="Delete", width=80, fg_color="Crimson", 
                                                    font=("Calibri",15, "bold"), command=self.parse_project)
        self.del_button.grid(row=1, column=1, padx=20, pady=(20, 10), sticky="w")

    # Creates and refreshes options menu in delete projets
    def construct_optionmenu(self) -> None:
        self.project_names = app.temp_project_names
        self.optionmenu = customtkinter.CTkOptionMenu(
                                                    self, dynamic_resizing=False, values=self.project_names, 
                                                    font=("Consolas", 15, "bold"), text_color="black", width=200)
        self.optionmenu.set("Select..")
        self.optionmenu.grid(row=1, padx=20, pady=(20, 10), sticky="e")
    
    def parse_project(self) -> None:
        project_name = self.optionmenu.get()

        if not project_name == "Select..":
            app.delete_selected_project(project_name)
            self.construct_optionmenu()
            self.reset()
    
    def reset(self) -> None:
        self.destroy()
        app.deletion_window=None

if __name__ == "__main__":

    try:
        with open("data.json", "r") as file:
                data = json.load(file)

    except FileNotFoundError as e:
        with open("data.json", "w") as file:
            json.dump({}, file, indent=4)

        with open("data.json", "r") as file:
                data = json.load(file)

    # Main object
    app = App()
    app.full_init()

    def on_closing() -> None:
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            # save and close the file
            data = app.temp_data
            with open("data.json", "w") as file:
                json.dump(data, file, indent=4)
            # Close the window
            app.destroy()
    app.protocol("WM_DELETE_WINDOW", on_closing)

    app.mainloop()
        