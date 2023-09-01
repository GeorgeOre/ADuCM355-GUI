import tkinter as tk

class Frame1(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        label = tk.Label(self, text="Frame 1", font=("Helvetica", 24))
        label.pack(pady=20)

        button = tk.Button(self, text="Go to Frame 2", command=lambda: master.show_frame(master.frame2))
        button.pack()

        button_back = tk.Button(self, text="Back to Main Menu", command=lambda: master.show_frame(master.frame1))
        button_back.pack()
