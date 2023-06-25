import customtkinter as ctk
from settings import *
from textwrap import TextWrapper


class ToDo(ctk.CTkScrollableFrame):

    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")

        self.text_input = TextInput(self, self.add_label, self.close_input)
        self.grid(row=0, column=1, rowspan=2, sticky="NSEW")

        self.font = ctk.CTkFont(*INPUT_TEXT_FONT)
        self.wrap = TextWrapper()

        self.parent = parent

    def add_label(self, text):
        label = ctk.CTkLabel(
            self,
            justify="left",
            font=INPUT_TEXT_FONT,
            fg_color=INPUT_TEXT_COLOR,
            corner_radius=5,
            anchor="w")

        label.pack(fill="x", pady=5)
        self.update()
        size = label.winfo_width() - 20

        char_size = []
        for char in text:
            char_size.append(self.font.measure(char))
        char_size = sum(char_size) / len(char_size)
        char_num = size / char_size
        self.wrap.width = round(char_num)

        text_list = self.wrap.wrap(text)
        formatted_text = '\n'.join(text_list)
        label.configure(text=formatted_text)

        self.text_input.pack_forget()
        self.text_input.pack(fill="x", padx=1, pady=1)

    def close_input(self):
        self.grid_forget()
        self.grid(row=0, column=1, sticky="NSEW")
        self.create_input_frame = CreateInputFrame(
            self.parent, self.open_input)
        self.text_input.pack_forget()

    def open_input(self):
        self.grid_forget()
        self.grid(row=0, column=1, rowspan=2, sticky="NSEW")
        self.create_input_frame.grid_forget()
        self.text_input.pack(fill="x")


class TextInput(ctk.CTkFrame):
    def __init__(self, parent, add_label_func, close_input):
        super().__init__(parent, fg_color="transparent")

        # Layout
        self.columnconfigure(tuple(range(5)), weight=1, uniform="a")
        self.rowconfigure(0, weight=2, uniform="b")
        self.rowconfigure(1, weight=1, uniform="b")

        # Input Entry
        self.input = ctk.CTkTextbox(
            self,
            height=65,
            fg_color=INPUT_TEXT_COLOR,
            font=INPUT_TEXT_FONT)

        self.add_label_func = add_label_func

        self.add_button = ctk.CTkButton(
            self,
            text="Add card",
            fg_color=ADD_BUTTON["color"]["bg"],
            hover_color=ADD_BUTTON["color"]["hover"],
            text_color=ADD_BUTTON["color"]["text"],
            width=1,
            command=self.add_label)

        self.input.grid(row=0, column=0, columnspan=5, sticky="NSEW")

        self.add_button.grid(
            row=1,
            column=0,
            columnspan=2,
            sticky="NSEW",
            pady=7)

        self.close_button = ctk.CTkButton(
            self,
            text="X",
            fg_color="transparent",
            hover_color="#FF0000",
            command=close_input)

        self.close_button.grid(row=1, column=2, sticky="NSEW", pady=7, padx=7)

        self.pack(fill="x")

    def add_label(self):
        text = self.input.get(1.0, "end")
        self.add_label_func(text)
        self.input.delete(1.0, "end")


class CreateInputFrame(ctk.CTkFrame):

    def __init__(self, parent, open_func):
        super().__init__(parent)

        self.label = ctk.CTkButton(
            self, text="+ Add a card", font=INPUT_TEXT_FONT, height=1, width=1, command=open_func)
        self.label.pack(expand=True, fill="x")

        self.grid(row=1, column=1, sticky="NSEW")
