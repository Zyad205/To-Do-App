import customtkinter as ctk
from settings import *
from text_frames import ToDo, DoingDone
import os
from sys import argv


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        # Title
        self.title("To Do")

        # Geometry
        self.geometry(f"{APP_SIZE[0]}x{APP_SIZE[1]}")
        self.minsize(APP_MINSIZE[0], APP_MINSIZE[1])

        ctk.set_appearance_mode("dark")
        self.main_font = ctk.CTkFont(*HEADER_FONT)
        # Layout
        self.columnconfigure((0, 1, 2), weight=1, uniform="a")
        self.rowconfigure(0, weight=3, uniform="a")
        self.rowconfigure(1, weight=15, uniform="a")
        self.rowconfigure(2, weight=1, uniform="a")

        # Text frames
        self.to_do = ToDo(self, "todo")
        self.doing = DoingDone(self, 1, "doing")
        self.done = DoingDone(self, 2, "done")
        self.to_do.parents_list = [self.to_do, self.doing, self.done]
        self.doing.parents_list = [self.to_do, self.doing, self.done]
        self.done.parents_list = [self.to_do, self.doing, self.done]

        # Headers
        self.create_header(0, "TO DO")
        self.create_header(1, "DOING")
        self.create_header(2, "DONE")

        self.after(100, self.check_for_last_save)

        self.mainloop()

    def create_header(self, column, text):
        """Creates a labels on top of the text frames"""
        label = ctk.CTkLabel(
            self,
            text=text,
            font=self.main_font,
            fg_color="transparent",
            anchor="nw",
            text_color="#b6c2cf",
        )

        label.grid(
            row=0,
            column=column,
            sticky="NSEW",
            padx=10,
            pady=10)

    def check_for_last_save(self):
        """Checks for widget from the last run"""

        # Get current directory
        current_directory = os.path.dirname(argv[0])

        # Endings for every save file
        dirs = ["todo.txt", "doing.txt", "done.txt"]

        # A list for the full path of all files
        directories = [os.path.join(current_directory, dir) for dir in dirs]

        # A list for the add label function for the text frames
        func_list = [self.to_do.add_label,
                     self.doing.add_label, self.done.add_label]

        for index, dir in enumerate((directories)):  # Loop over every save file
            with open(dir, "r") as file:
                lines = file.readlines()
                for line in lines:
                    func = func_list[index]
                    # Call the add label function add delete the last character
                    # if it's a escape character
                    func(line[:-1] if line[:-1] == "\n" else line)


if __name__ == "__main__":
    App()
