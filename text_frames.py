import customtkinter as ctk
from settings import *
from textwrap import TextWrapper


class DoingDone(ctk.CTkScrollableFrame):

    def __init__(self, parent, column):
        super().__init__(parent, fg_color="#000000")
        self.parent = parent
        self.main_font = ctk.CTkFont(*TEXT_FONT)
        self.labels = []
        self.wrap = TextWrapper()
        self.width = self.winfo_width()
        self.height = self.winfo_height()

        self.grid(row=1, column=column, rowspan=2, sticky="NSEW", padx=10)

    def reformat_text(self, event):
        self._parent_canvas.configure(
            scrollregion=self._parent_canvas.bbox("all"))
        if event.width != self.width or event.height != self.height:
            for label in self.labels:

                self.update()
                size = self.text_input.winfo_width() - 20
                label_text = label.original_text
                formatted_text = self.get_formatted_text(
                    text=label_text, size=size)

                label.configure(text=formatted_text)
            self.width = event.width
            self.height = event.height

    def get_formatted_text(self, text, size):
        if text:
            char_size = []
            for char in text:
                char_size.append(self.main_font.measure(char))

            char_size = sum(char_size) / len(char_size)
            char_num = size / char_size
            self.wrap.width = round(char_num)

            text_list = self.wrap.wrap(text)
            formatted_text = '\n'.join(text_list)
        else:
            formatted_text = ""
        return formatted_text

    def add_label(self, label_text):
        index = len(self.labels)
        label = Label(self, self.get_out_of_frame, self.main_font, index)

        self.labels.append(label)

        label.pack(fill="x", pady=5)
        self.update()
        size = label.winfo_width() - 20

        formatted_text = self.get_formatted_text(text=label_text, size=size)

        label.original_text = label_text

        label.configure(text=formatted_text)

    def get_out_of_frame(self, _, index):
        current_label = self.labels[index]
        text = current_label.cget("text")
        original_text = current_label.original_text
        current_label.destroy()
        del self.labels[index]
        current_label = Label(self.parent, self.move, self.main_font, index, out_out_frame=True,
                              parents_list=self.parents_list)
        current_label.original_text = original_text

        current_label.configure(text=text, cursor="fleur")

        root = current_label.winfo_toplevel()
        current_label.place(
            x=root.winfo_pointerx() - root.winfo_rootx(),
            y=root.winfo_pointery() - root.winfo_rooty(),
            anchor="center")
        for index, label in enumerate(self.labels):
            label.index = index

    def move(self, _, index):
        current_label = self.labels[index]
        root = current_label.winfo_toplevel()
        current_label.place(
            x=root.winfo_pointerx() - root.winfo_rootx(),
            y=root.winfo_pointery() - root.winfo_rooty(),
            anchor="center")


