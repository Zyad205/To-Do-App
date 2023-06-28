import customtkinter as ctk
from settings import *
from text_frames import ToDo, DoingDone


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
        self.columnconfigure((0, 1, 2, 3), weight=1, uniform="a")
        self.rowconfigure(0, weight=3, uniform="a")
        self.rowconfigure(1, weight=15, uniform="a")
        self.rowconfigure(2, weight=1, uniform="a")
        self.to_do = ToDo(self)
        self.doing = DoingDone(self, 2)
        self.done = DoingDone(self, 3)
        self.to_do.parents_list = [self.to_do, self.doing, self.done]
        self.doing.parents_list = [self.to_do, self.doing, self.done]
        self.done.parents_list = [self.to_do, self.doing, self.done]

        self.create_header(1, "TO DO")
        self.create_header(2, "DOING")
        self.create_header(3, "DONE")

        self.mainloop()

    def create_header(self, column, text):
        ctk.CTkLabel(
            self,
            text=text,
            font=self.main_font,
            fg_color="transparent",
            anchor="nw",text_color="#b6c2cf").grid(row=0, column=column, sticky="NSEW", padx=10, pady=10)


if __name__ == "__main__":
    App()
