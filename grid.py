import customtkinter

root = customtkinter.CTk()

root.title("Tasker")
root.geometry("800x600")
root.resizable(height=True, width=True)

root.grid_columnconfigure(0, weight=0)
root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(0,weight=0)
root.grid_rowconfigure(1,weight=1)

frame1 = customtkinter.CTkFrame(root, width=150, corner_radius=0)
frame2 = customtkinter.CTkFrame(root, height=50, corner_radius=0)
frame3 = customtkinter.CTkFrame(root, corner_radius=0)

frame4 = customtkinter.CTkFrame(frame3, height=100, corner_radius=0)
frame5 = customtkinter.CTkFrame(frame3, corner_radius=0)

frame3.grid_rowconfigure(0, weight=0)
frame3.grid_rowconfigure(1, weight=1)
frame3.grid_columnconfigure((0,1), weight=1)

frame1.grid(row=0, column=0, rowspan=2, padx=(5,2.5), pady=(5,2.5), sticky="nsew")
frame2.grid(row=0, column=1, padx=(2.5,5), pady=(5,2.5), sticky="nsew")
frame3.grid(row=1, column=1, padx=(2.5,5), pady=(2.5,5), sticky="nsew")

frame4.grid(row=0, columnspan=2, pady=(0,2.5), sticky="nsew")
frame5.grid(row=1, columnspan=2, pady=(2.5,0), sticky="nsew")




root.mainloop()