class ToDo(ctk.CTkScrollableFrame):

    def __init__(self, parent):
        super().__init__(parent, fg_color="#000000")

        self.main_font = ctk.CTkFont(*TEXT_FONT)

        self.text_input = TextInput(
            self, self.add_label, self.close_input, self.main_font)
        self.grid(row=1, column=1, rowspan=2, sticky="NSEW", padx=10)

        self.wrap = TextWrapper()

        self.parent = parent
        self.labels = []
        self.width = self.winfo_width()
        self.height = self.winfo_height()
        self.bind("<Configure>", self.reformat_text)

    def add_label(self, label_text):

        index = len(self.labels)
        label = Label(self, self.get_out_of_frame, self.main_font, index)
        label.original_text = label_text

        self.labels.append(label)

        label.pack(fill="x", pady=5)
        self.update()
        size = label.winfo_width() - 20

        formatted_text = self.get_formatted_text(text=label_text, size=size)

        label.configure(text=formatted_text)
        self.text_input.pack_forget()
        self.text_input.pack(fill="x", padx=1, pady=1)

    def close_input(self):
        self.grid_forget()
        self.grid(row=1, column=1, sticky="NSEW")
        self.create_input_frame = CreateInputFrame(
            self.parent, self.open_input, self.main_font)
        self.text_input.pack_forget()

    def open_input(self):
        self.grid_forget()
        self.grid(row=1, column=1, rowspan=2, sticky="NSEW", padx=10)
        self.create_input_frame.grid_forget()
        self.text_input.pack(fill="x")

    def reformat_text(self, event):
        self._parent_canvas.configure(
            scrollregion=self._parent_canvas.bbox("all"))
        if event.width != self.width or event.height != self.height:
            for label in self.labels:

                self.update()
                size = self.text_input.winfo_width() - 20
                label_text = label.original_text
                formatted_text = self.get_formatted_text(
                    text=label_text, size=size)

                label.configure(text=formatted_text)
            self.width = event.width
            self.height = event.height

    def get_out_of_frame(self, _, index):

        current_label = self.labels[index]
        text = current_label.cget("text")
        original_text = current_label.original_text
        
        current_label.destroy()

        del self.labels[index]

        

        new_label = Label(self.parent, self.move, self.main_font, index, out_out_frame=True,
                          parents_list=self.parents_list)
        new_label.original_text = original_text
        new_label.configure(text=text, cursor="fleur")

        root = new_label.winfo_toplevel()

        new_label.place(
            x=root.winfo_pointerx() - root.winfo_rootx(),
            y=root.winfo_pointery() - root.winfo_rooty(),
            anchor="center")

        for index, label in enumerate(self.labels):
            label.index = index

    def move(self, event, index):
        current_label = self.labels[index]
        root = current_label.winfo_toplevel()
        current_label.place(
            x=root.winfo_pointerx() - root.winfo_rootx(),
            y=root.winfo_pointery() - root.winfo_rooty(),
            anchor="center")

    def get_formatted_text(self, text, size):
        if text:
            char_size = []
            for char in text:
                char_size.append(self.main_font.measure(char))

            char_size = sum(char_size) / len(char_size)
            char_num = size / char_size
            self.wrap.width = round(char_num)

            text_list = self.wrap.wrap(text)
            formatted_text = '\n'.join(text_list)
        else:
            formatted_text = ""
        return formatted_text


class Label(ctk.CTkLabel):

    def __init__(self, parent, move_func, font, index, out_out_frame=False, parents_list=None):
        super().__init__(
            parent,
            justify="left",
            font=font,
            fg_color=INPUT_TEXT_COLOR,
            corner_radius=5,
            anchor="w")

        self.index = index
        self.parents_list = parents_list
        if not out_out_frame:
            self.bind("<B1-Motion>", lambda event:
                      move_func(event, self.index))
        else:
            self.bind("<B1-Motion>", self.move)
            self.bind("<ButtonRelease-1>", self.release)

    def move(self, _):
        root = self.winfo_toplevel()
        self.place(
            x=root.winfo_pointerx() - root.winfo_rootx(),
            y=root.winfo_pointery() - root.winfo_rooty(),
            anchor="center")

    def release(self, _):
        root = self.winfo_toplevel()
        x_pos = root.winfo_pointerx() - root.winfo_rootx()
        one_column = round(root.winfo_width() / 4)
        first_point = one_column + round(root.winfo_width() * 0.125)
        second_point = first_point + one_column
        third_point = second_point + one_column

        first_point = abs(first_point - x_pos)
        second_point = abs(second_point - x_pos)
        third_point = abs(third_point - x_pos)

        temp_dict = {first_point: self.parents_list[0],
                     second_point: self.parents_list[1],
                     third_point: self.parents_list[2]}

        parent = temp_dict[min(first_point, second_point, third_point)]

        text = self.original_text
        self.destroy()
        parent.add_label(text)


class TextInput(ctk.CTkFrame):
    def __init__(self, parent, add_label_func, close_input, font):
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
            font=font)

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
        self.input.bind("<Shift-Return>", lambda _: self.add_label())
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

    def __init__(self, parent, open_func, font):
        super().__init__(parent)

        self.label = ctk.CTkButton(
            self, text="+ Add a card", font=font, height=1, width=1, command=open_func)
        self.label.pack(expand=True, fill="x")

        self.grid(row=2, column=1, sticky="NSEW")
