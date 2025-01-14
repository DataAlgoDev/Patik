import tkinter
from tkinter import messagebox
import customtkinter
import json
import time

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
        # #########################
        # Configuring grid pattern: root/main app window [4x4 grid : (0,0),(0,1),(1.0),(1,1)]
        # #########################
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1,weight=1)
        self.grid_rowconfigure(0,weight=0)

        # Sidebar frame
        self.frame1 = customtkinter.CTkFrame(self, width=200, corner_radius=10)
        # Sidebar frame => Progress bar frame
        self.progressbar_frame = customtkinter.CTkFrame(self.frame1, corner_radius=10, fg_color="transparent", height=50)
        # Sidebar frame => Progress bar frame => left
        self.progressbar_frame_left = customtkinter.CTkFrame(self.progressbar_frame, width=40, corner_radius=10, fg_color="transparent")
        # Sidebar frame => Progress bar frame => right
        self.progressbar_frame_right = customtkinter.CTkFrame(
                                                            self.progressbar_frame, corner_radius=10, fg_color="black", 
                                                            border_width=1, border_color="darkgray"
                                                            )
        # Top frame
        self.frame2 = customtkinter.CTkFrame(self, height=50, corner_radius=0, fg_color="transparent")
        # Top frame => Project Title
        self.project_title = customtkinter.CTkLabel(self.frame2, text="Project 1", font=("Terminal", 50))
        # Bottom frame
        self.frame3 = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent", border_width=0)
        # Bottom frame => Inserter frame
        self.inserter_frame = customtkinter.CTkFrame(self.frame3, height=100, corner_radius=10, fg_color="black")
        # Bottom frame => Task display frame
        # Creating the task displayer frame

        # ######################################################
        # Grid configuration(Frames and Subframes) and placement
        # ######################################################

        # Sidebar frame
        self.frame1.rowconfigure((0,1), weight=1)
        # self.frame1.columnconfigure()
        self.frame1.grid(row=0, column=0, rowspan=2, padx=(5,2.5), pady=(5,2.5), sticky="nsew")
        # Progress bar grid configure
        self.progressbar_frame.rowconfigure(0, weight=0)
        self.progressbar_frame.columnconfigure((0,1), weight=1)
        # Progress bar frame placement
        self.progressbar_frame.grid(row=1,padx=(0,0), pady=(0,0), sticky="s")
        # Progress bar frame 'left' grid configure
        self.progressbar_frame_left.grid(row=0, column=0, sticky="s")
        # Progress text
        self.progress_text = customtkinter.CTkLabel(self.progressbar_frame_left, text="1/5", font=("Terminal", 10))
        self.progress_text.grid(padx=(5,5), pady=(0,0), sticky="s")
        # Progress bar frame 'right' grid configure
        self.progressbar_frame_right.grid(row=0, column=1, sticky="s", pady=(5,5))
        self.progressbar = customtkinter.CTkProgressBar(self.progressbar_frame_right, progress_color="red", width=160)
        self.progressbar.set(value=0) # 0 to 1
        # Progress bar placement
        self.progressbar.grid(padx=(5,5), pady=(5,5), sticky="s")

        # Top frame
        self.frame2.rowconfigure(0, weight=1)
        self.frame2.columnconfigure(0, weight=1)
        self.frame2.grid(row=0, column=1, padx=(2.5,5), pady=(5,25), sticky="nsew")
        # Top frame => Project title
        self.project_title.grid(padx=(10,0), sticky="w")

        # Bottom frame [4x4 grid]
        self.frame3.grid_rowconfigure(0, weight=0)
        # self.frame3.grid_rowconfigure(1, weight=1)
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
                                                    command=self.add_new_task
                                                    )
        # Insert button placement
        self.insert_button.grid(row=0, column=1, padx=(30, 0), pady=(10, 10), sticky="w")
        # Bottom frame => Inserter frame => Delete Button
        self.delete_button = customtkinter.CTkButton(
                                                    self.inserter_frame, text="Clear", width=80, fg_color="Crimson", 
                                                    font=("Calibri",15, "bold"), command=self.clear_all_tasks
                                                    )
        # Delete Button placement
        self.delete_button.grid(row=0, column=2, padx=(0, 10), pady=(10, 10), sticky="e")
        # Creating and placing task_display_frame
        self.task_display_frame_creator()

        
        ## Functions
        # List of tasks from local file
        self.temp_data = globals()["data"]
        self.temp_data_list = self.temp_data["task_data"]
        # self.row_count = len(self.temp_data["task_data"])
        self.objects_list = list()

    def task_display_frame_creator(self):
            # frame3 => task_display_frame
            self.task_display_frame = customtkinter.CTkFrame(self.frame3, corner_radius=10, height=200, fg_color="transparent")
            # Bottom frame => Task display frame
            self.task_display_frame.rowconfigure(0, weight=0)
            self.task_display_frame.columnconfigure((0,1), weight=1)
            self.task_display_frame.grid(row=1, columnspan=2, pady=(5,0), sticky="nsew")

    def add_new_task(self):
        new_task = self.textbox.get()
        if new_task:
            row_number = len(self.temp_data_list)
            self.temp_data_list.append({new_task: 0})
            self.task_maker(row_number)
            print(row_number)
            self.textbox.delete(first_index=0, last_index=30)

    def clear_all_tasks(self):
        if not self.objects_list:
            return
        self.temp_data_list.clear()

        for obj in self.objects_list:
            print(obj)
            self.task_display_frame.destroy()
            # obj.destroy_objects()
        self.objects_list.clear()
        # time.sleep(2)
        print(self.objects_list)
        self.task_display_frame_creator()
        # self.task_maker()


    # Task maker method : Creates task based on data from the local file
    def task_maker(self, row_number=None):
        print(self.temp_data_list)
        if row_number:
            for task, value in self.temp_data_list[-1].items():
                task, value = task, value
            obj = self._task_creator(row_number, task, value)
            self.objects_list.append(obj)
        else:
            for row_number, dixnry in enumerate(self.temp_data_list):
                for task, value in dixnry.items():
                    task, value = task, value
                self._task_creator(row_number, task, value)
                obj = self._task_creator(row_number, task, value)
                self.objects_list.append(obj)
        # print(self.objects_list)

    # def _task_creater(self, row_number, task, value):
    #     self.checkbox_frame = customtkinter.CTkFrame(self.task_display_frame, corner_radius=10, border_color="darkgray", border_width=1)
    #     # self.checkbox_frame.rowconfigure(0, weight=0)
    #     self.checkbox_frame.columnconfigure((0,1), weight=1)
    #     # Bottom frame => Task display frame => checkbox 1 frame => Checkbox 1
    #     self.checkbox = customtkinter.CTkCheckBox(self.checkbox_frame, text=f"{task}", font=("Consolas", 18, "bold"), onvalue=1, offvalue=0, command=None,checkbox_height=22, checkbox_width=22, corner_radius=5, border_width=3, variable=customtkinter.IntVar(value=value))
    #     # Task del button
    #     self.task_del_button = customtkinter.CTkButton(self.checkbox_frame, text="-", width=10, font=("Calibri",15, "bold"), fg_color="black", corner_radius=10, command=None, hover_color="crimson")
        
    #     # Placing del button
    #     self.task_del_button.grid(row=row_number, column=1, padx=(0, 10), pady=(0,0), sticky="e")
        
    #     # Frame placement
    #     self.checkbox_frame.grid(row=row_number, columnspan=2, pady=(5,0), sticky="nsew")
    #     # Checkbox placement
    #     self.checkbox.grid(row=row_number, column=0, padx=(22, 0), pady=(10, 10), sticky="w")
    #     # return [self.c, self.d]

    def _task_creator(self, row_number, task, value):
        obj = Taskbar(self.task_display_frame, task, value)

        obj.checkbox_frame.grid(row=row_number, columnspan=2, pady=(5,0), sticky="nsew")
        obj.checkbox.grid(row=row_number, column=0, padx=(22, 0), pady=(10, 10), sticky="w")
        obj.task_del_button.grid(row=row_number, column=1, padx=(0, 10), pady=(0,0), sticky="e")
        
        self.objects_list.append(obj)

