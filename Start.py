import customtkinter

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")


root = customtkinter.CTk()

root.title("Tasker")
root.geometry("800x600")

label = customtkinter.CTkLabel(master=root, text="Welcome to Tasker", font=customtkinter.CTkFont(size=30, weight="bold"))
label.place(relx="0.5", rely="0.1", anchor="center")

new_project_btn = customtkinter.CTkButton(master=root, text="New Project +")
new_project_btn.place(relx="0.5", rely="0.3", anchor="center")


ex_proj_btn1 = customtkinter.CTkButton(master=root, width=200, text="Project1", fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"))
proj_del_button1 = customtkinter.CTkButton(master=root, width=10, text=" - ", border_width=2)

ex_proj_btn1.place(relx="0.4", rely="0.5")
proj_del_button1.place(relx="0.7", rely="0.5")

ex_proj_btn2 = customtkinter.CTkButton(master=root, width=200, text="Project2", fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"))
proj_del_button1 = customtkinter.CTkButton(master=root, width=10, text=" - ", border_width=2)

ex_proj_btn2.place(relx="0.4", rely="0.6")
proj_del_button1.place(relx="0.7", rely="0.6")

root.mainloop()
