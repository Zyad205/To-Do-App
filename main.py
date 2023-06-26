import customtkinter as ctk
from settings import *
from text_frames import ToDo, Doing


class App(ctk.CTk):

    def __init__(self):
        super().__init__()
        # Title
        self.title("To Do")

        # Geometry
        self.geometry(f"{APP_SIZE[0]}x{APP_SIZE[1]}")
        self.minsize(APP_MINSIZE[0], APP_MINSIZE[1])

        ctk.set_appearance_mode("dark")

        # Layout
        self.columnconfigure((0, 1, 2, 3), weight=1, uniform="a")
        self.rowconfigure(0, weight=3, uniform="a")
        self.rowconfigure(1, weight=15, uniform="a")
        self.rowconfigure(2, weight=1, uniform="a")
        self.to_do = ToDo(self)
        self.doing = Doing(self)
        self.to_do.parents_list = [self.to_do, self.doing]
        self.doing.parents_list = [self.to_do, self.doing]
        # Developing settings
        self.bind("<FocusOut>", exit)
        self.mainloop()


if __name__ == "__main__":
    App()