class Taskbar():
    def __init__(self, task_display_frame, task, value):
        
        self.task = task
        self.value = value

        self.checkbox_frame = customtkinter.CTkFrame(task_display_frame, corner_radius=10, border_color="darkgray", border_width=1, fg_color="transparent")

        self.checkbox_frame.rowconfigure(0, weight=0)
        self.checkbox_frame.columnconfigure((0,1), weight=1)

        self.checkbox = customtkinter.CTkCheckBox(self.checkbox_frame, text=f"{task}", font=("Consolas", 18, "bold"), onvalue=1, offvalue=0, command=None,checkbox_height=22, checkbox_width=22, corner_radius=5, border_width=3, variable=customtkinter.IntVar(value=value))

        self.task_del_button = customtkinter.CTkButton(self.checkbox_frame, text="-", width=10, font=("Calibri",15, "bold"), fg_color="black", corner_radius=10, command=None, hover_color="crimson")


        # self.checkbox_frame.grid(row=0, columnspan=2, pady=(5,0), sticky="nsew")
        # self.checkbox.grid(row=0, column=0, padx=(22, 0), pady=(10, 10), sticky="w")
        # self.task_del_button.grid(row=0, column=1, padx=(0, 10), pady=(0,0), sticky="e")



if __name__ == "__main__":

    app = App()
    app.task_maker()

    # def on_closing():
    #     if messagebox.askokcancel("Quit", "Do you want to quit?"):
    #         # save and close the file
    #         app.destroy()  # Close the window
    # app.protocol("WM_DELETE_WINDOW", on_closing)
    

    app.mainloop()