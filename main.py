import customtkinter as ctk
from settings import *


class App(ctk.CTk):

    def __init__(self):
        super().__init__()
        # Title
        self.title("To Do")

        # Geometry
        self.geometry(f"{APP_SIZE[0]}x{APP_SIZE[1]}")
        self.minsize(APP_MINSIZE[0], APP_MINSIZE[1])

        self.mainloop()


if __name__ == "__main__":
    App()
