import tkinter
import customtkinter
import json

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
        # Top frame
        self.frame2 = customtkinter.CTkFrame(self, height=50, corner_radius=0, fg_color="transparent")
        # Top frame => Project Title
        self.project_title = customtkinter.CTkLabel(self.frame2, text="Project 1", font=("Terminal", 50))
        # Bottom frame
        self.frame3 = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        # Bottom frame => Inserter frame
        self.inserter_frame = customtkinter.CTkFrame(self.frame3, height=100, corner_radius=10, fg_color="black")
        # Bottom frame => Task display frame
        self.task_display_frame = customtkinter.CTkFrame(self.frame3, corner_radius=10)

        # ######################################################
        # Grid configuration(Frames and Subframes) and placement
        # ######################################################
        # Sidebar frame
        self.frame1.grid(row=0, column=0, rowspan=2, padx=(5,2.5), pady=(5,2.5), sticky="nsew")
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
        self.inserter_frame.grid(row=0, columnspan=2, pady=(0,5), sticky="nsew")
        # Bottom frame => Inserter frame => Text box
        self.textbox = customtkinter.CTkEntry(self.inserter_frame, width=250, placeholder_text="Add new task", font=("Calibri",15, "bold"))
        # Text box Placement
        self.textbox.grid(row=0, column=0, padx=(10, 0), pady=(10, 10), sticky="w")
        # Bottom frame => Inserter frame => Insert button
        self.insert_button = customtkinter.CTkButton(self.inserter_frame, text="+ Add ", width=70, font=("Calibri",15, "bold"), command=None)
        # Insert button placement
        self.insert_button.grid(row=0, column=1, padx=(30, 0), pady=(10, 10), sticky="w")
        # Bottom frame => Inserter frame => Delete Button
        self.delete_button = customtkinter.CTkButton(self.inserter_frame, text="Clear", width=80, fg_color="Crimson", font=("Calibri",15, "bold"), command=None)
        # Delete Button placement
        self.delete_button.grid(row=0, column=2, padx=(0, 10), pady=(10, 10), sticky="e")
        # Bottom frame => Task display frame
        self.task_display_frame.grid(row=1, columnspan=2, pady=(5,0), sticky="nsew")
        # Bottom frame => Task display frame => Checkbox
        self.checkbox = customtkinter.CTkCheckBox(self.task_display_frame, text=f"Complete all the below tasks", font=("Consolas", 18, "bold"), onvalue=1, offvalue=0, command=None,checkbox_height=22, checkbox_width=22, corner_radius=5, border_width=3)
        # Checkbox placement
        self.checkbox.grid(row=1, column=0, padx=(22, 0), pady=(10, 10), sticky="w")

        # Status bar






if __name__ == "__main__":
    app = App()
    app.mainloop()