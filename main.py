import customtkinter as ctk
from settings import *
from text_frames import ToDo


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
        self.rowconfigure(0, weight=16, uniform="a")
        self.rowconfigure(1, weight=1, uniform="a")
        
        ToDo(self)
        self.mainloop()


if __name__ == "__main__":
    App()
